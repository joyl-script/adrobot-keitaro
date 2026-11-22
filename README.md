# Adrobot Keitaro

Тестовое задание Adrobot. Сервис создаёт кампании в Keitaro и редактирует офферы в существующей кампании.

## Что умеет

- `POST /campaigns` создаёт кампанию с префиксом `test_vedernikova_` и сохраняет её в SQLite.
- `PATCH /campaigns/{id}/offers` добавляет и удаляет офферы, не создавая дубли.
- `GET /health` проверяет, что сервер жив.
- `GET /` открывает минимальный интерфейс с двумя формами.

## Стек

FastAPI, SQLAlchemy, Alembic, SQLite, httpx, Pydantic. Фронт на обычном HTML и JavaScript.

## Запуск

Нужен Python 3.14 или новее.

```bash
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env