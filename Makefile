
.PHONY: setup api ui lint test embed index

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

api:
	uvicorn api.main:app --reload --port 8000

ui:
	streamlit run ui/app.py

lint:
	ruff check .

test:
	pytest -q

embed:
	python indexer/embed.py

index:
	python indexer/index_opensearch.py
