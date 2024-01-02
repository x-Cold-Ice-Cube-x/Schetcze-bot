class Text:
    # ---------- Пути к файлам --------- #
    databaseFilepath = "databases/bot_database.sqlite"  # относительный путь к Sqlite базе
    logsFilepath = "databases/logs.log"  # относительный путь к логам
    # ---------------------------------- #

    # ---------- Протокольные сообщения ---------- #
    fillingTheTableAuthorization = ("Таблица {} успешно обновлена. Старые данные удалены. Новые данные:"
                                    "{}: {}, {}: {}")
    fillingTheTableUsers = ("Таблица {} успешно обновлена. Заполнены данные о новом пользователе: "
                            "{}: {}, {}: {}")

    loggerConnected = "Логгер успешно импортирован. "
    authorizationConnected = "Класс Authorization успешно импортирован. Таблица Authorization подключена."
    usersConnected = "Класс Users успешно импортирован. Таблица Users подключена."
    tokenVerificationPassed = "Телеграмм токен действителен. Выполняется запуск поллинга..."
    tokenVerificationError = ("Телеграмм токен недействителен. "
                              "Заполните таблицу Authorization заново и повторите попытку."
                              "Бот деактивирован.")
    pollingStarted = "Поллинг бота успешно запущен"

