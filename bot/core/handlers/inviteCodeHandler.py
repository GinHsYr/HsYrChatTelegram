from bot.utils.logger import logger
from bot.utils.users import User


def inviteCodeHandler(bot, message, code):
    uid = message.from_user.id
    user = User(uid)
    shareUser = User(code)

    if not shareUser.isRegistered():
        bot.reply_to(message, "未知邀请码")
        return
    if user.sharedStatus == 1:
        bot.reply_to(message, "您已填写过邀请码,请勿重复填写")
        return

    # 邀请人的邀请数加一并添加五次免费次数
    shareUser.setSharedCount(shareUser.sharedCount + 1)
    shareUser.setFreeTimes(shareUser.freeTimes + 5)
    bot.send_message(chat_id=shareUser.uid, text=f"邀请用户成功:{uid}, 免费次数+5")
    logger.info(f"user {uid} used invite code {shareUser.uid}")

    user.setSharedStatus(1)