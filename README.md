![workflow](https://github.com/p1vosos/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Foodgram

## Описание проекта
**Foodgram** – «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Как запустить проект в docker (dev-режим):

- Клонировать репозиторий и перейти в директорию с docker-compose.yaml:

```
git clone git@github.com:p1vosos/foodgram-project-react.git
cd foodgram-project-react/infra
```

- Развернуть 3 контейнера, nginx, database и web(сам проект + gunicorn):

```
docker-compose up -d
```

- Выполнить миграции и собрать статику:

```
docker-compose exec web python3 manage.py migrate
docker-compose exec web python3 manage.py collectstatic --no-input
```

- Заполнить базу тестовыми данными:

```
docker-compose exec web python3 manage.py loaddata fixtures.json
```

## Проект запущен и доступен по адресу:
- http://localhost/api/docs/ - подробная документация
- http://localhost/recipes/ - главная страница
- http://localhost/admin - админ зона

## Шаблон заполнения файла .env

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql  
DB_NAME=postgres # имя базы данных  
POSTGRES_USER=postgres # логин для подключения к базе данных  
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)  
DB_HOST=db # название сервиса (контейнера)  
DB_PORT=5432 # порт для подключения к БД

SECRET_KEY='a&l%11111aaaaaa^##a1)aaa@4aaa=aa&aaaal^##aaa1(aa'

## Автор

Петров Алексей <alexeypetrow21@gmail.com>  
