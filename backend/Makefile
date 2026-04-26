dev:
	uvicorn app.main:app --reload --port 8000

db:
	docker compose up -d

db-stop:
	docker compose down

migrate:
	alembic upgrade head

migration:
	alembic revision --autogenerate -m "$(m)"

install:
	pip install -r requirements.txt
