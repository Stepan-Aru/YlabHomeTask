# YlabHomeTask

## Домашнее задание.

### Запуск:

Для запуска проекта, находясь в кроневой директории проекта выполните команду:
```sh
docker-compose up
```
Тесты можно запустить в двух режимах:

С отдельным контейнером с СУБД:
```sh
docker-compose -f docker-compose-test-standalone.yaml up
```
С использованием основного контейнера с СУБД (в нем создается тестовая БД, которая удаляется после тестов):
```sh
docker-compose -f docker-compose-test.yaml up
```

### Описание:

В проекте применен следующий стек технологий:

* FastAPI
* Uvicorn
* PosgresSQL
* SQLAlchemy
* Asyncpg
* Redis
* Celery
* Rabbitmq
* Flower
* Docker, docker-compose
*
