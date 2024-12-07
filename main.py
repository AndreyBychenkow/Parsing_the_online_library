import os
from urllib.parse import urljoin, urlsplit, unquote

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


def download_image(url, folder='images'):
    response = fetch_page(url)

    os.makedirs(folder, exist_ok=True)

    filename = unquote(urlsplit(url).path.split('/')[-1])
    filepath = os.path.join(folder, filename)

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return filepath


def get_book_cover_url(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = fetch_page(url)

    soup = BeautifulSoup(response.text, 'lxml')
    img_tag = soup.find('div', class_='bookimage').find('img')

    if img_tag and img_tag.get('src'):
        return urljoin(url, img_tag['src'])

    return None


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
    for book_id in range(5, 11):
        try:
            download_txt(book_id)

            title = _parse_book_page(book_id)
            cover_url = get_book_cover_url(book_id)

            if title and cover_url:
                filepath = download_image(cover_url)
                print(f"\nЗаголовок: {title}\nСсылка на картинку: {cover_url}\nОбложка: {filepath}\n")

        except requests.HTTPError as e:
            print(f"Ошибка: Книга с id {book_id} не доступна. {e}\n")
        except requests.OSError:
            print(f"Книга с id {book_id}. Ошибка записи файла\n")

    print("Все доступные книги обработаны.")


if __name__ == "__main__":
    main()
