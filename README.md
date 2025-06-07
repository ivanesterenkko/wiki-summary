# 🚀 Wiki Summary 

Асинхронный проект на FastAPI + SQLAlchemy с использование BeautifulSoup и OpenAI.

## 📦 Требования

- Python 3.12+
- Docker, Docker Compose
- pre-commit

## ⚙️ Настройка окружения

1. Клонируйте репозиторий:

```bash
git clone <repo-url>
cd roof-backend
```

2. Установите pre-commit:

```bash
pip install pre-commit
pre-commit install
```

Теперь при коммите будет выполняться автоматическая проверка всех файлов на соответствие PEP8 (ruff/black/isort).

## ⚙️ Настройка .env

Создайте файл `.env` (пример: `.env.example`) с переменными окружения:

```dotenv
SECRET_KEY="e8a702f8-b6a5ae1afa0515"
ALGORITHM=HS256

# Service
SERVICE_NAME="WIKI Summary"
SERVICE_VERSION=1.0.0
APP_RELEASE=""
API_VERSION=v1
ENVIRONMENT=local
SERVICE_PORT=8000

# POSTGRES
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=wiki_app

# OpenAI
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
OPENAI_URL="https://api.proxyapi.ru/openai/v1"
```

Для получения OPENAI_API_KEY был использован `proxyapi`. Можно использовать другой, подходящих к OpenAI сервис или сам OpenAI. Если будет использоваться другой, то необходимо поленять `OPENAI_URL` на тот, который будет указан в данном сервисе.


## 🐳 Локальный запуск в Docker

```bash
./start-full.sh
```

## ✅ Миграции Alembic

Для создания миграции необходимо выполнить данные команды:
```bash
docker exec -it wiki_api bash
alembic -c src/alembic.ini revision --autogenerate -m "init"
alembic -c src/alembic.ini upgrade head
```

## 📁 Основная структура проекта

```
src/
 ├── api/          # Эндпоинты FastAPI
 ├── services/     # Бизнес-логика
 ├── crud/         # CRUD-операции
 ├── models/       # ORM-модели SQLAlchemy
 ├── schemas/      # Pydantic-схемы
 ├── security/     # Аутентификация и авторизация
 ├── databases/    # Alembic миграции, настройки БД
 ├── configs/      # Конфиги и .env
 ├── constants/    # Константы проекта
 ├── utilities/    # Утилиты, интеграции (BeautifulSoup, OpenAI и др.)
 ├── main.py       # Точка входа (FastAPI app)
```
