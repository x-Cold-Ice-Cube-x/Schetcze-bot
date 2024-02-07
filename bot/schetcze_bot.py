# --------- Импорты встроенных библиотек --------- #
from os import remove
from json import loads, dumps
from logging import getLogger, INFO, basicConfig
from datetime import datetime
# ------------------------------------------------ #


# ---------- Импорты дополнительных библиотек --------- #
from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, FSInputFile, CallbackQuery, LabeledPrice
from aiogram.types.pre_checkout_query import PreCheckoutQuery
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from tables.authorization_table import AuthorizationTable
from tables.users_table import UsersTable
from tables.tournaments_table import TournamentsTable
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
    __tournaments = None  # тип: TournamentsTable (обеспечить единственность объекта)
    __dispatcher = None  # тип: aiogram.Dispatcher (обеспечить единственность объекта)
    __logger = getLogger("botLogger")  # тип: logging.Logger (обеспечить единственность объекта)

    # --------------------------------------------- #

    # ---------- Конструктор класса SchetczeBot ---------- #
    def __init__(self):
        self.__setBasicConfig()  # создание объекта Logger (заранее, потому что дальше идет инициализация объектов)
        self.__setAttributes()  # заполнение всех полей класса
        super().__init__(token=self.__auth.getTelegramToken())  # авторизация бота в Telegram

        # Подключение хэндлера команды /start ↓
        self.__dispatcher.message.register(self.__startCommandHandler, CommandStart(),
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id))
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.startCommand))

        # Подключение хэндлера команды /tournament_create ↓
        self.__dispatcher.message.register(self.__createTournamentCommandHandler, Command(Text.createTournamentCommand),
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                           RegistrationFilter(users=self.__users),
                                           AdminFilter())
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.createTournamentCommand))

        # Подключение хэндлера команды /tournament_start ↓
        self.__dispatcher.message.register(self.__startTournamentCommandHandler, Command(Text.startTournamentCommand),
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                           RegistrationFilter(users=self.__users),
                                           AdminFilter())
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.startTournamentCommand))

        # Подключение хэндлера команды /tournament_close ↓
        self.__dispatcher.message.register(self.__closeTournamentCommandHandler, Command(Text.closeTournamentCommand),
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                           RegistrationFilter(users=self.__users),
                                           AdminFilter())
        self.__logger.info(Text.commandHandlerConnectedLog.format(Text.closeTournamentCommand))

        # Подключение хэндлера кнопки registration ↓
        self.__dispatcher.callback_query.register(self.__registrationCallbackHandler,
                                                  F.data == Text.registrationButton[1],
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.registrationButton[1]))

        # Подключение хэндлера кнопки profile ↓
        self.__dispatcher.callback_query.register(self.__profileCallbackHandler,
                                                  F.data == Text.profileButton[1],
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                                  RegistrationFilter(users=self.__users))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.profileButton[1]))

        # Подключение хэндлера кнопки balance
        self.__dispatcher.callback_query.register(self.__balanceIncreasingCallbackHandler,
                                                  F.data == Text.balanceIncreasingButton[1],
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                                  RegistrationFilter(users=self.__users))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.balanceIncreasingButton[1]))

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

        # Подключение хэндлера кнопок participationType
        self.__dispatcher.callback_query.register(self.__participationCallbackHandler,
                                                  F.data.startswith(Text.participationButtonType),
                                                  SubscriptionFilter(bot=self, chatID=Text.channel_id),
                                                  RegistrationFilter(users=self.__users))
        self.__logger.info(Text.buttonHandlerConnectedLog.format(Text.participationButtonType + " type"))

        # Подключение хэндлера готовности contribution платежа ↓
        self.__dispatcher.pre_checkout_query.register(self.__balancePreCheckoutHandler,
                                                      F.invoice_payload == Text.balanceInvoiceButton["payload"])
        self.__logger.info(Text.checkoutHandlerConnectedLog.format(Text.balanceInvoiceButton["payload"]))

        # Подключение хэндлера успешной оплаты товара balance ↓
        self.__dispatcher.message.register(self.__balanceSuccessfulPaymentHandler,
                                           F.successful_payment.invoice_payload ==
                                           Text.balanceInvoiceButton["payload"])
        self.__logger.info(Text.successfulPaymentHandlerConnectedLog.format(Text.balanceInvoiceButton["payload"]))

        # Подключение механизма регистрации пользователя ↓
        self.__dispatcher.message.register(self.__registrationMessageHandler, States.registrationState,
                                           SubscriptionFilter(bot=self, chatID=Text.channel_id))
        self.__logger.info(Text.registrationMessageHandlerConnectedLog)

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
        cls.__tournaments = TournamentsTable()  # заполнение поля класса __tournaments
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

        # Если пользователь уже зарегистрирован ↓
        if message.chat.id in self.__users.getDataFromColumn(columnName=self.__users.TELEGRAM_ID):
            await self.send_message(chat_id=message.chat.id, text=Text.startMessage_1.format(message.chat.first_name),
                                    parse_mode="HTML", reply_markup=Markup.mainMarkup)
            return

        # Переадресация на меню регистрации пользователя ↓
        await self.send_message(chat_id=message.chat.id,
                                text=Text.startMessage_0.format(message.chat.first_name), parse_mode="HTML",
                                reply_markup=Markup.registrationMarkup)

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

    async def __createTournamentCommandHandler(self, message: Message, command: CommandObject) -> None:
        """
        Метод-хэндлер: обработка команды /tournament_create
        :param message: aiogram.types.Message
        :param command: aiogram.filters.CommandObject
        :return: NoneType
        """

        # Проверка на дурака: есть ли аргументы к команде в нужном количестве, если дата адекватная ↓
        if (command.args is None or len(command.args.split()) != 2
                or datetime.strptime(command.args.split()[0], "%d.%m.%Y:%H:%M").timestamp()
                < datetime.now().timestamp()):
            # Отправка админу сообщения createTournamentCommandExceptionMessage ↓
            await self.send_message(chat_id=message.chat.id,
                                    text=Text.createTournamentCommandExceptionMessage.format(message.chat.first_name),
                                    parse_mode="HTML")
            return

        # Проверка можно ли преобразовать второй аргумент в целочисленный тип данных ↓
        try:
            args = command.args.split()  # получение аргументов команды
            self.__tournaments.fillingTheTable(datetime=args[0], contribution=int(args[1]))  # создание информации

            # Получение информации о турнире (нет порядкового номера турнира) ↓
            data = self.__tournaments.getDataFromLine(lineData=args[0])

            # Отправка сообщения participationMessage всем зарегистрированным пользователям ↓
            for telegramID in self.__users.getDataFromColumn(columnName=self.__users.TELEGRAM_ID):
                chat = await self.get_chat(chat_id=int(telegramID))  # получение чата с пользователем
                # Отправка сообщения participationMessage ↓
                await self.send_message(chat_id=chat.id, text=Text.participationOfferMessage.format(chat.first_name,
                                                                                                    data[0], data[1],
                                                                                                    data[2]),
                                        parse_mode="HTML",
                                        reply_markup=Markup.getParticipationMarkup(datetime=str(data[1])))
        except ValueError:
            # Отправка админу сообщения createTournamentCommandExceptionMessage ↓
            await self.send_message(chat_id=message.chat.id,
                                    text=Text.createTournamentCommandExceptionMessage.format(message.chat.first_name),
                                    parse_mode="HTML")

    async def __startTournamentCommandHandler(self, message: Message, command: CommandObject) -> None:
        """
        Метод-хэндлер: обработка команды /tournament_start
        :param message: aiogram.types.Message
        :param command: aiogram.filters.CommandObject
        :return: NoneType
        """

        # Проверка на дурака: есть ли аргументы к команде в нужном количестве, если турнир существует в базе данных
        if (command.args is None or len(command.args.split()) != 2
                or self.__tournaments.getDataFromLine(lineData=command.args.split()[0]) is None):
            # Отправка админу сообщения startTournamentCommandExceptionMessage ↓
            await self.send_message(chat_id=message.chat.id,
                                    text=Text.startTournamentCommandExceptionMessage.format(message.chat.first_name),
                                    parse_mode="HTML")
            return

        args = command.args.split()  # получение аргументов команды

        # Отправка каждому участнику турнира сообщение startTournamentMessage ↓
        for memberID in self.__tournaments.getMembers(args[0]):
            chat = await self.get_chat(memberID)
            await self.send_message(chat_id=chat.id, text=Text.startTournamentMessage.format(chat.first_name, args[1]),
                                    parse_mode="HTML")
        # Закрытие регистрации на турнир ↓
        self.__tournaments.updateField(lineData=args[0], columnName=self.__tournaments.PARTICIPATION, field=0)

    async def __closeTournamentCommandHandler(self, message: Message, command: CommandObject) -> None:
        """
        Метод-хэндлер: обработка команды /tournament_close
        :param message: aiogram.types.Message
        :param command: aiogram.filters.CommandObject
        :return: NoneType
        """

        # Проверка на дурака: есть ли аргументы к команде в нужном количестве, если турнир существует в базе данных
        if (command.args is None or len(command.args.split()) != 1
                or self.__tournaments.getDataFromLine(lineData=command.args.split()[0]) is None):
            # Отправка админу сообщения closeTournamentCommandExceptionMessage ↓
            await self.send_message(chat_id=message.chat.id,
                                    text=Text.closeTournamentCommandExceptionMessage.format(message.chat.first_name),
                                    parse_mode="HTML")
            return

        args = command.args.split()  # получение аргументов команды
        # Получение значения взноса турнира ↓
        contribution = int(self.__tournaments.getDataFromField(lineData=args[0],
                                                               columnName=self.__tournaments.CONTRIBUTION))
        # Отправка каждому участнику турнира сообщение closeTournamentMessage; возвращение взноса на баланс ↓
        for memberID in self.__tournaments.getMembers(datetime=args[0]):
            chat = await self.get_chat(memberID)
            balance = int(self.__users.getDataFromField(lineData=chat.id, columnName=self.__users.BALANCE))

            self.__users.updateField(lineData=memberID, columnName=self.__users.BALANCE, field=balance + contribution)
            await self.send_message(chat_id=chat.id,
                                    text=Text.closeTournamentMessage.format(message.chat.first_name, args[0],
                                                                            contribution),
                                    parse_mode="HTML")

        self.__tournaments.removeLine(lineData=args[0])  # удаление турнира из базы данных
    # --------------------------------------------------------- #

    # ---------- Хэндлеры бота SchetczeBot: CallbackQuery --------- #
    async def __participationCallbackHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопок типа participation
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        tournamentDatetime = call.data[14::]  # получение идентификатора турнира
        tournament = self.__tournaments.getDataFromLine(lineData=tournamentDatetime)  # получение всех данных о турнире
        # Проверка: открыта ли регистрация на турнир (0 - закрыта) ↓
        if tournament[3] == 0:
            # Отправка пользователю сообщения participationExceptionMessage_1 ↓
            await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         text=Text.participationExceptionMessage_1.format(call.message.chat.first_name),
                                         parse_mode="HTML")
            return

        # Назначение переменных, отвечающих за баланс пользователя и размер взноса на турнир ↓
        balance = int(self.__users.getDataFromField(lineData=call.message.chat.id, columnName=self.__users.BALANCE))
        contribution = int(tournament[2])

        # Если баланс игрока больше взноса на турнир
        if balance >= contribution:
            # Добавление пользователя турнир и списание взноса, отправка сообщения successfulParticipationMessage ↓
            self.__tournaments.addMember(datetime=tournamentDatetime, telegramID=call.message.chat.id)
            await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         text=Text.successfulParticipationMessage.format(call.message.chat.first_name,
                                                                                         contribution),
                                         parse_mode="HTML")
            self.__users.updateField(lineData=call.message.chat.id, columnName=self.__users.BALANCE,
                                     field=balance - contribution)
        else:
            # Отправка пользователю сообщения participationExceptionMessage_0 ↓
            await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                         text=Text.participationExceptionMessage_0.format(call.message.chat.first_name,
                                                                                          contribution - balance),
                                         parse_mode="HTML", reply_markup=call.message.reply_markup)

    async def __registrationCallbackHandler(self, call: CallbackQuery, state: FSMContext) -> None:
        """
        Метод-хэндлер: обработка кнопки registration
        :param call: aiogram.types.CallbackQuery
        :param state: aiogram.fsm.context.FSMContext
        :return: NoneType
        """

        # Отправка пользователю сообщение registrationMessage ↓
        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.registrationMessage.format(call.message.chat.first_name),
                                     parse_mode="HTML")

        await state.set_state(States.registrationState)  # активация registrationState

        # Передача message_id для дальнейшего изменения ↓
        await state.update_data({"message_id": call.message.message_id})

    async def __profileCallbackHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопки profile
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        userData = self.__users.getDataFromLine(lineData=call.message.chat.id)  # получение информации о пользователе
        # Отправка сообщения profileMessage ↓
        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.profileMessage.format(call.message.chat.first_name,
                                                                     userData[2], userData[5],
                                                                     userData[6], len(loads(str(userData[7])))),
                                     parse_mode="HTML", reply_markup=Markup.profileMarkup)

    async def __balanceIncreasingCallbackHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопки contribution
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        # Ответ ↓
        await self.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                     text=Text.balanceIncreasingMessage.format(call.message.chat.first_name),
                                     parse_mode="HTML", reply_markup=Markup.contributionMarkup)

    async def __contributionPaymentHandler(self, call: CallbackQuery) -> None:
        """
        Метод-хэндлер: обработка кнопок типа payment
        :param call: aiogram.types.CallbackQuery
        :return: NoneType
        """

        value = int(call.data[8:]) * 100  # получение размера взноса из callback.data

        # Генерация объекта provider_data, который требует Ю-касса ↓
        receipt = {
            "receipt": {"items": [
                {
                    "description": Text.balanceInvoiceButton["label"],
                    "quantity": "1.00",
                    "amount": {"value": format(value / 100, ".2f"),
                               "currency": Text.balanceInvoiceButton["currency"]},
                    "vat_code": 1
                }
            ]}
        }
        # Удаление прошлого сообщения; отправка запроса на оплату ↓
        await self.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await self.send_invoice(chat_id=call.message.chat.id, title=Text.balanceInvoiceButton["title"].format(self.__users.getDataFromField(lineData=call.message.chat.id, columnName=self.__users.BS_USERNAME)),
                                description=Text.balanceInvoiceButton["description"],
                                payload=Text.balanceInvoiceButton["payload"],
                                provider_token=self.__auth.getPaymentToken(),
                                currency=Text.balanceInvoiceButton["currency"], need_email=True,
                                need_phone_number=True, send_email_to_provider=True, send_phone_number_to_provider=True,
                                prices=[LabeledPrice(label=Text.balanceInvoiceButton["label"],
                                                     amount=value)])
                                # provider_data=dumps(receipt))
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
                                     text=Text.startMessage_1.format(call.message.chat.first_name),
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
    async def __balancePreCheckoutHandler(self, checkout: PreCheckoutQuery) -> None:
        """
        Метод-хэндлер: обработка товара balance
        :param checkout: aiogram.types.pre_checkout_query.PreCheckoutQuery
        :return: NoneType
        """
        # Приходит, как только была нажата кнопка оплаты
        # Ответ ↓
        await self.answer_pre_checkout_query(checkout.id, ok=True)

    # ----------------------------------------------------------------- #

    # --------- Хэндлеры бота SchetczeBot: SuccessfulPayment ---------- #
    async def __balanceSuccessfulPaymentHandler(self, message: Message) -> None:
        """
        Метод-хэндлер: обработка успешной оплаты balance
        :param message: aiogram.types.Message
        :return: NoneType
        """
        # Получение значения ячейки Balance пользователя ↓
        filed = int(self.__users.getDataFromField(lineData=message.chat.id, columnName=self.__users.BALANCE))

        # Заполнение|Обновление ячеек Email, Phone_number, Contribution пользователя ↓
        self.__users.updateField(lineData=message.chat.id, columnName=self.__users.EMAIL,
                                 field=message.successful_payment.order_info.email)
        self.__users.updateField(lineData=message.chat.id, columnName=self.__users.PHONE_NUMBER,
                                 field=message.successful_payment.order_info.phone_number)
        self.__users.updateField(lineData=message.chat.id, columnName=self.__users.BALANCE,
                                 field=filed + int(message.successful_payment.total_amount // 100))

        # Генерация и отправка благодарственного сообщения ↓
        replyMessage = Text.thankForBuyingMessage.format(message.chat.first_name)
        await self.send_message(chat_id=message.chat.id, text=replyMessage, parse_mode="HTML")

        # Отправка главного меню ↓
        await self.send_message(chat_id=message.chat.id, text=Text.startMessage_1.format(message.chat.first_name),
                                parse_mode="HTML", reply_markup=Markup.mainMarkup)
        self.__logger.info(Text.successfulPaymentLog.format(message.chat.first_name,
                                                            Text.balanceInvoiceButton["payload"],
                                                            int(message.successful_payment.total_amount // 100)))

    # ----------------------------------------------------------------- #

    # ---------- Хэндлер бота SchetczeBot: Message ---------- #
    async def __registrationMessageHandler(self, message: Message, state: FSMContext):
        # Обработка перерегистрации ↓
        if message.chat.id in self.__users.getDataFromColumn(self.__users.TELEGRAM_ID):
            self.__users.removeLine(message.chat.id)

        stateData = await state.get_data()  # получение stateData (cм __registrationCallbackHandler)
        if ":" in message.text:
            BSData = message.text.split(":")
            # Регистрация пользователя ↓
            self.__users.fillingTheTable(telegramID=message.chat.id, telegramUsername=message.chat.username,
                                         BSID=BSData[0], BSUsername=BSData[1])

            # Удаление прошлого сообщения и отправка successfulRegistrationMessage ↓
            await self.delete_message(chat_id=message.chat.id, message_id=stateData["message_id"])
            await self.send_message(chat_id=message.chat.id,
                                    text=Text.successfulRegistrationMessage.format(message.chat.first_name),
                                    parse_mode="HTML", reply_markup=Markup.mainMarkup)
            return

        # Удаление прошлого сообщения и отправка RegistrationExceptionMessage ↓
        await self.delete_message(chat_id=message.chat.id, message_id=stateData["message_id"])
        await self.send_message(chat_id=message.chat.id,
                                text=Text.registrationExceptionMessage.format(message.chat.first_name),
                                parse_mode="HTML", reply_markup=Markup.registrationMarkup)

        await state.clear()

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
                                text=Text.startMessage_1.format(message.chat.first_name),
                                parse_mode="HTML", reply_markup=Markup.mainMarkup)
        await state.clear()

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
