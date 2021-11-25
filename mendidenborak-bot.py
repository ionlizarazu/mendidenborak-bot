import logging
import os

from mendidenborak import MendiDenborak
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

import os

TOKEN = os.getenv('TOKEN')
logger = logging.getLogger(__name__)
PORT = int(os.environ.get("PORT", 5000))
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

def startingMenu():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Hasi ibilbidearekin", callback_data="hasiIbilbidea"
                )
            ],
        ]
    )



def startBot(update, context, update_message=False, language=False):
    if update.message:
        message = update.message
        user = message.from_user
    else:
        message = update.callback_query.message
        user = message.chat

    context.bot.send_message(
        chat_id=message.chat.id,
        text="Kaixo {}!\n\nNi Mendidenborak naiz, zure mendiko ibilbideen denborak kalkulatzen lagunduko dizun bot-a.".format(
            user.first_name
        ),
        reply_markup=startingMenu(),
    )


def hasiIbilbidea(
    update,
    context,
    update_message=False,
    language=False,
):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Denbora kalkulatzeko, aurrena aukeratu bide mota nagusia:",
        reply_markup=ibilbideaMenu(),
    )


def ibilbideaMenu():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "pista", callback_data="Pista"
                )
            ],
            [
                InlineKeyboardButton(
                    "bidexka", callback_data="Bidexka"
                )
            ],
            [
                InlineKeyboardButton(
                    "bidexka-zaila", callback_data="BidexkaZaila"
                )
            ],
            [
                InlineKeyboardButton(
                    "bidez-kanpo", callback_data="BidezKanpo"
                )
            ],
        ]
    )



def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", startBot))
    dp.add_handler(CommandHandler("hasi", startBot))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)

    updater.bot.setWebhook("https://mendidenborak-bot.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
