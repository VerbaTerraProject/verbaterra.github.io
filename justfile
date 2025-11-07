# If you have `just` installed
install: 
	pip install -e ".[dev,ui]"
ui:
	streamlit run app/streamlit_app.py
lint:
	ruff check src tests
	black --check .
test:
	pytest -q
