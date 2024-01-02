# ---------- Импорты дополнительных библиотек --------- #
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from configs.text import Text
# ---------------------------------------- #


class Markup:
    # ---------- Поля класса Markup: кнопки ---------- #
    __contributionButton = InlineKeyboardButton(text=Text.contributionButton[0],
                                                callback_data=Text.contributionButton[1])
    __donationButton = InlineKeyboardButton(text=Text.donationButton[0], url=Text.donationButton[1])
    __responseButton = InlineKeyboardButton(text=Text.responseButton[0], callback_data=Text.responseButton[1])
    __cancellationButton = InlineKeyboardButton(text=Text.cancellationButton[0],
                                                callback_data=Text.contributionButton[1])
    __subscribeButton = InlineKeyboardButton(text=Text.subscribeButton[0], url=Text.subscribeButton[1])
    __paymentButtons = [InlineKeyboardButton(text=Text.paymentButtons[0][0], callback_data=Text.paymentButtons[0][1]),
                        InlineKeyboardButton(text=Text.paymentButtons[1][0], callback_data=Text.paymentButtons[1][1]),
                        InlineKeyboardButton(text=Text.paymentButtons[2][0], callback_data=Text.paymentButtons[2][1]),
                        InlineKeyboardButton(text=Text.paymentButtons[3][0], callback_data=Text.paymentButtons[3][1])]
    # ------------------------------------------------ #

    # ---------- Поля класса Markup: разметки ---------- #
    __mainKeyboard = [[__contributionButton, __donationButton], [__responseButton]]
    __responseKeyboard = [[__cancellationButton]]
    __subscribeKeyboard = [[__subscribeButton]]
    __contributionKeyboard = [[__paymentButtons[0], __paymentButtons[1]], [__paymentButtons[2], __paymentButtons[3]],
                              [__contributionButton]]
    # -------------------------------------------------- #

    # ---------- Поля класса Markup: клавиатуры ---------- #
    mainMarkup = InlineKeyboardMarkup(inline_keyboard=__mainKeyboard)
    responseMarkup = InlineKeyboardMarkup(inline_keyboard=__responseKeyboard)
    subscribeMarkup = InlineKeyboardMarkup(inline_keyboard=__subscribeKeyboard)
    contributionMarkup = InlineKeyboardMarkup(inline_keyboard=__contributionKeyboard)
    # ----------------------------------------------------- #
