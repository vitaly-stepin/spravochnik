.PHONY: up down migrate feed dev test

up:
	docker-compose up -d --build

down:
	docker-compose down -v

migrate:
	docker-compose exec app alembic upgrade head

feed:
	docker-compose exec app python scripts/generate_data_for_db.py

dev:
	poetry run uvicorn main:app --reload

test:
	poetry run pytest
	
