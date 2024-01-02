# --------- Импорты встроенных библиотек --------- #
from logging import getLogger, INFO, basicConfig
# ------------------------------------------------ #


# ---------- Импорты дополнительных библиотек --------- #
from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.types import Message
from aiogram.filters import CommandStart
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from tables.authorization import Authorization
from tables.users import Users
from configs.text import Text
# ---------------------------------------- #


class SchetczeBot:
    # ---------- Поля класса SchetczeBot ---------- #
    __auth = None  # тип: Authorization (обеспечить единственность объекта)
    __users = None  # тип: Users (обеспечить единственность объекта)
    __bot = None  # тип: aiogram.Bot (обеспечить единственность объекта)
    __dispatcher = Dispatcher()  # тип: aiogram.Dispatcher (обеспечить единственность объекта)
    __logger = getLogger("botLogger")  # тип: logging.Logger (обеспечить единственность объекта)
    # --------------------------------------------- #

    def __init__(self):
        self.__setBasicConfig()
        self.__doAuthorization()

        self.__dispatcher.message.register(self.startCommandHandler)

    # ---------- Метод-запуск бота SchetczeBot ---------- #
    async def startPolling(self):
        await self.__tokenVerification()  # асинхронная проверка актуальности Telegram-токена
        await self.__dispatcher.start_polling(self.__bot)  # запуск бесконечного ожидания
        self.__logger.info(Text.pollingStarted)
    # --------------------------------------------------- #

    # ---------- Методы класса SchetczeBot ---------- #
    @classmethod
    def __doAuthorization(cls):
        """
        Метод-авторизация бота в Telegram; заполнение поля __bot
        :return: NoneType
        """
        cls.__auth = Authorization()  # запись объекта Authorization в поля класса
        cls.__users = Users()  # Запись объекта Authorization в поля класса
        cls.__bot = Bot(token=cls.__auth.getTelegramToken())  # запись объекта aiogram.Bot в поля класса

    @classmethod
    async def __tokenVerification(cls) -> None:
        """
        Метод, проверяющий актуальность Telegram-токена, хранящегося в таблице Users
        :return: NoneType
        """
        # Если Telegram-токен верен, то блок выполнится без ошибки (возможно есть более простой путь) ↓
        # P.S - теперь при неактуальном Telegram-токене, программа завершает свое действие
        try:
            await cls.__bot.get_me()
            cls.__logger.info(Text.tokenVerificationPassed)

        except TelegramUnauthorizedError:
            cls.__logger.error(Text.tokenVerificationError)
            exit()

    @classmethod
    def __setBasicConfig(cls) -> None:
        """
        Метод, устанавливающий базовую конфигурацию логирования
        :return: NoneType
        """
        # Установление конфигурации логирования ↓
        basicConfig(level=INFO, format='%(asctime)s [%(levelname)s] - %(filename)s - %(message)s',
                    filename=Text.logsFilepath, filemode='a')
        cls.__logger.info(Text.loggerConnected)
    # ---------------------------------------------- #

    # ---------- Хэндлеры бота SchetczeBot ---------- #
    async def startCommandHandler(self, message: Message):
        await self.__bot.send_message(chat_id=message.chat.id, text="Оно работает бля!")
    # ------------------------------------------------- #


