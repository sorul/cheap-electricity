import datetime
import json
import os
from typing import Any, Dict, Optional

import requests

from cheap_electricity import config


def _read_cache(path: str) -> Optional[Dict[str, Any]]:
  """Reads and decodes the JSON cache file."""
  if not os.path.exists(path):
    return None
  with open(path, 'r') as f:
    try:
      return json.load(f)
    except json.JSONDecodeError:
      return None


def _is_cache_valid(data: Optional[Dict[str, Any]],
                    today: datetime.date) -> bool:
  """Validates that the cache data is not corrupt and is for the current day."""
  if not data or 'indicator' not in data or not data['indicator'].get('values'):
    return False
  try:
    value_date_str = data['indicator']['values'][0]['datetime']
    value_date = datetime.datetime.fromisoformat(value_date_str).date()
    return value_date == today
  except (KeyError, IndexError, ValueError):
    return False


def _fetch_and_cache_prices(path: str,
                            today: datetime.date) -> Optional[Dict[str, Any]]:
  """Fetches prices from the API and saves them to the cache."""
  if not config.ESIOS_API_TOKEN:
    print("Error: ESIOS_API_TOKEN not configured in .env file.")
    return None

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
    print(f"Fetching prices for {today} from ESIOS API...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
      json.dump(data, f)
    return data
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from esios API: {e}")
    return None


def get_prices_for_today() -> Optional[Dict[str, Any]]:
  """
    Fetches the PVPC electricity prices for the current day from the esios API.
    It caches the prices in a file to avoid making multiple calls to the API.
    The cache is checked for today's date before being used.
    """
  data_dir = os.path.join(os.path.dirname(__file__), 'data')
  cache_file = os.path.join(data_dir, 'prices.json')
  today = datetime.date.today()

  cached_data = _read_cache(cache_file)
  if _is_cache_valid(cached_data, today):
    print(f"Using cached prices for {today}.")
    return cached_data

  return _fetch_and_cache_prices(cache_file, today)
