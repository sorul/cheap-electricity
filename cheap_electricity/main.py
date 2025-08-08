import asyncio

from cheap_electricity.esios import get_prices_for_today
from cheap_electricity.price_processing import process_and_categorize_prices
from cheap_electricity.notifications import send_telegram_notification
from cheap_electricity.price import ColorEnum


async def main() -> None:
  price_data = get_prices_for_today()
  if not price_data:
    return

  current_price, previous_price = process_and_categorize_prices(price_data)
  if current_price is None or previous_price is None:
    return

  print(
      f"Current price: {current_price.value} {current_price.category.emoji}, "
      f"Previous price: {previous_price.value} {previous_price.category.emoji}")

  prev_green = previous_price.category.color is ColorEnum.GREEN
  curr_green = current_price.category.color is ColorEnum.GREEN
  if prev_green != curr_green:
    await send_telegram_notification(current_price, previous_price)


def run_main() -> None:
  """Entry point for the script."""
  asyncio.run(main())
