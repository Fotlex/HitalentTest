Использовал стек:
    Python 3.13 + Django 5.2 + DRF

    PostgreSQL 17

    Pydantic v2 (управление настройками)

    Docker & Docker Compose

    Pytest (тестирование)

    drf-spectacular (OpenAPI 3.0)

Запуск
1. Подготовка окружения
Создайте файл .env в корневом каталоге проекта и заполните его (examle.env)
2. Запуск проекта
Использование Makefile (рекомендуется)

Если у вас установлена утилита make, запуск выполняется двумя командами:
code Bash

make build          # Сборка образов
make up             # Запуск контейнеров в фоне

Без использования make (напрямую через Docker)

Если make не установлен, используйте стандартные команды Docker Compose (учитывая путь к конфигу):

    Сборка:
    code Bash

    docker compose -f docker/docker-compose.prod.yaml --env-file .env build

    Запуск:
    code Bash

    docker compose -f docker/docker-compose.prod.yaml --env-file .env up -d



После запуска проект будет доступен по адресу: http://127.0.0.1/

    Swagger UI: http://127.0.0.1/api/docs/ — здесь можно протестировать все методы вручную.

    Схема OpenAPI (YAML): http://127.0.0.1/api/schema/




В проекте написаны автоматические тесты, покрывающие создание структур, каскадное удаление и валидацию циклов.

Запуск через Makefile:
code Bash

make test

Запуск без make:
code Bash

docker compose -f docker/docker-compose.prod.yaml --env-file .env exec web pytest -v


Для создания новых миграций (если вы изменили модели):
code Bash

docker compose -f docker/docker-compose.prod.yaml --env-file .env exec web python web/manage.py makemigrations

docker compose -f docker/docker-compose.prod.yaml --env-file .env exec web python web/manage.py migrate