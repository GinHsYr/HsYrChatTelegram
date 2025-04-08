import sqlite3
from decimal import Decimal

from bot.utils.logger import logger
from bot.utils.users import User
from bot.utils.vars import giftCodeInputtingList


def giftCodeHandler(bot, message, code):
    uid = message.from_user.id
    user = User(uid)
    try:
        giftCodeState = __checkGiftCode(code)
        exist, amount, isUsed = giftCodeState["exist"], giftCodeState["amount"], giftCodeState["isUsed"]

        if not exist:
            bot.send_message(message.chat.id, "该兑换码不存在")
            return
        if isUsed:
            bot.send_message(message.chat.id, "该兑换码已被使用")
            return

        user.setBalance(str(Decimal(user.balance) + Decimal(amount)))
        __setState(1, code)
        bot.send_message(uid, f"成功使用兑换码!余额+ ¥{amount}\n剩余余额:¥{user.balance}")
        logger.info(f"user {uid} use gift code {code}")
    finally:
        giftCodeInputtingList.remove(uid)


def __checkGiftCode(code):
    """
    Check a gift code's existence, amount, and usage status in one function.

    Args:
        code (str): The gift code to check

    Returns:
        dict: A dictionary containing:
            - exists (bool): Whether the code exists
            - amount (int/None): The code's amount if exists, else None
            - is_used (bool/None): Whether the code is used if exists, else None
    """
    result = {
        'exist': False,
        'amount': None,
        'isUsed': None,
    }

    try:
        conn = sqlite3.connect("bot/data/data.db")
        cursor = conn.cursor()

        # Check if code exists and get all data in one query
        cursor.execute(
            "SELECT amount, isUsed FROM giftCodes WHERE content = ?",
            (code,)
        )
        db_result = cursor.fetchone()

        if db_result:
            result['exist'] = True
            result['amount'] = db_result[0]
            result['isUsed'] = db_result[1]

    except sqlite3.Error as e:
        result['error'] = f"数据库错误: {e}"
    finally:
        if conn:
            conn.close()

    return result


def __setState(state: int, code):
    conn = sqlite3.connect("bot/data/data.db")
    cur = conn.cursor()
    cur.execute("UPDATE giftCodes SET isUsed = ? WHERE content = ?", (state, code,))
    conn.commit()
    cur.close()
    conn.close()
