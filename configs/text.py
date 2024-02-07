class Text:
    # ---------- Пути к файлам --------- #
    tournamentFilepath = "databases/tournament.json"
    databaseFilepath = "databases/bot_database.sqlite"
    logsFilepath = "databases/logs.log"
    exportFilepath = "databases/users.xlsx"
    # ---------------------------------- #

    # ---------- Протокольные сообщения ---------- #
    fillingTheTableAuthorizationLog = ("Таблица {} успешно обновлена. Старые данные удалены. Новые данные:"
                                       "{}: {}, {}: {}")
    fillingTheTableUsersLog = ("Таблица {} успешно обновлена. Заполнены данные о новом пользователе: "
                               "{}: {}, {}: {}, {}: {}, {}: {}")
    fillingTheTableTournamentsLog = ("Таблица {} успешно обновлена. Заполнены данные о новом турнире: "
                                     "{}: {}, {}: {}")

    loggerConnectedLog = "Логгер успешно импортирован. "
    authorizationConnectedLog = "Класс Authorization успешно импортирован. Таблица Authorization подключена."
    usersConnectedLog = "Класс Users успешно импортирован. Таблица Users подключена."
    tokenVerificationPassedLog = "Телеграмм токен действителен. Выполняется запуск поллинга..."
    tokenVerificationErrorLog = ("Телеграмм токен недействителен. "
                                 "Заполните таблицу Authorization заново и повторите попытку."
                                 "Бот деактивирован.")
    pollingStartedLog = "Поллинг бота успешно запущен."

    commandHandlerConnectedLog = "Обработчик команды {} успешно подключен."
    unknownMessageHandlerConnectedLog = "Обработчик неизвестных сообщений успешно подключен."
    unregisteredUserHandlerConnectedLog = "Обработчик незарегистрированного пользователя успешно подключен."
    unsubscribedUserHandlerConnectedLog = "Обработчик неподписанного пользователя успешно подключен."
    responseMessageHandlerConnectedLog = "Обработчик получение отзывов успешно подключен."
    registrationMessageHandlerConnectedLog = "Обработчик регистрации успешно подключен."

    buttonHandlerConnectedLog = "Обработчик кнопки {} успешно подключен."
    checkoutHandlerConnectedLog = "Обработчик готовности товара {} успешно подключен."
    successfulPaymentHandlerConnectedLog = "Обработчик успешной оплаты товара {} успешно подключен."
    successfulPaymentLog = "Пользователь {} успешно купил товар {} за {} рублей."
    # -------------------------------------------- #

    # ---------- ID групп, каналов и чатов ---------- #
    channel_id = -1002053615201
    admins_id = (1354516894, 1248242965)
    # ----------------------------------------------- #

    # ---------- Содержание кнопок ---------- #
    registrationButton = ("Зарегистрироваться  ️⚔️", "registration")
    balanceIncreasingButton = ("Пополнить баланс 💵", "balance")
    profileButton = ("Мой профиль ⚔️", "profile")
    donationButton = ("Донат 💵", "https://yoomoney.ru/to/410019925458398")
    responseButton = ("Оставить отзыв 🖊", "response")
    youtubeButton = ("Наш YouTube 📹", "http://www.youtube.com/@Shetcze")
    participationButton = ("Участвую ⚔️", "participation")

    cancellationButton = ("Отмена ⚙️", "cancellation")
    paymentButtonType = "payment"
    participationButtonType = "participation"
    paymentButtons = (("100₽ 💵", "payment_100"), ("150₽ 💵", "payment_150"), ("200₽ 💵", "payment_200"),
                      ("300₽ 💵", "payment_300"))

    subscribeButton = ("Турниры Бравл Старс 🎭", "https://t.me/KaktusTournaments")
    infoButton = ("Информация ⚙️", "info")
    balanceInvoiceButton = {"title": "Пополнение баланса пользователя {} 💵",
                            "description": "Пополнение баланса Tournaments | Brawl Stars 🎭, для участия в "
                                           "платных турнирах",
                            "payload": "balance", "currency": "RUB", "label": "Пополнение баланса 💵"}

    # -------------------------------------- #

    # ---------- Команды бота ---------- #
    startCommand = "start"
    databaseCommand = "database"
    logsCommand = "logs"
    createTournamentCommand = "tournament_create"
    startTournamentCommand = "tournament_start"
    closeTournamentCommand = "tournament_close"
    # ---------------------------------- #

    # ---------- Сообщения бота ---------- #
    createTournamentCommandExceptionMessage = ("<b>{}</b>, произошла ошибка во время выполнении команды ⚙️😔\n"
                                               "💡 Проверь корректность введенных данных, пример:\n"
                                               f"/{createTournamentCommand} <b>05.06.2024:12:00 100</b>")
    startTournamentCommandExceptionMessage = ("<b>{}</b>, произошла ошибка во время выполнении команды ⚙️😔\n"
                                              "💡 Проверь корректность введенных данных, пример:\n"
                                              f"/{startTournamentCommand} <b>05.06.2024:12:00 XWUC8328C</b>")
    closeTournamentCommandExceptionMessage = ("<b>{}</b>, произошла ошибка во время выполнении команды ⚙️😔\n"
                                              "💡 Проверь корректность введенных данных, пример:\n"
                                              f"/{closeTournamentCommand} <b>05.06.2024:12:00</b>")
    closeTournamentMessage = ("<b>{}</b>, турнир, назначенный на <b>{}</b>, к сожалению, не состоится 😔\n"
                              "💡 Подробности можешь прочитать в канале ☺️\n"
                              "💵 Я вернул на твой баланс <b>{}</b>")
    startMessage_0 = ("Привет, боец <b>{}</b>! 💫 \n"
                      "Чтобы завершить регистрацию, нажми на кнопку ниже 🎭 ↓")

    startMessage_1 = ("Привет, боец <b>{}</b>! 💫 \n"
                      "Давно не виделись, выбирай одну из предложенных функций ↓")

    registrationMessage = ("<b>{}</b>, чтобы участвовать в турнирах, ты должен сказать мне две вещи: ☺️\n"
                           "1) <b>Код игрока</b> 🎮\n"
                           "1) <b>Игровой ник</b> 🎮\n"
                           "Шаблон для ввода данных: <i>#P2VOGQCCJ</i><b>:</b><i>MF | Schetcze</i>\n"
                           "<i>(Двоеточие <b>обязательно</b> должно присутствовать)</i>")
    registrationExceptionMessage = ("<b>{}</b>, ты не зарегистрирован, попробуй ещё раз! ❌\n"
                                    "<i>(Возможно, ты забыл двоеточие)</i>")
    successfulRegistrationMessage = ("<b>{}</b>, ты успешно зарегистрирован ☺️\n"
                                     "Выбирай одну из предложенных функций ↓")

    participationOfferMessage = ("<b>{}</b>, ты приглашён на турнир ☺️\n"
                                 "⚙️ Порядковый номер турнира: <b>{}</b>\n"
                                 "🕘 Дата: <b>{}</b>\n"
                                 "💵 Взнос: <b>{}</b>\n"
                                 "Присоединяйся, и пусть победит сильнейший! ⚔️")
    successfulParticipationMessage = ("<b>{}</b>, ты успешно зарегистрирован на турнир ☺️\n"
                                      "Перед началом турнира я отправлю тебе <b>код комнаты</b> ⚔️\n"
                                      "💡 С твоего баланса списано <b>{}</b> 💵")
    startTournamentMessage = "<b>{}</b>, код комнаты - <code>{}</code>, залетай, мы ждем тебя! ⚔️"
    participationExceptionMessage_0 = ("<b>{}</b>, у тебя не хватает <b>{}</b> 💵 для участия в турнире 😔\n"
                                       "💡 <b>Пополни баланс</b> и сможешь участвовать в платных турнирах! ")
    participationExceptionMessage_1 = ("<b>{}</b>, к сожалению, ты не зарегистрирован на турнир 😔⚔️\n"
                                       "Регистрация на него уже закрыта, ты не успел 😔")

    profileMessage = ("💡 Профиль: <b>{}</b>\n"
                      "💵 Баланс: <b>{}</b>\n"
                      "⚙️ Код игрока: <b>{}</b>\n"
                      "🎮 Игровой ник: <b>{}</b>\n"
                      "💡 Количество отзывов: <b>{}</b>\n"
                      "<i>(Для перерегистрации жми на кнопку ↓)</i>")

    responseMessage = ("<b>{}</b>, все ли устраивает в сервисе? ⚙️\n"
                       "Напиши небольшой отзыв, это очень важно для нас! 😊\n\n"
                       "Требования к отзыву:\n"
                       "1. <b>Аргументированная критика</b> 📈\n"
                       "2. <b>Адекватные предложения</b> 💡\n\n"
                       "Напоминаю, что за <b>5 адекватных аргументов</b> следует оплата 200₽ и "
                       "бесплатное участие в турнире! ⚔️ \n\n"
                       "<b>Принимаю отзыв следующим сообщением ↓</b>")

    responseCommitMessage = "<b>{}</b>, твой отзыв успешно принят! 😊"

    balanceIncreasingMessage = "<b>{}</b>, выбери одну из сумм пополнения ↓"
    unsubscribedMessage = "<b>{}</b>, чтобы пользоваться услугами бота, подпишись, а потом пропиши /start ↓ 😊"
    unknownMessage = "<b>{}</b>, я не знаю что ответить на: \n<i>{}</i> 😔"
    thankForBuyingMessage = "<b>{}</b>, благодарим за покупку! 😊"
    unregisteredMessage = "<b>{}</b>, чтобы пользоваться услугами бота, пропиши /start ⚙️"
    infoMessage = ("<b>Добро пожаловать! Здесь ты можешь ознакомиться с основной информацией:</b>\n"
                   "1) В нашем лагере игрок всегда может купить пропуск на пользовательский турнир по Brawl Stars, "
                   "где соревнуется либо 10 человек, либо 2 команды по 3!\n\n"
                   "После оплаты игрок должен отправить скриншот оплаты администрации, указав:\n"
                   "1) <b>Игровой ник</b>\n"
                   "2) <b>Номер телефона</b>\n"
                   "3) <b>На какую сумму куплен проход</b> ⚔️🎫\n\n"
                   "<i>Затем администрация создаёт комнату в игре, куда приглашает игроков, оплативших взнос.</i>\n\n"
                   "<i>Начинается игра. По окончании битвы разделяется собранный игровой банк среди 4 игроков (ШД), "
                   "или команды (3х3)</i>\n\n"
                   "2) Также всегда имеется возможность оставить свое мнение о сервисе, ведь <b>мнение клиента - "
                   "главное. </b>☄️\n\n"
                   "3) Или же ты можешь перейти по ссылке на наши другие социальные сети, "
                   "где мы <b>активно публикуем записи, или видео!</b> 😉\n")
    # ------------------------------------ #
