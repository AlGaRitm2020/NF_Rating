
  
import json
import logging
from time import time
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Bot, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext, ConversationHandler, InlineQueryHandler, CallbackQueryHandler

from Markups import Markups




# import token
try:
    # manual start
    # from local config file
    from config import TEST_TOKEN

    TOKEN = TEST_TOKEN
except ModuleNotFoundError:
    # else deployed on Heroku
    # DEPLOY TOKEN - env var on Heroku
    from load_env_vars import DEPLOY_TOKEN

    TOKEN = DEPLOY_TOKEN
    if not TOKEN:
        print('Copy config.py to root directory from Telegram chat')

bot = Bot(TOKEN)
CHAT_ID = ""
MESSAGE_IDS = []
CURRENT_TASK = -1
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
ANSWER = ""
VARIANT = []
ANSWERS = [None] * 27
TASK_NUMBER = 0
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    reply_keyboard = Markups.start
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Это NoFap Rating bot \n '

                              ,reply_markup=markup)
    # register user
    sql_work.register(update.message.from_user.name, update.message.chat_id)





def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    


    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
