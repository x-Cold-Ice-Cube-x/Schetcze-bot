class Text:
    # ---------- Пути к файлам --------- #
    databaseFilepath = "databases/bot_database.sqlite"
    logsFilepath = "databases/logs.log"
    exportFilepath = "databases/users.xlsx"
    # ---------------------------------- #

    # ---------- Протокольные сообщения ---------- #
    fillingTheTableAuthorizationLog = ("Таблица {} успешно обновлена. Старые данные удалены. Новые данные:"
                                       "{}: {}, {}: {}")
    fillingTheTableUsersLog = ("Таблица {} успешно обновлена. Заполнены данные о новом пользователе: "
                               "{}: {}, {}: {}")

    loggerConnectedLog = "Логгер успешно импортирован. "
    authorizationConnectedLog = "Класс Authorization успешно импортирован. Таблица Authorization подключена."
    usersConnectedLog = "Класс Users успешно импортирован. Таблица Users подключена."
    tokenVerificationPassedLog = "Телеграмм токен действителен. Выполняется запуск поллинга..."
    tokenVerificationErrorLog = ("Телеграмм токен недействителен. "
                                 "Заполните таблицу Authorization заново и повторите попытку."
                                 "Бот деактивирован.")
    pollingStartedLog = "Поллинг бота успешно запущен."
    startCommandHandlerConnectedLog = "Обработчик /start успешно подключен."
    databaseCommandHandlerConnectedLog = "Обработчик /database успешно подключен."
    # -------------------------------------------- #

    # ---------- ID групп и каналов ---------- #
    channel_id = -1002091618042
    # ---------------------------------------- #

    # ---------- Содержание кнопок ---------- #
    contributionButton = ("Оплатить взнос ⚔️", "contribution")
    donationButton = ("Донат 💵", "https://yoomoney.ru/to/410019925458398")
    responseButton = ("Оставить отзыв 🖊", "response")

    cancellationButton = ("Отмена ⚙️", "cancellation")

    paymentButtons = (("100₽ 💵", "payment_100"), ("200₽ 💵", "payment_200"), ("300₽ 💵", "payment_300"),
                      ("500₽ 💵", "payment_500"))

    subscribeButton = ("Турниры Бравл Старс 🎭", "https://t.me/KaktusTournaments")
    # -------------------------------------- #

    # ---------- Команды бота (кроме start) ---------- #
    databaseCommand = "database"
    # ------------------------------------------------ #

    # ---------- Сообщения бота ---------- #
    startMessage = ("Привет, боец <b>{}</b>! 💫 \n"
                    "Выбирай одну из предложенных в клавиатуре функций ↓ ")

    responseMessage = ("<b>{}</b>, все ли устраивает в сервисе? ⚙️\n"
                       "Напиши небольшой отзыв, это очень важно для нас! 😊\n\n"
                       "Требования к отзыву:\n"
                       "1. <b>Аргументированная критика</b> 📈\n"
                       "2. <b>Адекватные предложения</b> 💡\n\n"
                       "Напоминаю, что за <b>5 адекватных аргументов</b> следует оплата 200₽ и "
                       "бесплатное участие в турнире! ⚔️ \n\n"
                       "<b>Принимаю отзыв следующим сообщением ↓</b>")

    responseCommitMessage = "<b>{}</b>, твой отзыв успешно принят! 😊"

    contributionMessage = "<b>{}</b>, выбери одну из сумм взноса ↓"
    unsubscribedMessage = "<b>{}</b>, чтобы пользоваться услугами бота, подпишись ↓ 😊"
    # ------------------------------------ #
