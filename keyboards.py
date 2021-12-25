from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
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

def bideaMenu():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Pista", callback_data="pista"),
            InlineKeyboardButton("Bidexka", callback_data="bidexka")],
            [InlineKeyboardButton("Bidexka zaila", callback_data="bidexka-zaila"),
            InlineKeyboardButton("Bidez-kanpo", callback_data="bidez-kanpo")],
        ]
    )
