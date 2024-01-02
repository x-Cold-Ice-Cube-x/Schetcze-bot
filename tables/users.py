# --------- Импорты встроенных библиотек --------- #
from json import dumps
# ------------------------------------------------ #

# ---------- Импорты из проекта ---------- #
from tables.table import Table
from configs.text import Text
# ---------------------------------------- #


class Users(Table):
    # ---------- Поля и свойства класса Authorization --------- #
    TELEGRAM_ID = "Telegram_ID"
    TELEGRAM_USERNAME = "Telegram_username"
    EMAIL = "Email"
    PHONE_NUMBER = "Phone_number"
    CONTRIBUTION = "Contribution"
    RESPONSES = "Responses"
    # --------------------------------------------------------- #

    def __init__(self):
        """
        Конструктор класса Users: выполнение конструктора класса-родителя
        """

        # Определение необходимых полей, для корректной работы методов экспорта и импорта ↓
        super().__init__("Users", self.TELEGRAM_ID)

        # Логирование ↓
        self._logger.info(Text.usersConnected)

    def fillingTheTable(self, telegramID: int, telegramUsername: str | None) -> None:
        """
        Переопределенный метод Table, заполняющий таблицу Users
        :param telegramID: Идентификационный код пользователя Telegram
        :param telegramUsername: Имя пользователя Telegram
        :return: NoneType
        """
        # Добавление нового пользователя в базу данных ↓
        self._cursor.execute(f"INSERT INTO {self._tableName} VALUES (?,?,?,?,?,?)",
                             (telegramID, telegramUsername, None, None, 0, dumps([])))
        self._connection.commit()  # сохранение изменений

        # Логирование ↓
        self._logger.info(Text.fillingTheTableUsers.format(self._tableName, self.TELEGRAM_ID, telegramID,
                                                           self.TELEGRAM_USERNAME, telegramUsername))
