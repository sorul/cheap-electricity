import asyncio

from cheap_electricity.esios import get_prices_for_today
from cheap_electricity.price_processing import process_and_categorize_prices
from cheap_electricity.notifications import send_telegram_notification
from cheap_electricity.price import PriceCategory


async def main() -> None:
    price_data = get_prices_for_today()
    if not price_data:
        return

    current_price, previous_price = process_and_categorize_prices(price_data)
    if current_price is None or previous_price is None:
        return

    color_map = {
        PriceCategory.GREEN: "\033[92m",
        PriceCategory.YELLOW: "\033[93m",
        PriceCategory.RED: "\033[91m",
    }
    color_end = "\033[0m"
    category = current_price.category
    print(
        f"The current price is {current_price.value} {current_price.unit}. "
        f"Category: {color_map.get(category, '')}{category.value}{color_end}"
    )

    prev_green = previous_price.category is PriceCategory.GREEN
    curr_green = current_price.category is PriceCategory.GREEN
    if prev_green != curr_green:
        await send_telegram_notification(current_price, previous_price)


if __name__ == "__main__":
    asyncio.run(main())
