import os
import sys
import telebot
from dotenv import load_dotenv


def main():
    # Load .env if present (useful for local development)
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN environment variable is not set. Create a .env or export the variable.")
        sys.exit(1)

    bot = telebot.TeleBot(token)

    @bot.message_handler(func=lambda m: True)
    def get_id(message):
        chat_id = message.chat.id
        print("CHAT ID:", chat_id)
        bot.reply_to(message, f"Chat ID: {chat_id}")

    try:
        bot.infinity_polling()
    except Exception as e:
        print("ERROR: polling failed:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()