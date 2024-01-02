class Text:
    # ---------- Пути к файлам --------- #
    databaseFilepath = "databases/bot_database.sqlite"
    logsFilepath = "databases/logs.log"
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
    pollingStartedLog = "Поллинг бота успешно запущен"
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
    # ---------------------------- #
