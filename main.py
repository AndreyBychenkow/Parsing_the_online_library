import os

import requests

os.makedirs('books', exist_ok=True)

for book_id in range(1, 11):
    url = f"https://tululu.org/txt.php?id={book_id}"

    response = requests.get(url)
    response.raise_for_status()

    filename = f'books/id_book_{book_id}.txt'

    with open(filename, 'wb') as file:
        file.write(response.content)

    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        decoded_text = file.read()

print("Все книги скачаны.")
