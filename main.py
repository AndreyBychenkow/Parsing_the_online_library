import argparse
import os
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError

BASE_URL = "https://tululu.org"


def check_for_redirect(response):
    if response.history:
        raise HTTPError(f"Редирект на главную страницу. URL: {response.url}")


def fetch_page(url):
    with requests.get(url) as response:
        response.raise_for_status()
        check_for_redirect(response)
        return response


def create_directory(folder):
    os.makedirs(folder, exist_ok=True)


def get_comments(soup):
    comments_section = soup.find_all('div', class_='texts')
    return [
        comment_div.find('span').text.strip()
        for comment_div in comments_section
        if comment_div.find('span')
    ]


def download_txt(book_id, title, folder='books'):
    url = f"{BASE_URL}/txt.php?id={book_id}"
    create_directory(folder)

    safe_filename = f"{book_id}. {sanitize_filename(title)}.txt"
    filepath = os.path.join(folder, safe_filename)

    response = fetch_page(url)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def download_image(url, folder='images'):
    response = fetch_page(url)
    create_directory(folder)

    filename = unquote(urlsplit(url).path.split('/')[-1])
    filepath = os.path.join(folder, filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def get_book_cover_url(soup):
    img_tag = soup.find('div', class_='bookimage').find('img')
    if img_tag and img_tag.get('src'):
        return urljoin(BASE_URL, img_tag['src'])
    return None


def parse_book_page(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    title_tag = soup.find('div', id='content').find('h1')
    genre_tags = soup.find('span', class_='d_book').find_all('a')
    author_tags = soup.find('div', id='content').find('h1', title='').text

    title = title_tag.text.split(':')[0].strip() if title_tag else "Неизвестный заголовок"
    genres = [genre.text.strip() for genre in genre_tags] if genre_tags else []
    author = author_tags.split('::')[-1].strip() if author_tags else "Автор неизвестен"

    return {
        'title': title,
        'author': author,
        'genres': genres,
        'cover_url': get_book_cover_url(soup),
        'comments': get_comments(soup)
    }


def collect_book_data(book_id):
    url = f"{BASE_URL}/b{book_id}/"
    response = fetch_page(url)
    return parse_book_page(response.text)


def display_book_info(book_data):
    book_info = {
        "\nЗаголовок": book_data['title'],
        "Автор": book_data['author'],
        "Жанр": str(book_data['genres']) if book_data['genres'] else "[]",
        "Ссылка на обложку": book_data['cover_url'] or "Обложка отсутствует",
        "Комментарии": "\n".join(book_data['comments']) if book_data['comments'] else "Нет комментариев",
    }
    print("\n".join(f"{key}: {value}" for key, value in book_info.items()), "-" * 100, sep="\n")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Скачать книги с сайта tululu.org.")
    parser.add_argument("start_id", type=int, help="ID книги, с которой начать скачивание.")
    parser.add_argument("end_id", type=int, help="ID книги, на которой закончить скачивание.")
    parser.add_argument("--no-txt", action="store_false", dest="download_txt", help="Не скачивать текст книги.")
    parser.add_argument("--no-cover", action="store_false", dest="download_cover", help="Не скачивать обложку книги.")

    return parser.parse_args()


def main():
    args = parse_arguments()

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            book_data = collect_book_data(book_id)
            display_book_info(book_data)

            if args.download_txt:
                download_txt(book_id, book_data['title'])

            if args.download_cover and book_data['cover_url']:
                download_image(book_data['cover_url'])

        except HTTPError as e:
            print(f"Ошибка обработки книги ID {book_id}: {e}\n{'-' * 100}")
        except OSError as e:
            print(f"Ошибка записи файла для книги ID {book_id}: {e}\n{'-' * 100}")


if __name__ == "__main__":
    main()
