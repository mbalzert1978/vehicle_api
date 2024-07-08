format:
	@echo "Running ruff format..."
	poetry run ruff format vehicle_api
	@echo "Running ruff check --fix..."
	poetry run ruff check --fix vehicle_api
