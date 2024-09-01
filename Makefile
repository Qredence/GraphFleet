.PHONY: install test lint format run cli api docker-build docker-run streamlit docs docs-serve

install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run flake8 src tests

format:
	poetry run black src tests

run:
	poetry run python -m src.graphfleet

cli:
	poetry run graphfleet info

api:
	poetry run uvicorn src.graphfleet.api:app --reload --port 8000

docker-build:
	docker build -t graphfleet .

docker-run:
	docker run -p 8000:8000 graphfleet

streamlit:
	poetry run streamlit run src/graphfleet/streamlit_app.py

docs:
	cd docs && poetry run make html

docs-serve:
	cd docs/_build/html && python -m http.server 8000

docker-build-streamlit:
	docker build -t graphfleet-streamlit -f Dockerfile.streamlit .

docker-run-streamlit:
	docker run -p 8501:8501 -e API_URL=http://host.docker.internal:8000 graphfleet-streamlit

mypy:
	poetry run mypy src tests

isort:
	poetry run isort src tests

check: lint mypy isort