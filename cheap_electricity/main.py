import asyncio

from .esios import get_prices_for_today
from .price_processing import process_and_categorize_prices
from .notifications import send_telegram_notification


async def main() -> None:
    price_data = get_prices_for_today()
    if not price_data:
        return

    current_price, category = process_and_categorize_prices(price_data)
    if current_price is None:
        return

    color_map = {"Green": "\033[92m", "Yellow": "\033[93m", "Red": "\033[91m"}
    color_end = "\033[0m"
    print(
        f"The current price is {current_price} €/MWh. "
        f"Category: {color_map.get(category, '')}{category or ''}{color_end}"
    )

    if category == "Green":
        await send_telegram_notification(current_price)


if __name__ == "__main__":
    asyncio.run(main())
