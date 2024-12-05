import os

import requests
from requests.exceptions import HTTPError


def check_for_redirect(response):
    if response.history:
        raise HTTPError("Редирект на главную страницу.")


def download_book(book_id, folder='books'):
    url = f"https://tululu.org/txt.php?id={book_id}"
    response = requests.get(url)

    if not response.ok:
        raise HTTPError(f"Не удалось получить данные для книги с ID {book_id}.")

    check_for_redirect(response)

    filename = os.path.join(folder, f'id_book_{book_id}.txt')
    with open(filename, 'wb') as file:
        file.write(response.content)

    return filename


def read_book_content(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()


def main():
    os.makedirs('books', exist_ok=True)

    for book_id in range(1, 11):
        try:
            filepath = download_book(book_id)
            content = read_book_content(filepath)
            print(f"Книга с ID {book_id} успешно скачана.")
        except requests.HTTPError as e:
            print(f"Ошибка при скачивании книги с ID {book_id}: {e}")
        except requests.DecodeError as e:
            print(f"Произошла ошибка при обработке книги с ID {book_id}: {e}")

    print("Все доступные книги обработаны.")


if __name__ == "__main__":
    main()
