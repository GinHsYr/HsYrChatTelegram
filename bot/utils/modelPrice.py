import sqlite3

def getAllModelPrices():
    conn = sqlite3.connect("bot/data/data.db")
    cur = conn.cursor()
    cur.execute("SELECT modelName, promptPrice, completionPrice, isActive FROM modelPricing")
    models = cur.fetchall()
    cur.close()
    conn.close()
    result = [
        {
            "model": model[0],
            "promptPrice": model[1],
            "completionPrice": model[2],
            "isActive": model[3]
        }
        for model in models
    ]
    return result


class ModelPrice:
    model = ""
    pricingStrategy = ""
    promptPrice = ""
    completionPrice = ""
    perRequestPrice = ""
    unitScale = 0
    isActive = True
    updateAt = ""

    def __init__(self, model):
        self.model = model
        self.pricingStrategy = self.getPricingStrategy()
        self.promptPrice = self.getPromptPrice()
        self.completionPrice = self.getCompletionPrice()
        self.perRequestPrice = self.getPerRequestPrice()
        # self.unitScale = self.getUnitScale()
        self.isActive = self.isActiveS()
        self.updateAt = self.getUpdateTime()

    def reLoadBy(self, model):
        self.__init__(model)

    def getPricingStrategy(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT pricingStrategy FROM modelPricing WHERE modelName = ?", (self.model,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setPricingStrategy(self, newStrategy):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE modelPricing SET pricingStrategy = ? WHERE modelName = ?", (newStrategy, self.model,))
        conn.commit()
        cur.close()
        conn.close()
        self.pricingStrategy = newStrategy

    def getPromptPrice(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT promptPrice FROM modelPricing WHERE modelName = ?", (self.model,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setPromptPrice(self, newPrice):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE modelPricing SET promptPrice = ? WHERE modelName = ?", (newPrice, self.model,))
        conn.commit()
        cur.close()
        conn.close()
        self.promptPrice = newPrice

    def getCompletionPrice(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT completionPrice FROM modelPricing WHERE modelName = ?", (self.model,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setCompletionPrice(self, newPrice):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE modelPricing SET completionPrice = ? WHERE modelName = ?", (newPrice, self.model,))
        conn.commit()
        cur.close()
        conn.close()
        self.completionPrice = newPrice

    def getPerRequestPrice(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT perRequestPrice FROM modelPricing WHERE modelName = ?", (self.model,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setPerRequestPrice(self, newPrice):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE modelPricing SET perRequestPrice = ? WHERE modelName = ?", (newPrice, self.model,))
        conn.commit()
        cur.close()
        conn.close()
        self.perRequestPrice = newPrice

    def isActiveS(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT isActive FROM modelPricing WHERE modelName = ?", (self.model,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setActiveS(self, newState: int):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE modelPricing SET isActive = ? WHERE modelName = ?", (newState, self.model,))
        conn.commit()
        cur.close()
        conn.close()
        self.isActive = newState

    def getUpdateTime(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT updatedAt FROM modelPricing WHERE modelName = ?", (self.model,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setUpdateTime(self, newTime):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE modelPricing SET updatedAt = ? WHERE modelName = ?", (newTime, self.model,))
        conn.commit()
        cur.close()
        conn.close()
        self.updateAt = newTime

    def toDict(self):
        return {
            "model": self.model,
            "pricingStrategy": self.pricingStrategy,
            "promptPrice": self.promptPrice,
            "completionPrice": self.completionPrice,
            "perRequestPrice": self.perRequestPrice,
            "isActive": self.isActive,
            "updateAt": self.updateAt
        }
    # def getUnitScale(self):
    #     conn = sqlite3.connect("bot/data/data.db")
    #     cur = conn.cursor()
    #     cur.execute("SELECT unitScale FROM modelPricing WHERE modelName = ?", (self.model,))
    #     result = cur.fetchone()
    #     cur.close()
    #     conn.close()
    #     if result is not None:
    #         return result[0]
    #     else:
    #         return None
    #
    # def setUnitScale(self, newScale):
    #     conn = sqlite3.connect("bot/data/data.db")
    #     cur = conn.cursor()
    #     cur.execute("UPDATE modelPricing SET unitScale = ? WHERE modelName = ?", (newScale, self.model,))
    #     conn.commit()
    #     cur.close()
    #     conn.close()
    #     self.unitScale = newScale
