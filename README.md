# Crypto Telegram Bot
This repository contains the implementation of the crypto Telegram bot for the
test task for the AI engineer role. The structure of the project follows:
1. `crypto-projects.json`: the JSON file that contains information about 5 cryptocurrency projects. It emulates the database.
2. `crypto-project-processor.py`: the script that processes the file and can search by status, tasks and group them together.
3. `bot`: the main Telegram bot that uses OpenAI API to answer user requests.

## Getting started
Here's how to get started:
1. Create the virtual environment:
```shell
python -m venv .venv
source .venv/bin/activate
```
2. Install dependencies:
```shell
pip install -r requirements.txt
```
3. Build the Docker container:
```shell
docker build -t crypto-telegram-bot .
```
4. Run the bot:
```shell
docker run --env-file ./.env crypto-telegram-bot
# Or without Docker:
PYTHONPATH=$(pwd) python -m bot
```
You will need to pass the `TELEGRAM_API_TOKEN` and `OPENAI_API_KEY` 
environmental variables. The bot instance will be started and respond
to commands to the Telegram bot.