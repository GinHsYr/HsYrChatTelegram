from bot.core.events import callbacks
from bot.utils import configLoader
from telebot import types


def selectProvider(bot, message, configs):
    markup = types.InlineKeyboardMarkup()
    for providerName, providerConfig in configs.aiConfig.items():
        if providerConfig.get("enable", False):
            markup.add(types.InlineKeyboardButton(
                text=f"{providerName}",
                callback_data=f"selectProvider{providerName}"
            ))

    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text="请选择一个模型提供商:", reply_markup=markup)


def selectModel(bot, call, configs):
    providerName = call.data.replace('selectProvider', '')
    config = configs.aiConfig

    if providerName in config and config[providerName].get("enable", False):
        markup = types.InlineKeyboardMarkup()

        # Add buttons for each model in the selected provider
        for model in config[providerName].get("modelList", []):
            markup.add(types.InlineKeyboardButton(
                text=model,
                callback_data=f"selectModel@&{providerName}@&{model}"
            ))

        markup.add(types.InlineKeyboardButton(
            text="返回提供商列表",
            callback_data="backToProviders"
        ))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"请从 {providerName} 中选择一个模型:",
            reply_markup=markup
        )
    else:
        bot.answer_callback_query(call.id, "无效模型")


def setDefaultChatModelHandler(bot):
    """
    Setting up the /set_chat_model command processor
    """
    configs = configLoader.Config()
    callbacks.callback(bot, configs)

    @bot.message_handler(commands=['set_chat_model'])
    def setChatModelHandel(message):
        msg = bot.reply_to(message, "loading...")
        selectProvider(bot, msg, configs)