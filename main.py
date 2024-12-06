import os

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from requests.exceptions import HTTPError


def check_for_redirect(response):
    if response.history:
        raise HTTPError("Редирект на главную страницу.")


def fetch_page(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def download_txt(book_id, folder='books'):
    url = f"https://tululu.org/txt.php?id={book_id}"
    response = fetch_page(url)

    os.makedirs(folder, exist_ok=True)

    title = _parse_book_page(book_id)

    safe_filename = f"{book_id}. {sanitize_filename(title)}.txt"
    filepath = os.path.join(folder, safe_filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def _parse_book_page(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = fetch_page(url)

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('div', id='content').find('h1')

    if title_tag:
        title_parts = title_tag.text.split(':')
        return title_parts[0].strip()

    return f"Книга_{book_id}"


def main():
    downloaded_books = []

    for book_id in range(1, 11):
        try:
            filepath = download_txt(book_id)

            if filepath:
                title = _parse_book_page(book_id)
                downloaded_books.append((book_id, title))
                print(f"{book_id}. {title}.txt")

        except requests.HTTPError as e:
            print(f"{book_id}. Ошибка при скачивании книги: {e}")

    print("Все доступные книги обработаны.")


if __name__ == "__main__":
    main()
