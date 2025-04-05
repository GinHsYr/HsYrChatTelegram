import telebot
from bot.utils import configLoader

lowest, low, default, medium, premium = 1, 2, 3, 4, 5
commandsDict = {"start": "开始", "clear": "清空聊天记录", "set_chat_model": "设置默认聊天模型", "help": "帮助"}
giftCodeInputtingList = set()
configs = configLoader.Config()
bot = telebot.TeleBot(configs.botApiToken)
