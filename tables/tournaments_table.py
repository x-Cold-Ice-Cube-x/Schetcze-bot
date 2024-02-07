# ---------- Импорты из проекта ---------- #
from tables.table import Table
from configs.text import Text
# ---------------------------------------- #

# --------- Импорты встроенных библиотек --------- #
from json import dumps, loads
# ------------------------------------------------ #


class TournamentsTable(Table):
    # ---------- Поля класса TournamentsTable ---------- #
    SEQUENCE_NUMBER = "Sequence_number"
    DATETIME = "Datetime"
    CONTRIBUTION = "Contribution"
    PARTICIPATION = "Participation"
    MEMBERS = "Members"
    # -------------------------------------------------- #

    # ---------- Конструктор класса TournamentsTable ---------- #
    def __init__(self):
        """
        Конструктор класса TournamentsTable: выполнение конструктора класса-родителя
        """

        # Определение необходимых полей, для корректной работы методов экспорта и импорта ↓
        super().__init__(tableName="Tournaments", searchColumn=self.DATETIME)
    # --------------------------------------------------------- #

    # ---------- Переопределенные методы Table ---------- #
    def fillingTheTable(self, datetime: str, contribution: int) -> None:
        """
        Переопределенный метод Table, заполняющий таблицу Tournaments
        :param datetime: Дата и время турнира (будет использоваться для информирования)
        :param contribution: Сумма взноса (минимальный баланс, необходимый для участия в турнире)
        :return: NoneType
        """

        # Заполнение необходимых для реализации турнира данных ↓
        self._cursor.execute(f"INSERT INTO {self._tableName} "
                             f"({self.DATETIME}, {self.CONTRIBUTION}, {self.PARTICIPATION}, {self.MEMBERS}) VALUES (?,?,?,?)",
                             (datetime, contribution, 1, "[]"))
        self._connection.commit()  # сохранение изменений

        # Логирование ↓
        self._logger.info(Text.fillingTheTableTournamentsLog.format(self._tableName, self.DATETIME, datetime,
                                                                    self.CONTRIBUTION, contribution))
    # --------------------------------------------------- #

    def getMembers(self, datetime: str) -> list[int]:
        """
        Метод, возвращающий список с участниками турнира
        :param datetime: Дата и время турнира
        :return: List[int]
        """
        return list(loads(str(self.getDataFromField(lineData=datetime, columnName=self.MEMBERS))))

    def addMember(self, datetime: str, telegramID: int) -> None:
        """
        Метод, добавляющий в список с участниками турнира нового пользователя
        :param datetime: Дата и время турнира
        :param telegramID: Идентификационный код пользователя Telegram
        :return: NoneType
        """

        members = self.getMembers(datetime=datetime)  # получение списка с участниками
        members.append(telegramID)  # добавление нового участника
        self.updateField(lineData=datetime, columnName=self.MEMBERS, field=dumps(members))  # сохранение в базу


