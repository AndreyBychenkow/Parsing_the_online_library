import argparse
import json
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, ConnectionError, Timeout

from tululu import (
    download_image,
    download_txt,
    parse_book_page,
    fetch_page,
)

BASE_URL = "https://tululu.org"
CATEGORY_URL = f"{BASE_URL}/l55/"


def save_books_to_json(books, filename='books.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=4)


def get_book_links_from_page(page_url):
    response = fetch_page(page_url)
    soup = BeautifulSoup(response.text, 'lxml')

    book_cards = soup.select('table.d_book')
    if not book_cards:
        raise ValueError("Книги не найдены на странице.")

    book_links = [
        urljoin(BASE_URL, card.select_one('a')['href'])
        for card in book_cards if card.select_one('a') and card.select_one('a').get('href')
    ]
    return book_links


def get_all_book_links(start_page, end_page):
    all_links = []
    for page_number in range(start_page, end_page + 1):
        page_url = f"{CATEGORY_URL}{page_number}/"
        print(f"Парсим страницу: {page_url}")
        links = get_book_links_from_page(page_url)
        all_links.extend(links)
    return all_links


def main():
    parser = argparse.ArgumentParser(description="Скачивание книг с сайта tululu.org")

    parser.add_argument("--start_page", type=int, required=True,
                        help="Номер начальной страницы для скачивания книг.")
    parser.add_argument("--end_page", type=int, default=None,
                        help="Номер конечной страницы для скачивания книг. Если не указан, скачаются с начальной страницы.")

    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page if args.end_page else start_page

    all_links = get_all_book_links(start_page, end_page)
    print(f"Найдено {len(all_links)} ссылок на книги.")

    books_data = []
    retries = 5
    delay = 3

    for index, url in enumerate(all_links, start=1):
        print(f"Обработка книги {index}/{len(all_links)}: {url}")
        for attempt in range(1, retries + 1):
            try:
                response = fetch_page(url)
                book_details = parse_book_page(response.text, url)

                download_txt(book_details['id'], book_details['title'])

                if book_details['cover_url']:
                    download_image(book_details['cover_url'])

                books_data.append(book_details)
                save_books_to_json(books_data)

                break
            except (ConnectionError, Timeout):
                print(f"Попытка {attempt}/{retries}: Ошибка подключения.")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    print(f"Пропускаем книгу {url} из-за сетевых проблем.")
            except HTTPError:
                print(f"Ошибка обработки книги. Редирект на главную страницу. URL:{BASE_URL}")
                break
            except OSError:
                print(f"Ошибка записи файла для книги {url}:")
                break

    print(f'\nЗавершено! Все доступные файлы были скачаны!')


if __name__ == "__main__":
    main()
