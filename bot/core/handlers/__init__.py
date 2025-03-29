from bot.core.handlers.aiChatHandler import questionMessageHandler
from bot.core.handlers.clearChatHistoryHandler import clearChatHistoryHandler
from bot.core.handlers.helpHandler import helpHandler
from bot.core.handlers.startHandler import startHandler
from bot.core.handlers.setDefaultChatModelHandler import setDefaultChatModelHandler

def setupHandlers(bot):
    """
    Setting up the all command processor
    """
    startHandler(bot)
    clearChatHistoryHandler(bot)
    setDefaultChatModelHandler(bot)
    helpHandler(bot)
    questionMessageHandler(bot)
