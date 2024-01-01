# ---------- Импорты из проекта ---------- #
from tables.table import Table
from configs.text import Text
# ---------------------------------------- #


class Authorization(Table):
    # ---------- Поля и свойства класса Authorization --------- #
    TELEGRAM_TOKEN = "Telegram_token"
    PAYMENT_TOKEN = "Payment_token"
    __tableName = "Authorization"
    __searchColumn = TELEGRAM_TOKEN
    # --------------------------------------------------------- #

    # ---------- Переопределенные методы Table ---------- #
    def fillingTheTable(self, telegramToken: str, paymentToken: str) -> None:
        """
        Переопределенный метод Table, заполняющий таблицу Authorization
        :param telegramToken: Авторизационный токен бота Telegram
        :param paymentToken: Авторизационный токен оплаты бота
        :return: NoneType
        """
        # Удаление всех исходных данных из таблицы ↓
        self._cursor.execute(f"DELETE * FROM {self.__tableName}")

        # Добавление актуальных авторизационных данных в таблицу ↓
        self._cursor.execute(f"INSERT INTO {self.__tableName} VALUES (?, ?)", (telegramToken, paymentToken))
        self._connection.commit()  # сохранение изменений

        # Логирование ↓
        self._logger.warning(Text.fillingTheTableAuthorization.format(self.__tableName, self.TELEGRAM_TOKEN,
                                                                      telegramToken, self.PAYMENT_TOKEN, paymentToken))
    # --------------------------------------------------- #

    # ---------- Методы импорта данных из таблицы Authorization ---------- #
    def getTelegramToken(self) -> str:
        """
        Метод, возвращающий Telegram токен бота
        :return: telegramToken
        """
        # Возвращение телеграмм-токена из таблицы ↓
        return str(self.getDataFromColumn(columnName=self.TELEGRAM_TOKEN)[0])

    def getPaymentToken(self) -> str:
        """
        Метод, возвращающий токен оплаты бота
        :return: paymentToken
        """
        # Возвращение токена оплаты из таблицы ↓
        return str(self.getDataFromColumn(columnName=self.PAYMENT_TOKEN)[0])
    # --------------------------------------------------------------------- #
