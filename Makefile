# Makefile para el proyecto tarifaluz

.PHONY: install run

# Instala las dependencias del proyecto usando Poetry
install:
	@echo "--- Instalando dependencias... ---"
	@poetry install

# Ejecuta el script principal
# El script se encarga de cargar las variables del .env por sí mismo
run:
	@echo "--- Ejecutando el script de precio de la luz... ---"
	@poetry run python tarifaluz/precio_luz.py
