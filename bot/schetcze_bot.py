# --------- Импорты встроенных библиотек --------- #
from os import remove
from logging import getLogger, INFO, basicConfig
# ------------------------------------------------ #


# ---------- Импорты дополнительных библиотек --------- #
from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from tables.authorization_table import AuthorizationTable
from tables.users_table import UsersTable
from configs.text import Text
from bot.markup.markup import Markup
from bot.filters.registration_filter import RegistrationFilter
from bot.filters.subscription_filter import SubscriptionFilter
# ---------------------------------------- #


class SchetczeBot:
    # ---------- Поля класса SchetczeBot ---------- #
    __auth = None  # тип: AuthorizationTable (обеспечить единственность объекта)
    __users = None  # тип: UsersTable (обеспечить единственность объекта)
    __bot = None  # тип: aiogram.Bot (обеспечить единственность объекта)
    __dispatcher = Dispatcher()  # тип: aiogram.Dispatcher (обеспечить единственность объекта)
    __logger = getLogger("botLogger")  # тип: logging.Logger (обеспечить единственность объекта)
    # --------------------------------------------- #

    # ---------- Конструктор класса SchetczeBot ---------- #
    def __init__(self):
        self.__setBasicConfig()  # установка базовой конфигурации логирования
        self.__doAuthorization()  # авторизация в телеграм; инициализация полей класса

        # Подключение хэндлера /start ↓
        self.__dispatcher.message.register(self.__startCommandHandler, CommandStart())
        self.__logger.info(Text.startCommandHandlerConnectedLog)

        # Подключение хэндлера /database ↓
        self.__dispatcher.message.register(self.__databaseCommandHandler, Command(Text.databaseCommand),
                                           RegistrationFilter(users=self.__users),
                                           SubscriptionFilter(bot=self.__bot, chatID=Text.channel_id))
        self.__logger.info(Text.databaseCommandHandlerConnectedLog)
    # ---------------------------------------------------- #

    # ---------- Метод-запуск бота SchetczeBot ---------- #
    async def startPolling(self):
        await self.__tokenVerification()  # асинхронная проверка актуальности Telegram-токена
        await self.__dispatcher.start_polling(self.__bot)  # запуск бесконечного ожидания
        # Логирование ↓
        self.__logger.info(Text.pollingStartedLog)
    # --------------------------------------------------- #

    # ---------- Методы класса SchetczeBot ---------- #
    @classmethod
    def __doAuthorization(cls):
        """
        Метод-авторизация бота в Telegram; заполнение полей __bot, __auth, __users
        :return: NoneType
        """
        cls.__auth = AuthorizationTable()  # запись объекта Authorization в поля класса
        cls.__users = UsersTable()  # Запись объекта Authorization в поля класса
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
            # Логирование ↓
            cls.__logger.info(Text.tokenVerificationPassedLog)

        except TelegramUnauthorizedError:
            # Логирование ↓
            cls.__logger.error(Text.tokenVerificationErrorLog)
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
        # Логирование ↓
        cls.__logger.info(Text.loggerConnectedLog)
    # ---------------------------------------------- #

    # ---------- Хэндлеры бота SchetczeBot ---------- #
    async def __startCommandHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка команды /start
        :param message: aiogram.types.Message
        :return: NoneType
        """

        # Проверка существования пользователя в базе данных ↓
        if message.chat.id not in self.__users.getDataFromColumn(columnName=self.__users.TELEGRAM_ID):
            # Запись в таблицу Users ↓
            self.__users.fillingTheTable(telegramID=message.chat.id, telegramUsername=message.chat.username)

        # Ответ ↓
        await self.__bot.send_message(chat_id=message.chat.id, text=Text.startMessage.format(message.chat.first_name),
                                      parse_mode="HTML", reply_markup=Markup.mainMarkup)

    async def __databaseCommandHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка команды /getDatabase
        :param message: aiogram.types.Message
        :return: NoneType
        """
        # ДОБАВИТЬ ОБРАБОТЧИК АЙДИ!!!!
        self.__users.exportToExcel(Text.exportFilepath)  # экспорт таблицы Users

        # Ответ ↓
        await self.__bot.send_document(chat_id=message.chat.id, document=FSInputFile(Text.exportFilepath))
        remove(Text.exportFilepath)  # удаление файла

    # ------------------------------------------------- #
