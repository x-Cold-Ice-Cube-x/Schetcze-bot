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
    __infoButton = InlineKeyboardButton(text=Text.infoButton[0], callback_data=Text.infoButton[1])
    __donationButton = InlineKeyboardButton(text=Text.donationButton[0], url=Text.donationButton[1])
    __responseButton = InlineKeyboardButton(text=Text.responseButton[0], callback_data=Text.responseButton[1])
    __cancellationButton = InlineKeyboardButton(text=Text.cancellationButton[0],
                                                callback_data=Text.cancellationButton[1])
    __subscribeButton = InlineKeyboardButton(text=Text.subscribeButton[0], url=Text.subscribeButton[1])
    __youtubeButton = InlineKeyboardButton(text=Text.youtubeButton[0], url=Text.youtubeButton[1])
    __paymentButtons = [InlineKeyboardButton(text=Text.paymentButtons[0][0], callback_data=Text.paymentButtons[0][1]),
                        InlineKeyboardButton(text=Text.paymentButtons[1][0], callback_data=Text.paymentButtons[1][1]),
                        InlineKeyboardButton(text=Text.paymentButtons[2][0], callback_data=Text.paymentButtons[2][1]),
                        InlineKeyboardButton(text=Text.paymentButtons[3][0], callback_data=Text.paymentButtons[3][1])]
    # ------------------------------------------------ #

    # ---------- Поля класса Markup: разметки ---------- #
    __mainKeyboard = [[__infoButton], [__contributionButton, __donationButton], [__responseButton, __youtubeButton]]
    __cancellationKeyboard = [[__cancellationButton]]
    __subscribeKeyboard = [[__subscribeButton]]
    __contributionKeyboard = [[__paymentButtons[0], __paymentButtons[1]], [__paymentButtons[2], __paymentButtons[3]],
                              [__cancellationButton]]
    # -------------------------------------------------- #

    # ---------- Поля класса Markup: клавиатуры ---------- #
    mainMarkup = InlineKeyboardMarkup(inline_keyboard=__mainKeyboard)
    cancellationMarkup = InlineKeyboardMarkup(inline_keyboard=__cancellationKeyboard)
    subscribeMarkup = InlineKeyboardMarkup(inline_keyboard=__subscribeKeyboard)
    contributionMarkup = InlineKeyboardMarkup(inline_keyboard=__contributionKeyboard)
    # ----------------------------------------------------- #
