from bot.utils.vars import commandsDict


def helpHandler(bot):
    """
    Setting up the /help command processor
    """

    @bot.message_handler(commands=['help'])
    def helpHandle(message):
        helpContent = "机器人命令一览:\n"
        for command, describe in commandsDict.items():
            helpContent += f"/{command}\t{describe}\n"
        bot.reply_to(message, helpContent)
