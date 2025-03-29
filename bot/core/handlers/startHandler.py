import re

from bot.core.events import callbacks
from bot.core.handlers.inviteCodeHandler import inviteCodeHandler
from bot.utils import configLoader
from bot.utils.logger import logger
from bot.utils.users import User
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def startHandler(bot):
    """
    Setting up the /start command processor
    """
    configs = configLoader.Config()
    callbacks.callback(bot, configs)

    @bot.message_handler(commands=['start'])
    def startHandle(message):
        """
        Processing /start Command
        """

        uid = message.from_user.id
        matchI = re.search(r'/start\s+(\S+)', message.text)
        if matchI:
            matchText = matchI.group(1)
            inviteCodeHandler(bot, message, matchText)
            logger.info(f"user {uid} use invite code {matchText}")

        markUp = InlineKeyboardMarkup()
        markUp.row_width = 2
        markUp.add(InlineKeyboardButton("个人信息", callback_data="getPersonalInfo"),
                   InlineKeyboardButton("邀请", callback_data="invite"),
                   InlineKeyboardButton("兑换码填写", callback_data="giftCode"),
                   InlineKeyboardButton("帮助", callback_data="help"),
                   (InlineKeyboardButton("开源地址", url="https://github.com/GinHsYr/HsYrChatTelegram")))

        user = User(uid)
        bot.reply_to(message,
                     f"你好, 我是一个多功能AI聊天机器人, 支持多种生成式AI\n😆你可以与我聊天,讲故事,探讨问题或者编程!\n请向我发送您的问题\n或使用 /help 命令获取帮助",
                     reply_markup=markUp)
        logger.info(f"User {uid} sends command '/start'")

        if not user.isRegistered():
            user.register(configs)
            logger.info(
                f"User {uid} registration, free times {configs.defaultFreeTimes}, balance {configs.defaultBalance}CNY")
            bot.reply_to(message,
                         f"注册成功\n免费次数剩余:{configs.defaultFreeTimes}\n余额:¥{configs.defaultBalance}")
