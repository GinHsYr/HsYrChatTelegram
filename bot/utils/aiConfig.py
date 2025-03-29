import json


class aiConfigure:
    base = ""
    key = ""
    enable = False
    modelList = []
    systemPrompt = ""

    def __init__(self, provider):
        self.provider = provider
        with open(r"config.json", encoding="UTF-8") as f:
            configs = json.load(f)["aiConfig"]
        self.base = configs[provider]["apiBase"]
        self.key = configs[provider]["key"]
        self.modelList = configs[provider]["modelList"]
        self.enable = configs[provider]["enable"]
        self.systemPrompt = configs[provider]["systemPrompt"]

    def getBase(self):
        return self.base

    def getSystemPrompt(self):
        return self.systemPrompt

    def getKey(self):
        return self.key

    def getEnable(self):
        return self.enable

    def getModelList(self):
        return self.modelList

    def reLoad(self):
        self.__init__()
