# Electricity Tariff API Checker

This project consists of a Python script that queries the daily price of the PVPC (Voluntary Price for the Small Consumer) electricity tariff in Spain through the ESIOS API from Red Eléctrica de España (REE).

**Note:** Currently, the script is configured to fetch and process prices only for the **Iberian Peninsula**.

The script determines whether the price at the current hour is cheap, average, or expensive, and sends a notification to a Telegram chat when the price is low.

## Features

- **Real-Time Price Query**: Fetches the hourly electricity prices for the current day for the Spanish Peninsula.
- **Price Categorization**: Classifies prices into three categories (Green, Yellow, Red) using the 33rd and 66th percentiles as thresholds.
- **Console Output**: Displays the current price and its category with a color code for easy identification.
- **Telegram Notifications**: Sends an alert to a specific Telegram chat during the hours when the electricity price is cheapest (Green category).
- **Simple Configuration**: Manages API keys and other parameters through a `.env` file.

## Requirements

- Python 3.10 or higher
- Poetry for dependency management

## Installation

1.  **Clone the repository (if necessary):**
    ```bash
    git clone <REPOSITORY_URL>
    cd cheap_electricity
    ```

2.  **Create the configuration file:**
    Create a file named `.env` in the project root. You can use the following example as a template:

    ```ini
    # ESIOS API Token from Red Eléctrica
    ESIOS_API_TOKEN="YOUR_ESIOS_TOKEN"

    # Telegram Bot Token
    TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_TOKEN"

    # ID of the Telegram chat where notifications will be sent
    TELEGRAM_CHAT_ID="YOUR_CHAT_ID"
    ```
    - To get the `ESIOS_API_TOKEN`, request it by email from `consultasios@ree.es`.
    - To get the `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`, you will need to create a bot on Telegram and add it to the desired chat.

3.  **Install dependencies:**
    The `Makefile` provides a command to install everything needed using Poetry.
    ```bash
    make install
    ```
    This will install all the libraries specified in `pyproject.toml`.

## Usage

To run the script, simply use the `run` command from the `Makefile`:

```bash
make run
```

The script will execute, fetch the prices, display a DataFrame in the console with the day's prices for the Peninsula, and finally print the current hour's price along with its color category. If the category is "Green", it will send a notification to Telegram.
