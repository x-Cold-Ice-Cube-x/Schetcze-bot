# ---------- Импорты из проекта ---------- #
from tables.table import Table
from configs.text import Text


# ---------------------------------------- #


class UsersTable(Table):
    # ---------- Поля и свойства класса Authorization --------- #
    TELEGRAM_ID = "Telegram_ID"
    TELEGRAM_USERNAME = "Telegram_username"

    BALANCE = "Balance"
    EMAIL = "Email"
    PHONE_NUMBER = "Phone_number"

    BS_ID = "BS_ID"  # -> BrawlStars
    BS_USERNAME = "BS_username"  # -> BrawlStars

    RESPONSES = "Responses"

    # --------------------------------------------------------- #

    # ---------- Конструктор класса UsersTable ---------- #
    def __init__(self):
        """
        Конструктор класса UsersTable: выполнение конструктора класса-родителя
        """

        # Определение необходимых полей, для корректной работы методов экспорта и импорта ↓
        super().__init__("Users", self.TELEGRAM_ID)

        # Логирование ↓
        self._logger.info(Text.usersConnectedLog)

    # --------------------------------------------------- #

    # ---------- Переопределенные методы Table ---------- #
    def fillingTheTable(self, telegramID: int, telegramUsername: str | None, balance: int, email: str,
                        phoneNumber: str, BSID: str, BSUsername: str, responses: str) -> None:
        """
        Переопределенный метод Table, заполняющий таблицу Users
        :param telegramID: Идентификационный код пользователя Telegram
        :param telegramUsername: Имя пользователя Telegram
        :param balance: Сохраненный баланс пользователя (для перерегистрации)
        :param email: Сохраненный email пользователя (для перерегистрации)
        :param phoneNumber: Сохраненный номер телефона пользователя (для перерегистрации)
        :param BSID: Идентификационный код игрока BrawlStars
        :param BSUsername: Имя игрока BrawlStars
        :param responses: Сохраненные отзывы пользователя (для перерегистрации)
        :return: NoneType
        """

        # Добавление нового пользователя в базу данных ↓
        self._cursor.execute(f"INSERT INTO {self._tableName} VALUES (?,?,?,?,?,?,?,?)",
                             (telegramID, telegramUsername, balance, email, phoneNumber, BSUsername, BSID, responses))
        self._connection.commit()  # сохранение изменений

        # Логирование ↓
        self._logger.info(Text.fillingTheTableUsersLog.format(self._tableName, self.TELEGRAM_ID, telegramID,
                                                              self.TELEGRAM_USERNAME, telegramUsername,
                                                              self.BS_USERNAME, BSUsername, self.BS_ID, BSID))
    # ---------------------------------------------------- #
