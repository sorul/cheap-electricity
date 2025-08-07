# Makefile for the cheap_electricity project

.PHONY: install run

# Install project dependencies using Poetry
install:
	@echo "--- Installing dependencies... ---"
	@poetry install

# Run the main script
# The script handles loading variables from the .env file itself
run:
	@echo "--- Running the electricity price script... ---"
	@poetry run python cheap_electricity/main.py
