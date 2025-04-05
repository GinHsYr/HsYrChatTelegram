import sqlite3


def getAllModelPrices():
    conn = sqlite3.connect("bot/data/data.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT modelName, pricingStrategy, promptPrice, completionPrice, perRequestPrice, unitScale, isActive, updatedAt FROM modelPricing")
    models = cur.fetchall()
    cur.close()
    conn.close()
    result = [
        {
            "model": model[0],
            "strategy": model[1],
            "promptPrice": model[2],
            "completionPrice": model[3],
            "perRequestPrice": model[4],
            "unitScale": model[5],
            "isActive": model[6],
            "updateTime": model[7]
        }
        for model in models
    ]
    return result


def delModel(modelName):
    conn = sqlite3.connect('bot/data/data.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM modelPricing WHERE modelName = ?", (modelName,))
    conn.commit()
    conn.close()

def addModel(
        conn,
        modelName: str,
        pricingStrategy: str,
        promptPrice: str = "0.0",
        completionPrice: str = "0.0",
        perRequestPrice: str = "0.0",
        unitScale: str = 'M',
        isActive: int = 1
) -> bool:
    try:
        # 验证必填字段
        if not modelName or not pricingStrategy:
            raise ValueError("modelName和pricingStrategy是必填字段")

        if pricingStrategy not in ['TOKEN', 'REQUEST']:
            raise ValueError("pricingStrategy必须是'TOKEN'或'REQUEST'")

        if pricingStrategy == 'TOKEN' and (not promptPrice or not completionPrice):
            raise ValueError("TOKEN定价策略需要promptPrice和completionPrice")

        if pricingStrategy == 'REQUEST' and not perRequestPrice:
            raise ValueError("REQUEST定价策略需要perRequestPrice")

        # 准备SQL和参数
        sql = '''
        INSERT INTO modelPricing (
            modelName, pricingStrategy, 
            promptPrice, completionPrice, 
            perRequestPrice, unitScale, isActive
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        params = (
            modelName, pricingStrategy,
            promptPrice, completionPrice,
            perRequestPrice, unitScale, isActive
        )

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return True

    except Exception as e:
        print(f"添加模型失败: {e}")
        conn.rollback()
        return False


def updateModelPricing(conn, modelName, pricingStrategy=None, promptPrice=None,
                       completionPrice=None, perRequestPrice=None,
                       unitScale=None, isActive=None):
    updates = []
    params = []

    if pricingStrategy is not None:
        updates.append("pricingStrategy = ?")
        params.append(pricingStrategy)
    if promptPrice is not None:
        updates.append("promptPrice = ?")
        params.append(promptPrice)
    if completionPrice is not None:
        updates.append("completionPrice = ?")
        params.append(completionPrice)
    if perRequestPrice is not None:
        updates.append("perRequestPrice = ?")
        params.append(perRequestPrice)
    if unitScale is not None:
        updates.append("unitScale = ?")
        params.append(unitScale)
    if isActive is not None:
        updates.append("isActive = ?")
        params.append(isActive)

    if not updates:
        return False

    updates.append("updatedAt = datetime('now','localtime')")

    sql = f'''
    UPDATE modelPricing 
    SET {', '.join(updates)}
    WHERE modelName = ?
    '''
    params.append(modelName)

    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"更新模型定价失败: {e}")
        return False

class ModelPrice:
    model = ""
    pricingStrategy = ""
    promptPrice = ""
    completionPrice = ""
    perRequestPrice = ""
    unitScale: str = ""
    isActive = True
    updateAt = ""

    def __init__(self, model):
        self.model = model
        self.pricingStrategy = self.getPricingStrategy()
        self.promptPrice = self.getPromptPrice()
        self.completionPrice = self.getCompletionPrice()
        self.perRequestPrice = self.getPerRequestPrice()
        self.unitScale = self.getUnitScale()
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

    def getUnitScale(self):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("SELECT unitScale FROM modelPricing WHERE modelName = ?", (self.model,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def setUnitScale(self, scale: str):
        conn = sqlite3.connect("bot/data/data.db")
        cur = conn.cursor()
        cur.execute("UPDATE modelPricing SET unitScale = ? WHERE modelName = ?", (scale, self.model,))
        conn.commit()
        cur.close()
        conn.close()
        self.unitScale = scale

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
            "strategy": self.pricingStrategy,
            "promptPrice": self.promptPrice,
            "completionPrice": self.completionPrice,
            "perRequestPrice": self.perRequestPrice,
            "unitScale": self.unitScale,
            "isActive": self.isActive,
            "updateAt": self.updateAt
        }
