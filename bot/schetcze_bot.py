# --------- Импорты встроенных библиотек --------- #
from logging import getLogger, INFO, basicConfig
# ------------------------------------------------ #


# ---------- Импорты дополнительных библиотек --------- #
from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramUnauthorizedError

# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from tables.authorization import Authorization
from tables.users import Users
from configs.text import Text
# ---------------------------------------- #


class SchetczeBot:
    # ---------- Поля класса SchetczeBot ---------- #
    __auth = Authorization()  # тип: Authorization (обеспечить единственность объекта)
    __users = Users()  # тип: Users (обеспечить единственность объекта)
    __bot = None  # тип: aiogram.Bot (обеспечить единственность объекта)
    __dispatcher = Dispatcher()  # тип: aiogram.Dispatcher (обеспечить единственность объекта)
    __logger = getLogger("botLogger")  # тип: logging.Logger (обеспечить единственность объекта)
    # --------------------------------------------- #

    def __init__(self):
        self.__doAuthorization()

    # ---------- Метод-запуск бота SchetczeBot ---------- #
    async def startPolling(self):
        await self.__tokenVerification()  # асинхронная проверка актуальности Telegram-токена
        await self.__dispatcher.start_polling(self.__bot)  # запуск бесконечного ожидания
    # --------------------------------------------------- #

    # ---------- Методы класса SchetczeBot ---------- #
    @classmethod
    def __doAuthorization(cls):
        """
        Метод-авторизация бота в Telegram; заполнение поля __bot
        :return: NoneType
        """
        cls.__bot = Bot(token=cls.__auth.getTelegramToken())  # запись объекта aiogram.Bot в поля класса

    @classmethod
    async def __tokenVerification(cls) -> bool:
        """
        Метод, проверяющий актуальность Telegram-токена, хранящегося в таблице Users
        :return: bool
        """
        # Если Telegram-токен верен, то блок выполнится без ошибки (возможно есть более простой путь) ↓
        try:
            await cls.__bot.get_me()
            return True

        except TelegramUnauthorizedError:
            return False

    @classmethod
    def __setBasicConfig(cls) -> None:
        """
        Метод, устанавливающий базовую конфигурацию логирования
        :return: NoneType
        """
        # Установление конфигурации логирования ↓
        basicConfig(level=INFO, format='%(asctime)s [%(levelname)s] - %(filename)s - %(message)s',
                    filename=Text.logsFilepath, filemode='a')
    # ---------------------------------------------- #


