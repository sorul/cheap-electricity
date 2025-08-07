import datetime
import unicodedata
from typing import Any, Dict, Optional, Tuple

import pandas as pd



def process_and_categorize_prices(prices_data: Dict[str, Any]) -> Tuple[Optional[float], Optional[str]]:
    if not prices_data or 'indicator' not in prices_data or not prices_data['indicator'].get('values'):
        print("Invalid data format or no values.")
        return None, None

    all_hourly_prices = prices_data['indicator']['values']

    def _normalize(text: str) -> str:
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()

    # Filter prices for the Peninsula region
    hourly_prices = [p for p in all_hourly_prices if _normalize(p.get('geo_name', '')) == 'peninsula']

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
