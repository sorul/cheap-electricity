from telegram import Bot

from . import config


async def send_telegram_notification(price: float) -> None:
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("Error: Telegram environment variables not set in .env")
        return

    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    message = f"Time for cheap power! 🟢\nThe current price is {price} €/MWh."

    try:
        await bot.send_message(chat_id=config.TELEGRAM_CHAT_ID, text=message)
        print("Telegram notification sent.")
    except Exception as e:
        print(f"Error sending the Telegram notification: {e}")
