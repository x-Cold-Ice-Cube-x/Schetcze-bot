# --------- Импорты встроенных библиотек --------- #
from os import remove
from logging import getLogger, INFO, basicConfig
# ------------------------------------------------ #


# ---------- Импорты дополнительных библиотек --------- #
from aiogram import Dispatcher, Bot, F
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.types import Message, FSInputFile, CallbackQuery, LabeledPrice
from aiogram.types.pre_checkout_query import PreCheckoutQuery
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
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.startCommand))

        # Подключение хэндлера /database ↓
        self.__dispatcher.message.register(self.__databaseCommandHandler, Command(Text.databaseCommand),
                                           RegistrationFilter(users=self.__users),
                                           SubscriptionFilter(bot=self.__bot, chatID=Text.channel_id))
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.databaseCommand))

        # Подключение хэндлера /logs ↓
        self.__dispatcher.message.register(self.__logsCommandHandler, Command(Text.logsCommand),
                                           RegistrationFilter(users=self.__users),
                                           SubscriptionFilter(bot=self.__bot, chatID=Text.channel_id))
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.logsCommand))

        # Подключение хэндлера кнопки contribution ↓
        self.__dispatcher.callback_query.register(self.__contributionCallbackHandler,
                                                  F.data == Text.contributionButton[1],
                                                  RegistrationFilter(users=self.__users),
                                                  SubscriptionFilter(bot=self.__bot, chatID=Text.channel_id))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.contributionButton[1]))

        # Подключение хэндлера кнопок типа payment ↓
        self.__dispatcher.callback_query.register(self.__contributionPaymentHandler,
                                                  F.data.startswith(Text.paymentButtonType),
                                                  RegistrationFilter(users=self.__users),
                                                  SubscriptionFilter(bot=self.__bot, chatID=Text.channel_id))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.paymentButtonType))

        # Подключение хэндлера готовности contributionPayment платежа ↓
        self.__dispatcher.pre_checkout_query.register(self.__contributionPreCheckoutHandler,
                                                      F.invoice_payload == Text.contributionInvoiceButton["payload"])
        self.__logger.info(Text.checkoutHandlerConnectedLog.format(Text.contributionInvoiceButton["payload"]))

        # Подключение хэндлера успешной оплаты товара contributionPayment ↓
        self.__dispatcher.message.register(self.__contributionSuccessfulPaymentHandler,
                                           F.successful_payment.invoice_payload ==
                                           Text.contributionInvoiceButton["payload"])
        self.__logger.info(Text.successfulPaymentHandlerConnectedLog.format(Text.contributionInvoiceButton["payload"]))

        # Подключение хэндлера: обработка неизвестных сообщений ↓
        self.__dispatcher.message.register(self.__unknownMessageHandler,
                                           RegistrationFilter(users=self.__users),
                                           SubscriptionFilter(bot=self.__bot, chatID=Text.channel_id))
        self.__logger.info(Text.unknownMessageHandlerConnectedLog)
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

    # ---------- Хэндлеры бота SchetczeBot: Commands ---------- #
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
        Метод-хэндлер: обработка команды /database
        :param message: aiogram.types.Message
        :return: NoneType
        """

        # Проверка является ли пользователь админом ↓
        if self.__isAdmin(message.chat.id):
            self.__users.exportToExcel(Text.exportFilepath)  # экспорт таблицы Users

            # Ответ ↓
            await self.__bot.send_document(chat_id=message.chat.id, document=FSInputFile(Text.exportFilepath))
            remove(Text.exportFilepath)  # удаление файла
            return

        # Исключение: пользователь неадмин ↓
        await self.__unknownMessageHandler(message=message)

    async def __logsCommandHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка команды /logs
        :param message: aiogram.types.Message
        :return: NoneType
        """

        if self.__isAdmin(chatID=message.chat.id):
            # Ответ ↓
            await self.__bot.send_document(chat_id=message.chat.id, document=FSInputFile(Text.logsFilepath))
            return

        # Исключение: пользователь неадмин ↓
        await self.__unknownMessageHandler(message=message)

    # --------------------------------------------------------- #

    # ---------- Хэндлеры бота SchetczeBot: CallbackQuery --------- #
    async def __contributionCallbackHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопки contribution
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """
        # Ответ ↓
        await self.__bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                           text=Text.contributionMessage.format(call.message.chat.first_name),
                                           parse_mode="HTML", reply_markup=Markup.contributionMarkup)

    async def __contributionPaymentHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопок типа payment
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        contribution = int(call.data[8:]) * 100  # получение размера взноса из callback.data

        # Удаление прошлого сообщения; отправка запроса на оплату ↓
        await self.__bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await self.__bot.send_invoice(chat_id=call.message.chat.id, title=Text.contributionInvoiceButton["title"],
                                      description=Text.contributionInvoiceButton["description"],
                                      payload=Text.contributionInvoiceButton["payload"],
                                      provider_token=self.__auth.getPaymentToken(),
                                      currency=Text.contributionInvoiceButton["currency"], need_email=True,
                                      need_phone_number=True,
                                      prices=[LabeledPrice(label=Text.contributionInvoiceButton["label"],
                                                           amount=contribution)])
    # ------------------------------------------------------------- #

    # ---------- Хэндлеры бота SchetczeBot: PreCheckoutQuery ---------- #
    async def __contributionPreCheckoutHandler(self, checkout: PreCheckoutQuery) -> None:
        """
        Метод-хэндлер: обработка товара contributionPayment
        :param checkout: aiogram.types.pre_checkout_query.PreCheckoutQuery
        :return: NoneType
        """

        # Приходит, как только была нажата кнопка оплаты
        # Ответ ↓
        await self.__bot.answer_pre_checkout_query(checkout.id, ok=True)
    # ----------------------------------------------------------------- #

    # --------- Хэндлеры бота SchetczeBot: SuccessfulPayment ---------- #
    async def __contributionSuccessfulPaymentHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка успешной оплаты contributionPayment
        :param message: aiogram.types.Message
        :return: NoneType
        """
        print("ИВЕНТ!")
        # Получение значения ячейки Contribution пользователя ↓
        filed = int(self.__users.getDataFromField(lineData=message.chat.id, columnName=self.__users.CONTRIBUTION))

        # Заполнение|Обновление ячеек Email, Phone_number, Contribution пользователя ↓
        self.__users.updateField(lineData=message.chat.id, columnName=self.__users.EMAIL,
                                 field=message.successful_payment.order_info.email)
        self.__users.updateField(lineData=message.chat.id, columnName=self.__users.PHONE_NUMBER,
                                 field=message.successful_payment.order_info.phone_number)
        self.__users.updateField(lineData=message.chat.id, columnName=self.__users.CONTRIBUTION,
                                 field=filed + int(message.successful_payment.total_amount))

        # Генерация и отправка благодарственного сообщения ↓
        replyMessage = Text.thankForBuyingMessage.format(message.chat.first_name)
        await self.__bot.send_message(chat_id=message.chat.id, text=replyMessage, parse_mode="HTML")

        # Отправка главного меню ↓
        await self.__bot.send_message(chat_id=message.chat.id, text=Text.startMessage.format(message.chat.first_name),
                                      parse_mode="HTML", reply_markup=Markup.mainMarkup)
    # ----------------------------------------------------------------- #

    async def __unknownMessageHandler(self, message: Message) -> None:
        # Ответ ↓
        await self.__bot.send_message(chat_id=message.chat.id,
                                      text=Text.unknownMessage.format(message.chat.first_name, message.text),
                                      parse_mode="HTML")

    # ---------- Дополнительные методы хэндлеров ---------- #
    def __isAdmin(self, chatID: int) -> bool:
        """
        Метод, определяющий является ли пользователь админом
        :param chatID: Telegram ID пользователя
        :return: bool (True - админ, False - неадмин)
        """

        # Проверка является ли пользователь админом ↓
        return chatID in Text.admins_id
    # ----------------------------------------------------- #



