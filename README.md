# 📄 Парсер книг с сайта Tululu.org

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
python main.py 5 15   
```

В результате будут скачаны книги с ID от 5 до 15 включительно.

**Результаты:**
	
* Книги сохраняются в папке books.

* Обложки сохраняются в папке images.


![books](https://i.postimg.cc/xdbLLspV/books.jpg)

**Дополнительные опции:**

* Скачивание только текста книги:
```bash
python main.py 5 15 --no-cover  
```

* Скачивание только обложек:
```bash
python main.py 5 15 --no-txt 
```

📌 **Пример вывода**

При успешном выполнении скрипта в консоль будет выведена информация о книгах:

![Запуск скрипта](https://i.postimg.cc/VvHZXm30/07-12-2024-210643.gif)


## 🔍 Логирование ошибок

Если страница книги недоступна, скрипт отобразит сообщение об ошибке и продолжит работу:

![редирект ошибка](https://i.postimg.cc/7h1V0B6Z/Redirect-error.jpg)

## Ограничения

* Скрипт не проверяет доступность папок для сохранения данных.
* Парсер рассчитан на структуру страниц сайта Tululu.org и может не работать, если структура изменится.


## 🎯  Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
