import sqlite3
import time

from bot.utils.logger import logger
from bot.utils.users import getAllUsers
from bot.utils.vars import bot


def pubAnnounce(content: str):
    userData = getAllUsers(sqlite3.connect("bot/data/data.db"))["userId"]
    step = 0
    logger.info("Announcement sending starts")

    for i in userData:
        try:
            bot.send_message(i, f"**公告**\n{content}", parse_mode="markdown")
        except Exception as e:
            logger.error(f"pub ann err:{e}")
        step += 1
        if step % 10 == 0:
            time.sleep(1)
