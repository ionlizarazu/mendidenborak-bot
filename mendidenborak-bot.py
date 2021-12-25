import logging
import os
import re

from mendidenborak import MendiDenborak
from telegram.ext import (CallbackQueryHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

from ibilbidea import Ibilbidea
from keyboards import bideaMenu, startingMenu

TOKEN = os.getenv("TOKEN")
logger = logging.getLogger(__name__)
PORT = int(os.environ.get("PORT", 5000))
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

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
        text=f"Kaixo {user.first_name}!\n\n"
            "Ni Mendidenborak naiz, zure mendiko ibilbideen denborak kalkulatzen lagunduko dizun bot-a.\n\n"
            "Lau pausutan kalkulatuko dugu ibilbidea egiteko denbora:\n"
            " - Ibilbideko bide mota nagusia zein izango den aukeratu\n"
            " - Ibilbidearen luzeera bidali (18km, 23.7km edo 12000m formatuan)\n"
            " - Ibilbideak guztira izango duen ↗️ desnibel positiboa bidali\n"
            " - Ibilbideak guztira izango duen ↘️ desnibel negatiboa bidali\n",
        reply_markup=startingMenu(),
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

    update.callback_query.edit_message_text(text="Ez joan, oraintxe nator...")
    context.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Denbora kalkulatzeko, aurrena aukeratu bide mota nagusia:",
        reply_markup=bideaMenu(),
    )


def aukeratuLuzeera(update, context, resending=False):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message
    dp.remove_handler(posHandler)
    dp.remove_handler(negHandler)
    dp.add_handler(lonHandler)
    
    if not resending:
        context.bot_data.get("ibilbidea").set_bidea(update.callback_query.data)
        context.bot.send_message(
            chat_id=message.chat.id,
            text=f"Idatzi bidearen LUZEERA (18km, 23.7km edo 12000m formatuan):",
            # text=f"{formatIbilbidea(context.bot_data['ibilbidea'])}\n\nIdatzi bidearen LUZEERA METROTAN:",
            # reply_markup=ibilbideaMenu(),
        )
    else:
        context.bot.send_message(
            chat_id=message.chat.id,
            text=f"❌ FORMATU OKERRA!!\nProbatu modu hauetako bat:\n18km\n29.8km\n12500m\n\nIdatzi bidearen LUZEERA:",
            # reply_markup=ibilbideaMenu(),
        )


def aukeratuPositiboa(update, context, resending=False):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message
    dp.remove_handler(lonHandler)
    dp.remove_handler(negHandler)
    dp.add_handler(posHandler)

    if not resending:
        luzeera = getDistanceFromText(update.message.text)
        if luzeera == -1:
            aukeratuLuzeera(update, context, True)
        else:
            context.bot_data.get("ibilbidea").set_luzeera(luzeera)
            context.bot.send_message(
                chat_id=message.chat.id,
                text=f"Idatzi bidearen ↗️ DESNIBELA metrotan:",
            )
    else:
        context.bot.send_message(
                chat_id=message.chat.id,
                text=f"❌ FORMATU OKERRA!!\nIdatzi bidearen ↗️ DESNIBELA metrotan, zenbaki hutsez:",
            )

def aukeratuNegatiboa(update, context, resending=False):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message
    dp.remove_handler(lonHandler)
    dp.remove_handler(posHandler)
    dp.add_handler(negHandler)
    
    if not resending:
        result = context.bot_data.get("ibilbidea").set_positiboa(update.message.text)
        if result == -1:
            aukeratuPositiboa(update, context, True)
        else:
            context.bot.send_message(
                chat_id=message.chat.id,
                text=f"Idatzi bidearen ↘️ DESNIBELA metrotan:",
            )
    else:
        context.bot.send_message(
            chat_id=message.chat.id,
            text=f"❌ FORMATU OKERRA!!\nIdatzi bidearen ↘️ DESNIBELA metrotan zenbaki hutsez:",
        )

def kalkulatuDenbora(update, context):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message
    dp.remove_handler(lonHandler)
    dp.remove_handler(posHandler)
    dp.remove_handler(negHandler)

    result = context.bot_data.get("ibilbidea").set_negatiboa(update.message.text)
    if result == -1:
        aukeratuNegatiboa(update, context, True)
    else:
        ibilbidea = context.bot_data["ibilbidea"]
        md = MendiDenborak()
        denbora_raw = md.kalkulatuDenbora(
            ibilbidea.bidea, ibilbidea.luzeera, ibilbidea.positiboa, ibilbidea.negatiboa
        )
        ordu = int(denbora_raw)
        minutu = int((denbora_raw * 60) % 60)

        context.bot.send_message(
            chat_id=message.chat.id,
            text=f"⛰⛰ BIDAI ON!! ⛰⛰\n\n{formatIbilbidea(ibilbidea)}\n\nHau egiteko:\n{ordu} ordu {minutu} minutu",
            reply_markup=startingMenu(),
        )

def sendIbilbidea(update, context):
    if update.message:
        message = update.message
    else:
        message = update.callback_query.message

    ibilbidea = context.bot_data.get("ibilbidea")
    ibilbidea_text = ''
    if ibilbidea:
        ibilbidea_text = formatIbilbidea(ibilbidea)
    else:
        ibilbidea_text = "Ez dago ibilbiderik"
    context.bot.send_message(
        chat_id=message.chat.id,
        text=f"Hau da orain arte daukaguna:\n\n{ibilbidea_text}",
    )
    last_message = ""
    for handler in dp.handlers[0]:
        if handler.__class__.__name__ == 'MessageHandler':
            if handler.callback.__name__ == 'aukeratuPositiboa':
                last_message = f"Idatzi bidearen LUZEERA (18km, 23.7km edo 12000m formatuan):"
            elif handler.callback.__name__ == 'aukeratuNegatiboa':
                last_message = f"Idatzi bidearen ↗️ DESNIBELA metrotan:"
            elif handler.callback.__name__ == 'kalkulatuDenbora':
                last_message = f"Idatzi bidearen ↘️ DESNIBELA metrotan:"
    if last_message:
        context.bot.send_message(
            chat_id=message.chat.id,
            text=last_message,
        )
    
    
def formatIbilbidea(ibilbidea):
    result_text = (f"🏞 Bide mota: {ibilbidea.bidea}\n"
    f"📏 Luzeera: {ibilbidea.luzeera/1000}km\n"
    f"↗️ Desnibela: {ibilbidea.positiboa}m\n"
    f"↘️ Desnibela: {ibilbidea.negatiboa}m")
    return result_text

def getDistanceFromText(message):
    number_metric = r"([0-9]*\.?[0-9]*)(m|km|KM|M)"
    if re.match(number_metric, message):
        groups = re.search(number_metric, message).groups()
        if groups[1] == "m" or groups[1] == "M":
            luzeera = float(groups[0])
        elif groups[1] == "km" or groups[1] == "KM":
            luzeera = float(groups[0]) * 1000
        else:
            luzeera = -1
    else:
        return -1
    return luzeera
    

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
    dp.add_handler(CommandHandler("ibilbidea", sendIbilbidea))
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
