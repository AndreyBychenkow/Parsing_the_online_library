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


def get_comments(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = fetch_page(url)

    soup = BeautifulSoup(response.text, 'lxml')
    comments_section = soup.find_all('div', class_='texts')

    return [
        comment_div.find('span').text.strip()
        for comment_div in comments_section
        if comment_div.find('span')
    ]


def download_txt(book_id, title, folder='books'):
    url = f"https://tululu.org/txt.php?id={book_id}"
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


def get_book_cover_url(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = fetch_page(url)

    soup = BeautifulSoup(response.text, 'lxml')
    img_tag = soup.find('div', class_='bookimage').find('img')

    if img_tag and img_tag.get('src'):
        return urljoin(url, img_tag['src'])

    return None


def parse_book_page(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = fetch_page(url)

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('div', id='content').find('h1')
    genre_tags = soup.find('span', class_='d_book').find_all('a')

    title = title_tag.text.split(':')[0].strip() if title_tag else f"Книга_{book_id}"
    genres = [genre.text.strip() for genre in genre_tags] if genre_tags else []

    return title, genres


def main():
    for book_id in range(5, 11):
        try:

            title, genres = parse_book_page(book_id)
            download_txt(book_id, title)
            comments = get_comments(book_id)
            cover_url = get_book_cover_url(book_id)

            print(f"\nЗаголовок: {title}")
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
