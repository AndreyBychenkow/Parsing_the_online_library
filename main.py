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
        raise HTTPError("Редирект на главную страницу.")


def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def get_comments(soup):
    comments_section = soup.find_all('div', class_='texts')
    return [
        comment_div.find('span').text.strip()
        for comment_div in comments_section
        if comment_div.find('span')
    ]


def download_txt(book_id, title, folder='books'):
    url = f"{BASE_URL}/txt.php?id={book_id}"
    os.makedirs(folder, exist_ok=True)

    safe_filename = f"{book_id}. {sanitize_filename(title)}.txt"
    filepath = os.path.join(folder, safe_filename)

    response = fetch_page(url)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def download_image(url, folder='images'):
    response = fetch_page(url)

    os.makedirs(folder, exist_ok=True)

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

    book_data = {
        'title': title,
        'author': author,
        'genres': genres,
        'cover_url': get_book_cover_url(soup),
        'comments': get_comments(soup)
    }

    return book_data


def collect_book_data(book_id):
    url = f"{BASE_URL}/b{book_id}/"
    response = fetch_page(url)

    book_data = parse_book_page(response.text)

    return book_data


def main():
    parser = argparse.ArgumentParser(description="Скачать книги с сайта tululu.org.")
    parser.add_argument("start_id", type=int, help="ID книги, с которой начать скачивание.")
    parser.add_argument("end_id", type=int, help="ID книги, на которой закончить скачивание.")

    args = parser.parse_args()

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            book_data = collect_book_data(book_id)
            title, genres, comments, cover_url = (
                book_data['title'],
                book_data['genres'],
                book_data['comments'],
                book_data['cover_url']
            )

            download_txt(book_id, title)

            print(f"\nЗаголовок: {title}")
            print(f"Автор: {book_data['author']}")
            print(f"Жанр: {genres if genres else '[]'}")
            print(f"Ссылка на картинку: {cover_url if cover_url else 'Картинка отсутствует'}")
            print("Комментарии:")
            if comments:
                print("\n".join(f"- {comment}" for comment in comments))
            else:
                print("Данная книга не имеет комментариев.")
            print("-" * 50)

            if cover_url:
                download_image(cover_url)

        except requests.HTTPError as e:
            print(f"Ошибка: Книга с id {book_id} не доступна. {e}")
            print("-" * 50)
        except OSError:
            print(f"Книга с id {book_id}. Ошибка записи файла\n")

    print("Все доступные книги обработаны.")


if __name__ == "__main__":
    main()
