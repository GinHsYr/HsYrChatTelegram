import sqlite3
from decimal import Decimal

import pandas as pd
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
        giftCodeInputtingList.discard(uid)


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

    conn = None
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


def addGiftCodes(giftList: list[dict]):
    """
    批量添加兑换码。

    Args:
        giftList (list): 多个包含兑换码信息的字典，例如:
            [{"code": "code1", "amount": "1.2"}, {"code": "code2", "amount": "2.5"}]
    """
    if not giftList:
        logger.warning("Failed to add redemption codes in batches: the list is empty")
        return

    conn = None
    try:
        conn = sqlite3.connect("bot/data/data.db")
        cursor = conn.cursor()
        successCount = 0
        failCount = 0

        for gift in giftList:
            code = gift.get("code")
            amount = gift.get("amount")

            if not code or not amount:
                logger.warning("Skip invalid data: missing code or amount")
                failCount += 1
                continue

            try:
                cursor.execute(
                    "INSERT INTO giftCodes (content, amount, isUsed) VALUES (?, ?, 0)",
                    (code, amount)
                )
                successCount += 1
            except sqlite3.IntegrityError:
                logger.warning(f"Redemption code already exists, skip:{code}")
                failCount += 1
            except Exception as e:
                logger.error(f"Error inserting redemption code {code}: {e}")
                failCount += 1

        conn.commit()
        logger.info(f"Batch adding completed: {successCount} successful, {failCount} failed")

    except sqlite3.Error as e:
        logger.error(f"data base error: {e}")
    finally:
        if conn:
            conn.close()


def updateGiftCodes(df: pd.DataFrame):
    try:
        conn = sqlite3.connect("bot/data/data.db")
        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute(
                "UPDATE giftCodes SET amount = ?, isUsed = ? WHERE content = ?",
                (str(row["amount"]), int(row["isUsed"]), row["code"])
            )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"update gift codes error: {e}")


def getAllGiftCodes() -> pd.DataFrame:
    """
    获取所有兑换码的列表，包括 code、amount、isUsed 信息。

    Returns:
        list[dict]: 兑换码信息列表，例如：
        [
            {"code": "xxx", "amount": "1.2", "isUsed": 0},
            {"code": "yyy", "amount": "5.0", "isUsed": 1},
        ]
    """
    codes = pd.DataFrame()
    conn = None
    try:
        conn = sqlite3.connect("bot/data/data.db")

        codes = pd.read_sql_query("SELECT content AS code, amount, isUsed FROM giftCodes", conn)
    except sqlite3.Error as e:
        logger.error(f"Database error when reading redemption code: {e}")
    finally:
        if conn:
            conn.close()

    return codes


def __setState(state: int, code):
    conn = sqlite3.connect("bot/data/data.db")
    cur = conn.cursor()
    cur.execute("UPDATE giftCodes SET isUsed = ? WHERE content = ?", (state, code,))
    conn.commit()
    cur.close()
    conn.close()
