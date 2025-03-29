from bot.utils.aiConfig import aiConfigure
from bot.utils.logger import logger
from bot.utils.prompt import Prompts
from bot.utils.users import User


def clearChatHistoryHandler(bot):
    """
    Setting up the /clear command processor
    """

    @bot.message_handler(commands=["clear"])
    def clear(message):
        uid = message.from_user.id
        logger.info(f"user {uid} sends command '/clear' ")

        user = User(uid)
        if not user.isRegistered():
            bot.reply_to(message, "您尚未注册, 请发送 /start 命令注册")
            return
        if user.getChatHistory() == "":
            bot.reply_to(message, "🤖您还没有聊过天呢")
            return

        provider, model = str(user.defaultChatModel).split(":")
        aiConfigs = aiConfigure(provider)
        user.setChatHistory(str(Prompts(model).addSystemMessage(aiConfigs.systemPrompt).messages))
        bot.reply_to(message, "历史记录已清空!🤖")
