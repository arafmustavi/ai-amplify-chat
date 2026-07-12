.PHONY: install run dashboard test lint format docker-build docker-up docker-down clean

install:
	python -m pip install -r requirements.txt -r requirements-dev.txt

run:
	python app.py

dashboard:
	streamlit run dashboard.py

test:
	pytest --cov=amplify --cov-report=term-missing

lint:
	ruff check . && black --check .

format:
	ruff check . --fix && black .

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage
