
  
import json
import logging
from time import time
import datetime
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Bot, Message
from telegram.ext import Updater, CommandHandler, MessageHandler, \
    Filters, CallbackContext, ConversationHandler, InlineQueryHandler, CallbackQueryHandler

from Markups import Markups

from repo import *


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



def start(update: Update, context: CallbackContext):
    reply_keyboard = Markups.start
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text('Это NoFap Rating bot \n'

                              ,reply_markup=markup)
    # register user
    register(update.message.from_user.name, update.message.chat_id)


def enter_date(update: Update, context: CallbackContext):
    print('enter date')
    reply_keyboard = Markups.date
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Введите дату в формате ДД.ММ.ГГ или выберите из вариантов внизу", reply_markup=markup)
    return 1

def enter_result(update: Update, context: CallbackContext):
    global date
    date = update.message.text
    if date == Markups.date[0][0]:
        date = datetime.date.today()
    elif date == Markups.date[0][1]:
        date = datetime.date.today() - datetime.timedelta(days = 1)
    else:
    
        dateFormatter = "%d.%m.%y"
        date = datetime.datetime.strptime(date, dateFormatter)
    
    reply_keyboard = Markups.result
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Введите результат", reply_markup=markup)
    return 2

def data_added(update: Update, context: CallbackContext):
    global date
    result = update.message.text
    if result == Markups.result[0][0]:
        points = 1
    elif result == Markups.result[0][1]:
        points = 0
    else:
        update.message.reply_text('Воспользуйтесь кнопками внизу')
        return 2
    status = add_score(date, points, update.message.chat_id)


    reply_keyboard = Markups.start
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Данные добавлены", reply_markup=markup)
    return ConversationHandler.END

def get_data(update: Update, context: CallbackContext):
    print('get data')
    clean_days, all_days = get_score(update.message.chat_id)
    rating = clean_days / all_days * 100
    update.message.reply_text(f"WinRate: {str(rating)}% \n" \
                            f"Чистых дней всего: {str(clean_days)} \n" \
                            f"Очки: {str((rating / 100) ** 2 * clean_days)}")



def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    add_data_dialog = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(Markups.start[0][0]), enter_date),
                      CommandHandler('practice', enter_date)],
        states={
            1: [MessageHandler(Filters.text, enter_result)],
            2: [MessageHandler(Filters.text, data_added)],
        },
        fallbacks=[MessageHandler(Filters.text, start)]
    )

    _data_dialog = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(Markups.start[0][0]), enter_date),
                      CommandHandler('practice', enter_date)],
        states={
            1: [MessageHandler(Filters.text, enter_result)],
            2: [MessageHandler(Filters.text, data_added)],
        },
        fallbacks=[MessageHandler(Filters.text, start)]
    )

    dispatcher.add_handler(add_data_dialog)
    dispatcher.add_handler(MessageHandler(Filters.regex(Markups.start[0][1]), get_data))
    dispatcher.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
