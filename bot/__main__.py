import os
import sys

from bot.telegram_integration import CryptoProjectBot

if __name__ == "__main__":
    telegram_token = os.getenv("TELEGRAM_API_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not telegram_token or not openai_api_key:
        sys.stderr.write("Please set TELEGRAM_API_TOKEN and OPENAI_API_KEY environment variables.\n")
        sys.exit(1)

    bot = CryptoProjectBot(telegram_token, openai_api_key)
    bot.run()
