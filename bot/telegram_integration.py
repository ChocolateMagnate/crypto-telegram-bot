from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from bot.llm import LLM


class CryptoProjectBot:
    def __init__(self, telegram_token: str, openai_api_key: str):
        self.app = Application.builder().token(telegram_token).build()
        self.llm = LLM(
            model="gpt-4o",
            openai_api_key=openai_api_key,
            temperature=0.8,
        )

        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Hi! I can help you learn about cryptocurrency projects. Ask me anything!"
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Send "thinking" message first
        thinking_message = await update.message.reply_text("Thinking...")

        # Process the text
        response = await self.llm.respond(update.message.text)

        # Edit the "thinking" message with the actual response
        await thinking_message.edit_text(response)

    def run(self) -> None:
        """Start the bot."""
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

