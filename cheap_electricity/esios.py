import datetime
from typing import Any, Dict, Optional

import requests

from cheap_electricity import config


def get_prices_for_today() -> Optional[Dict[str, Any]]:
    """Fetches the PVPC electricity prices for the current day from the esios API."""
    if not config.ESIOS_API_TOKEN:
        print("Error: ESIOS_API_TOKEN not configured in .env file.")
        return None

    today = datetime.date.today()
    start_date = today.strftime('%Y-%m-%dT00:00:00')
    end_date = today.strftime('%Y-%m-%dT23:59:59')
    url = f"https://api.esios.ree.es/indicators/1001?start_date={start_date}&end_date={end_date}"
    headers = {
        'Accept': 'application/json; application/vnd.esios-api-v2+json',
        'Content-Type': 'application/json',
        'x-api-key': config.ESIOS_API_TOKEN,
        'User-Agent': 'cheap_electricity-python-client/1.0'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from esios API: {e}")
        return None
