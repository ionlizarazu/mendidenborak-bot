import logging
import os

from mendidenborak import MendiDenborak
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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


def startBot(update, context, update_message=False, language=False):
    dp.remove_handler(lonHandler)
    dp.remove_handler(posHandler)
    dp.remove_handler(negHandler)
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


def startingMenu():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Hasi ibilbidearekin", callback_data="aukeratuBidea"
                )
            ],
        ]
    )


def aukeratuBidea(
    update,
    context,
):
    ibilbidea = Ibilbidea()
    context.bot_data["ibilbidea"] = ibilbidea
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    update.callback_query.edit_message_text(text="Updating text")
    context.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Denbora kalkulatzeko, aurrena aukeratu bide mota nagusia:",
        reply_markup=bideaMenu(),
    )


def bideaMenu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Pista", callback_data="pista")],
            [InlineKeyboardButton("Bidexka", callback_data="bidexka")],
            [InlineKeyboardButton("Bidexka zaila", callback_data="bidexka-zaila")],
            [InlineKeyboardButton("Bidez-kanpo", callback_data="bidez-kanpo")],
        ]
    )


def aukeratuLuzeera(update, context):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    context.bot_data.get("ibilbidea").set_bidea(update.callback_query.data)
    ibilbidea = context.bot_data["ibilbidea"]
    dp.remove_handler(posHandler)
    dp.remove_handler(negHandler)
    dp.add_handler(lonHandler)

    context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Definitutako ibilbidea:\n- Bide mota: {ibilbidea.bidea}\n- Luzeera (m): {ibilbidea.luzeera}\n- Denibel positiboa: {ibilbidea.positiboa}\n- Desnibel negatiboa: {ibilbidea.negatiboa}\n\nIdatzi bidearen LUZEERA METROTAN:",
        # reply_markup=ibilbideaMenu(),
    )


def aukeratuPositiboa(update, context):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    context.bot_data.get("ibilbidea").set_luzeera(update.message.text)
    ibilbidea = context.bot_data["ibilbidea"]
    dp.remove_handler(lonHandler)
    dp.remove_handler(negHandler)
    dp.add_handler(posHandler)

    context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Definitutako ibilbidea:\n- Bide mota: {ibilbidea.bidea}\n- Luzeera (m): {ibilbidea.luzeera}\n- Denibel positiboa: {ibilbidea.positiboa}\n- Desnibel negatiboa: {ibilbidea.negatiboa}\n\nIdatzi bidearen DESNIBEL POSITIBOA metrotan:",
        # reply_markup=ibilbideaMenu(),
    )


def aukeratuNegatiboa(update, context):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    context.bot_data.get("ibilbidea").set_positiboa(update.message.text)
    ibilbidea = context.bot_data["ibilbidea"]
    dp.remove_handler(lonHandler)
    dp.remove_handler(posHandler)
    dp.add_handler(negHandler)

    context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Definitutako ibilbidea:\n- Bide mota: {ibilbidea.bidea}\n- Luzeera (m): {ibilbidea.luzeera}\n- Denibel positiboa: {ibilbidea.positiboa}\n- Desnibel negatiboa: {ibilbidea.negatiboa}\n\nIdatzi bidearen DESNIBEL NEGATIBOA metrotan:",
        # reply_markup=ibilbideaMenu(),
    )


def kalkulatuDenbora(update, context):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    context.bot_data.get("ibilbidea").set_negatiboa(update.message.text)
    ibilbidea = context.bot_data["ibilbidea"]
    dp.remove_handler(lonHandler)
    dp.remove_handler(posHandler)
    dp.add_handler(negHandler)
    md = MendiDenborak()
    denbora_raw = md.kalkulatuDenbora(
        ibilbidea.bidea, ibilbidea.luzeera, ibilbidea.positiboa, ibilbidea.negatiboa
    )
    ordu = int(denbora_raw)
    minutu = int((denbora_raw * 60) % 60)

    context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Definitutako ibilbidea:\n- Bide mota: {ibilbidea.bidea}\n- Luzeera (m): {ibilbidea.luzeera}\n- Denibel positiboa: {ibilbidea.positiboa}\n- Desnibel negatiboa: {ibilbidea.negatiboa}",
        # reply_markup=ibilbideaMenu(),
    )

    context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Ibilbide hau egiteko kalkulatutako denbora:\n\n{ordu} ordu eta {minutu} minutu.",
        reply_markup=startingMenu(),
    )


def aukerak(update, context):
    query = update.callback_query
    query.answer()

    theFunction = globals()[query.data]
    theFunction(update, context)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


lonHandler = MessageHandler(Filters.text & ~Filters.command, aukeratuPositiboa)
posHandler = MessageHandler(Filters.text & ~Filters.command, aukeratuNegatiboa)
negHandler = MessageHandler(Filters.text & ~Filters.command, kalkulatuDenbora)


def main():
    """Start the bot."""

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", startBot))
    dp.add_handler(CommandHandler("hasi", startBot))
    dp.add_handler(CallbackQueryHandler(aukeratuBidea, pattern="aukeratuBidea"))
    dp.add_handler(
        CallbackQueryHandler(
            aukeratuLuzeera, pattern="(pista|bidexka|bidexka-zaila|bidez-kanpo)"
        )
    )
    dp.add_handler(CallbackQueryHandler(aukerak))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook("https://mendidenborak-bot.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
