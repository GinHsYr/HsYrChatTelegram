import json

class Config:
    botApiToken = ""
    botName = ""
    botNickname = ""
    proxyHttp = ""
    proxyHttps = ""

    wHost = ""
    wListen = ""
    wPort = 0
    wSslCert = ""
    wSslPRIV = ""
    wUrlBase = f"https://{wHost}:{wPort}"
    wUrlPath = f"/{botApiToken}/"

    loggingFileName = ""

    defaultFreeTimes = 0
    defaultBalance = 0

    aiConfig = ""

    def __init__(self):
        with open(r"config.json", encoding="UTF-8") as f:
            configs = json.load(f)
        telegramConfig = configs["telegramConfig"]

        self.botApiToken = telegramConfig["apiToken"]
        self.botName = telegramConfig["botName"]
        self.botNickname = telegramConfig["botNickname"]
        self.proxyHttp = telegramConfig["proxy"]["http"]
        self.proxyHttps = telegramConfig["proxy"]["https"]

        webHook = telegramConfig["webHook"]
        self.wHost = webHook["host"]
        self.wListen = webHook["listen"]
        self.wPort = webHook["port"]
        self.wSslCert = webHook["sslCert"]
        self.wSslPRIV = webHook["sslPRIV"]
        self.wUrlBase = f"https://{self.wHost}:{self.wPort}"
        self.wUrlPath = f"/{self.botApiToken}/"

        self.loggingFileName = configs["logging"]["fileName"]

        users = configs["users"]
        self.defaultFreeTimes = users["defaultFreeTimes"]
        self.defaultBalance = users["defaultBalance"]

        self.aiConfig = configs["aiConfig"]

    def reLoad(self):
        self.__init__()