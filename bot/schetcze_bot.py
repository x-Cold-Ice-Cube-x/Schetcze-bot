# --------- Импорты встроенных библиотек --------- #
from os import remove
from json import loads, dumps
from logging import getLogger, INFO, basicConfig
# ------------------------------------------------ #


# ---------- Импорты дополнительных библиотек --------- #
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, FSInputFile, CallbackQuery, LabeledPrice
from aiogram.types.pre_checkout_query import PreCheckoutQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from tables.authorization_table import AuthorizationTable
from tables.users_table import UsersTable
from configs.text import Text
from bot.markup.markup import Markup
from bot.filters.registration_filter import RegistrationFilter
from bot.filters.subscription_filter import SubscriptionFilter
from bot.filters.admin_filter import AdminFilter
from bot.states.states import States


# ---------------------------------------- #


class SchetczeBot(Bot):
    # ---------- Поля класса SchetczeBot ---------- #
    __auth = None  # тип: AuthorizationTable (обеспечить единственность объекта)
    __users = None  # тип: UsersTable (обеспечить единственность объекта)
    __dispatcher = None  # тип: aiogram.Dispatcher (обеспечить единственность объекта)
    __logger = getLogger("botLogger")  # тип: logging.Logger (обеспечить единственность объекта)

    # --------------------------------------------- #

    # ---------- Конструктор класса SchetczeBot ---------- #
    def __init__(self):
        self.__setBasicConfig()  # создание объекта Logger (заранее, потому что дальше идет инициализация объектов)
        self.__setAttributes()  # заполнение всех полей класса
        super().__init__(token=self.__auth.getTelegramToken())  # авторизация бота в Telegram

        # Подключение хэндлера кнопки contribution
        self.__dispatcher.callback_query.register(self.__contributionCallbackHandler,
                                                  F.data == Text.contributionButton[1],
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                                  RegistrationFilter(users=self.__users))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.contributionButton[1]))

        # Подключение хэндлера кнопки response
        self.__dispatcher.callback_query.register(self.__responseCallbackHandler,
                                                  F.data == Text.responseButton[1],
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                                  RegistrationFilter(users=self.__users))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.responseButton[1]))

        # Подключение хэндлера кнопки info
        self.__dispatcher.callback_query.register(self.__infoCallbackHandler,
                                                  F.data == Text.infoButton[1],
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                                  RegistrationFilter(users=self.__users))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.infoButton[1]))

        # Подключение хэндлера кнопки cancellation
        self.__dispatcher.callback_query.register(self.__cancellationCallbackHandler,
                                                  F.data == Text.cancellationButton[1],
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                                  RegistrationFilter(users=self.__users))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.cancellationButton[1]))

        # Подключение хэндлера кнопок paymentType
        self.__dispatcher.callback_query.register(self.__contributionPaymentHandler,
                                                  F.data.startswith(Text.paymentButtonType),
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                                  RegistrationFilter(users=self.__users))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.paymentButtonType + " type"))

        # Подключение хэндлера готовности contribution платежа ↓
        self.__dispatcher.pre_checkout_query.register(self.__contributionPreCheckoutHandler,
                                                      F.invoice_payload == Text.contributionInvoiceButton["payload"])
        self.__logger.info(Text.checkoutHandlerConnectedLog.format(Text.contributionInvoiceButton["payload"]))

        # Подключение хэндлера успешной оплаты товара contribution ↓
        self.__dispatcher.message.register(self.__contributionSuccessfulPaymentHandler,
                                           F.successful_payment.invoice_payload ==
                                           Text.contributionInvoiceButton["payload"])
        self.__logger.info(Text.successfulPaymentHandlerConnectedLog.format(Text.contributionInvoiceButton["payload"]))

        # Подключение хэндлера получения и записи отзыва
        self.__dispatcher.message.register(self.__responseMessageHandler,
                                           States.responseState,
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                           RegistrationFilter(users=self.__users))
        self.__dispatcher.message.register(self.__responseMessageHandler,
                                           States.responseState, CommandStart(),
                                           Command(Text.logsCommand), Command(Text.databaseCommand),
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                           RegistrationFilter(users=self.__users))
        self.__logger.info(Text.responseMessageHandlerConnectedLog)

        # Подключение хэндлера команды /start ↓
        self.__dispatcher.message.register(self.__startCommandHandler, CommandStart(),
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id))
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.startCommand))

        # Подключение хэндлера команды /database
        self.__dispatcher.message.register(self.__databaseCommandHandler, Command(Text.databaseCommand),
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                           RegistrationFilter(users=self.__users), AdminFilter())
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.databaseCommand))

        # Подключение хэндлера команды /logs
        self.__dispatcher.message.register(self.__logsCommandHandler, Command(Text.logsCommand),
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                           RegistrationFilter(users=self.__users), AdminFilter())
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.logsCommand))

        # Подключение хэндлера неизвестных сообщений ↓
        self.__dispatcher.message.register(self.__unknownMessageHandler,
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                           RegistrationFilter(users=self.__users))
        self.__logger.info(Text.unknownMessageHandlerConnectedLog)

        # Подключение хэндлера незарегистрированных пользователей ↓
        self.__dispatcher.message.register(self.__unregisteredMessageHandler,
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id))
        self.__dispatcher.callback_query.register(self.__unregisteredCallbackHandler,
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id))
        self.__logger.info(Text.unregisteredUserHandlerConnectedLog)

        # Подключение хэндлера неподписанных пользователей ↓
        self.__dispatcher.message.register(self.__unsubscribedMessageHandler)
        self.__dispatcher.callback_query.register(self.__unsubscribedCallbackHandler)
        self.__logger.info(Text.unsubscribedUserHandlerConnectedLog)

    # ---------------------------------------------------- #

    # ---------- Методы класса SchetczeBot ---------- #
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

    @classmethod
    def __setAttributes(cls) -> None:
        """
        Метод, заполняющий поля класса SchetczeBot (создание необходимых объектов)
        :return: None
        """

        cls.__auth = AuthorizationTable()  # заполнение поля класса __auth
        cls.__users = UsersTable()  # заполнение поля класса __users
        cls.__dispatcher = Dispatcher()  # заполнение поля класса __dispatcher

    # ---------------------------------------------- #

    # ---------- Метод-запуск бота SchetczeBot ---------- #
    async def startPolling(self):
        await self.__dispatcher.start_polling(self)  # запуск бесконечного ожидания
        # Логирование ↓
        self.__logger.info(Text.pollingStartedLog)

    # --------------------------------------------------- #

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
        await self.send_message(chat_id=message.chat.id, text=Text.startMessage.format(message.chat.first_name),
                                parse_mode="HTML", reply_markup=Markup.mainMarkup)

    async def __databaseCommandHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка команды /database
        :param message: aiogram.types.Message
        :return: NoneType
        """

        self.__users.exportToExcel(filepath=Text.exportFilepath)  # экспорт таблицы Users в xlsx
        # Ответ ↓
        await self.send_document(chat_id=message.chat.id, document=FSInputFile(Text.exportFilepath))
        remove(Text.exportFilepath)  # удаление файла

    async def __logsCommandHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка команды /logs
        :param message: aiogram.types.Message
        :return: NoneType
        """

        # Ответ ↓
        await self.send_document(chat_id=message.chat.id, document=FSInputFile(Text.logsFilepath))

    # --------------------------------------------------------- #

    # ---------- Хэндлеры бота SchetczeBot: CallbackQuery --------- #
    async def __contributionCallbackHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопки contribution
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """
        # Ответ ↓
        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.contributionMessage.format(call.message.chat.first_name),
                                     parse_mode="HTML", reply_markup=Markup.contributionMarkup)

    async def __contributionPaymentHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопок типа payment
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        contribution = int(call.data[8:]) * 100  # получение размера взноса из callback.data

        # Генерация объекта provider_data, который требует Ю-касса ↓
        receipt = {
            "receipt": {"items": [
                {
                    "description": Text.contributionInvoiceButton["label"],
                    "quantity": "1.00",
                    "amount": {"value": format(contribution / 100, ".2f"), "currency": Text.contributionInvoiceButton["currency"]},
                    "vat_code": 1
                }
            ]}
        }
        # Удаление прошлого сообщения; отправка запроса на оплату ↓
        await self.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await self.send_invoice(chat_id=call.message.chat.id, title=Text.contributionInvoiceButton["title"],
                                description=Text.contributionInvoiceButton["description"],
                                payload=Text.contributionInvoiceButton["payload"],
                                provider_token=self.__auth.getPaymentToken(),
                                currency=Text.contributionInvoiceButton["currency"], need_email=True,
                                need_phone_number=True, send_email_to_provider=True, send_phone_number_to_provider=True,
                                prices=[LabeledPrice(label=Text.contributionInvoiceButton["label"],
                                                     amount=contribution)],
                                provider_data=dumps(receipt))
        # provider_data=)

    async def __responseCallbackHandler(self, call: CallbackQuery, state: FSMContext) -> None:
        """
        Метод-хэндлер: обработка кнопки response
        :param call: aiogram.types.CallbackQuery
        :param state: aiogram.fsm.FSMContext
        :return: NoneType
        """

        # Ответ ↓
        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.responseMessage.format(call.message.chat.first_name),
                                     parse_mode="HTML", reply_markup=Markup.cancellationMarkup)

        await state.set_state(States.responseState)  # активация responseState
        # Добавление значения сообщения для дальнейшего изменения ↓
        await state.update_data({"message_id": call.message.message_id})

    async def __cancellationCallbackHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработчик кнопку cancellation
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """
        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.startMessage.format(call.message.chat.first_name),
                                     parse_mode="HTML", reply_markup=Markup.mainMarkup)

    async def __infoCallbackHandler(self, call: CallbackQuery) -> None:
        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.infoMessage, parse_mode="HTML",
                                     reply_markup=Markup.cancellationMarkup)

    async def __unsubscribedCallbackHandler(self, call: Message) -> None:
        """
        Метод-хэндлер: обработка неподписанного пользователя
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.unsubscribedMessage.format(call.message.chat.first_name),
                                     parse_mode="HTML", reply_markup=Markup.subscribeMarkup)

    async def __unregisteredCallbackHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка незарегистрированного пользователя
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.unregisteredMessage.format(call.message.chat.first_name),
                                     parse_mode="HTML")

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
        await self.answer_pre_checkout_query(checkout.id, ok=True)

    # ----------------------------------------------------------------- #

    # --------- Хэндлеры бота SchetczeBot: SuccessfulPayment ---------- #
    async def __contributionSuccessfulPaymentHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка успешной оплаты contributionPayment
        :param message: aiogram.types.Message
        :return: NoneType
        """
        # Получение значения ячейки Contribution пользователя ↓
        filed = int(self.__users.getDataFromField(lineData=message.chat.id, columnName=self.__users.CONTRIBUTION))

        # Заполнение|Обновление ячеек Email, Phone_number, Contribution пользователя ↓
        self.__users.updateField(lineData=message.chat.id, columnName=self.__users.EMAIL,
                                 field=message.successful_payment.order_info.email)
        self.__users.updateField(lineData=message.chat.id, columnName=self.__users.PHONE_NUMBER,
                                 field=message.successful_payment.order_info.phone_number)
        self.__users.updateField(lineData=message.chat.id, columnName=self.__users.CONTRIBUTION,
                                 field=filed + int(message.successful_payment.total_amount // 100))

        # Генерация и отправка благодарственного сообщения ↓
        replyMessage = Text.thankForBuyingMessage.format(message.chat.first_name)
        await self.send_message(chat_id=message.chat.id, text=replyMessage, parse_mode="HTML")

        # Отправка главного меню ↓
        await self.send_message(chat_id=message.chat.id, text=Text.startMessage.format(message.chat.first_name),
                                parse_mode="HTML", reply_markup=Markup.mainMarkup)
        self.__logger.info(Text.successfulPaymentLog.format(message.chat.first_name,
                                                            Text.contributionInvoiceButton["payload"],
                                                            int(message.successful_payment.total_amount // 100)))

    # ----------------------------------------------------------------- #

    # ---------- Хэндлер бота SchetczeBot: Message ---------- #

    async def __responseMessageHandler(self, message: Message, state: FSMContext):
        if len(message.text) > 50:
            # Получение отзывов пользователя ↓
            responses = list(loads(str(self.__users.getDataFromField(lineData=message.chat.id,
                                                                     columnName=self.__users.RESPONSES))))
            responses.append(message.text)  # добавление нового отзыва
            # Добавление нового отзыва в ячейку пользователя ↓
            self.__users.updateField(lineData=message.chat.id,
                                     columnName=self.__users.RESPONSES, field=dumps(responses, ensure_ascii=False))

        stateData = await state.get_data()  # получение stateData (см ____responseCallbackHandler)
        # Удаление сообщения ↓
        await self.delete_message(chat_id=message.chat.id, message_id=stateData["message_id"])

        # Отправка сообщения: responseCommitMessage и startMessage ↓
        await self.send_message(chat_id=message.chat.id,
                                text=Text.responseCommitMessage.format(message.chat.first_name),
                                parse_mode="HTML")
        await self.send_message(chat_id=message.chat.id,
                                text=Text.startMessage.format(message.chat.first_name),
                                parse_mode="HTML", reply_markup=Markup.mainMarkup)
        await state.clear()  # очищение State

    async def __unknownMessageHandler(self, message: Message) -> None:
        # Ответ ↓
        await self.send_message(chat_id=message.chat.id,
                                text=Text.unknownMessage.format(message.chat.first_name, message.text),
                                parse_mode="HTML")

    async def __unsubscribedMessageHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка неподписанного пользователя
        :param message: aiogram.types.Message
        :return: NoneType
        """

        await self.send_message(chat_id=message.chat.id,
                                text=Text.unsubscribedMessage.format(message.chat.first_name),
                                parse_mode="HTML", reply_markup=Markup.subscribeMarkup)

    async def __unregisteredMessageHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка незарегистрированного пользователя
        :param message: aiogram.types.Message
        :return: NoneType
        """
        await self.send_message(chat_id=message.chat.id,
                                text=Text.unregisteredMessage.format(message.chat.first_name),
                                parse_mode="HTML")
    # ------------------------------------------------------- #
