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

TOKEN = os.getenv("TOKEN")
logger = logging.getLogger(__name__)
PORT = int(os.environ.get("PORT", 5000))
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher


class Ibilbidea:
    def __init__(self):
        self.bidea = ""
        self.positiboa = 0
        self.negatiboa = 0
        self.luzeera = 0

    def set_bidea(self, bidea):
        self.bidea = bidea

    def set_positiboa(self, positiboa):
        try:
            self.positiboa = int(positiboa)
            return 0
        except ValueError:
            self.positiboa = 0
            return -1, "Positiboa ez da zenbaki osoa"

    def set_negatiboa(self, negatiboa):
        try:
            self.negatiboa = int(negatiboa)
            return 0
        except ValueError:
            self.negatiboa = 0
            return -1, "Negatiboa ez da zenbaki osoa"

    def set_luzeera(self, luzeera):
        try:
            self.luzeera = int(luzeera)
            return 0
        except ValueError:
            self.luzeera = 0
            return -1, "Luzeera ez da zenbaki osoa"


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
            [InlineKeyboardButton("pista", callback_data="Pista")],
            [InlineKeyboardButton("bidexka", callback_data="Bidexka")],
            [InlineKeyboardButton("bidexka-zaila", callback_data="BidexkaZaila")],
            [InlineKeyboardButton("bidez-kanpo", callback_data="BidezKanpo")],
        ]
    )


def aukerak(update, context):
    query = update.callback_query
    query.answer()
    theFunction = globals()[query.data]
    theFunction(update, context)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", startBot))
    dp.add_handler(CommandHandler("hasi", startBot))
    dp.add_handler(CallbackQueryHandler(aukerak))

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
