# ---------- Импорты дополнительных библиотек --------- #
from aiogram import Bot
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from aiogram.enums.chat_member_status import ChatMemberStatus
# ----------------------------------------------------- #


class SubscriptionFilter(BaseFilter):
    # ---------- Конструктор класса SubscriptionFilter ---------- #
    def __init__(self, bot: Bot, chatID: int):
        """
        Конструктор класса SubscriptionFilter: предобработка события, полученного ботом
        :param bot: aiogram.Bot (обеспечить единственность объекта)
        :param chatID: int (Telegram ID группы|канала)
        """

        # Добавление необходимых полей экземпляру для корректной работы фильтра ↓
        self.__bot = bot
        self.__chatID = chatID
    # ----------------------------------------------------------- #

    # ---------- Переопределенный метод BaseFilter ---------- #
    async def __call__(self, response: CallbackQuery | Message) -> bool:
        """
        Переопределенный метод класса BaseFilter: предобработка события, полученного ботом
        :param response: aiogram.types.CallbackQuery | aiogram.types.Message
        :return: bool (True - подписан | False - не подписан)
        """

        # Получение объекта aiogram.types.Message ↓
        if isinstance(response, CallbackQuery):
            message = response.message
        else:
            message = response

        # Получение объекта ChatMember* ↓
        member = await self.__bot.get_chat_member(chat_id=self.__chatID, user_id=message.chat.id)

        # Проверка принадлежности пользователя необходимому каналу|группе ↓
        return member.status in [ChatMemberStatus.CREATOR, ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR]
    # ------------------------------------------------------- #
