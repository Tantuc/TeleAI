import logging
import os
from dotenv import load_dotenv
import gpt4all

load_dotenv()

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

MODEL_NAME = os.getenv('MODEL_NAME', 'ggml-gpt4all-j-v1.3-groovy')
gptj = gpt4all.GPT4All(MODEL_NAME)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    messages = [{"role": "user", "content": user_input}]
    response = gptj.chat_completion(messages, verbose=False)
    await update.message.reply_text(response['choices'][0]['message']['content'])

def main() -> None:
    token = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    application.run_polling()

if __name__ == "__main__":
    main()
