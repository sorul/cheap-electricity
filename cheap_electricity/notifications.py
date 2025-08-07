from telegram import Bot

from . import config
from .price import Price, ColorEnum


async def send_telegram_notification(current: Price, previous: Price) -> None:
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("Error: Telegram environment variables not set in .env")
        return

    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    if current.category.color is ColorEnum.GREEN:
        message = (
            f"Time for cheap power! {current.category.emoji}\n"
            f"Price changed from {previous.value} {previous.unit} ({previous.category.color.value}) "
            f"to {current.value} {current.unit} ({current.category.color.value})."
        )
    else:
        message = (
            "Cheap power period ended.\n"
            f"Price changed from {previous.value} {previous.unit} ({previous.category.color.value}) "
            f"to {current.value} {current.unit} ({current.category.color.value})."
        )

    try:
        await bot.send_message(chat_id=config.TELEGRAM_CHAT_ID, text=message)
        print("Telegram notification sent.")
    except Exception as e:
        print(f"Error sending the Telegram notification: {e}")
