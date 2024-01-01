# ---------- Импорты дополнительных библиотек --------- #
from asyncio import run
# ----------------------------------------------------- #

# ---------- Импорты из проекта ---------- #
from bot.schetcze_bot import SchetczeBot
# ---------------------------------------- #

if __name__ == "__main__":
    bot = SchetczeBot()
    run(bot.startPolling())
