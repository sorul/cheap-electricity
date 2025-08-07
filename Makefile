# Makefile for the cheap_electricity project

.PHONY: install run requirements dev_requirements

# Install project dependencies using Poetry
install:
	@echo "--- Installing dependencies... ---"
	@poetry install

# Run the main script
# The script handles loading variables from the .env file itself
run:
	@echo "--- Running the electricity price script... ---"
	@poetry run python cheap_electricity/main.py

# Generate requirements files
requirements:
	@poetry lock
	@poetry export -f requirements.txt --output requirements.txt --without-hashes

dev_requirements:
	@poetry lock
	@poetry export --with dev -f requirements.txt --output requirements_dev.txt --without-hashes
