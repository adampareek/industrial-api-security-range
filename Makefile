.PHONY: up down assess test lint clean

up:
	docker compose up --build -d

down:
	docker compose down

assess:
	python assessor/run_all.py

test:
	pytest -q

lint:
	python -m compileall -q api assessor internal_console tests

clean:
	rm -rf .pytest_cache findings/report.json
