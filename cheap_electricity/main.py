import asyncio
import datetime
import os
from typing import Any, Dict, Optional, Tuple

import pandas as pd
import requests
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables from .env file
load_dotenv()

# --- Environment Variables ---
ESIOS_API_TOKEN: Optional[str] = os.getenv("ESIOS_API_TOKEN")
TELEGRAM_BOT_TOKEN: Optional[str] = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID: Optional[str] = os.getenv("TELEGRAM_CHAT_ID")


# --- ESIOS API Functions ---
def get_prices_for_today() -> Optional[Dict[str, Any]]:
  """Fetches the PVPC electricity prices for the current day from the esios API."""
  if not ESIOS_API_TOKEN:
    print("Error: ESIOS_API_TOKEN not configured in .env file.")
    return None

  today = datetime.date.today()
  start_date = today.strftime('%Y-%m-%dT00:00:00')
  end_date = today.strftime('%Y-%m-%dT23:59:59')
  url = f"https://api.esios.ree.es/indicators/1001?start_date={start_date}&end_date={end_date}"
  headers = {
      'Accept': 'application/json; application/vnd.esios-api-v2+json',
      'Content-Type': 'application/json',
      'x-api-key': ESIOS_API_TOKEN,
      'User-Agent': 'cheap_electricity-python-client/1.0'
  }

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"Error fetching data from esios API: {e}")
    return None


def get_mock_prices() -> Dict[str, Any]:
  """Returns a mock JSON response simulating the esios API for development."""
  print("--- USING MOCK DATA ---")
  today_str = datetime.date.today().strftime('%Y-%m-%d')
  now_hour = datetime.datetime.now().hour
  prices = [
      130.1, 125.5, 120.0, 115.8, 110.2, 112.7, 122.3, 135.9, 150.0, 160.4,
      165.1, 163.2, 158.8, 155.6, 168.0, 170.3, 175.9, 180.5, 190.1, 200.6,
      210.0, 195.4, 185.2, 178.9
  ]
  # Force a cheap price at the current hour for testing notification
  prices[now_hour] = 90.0

  return {
      "indicator": {
          "name":
          "PVPC",
          "values": [{
              "value": p,
              "datetime": f"{today_str}T{h:02d}:00:00.000+02:00"
          } for h, p in enumerate(prices)]
      }
  }


# --- Price Processing Functions ---
def process_and_categorize_prices(prices_data: Dict[str, Any]) -> Tuple[Optional[float], Optional[str]]:
  if not prices_data or 'indicator' not in prices_data or not prices_data[
      'indicator'].get('values'):
    print("Invalid data format or no values.")
    return None, None

  all_hourly_prices = prices_data['indicator']['values']
  # Filter prices for the Peninsula region
  hourly_prices = [
      p for p in all_hourly_prices if p.get('geo_name') == 'Península'
  ]

  if not hourly_prices:
    print("No prices found for the 'Peninsula' region.")
    return None, None

  # --- Debug: Print prices in a pandas DataFrame ---
  df = pd.DataFrame(hourly_prices)
  df['datetime'] = pd.to_datetime(df['datetime'])
  df = df.set_index('datetime')
  # Drop geo columns for cleaner output as they are now redundant
  df = df.drop(columns=['geo_id', 'geo_name'], errors='ignore')
  print("--- Hourly electricity prices (Peninsula) ---")
  print(df)
  print("---------------------------------------------")
  # --- End Debug ---

  # Calculate percentile-based limits
  prices = [p['value'] for p in hourly_prices]
  green_limit = pd.Series(prices).quantile(0.33)
  red_limit = pd.Series(prices).quantile(0.66)

  now = datetime.datetime.now()
  current_price_info: Optional[Dict[str, Any]] = None
  for price_info in hourly_prices:
    price_time = datetime.datetime.fromisoformat(price_info['datetime'])
    if price_time.hour == now.hour:
      current_price_info = price_info
      break

  if not current_price_info:
    print(f"Price not found for the current hour ({now.hour}:00).")
    return None, None

  current_price = current_price_info['value']
  if current_price <= green_limit:
    category = "Green"
  elif current_price >= red_limit:
    category = "Red"
  else:
    category = "Yellow"

  return current_price, category


# --- Telegram Notification Function ---
async def send_telegram_notification(price: float) -> None:
  if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("Error: Telegram environment variables not set in .env")
    return

  bot = Bot(token=TELEGRAM_BOT_TOKEN)
  message = f"¡Hora de luz barata! 🟢\nEl precio actual es {price} €/MWh."

  try:
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    print("Notificación de Telegram enviada.")
  except Exception as e:
    print(f"Error al enviar la notificación de Telegram: {e}")


# --- Main Execution ---
async def main() -> None:
  # TODO: When the esios API token is active, change to True.
  USE_REAL_DATA = True

  if USE_REAL_DATA:
    price_data = get_prices_for_today()
  else:
    price_data = get_mock_prices()

  if not price_data:
    return

  current_price, category = process_and_categorize_prices(price_data)

  if current_price is None:
    return

  color_map = {"Green": "\033[92m", "Yellow": "\033[93m", "Red": "\033[91m"}
  color_end = "\033[0m"
  safe_category = category if isinstance(category, str) else ""
  print(
      f"The current price is {current_price} €/MWh. Category: {color_map.get(safe_category, '')}{safe_category}{color_end}"
  )

  if category == "Green":
    await send_telegram_notification(current_price)


if __name__ == "__main__":
  asyncio.run(main())
