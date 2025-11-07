.PHONY: install ui test lint run docs

install:
	pip install -e ".[dev,ui]"

ui:
	streamlit run app/streamlit_app.py

lint:
	ruff check src tests || true
	black --check . || true

test:
	pytest -q

docs:
	mkdocs serve
