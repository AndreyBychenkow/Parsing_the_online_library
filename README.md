# 📄 Парсер книг с сайта Tululu.org

## 🔗 Скрипт tululu.py

Скрипт позволяет скачивать книги, их описания, жанры, комментарии и обложки с сайта [Tululu.org](https://tululu.org).

## Описание
	
Программа парсит страницы книг, извлекая следующую информацию:
	- Название книги
	- Автор книги
	- Жанр
	- Ссылка на картинку
	- Комментарии

**Скачанные книги и обложки сохраняются в отдельные директории на вашем устройстве.**

##  🛠 Установка

1. 📌 **Клонируйте репозиторий:**
```bash
	git clone https://github.com/AndreyBychenkow/Parsing_the_online_library.git
```

2. 📌 **Убедитесь, что у вас установлен Python версии 3.7 или выше.**



3. 📌 **Установите зависимости:**   
       
```bash
    pip install -r requirements.txt       
```
   
## 🚀 Запуск

	
Скрипт принимает два обязательных аргумента:

1. start_id — ID книги, с которой начать скачивание.
2. end_id — ID книги, на которой закончить скачивание.
	
📌 **Пример запуска**

* Скачивание текста и обложек (по умолчанию):		
```bash
python tululu.py 5 15   
```

В результате будут скачаны книги с ID от 5 до 15 включительно.

**Результаты:**
	
* Книги сохраняются в папке books.

* Обложки сохраняются в папке images.


![books](https://i.postimg.cc/xdbLLspV/books.jpg)

**Дополнительные опции:**

* Скачивание только текста книги:
```bash
python tululu.py 5 15 --no-cover  
```

* Скачивание только обложек:
```bash
python tululu.py 5 15 --no-txt 
```

📌 **Пример вывода**

При успешном выполнении скрипта в консоль будет выведена информация о книгах:

![Запуск скрипта](https://i.postimg.cc/wBWRzqtP/14-12-2024-115140.gif)


# 🔗 Скрипт parse_tululu_category.py

Скрипт позволяет скачивать книги по жанрам:

## 🚀 Запуск

Скрипт принимает следующие аргументы командной строки:

- start_page — Номер страницы, с которой начать скачивание.
- end_page — Номер страницы, на которой закончить скачивание (если не указан, скачиваются книги только с указанной страницы).
- dest_folder — Путь к каталогу для сохранения книг, изображений и JSON. По умолчанию используется папка downloads.
- skip_imgs — Не скачивать изображения (если установлен).
- skip_txt — Не скачивать текстовые файлы (если установлен).


- Выбираем на сайте нужную категорию книг по жанрам и копируем url(на примере 'Научная фантастика')
- Вставляем данный url в строку CATEGORY_URL

![категория](https://i.postimg.cc/0QVwBJr4/image.jpg)


- Переходим в терминал и прописываем следующие команды в зависимости от желаемого результата:

1. Скачивание книг с обложками (по умолчанию):

```bash
python parse_tululu_category.py --start_page 1 --end_page 2
```

**В результате будут скачаны книги с 1 по 2 страницу включительно, включая их текст и обложки.**


2. Скачивание книг без изображений:

```bash
python parse_tululu_category.py --start_page 1 --end_page 2 --skip_imgs
```

**В результате будут скачаны только текст книги с 1 по 2 страницу включительно без обложки.**


3. Скачивание книг без текстовых файлов:

```bash
python parse_tululu_category.py --start_page 1 --end_page 2 --skip_txt
```

**В результате будут скачаны только обложки книг с 1 по 2 страницу включительно без текста.**


4. Скачивание книг в указанную папку:

```bash
python parse_tululu_category.py --start_page 1 --end_page 2 --dest_folder "/path/to/folder"
```

**В результате будут скачаны книги с 1 по 2 страницу включительно, включая их текст и обложки в указанную папку.**


📌 **Пример вывода**

При успешном выполнении скрипта в консоль будет выведена информация о книгах, а также процесс скачивания и сохранения:

![start](https://i.postimg.cc/gcZwRJWm/start.jpg)

![start](https://i.postimg.cc/zXwVtcvQ/end.jpg)


**В файле books.json можно посмотреть более подробную информацию о скачанных книгах**

![start](https://i.postimg.cc/8PLyzMPv/json.jpg)


## 🔍 Логирование ошибок

Если страница книги недоступна, скрипт отобразит сообщение об ошибке и продолжит работу:

![редирект ошибка](https://i.postimg.cc/7h1V0B6Z/Redirect-error.jpg)

## Ограничения

* Скрипт не проверяет доступность папок для сохранения данных.
* Парсер рассчитан на структуру страниц сайта Tululu.org и может не работать, если структура изменится.


## 🎯  Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
