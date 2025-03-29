import sqlite3
import time

from bot.utils.vars import default


class User:
    uid = ""
    registrationTime = ""
    freeTimes = 0
    GroupLevel = default
    bannedStatus = False
    sharedCount = 0
    sharedStatus = 0
    defaultChatModel = ""
    balance = 0

    def __init__(self, uid):
        self.uid = uid
        self.registrationTime = self.getRegistrationTime()
        self.freeTimes = self.getFreeTimes()
        self.GroupLevel = self.getGroupLevel()
        self.bannedStatus = self.getBannedStatus()
        self.sharedCount = self.getSharedCount()
        self.sharedStatus = self.isShared()
        self.defaultChatModel = self.getDefaultChatModel()
        self.balance = self.getBalance()

    def getRegistrationTime(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT registrationTime FROM users WHERE userId = ?", (self.uid,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def getFreeTimes(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT freeTimes FROM users WHERE userId = ?", (self.uid,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setFreeTimes(self, times: int):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET freeTimes = ? WHERE userId = ?", (times, self.uid,))
        conn.commit()
        cur.close()
        conn.close()
        self.freeTimes = times

    def getGroupLevel(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT userGroupLevel FROM users WHERE userId = ?", (self.uid,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setGroupLevel(self, level: int):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET userGroupLevel = ? WHERE userId = ?", (level, self.uid,))
        conn.commit()
        cur.close()
        conn.close()
        self.GroupLevel = level

    def getBannedStatus(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT bannedStatus FROM users WHERE userId = ?", (self.uid,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setBannedStatus(self, Status: int):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET bannedStatus = ? WHERE userId = ?", (Status, self.uid,))
        conn.commit()
        cur.close()
        conn.close()
        self.bannedStatus = Status

    def getDefaultChatModel(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT defaultChatModel FROM users WHERE userId = ?", (self.uid,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setDefaultChatModel(self, newModel: str):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET defaultChatModel = ? WHERE userId = ?", (newModel, self.uid,))
        conn.commit()
        cur.close()
        conn.close()
        self.defaultChatModel = newModel

    def getChatHistory(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT chatHistory FROM users WHERE userId = ?", (self.uid,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setChatHistory(self, content: str):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET chatHistory = ? WHERE userId = ?", (content, self.uid,))
        conn.commit()
        cur.close()
        conn.close()
        self.chatHistory = content

    def getBalance(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT balance FROM users WHERE userId = ?", (self.uid,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setBalance(self, newBalance):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET balance = ? WHERE userId = ?", (newBalance, self.uid,))
        conn.commit()
        cur.close()
        conn.close()
        self.balance = newBalance

    def isRegistered(self):
        try:
            conn = sqlite3.connect("bot/data/data.db")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE userId = ?", (self.uid,))
            result = cursor.fetchone()[0]
            conn.close()

            return result > 0

        except sqlite3.Error as e:
            print(f"数据库错误: {e}")
            return False

    def register(self, configs):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO users (
                userId, registrationTime, freeTimes, userGroupLevel, bannedStatus,
                sharedCount, defaultChatModel, chatHistory, balance
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.uid,
            int(time.time()),
            configs.defaultFreeTimes,
            default,
            False,
            0,
            "",
            "",
            configs.defaultBalance * 100
        ))
        conn.commit()
        cur.close()
        conn.close()

    def getSharedCount(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT sharedCount FROM users WHERE userId = ?", (self.uid,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setSharedCount(self, times: int):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET freeTimes = ? WHERE userId = ?", (times, self.uid,))
        conn.commit()
        cur.close()
        conn.close()
        self.sharedCount = times

    def isShared(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT isShared FROM users WHERE userId = ?", (self.uid,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setSharedStatus(self, status: int):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE users SET isShared = ? WHERE userId = ?", (status, self.uid,))
        conn.commit()
        cur.close()
        conn.close()
        self.sharedStatus = status
