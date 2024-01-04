# ---------- Импорты дополнительных библиотек --------- #
from aiogram.fsm.state import StatesGroup, State
# ----------------------------------------------------- #


class States(StatesGroup):
    # ---------- Поля класса States ---------- #
    responseState = State()
    # ---------------------------------------- #
