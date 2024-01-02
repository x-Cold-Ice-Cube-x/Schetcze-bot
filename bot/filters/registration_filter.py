# ---------- Импорты дополнительных библиотек --------- #
from aiogram.filters import BaseFilter
from aiogram.types import Message
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from tables.users_table import UsersTable
# ---------------------------------------- #


class RegistrationFilter(BaseFilter):

    def __init__(self, users: UsersTable):
        """
        Конструктор класса RegistrationFilter: предобработка события, полученного ботом
        :param users: UsersTable (обеспечить единственность объекта)
        """

        self.__users = users

    async def __call__(self, message: Message) -> bool:
        pass
