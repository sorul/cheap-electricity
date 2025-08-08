# Contexto del Proyecto: cheap-electricity

Este proyecto Python tiene como objetivo principal monitorizar los precios de la electricidad (PVPC) en España y enviar notificaciones a Telegram basadas en cambios significativos en la categoría del precio.

## Estructura de Archivos Clave:

-   `cheap_electricity/main.py`: Contiene la lógica principal para:
    -   Obtener los precios de la electricidad de la API de ESIOS (o datos mock).
    -   Procesar y categorizar los precios por hora (Verde, Amarillo, Rojo) basándose en percentiles.
    -   Determinar cuándo enviar una notificación de Telegram según la lógica de cambio de categoría.
    -   Imprimir el estado actual y anterior del precio en la consola.
-   `cheap_electricity/notification.py`: Contiene la función asíncrona `send_telegram_notification` que se encarga de construir y enviar el mensaje a Telegram.
-   `tests/test_electricity_prices.py`: Contiene las pruebas unitarias para la lógica de categorización de precios y la función de notificación de Telegram, utilizando datos mock para evitar llamadas a la API.
-   `pyproject.toml`: Define las dependencias del proyecto, incluyendo `requests`, `pandas`, `python-telegram-bot`, `python-dotenv` y las dependencias de desarrollo `pytest` y `pytest-asyncio`.
-   `.env`: Archivo para configurar las variables de entorno sensibles (`ESIOS_API_TOKEN`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`).

## Lógica Principal:

1.  **Obtención de Precios:** El script obtiene los precios de la electricidad para el día actual.
2.  **Categorización:** Los precios se categorizan en "Verde" (más baratos), "Amarillo" (intermedios) o "Rojo" (más caros) basándose en los percentiles 33 y 66 de los precios del día.
3.  **Notificación de Telegram:** Se envía una notificación a Telegram **solo si** la categoría del precio actual cambia a "Verde" desde cualquier otro color, o si cambia de "Verde" a cualquier otro color. El mensaje incluye el precio y la categoría de la hora anterior y la actual.

## Cómo Ejecutar:

Para ejecutar el script principal:
```bash
make run
```

## Cómo Ejecutar Tests:

Para ejecutar las pruebas unitarias:
```bash
poetry run pytest tests/
```

## Variables de Entorno Necesarias:

Asegúrate de que el archivo `.env` en la raíz del proyecto contenga las siguientes variables:
-   `ESIOS_API_TOKEN`: Token para acceder a la API de ESIOS.
-   `TELEGRAM_BOT_TOKEN`: Token de tu bot de Telegram.
-   `TELEGRAM_CHAT_ID`: ID del chat o usuario de Telegram al que enviar las notificaciones.

## Directrices de Desarrollo:

-   **Idioma:** Todo el código, comentarios, nombres de variables y documentación deben estar en inglés.
-   **Estilo de Código:** Identacion usando 2 espacios. Sigue las convenciones de estilo PEP 8 para Python. Pon el tipo de todas las funciones y parametros de entrada.
-   **Documentación:** Utiliza docstrings para documentar funciones y clases. Aseg
-   **Pruebas:** Asegúrate de que todas las nuevas funcionalidades estén cubiertas por pruebas unitarias.