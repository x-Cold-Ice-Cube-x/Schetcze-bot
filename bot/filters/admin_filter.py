# ---------- Импорты дополнительных библиотек --------- #
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from configs.text import Text
# ---------------------------------------- #


class AdminFilter(BaseFilter):
    # ---------- Переопределенный метод BaseFilter ---------- #
    async def __call__(self, response: CallbackQuery | Message):
        """
        Переопределенный метод класса BaseFilter: предобработка события, полученного ботом
        :param response: aiogram.types.CallbackQuery | aiogram.types.Message
        :return: bool (True - админ, False - неадмин)
        """

        # Получение объекта aiogram.types.Message ↓
        if isinstance(response, CallbackQuery):
            message = response.message
        else:
            message = response

        # Проверка является ли пользователь админом ↓
        return message.chat.id in Text.admins_id
    # ------------------------------------------------------- #
