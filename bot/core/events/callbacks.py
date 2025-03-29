import time

from bot.core.handlers.setDefaultChatModelHandler import selectModel, selectProvider
from bot.utils.logger import logger
from bot.utils.users import User
from bot.utils.vars import giftCodeInputtingList


def callback(bot, configs):
    @bot.callback_query_handler(func=lambda call: True)
    def callbackQuery(call):
        callData = call.data
        uid = call.from_user.id
        user = User(uid)
        if not user.isRegistered():
            bot.reply_to(call.message, "您尚未注册, 请发送 /start 命令注册")
            return

        registrationTime = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(int(user.getRegistrationTime())))
        if callData == "getPersonalInfo":
            logger.info(f"User {uid} clicks button 'getPersonalInfo'")
            bot.send_message(uid,
                             f"<b>{configs.botNickname}为您服务!</b>\n\n🆔用户id:{uid}\n\n🕞注册时间:{registrationTime}\n⏱️免费次数剩余:{user.freeTimes}\n💰余额:¥{user.balance}\n\n🔗邀请链接:<code>https://t.me/{configs.botName}?start={uid}</code>",
                             parse_mode="HTML")

        if callData == "invite":
            logger.info(f"User {uid} clicks button 'invite'")
            bot.send_message(uid,
                             f"<b>{configs.botNickname}\n🤖超强AI聚合机器人!随时随地使用各大AI助手\n\n🔗复制本条消息或将链接发送给其他人进行邀请,邀请成功获得5次免费次数:</b><code>https://t.me/{configs.botName}?start={uid}</code>",
                             parse_mode="HTML")

        if callData.startswith("selectProvider"):
            selectModel(bot, call, configs)

        if callData.startswith("selectModel"):
            _, providerName, modelName = call.data.split('@&', 2)

            # Get user and set their default model
            logger.info(f"user {uid} change default chat model to {providerName}:{modelName}")
            user.setDefaultChatModel(f"{providerName}:{modelName}")

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"已设置默认模型为: {providerName}:{modelName}"
            )
        if callData == "backToProviders":
            selectProvider(bot, call.message, configs)

        if callData == "giftCode":
            giftCodeInputtingList.add(uid)
            bot.send_message(uid, "请输入兑换码:")
