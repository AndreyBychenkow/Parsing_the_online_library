import argparse
import os
import time
from urllib.parse import urljoin, urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError

BASE_URL = "https://tululu.org"


def check_for_redirect(response):
    if response.history:
        raise HTTPError(f"Редирект на главную страницу. URL: {response.url}")


def fetch_page(url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def get_comments(soup):
    comments_section = soup.select('div.texts span')
    return [comment.text.strip() for comment in comments_section]


def download_txt(book_id, title, folder='books'):
    url = f"{BASE_URL}/txt.php"
    params = {"id": book_id}
    os.makedirs(folder, exist_ok=True)

    safe_filename = f"{book_id}. {sanitize_filename(title)}.txt"
    filepath = os.path.join(folder, safe_filename)

    response = fetch_page(url, params=params)

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


def get_book_cover_url(soup, page_url):
    img_tag = soup.select_one('div.bookimage img')
    if img_tag and img_tag.get('src'):
        return urljoin(page_url, img_tag['src'])
    return None


def parse_book_page(html_content, page_url):
    soup = BeautifulSoup(html_content, 'lxml')

    title_tag = soup.select_one('div#content h1')
    genres = soup.select('span.d_book a')
    author_tag = soup.select_one('div#content h1')

    title = title_tag.text.split(':')[0].strip() if title_tag else "Неизвестный заголовок"
    genres_list = [genre.text.strip() for genre in genres] if genres else []
    author = author_tag.text.split('::')[-1].strip() if author_tag else "Автор неизвестен"

    book_id = page_url.split('/')[-2][1:]

    return {
        'title': title,
        'id': book_id,
        'author': author,
        'genres': genres_list,
        'cover_url': get_book_cover_url(soup, page_url),
        'comments': get_comments(soup),
    }


def display_book_info(book_details):
    book_info = {
        "\nЗаголовок": book_details['title'],
        "Автор": book_details['author'],
        "Жанр": str(book_details['genres']) if book_details['genres'] else "[]",
        "Ссылка на обложку": book_details['cover_url'] or "Обложка отсутствует",
        "Комментарии": "\n".join(book_details['comments']) if book_details['comments'] else "Нет комментариев",
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
        url = f"{BASE_URL}/b{book_id}/"
        retries = 5
        delay = 3

        for attempt in range(1, retries + 1):
            try:
                response = fetch_page(url)
                book_details = parse_book_page(response.text, url)
                display_book_info(book_details)

                if args.download_txt:
                    download_txt(book_id, book_details['title'])

                if args.download_cover and book_details['cover_url']:
                    download_image(book_details['cover_url'])

                break

            except requests.exceptions.ConnectionError as e:
                print(f"Попытка {attempt}/{retries}: Ошибка подключения - {e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    print(f"Пропускаем книгу ID {book_id} из-за сетевых проблем.\n{'-' * 100}")
            except HTTPError as e:
                print(f"Ошибка обработки книги ID {book_id}: {e}\n{'-' * 100}")
                break
            except OSError as e:
                print(f"Ошибка записи файла для книги ID {book_id}: {e}\n{'-' * 100}")
                break


if __name__ == "__main__":
    main()
