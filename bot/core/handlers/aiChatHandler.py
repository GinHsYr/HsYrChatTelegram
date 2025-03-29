import ast
import base64
import json
import re
from decimal import Decimal

import openai
import requests
from bot.core.handlers.giftCodeHandler import giftCodeHandler
from bot.utils import configLoader
from bot.utils.aiConfig import aiConfigure
from bot.utils.logger import logger
from bot.utils.modelPrice import ModelPrice
from bot.utils.prompt import Prompts
from bot.utils.users import User
from bot.utils.vars import giftCodeInputtingList
from telebot import types


def questionMessageHandler(bot):
    @bot.message_handler(content_types=["text", "photo"], chat_types="private")
    def answer(message):
        uid = message.from_user.id
        user = User(uid)
        configs = configLoader.Config()
        logger.info(f"user {uid} send message")
        if not user.isRegistered():
            bot.reply_to(message, "您尚未注册, 请发送 /start 命令注册")
            return
        if uid in giftCodeInputtingList:
            giftCodeHandler(bot, message, message.text)
            return

        if user.getDefaultChatModel() == "":
            markup = types.InlineKeyboardMarkup()
            # Add buttons for enabled providers
            aiConfigs = configs.aiConfig
            for providerName, providerConfig in aiConfigs.items():
                if providerConfig.get("enable", False):
                    markup.add(types.InlineKeyboardButton(
                        text=f"{providerName}",
                        callback_data=f"selectProvider{providerName}"
                    ))

            bot.reply_to(message, "请选择一个模型提供商:", reply_markup=markup)
            return
        answerTo(bot, message, user)


chattingList = set()


def answerTo(bot, message, user: User):
    uid = user.uid
    payment = ""
    if uid in chattingList:
        bot.reply_to(message, "上轮对话还未完成, 稍安勿躁🤖")
        return
    if user.freeTimes > 0:
        payment = "freeTimes"
    elif Decimal(user.balance) > 0:
        payment = "balance"
    else:
        bot.reply_to(message, "您的余额不足🥹")
        return

    chattingList.add(uid)
    completionTokens, promptTokens, totalTokens = 0, 0, 0
    actualModel = ""  # 实际调用模型
    url = ""  # 用户发送图片的url

    try:
        provider, model = str(user.defaultChatModel).split(":")
        aiConfigs = aiConfigure(provider)
        logger.info(f"get user {uid} provider {provider} & model {model}")
        client = openai.OpenAI(base_url=aiConfigs.base, api_key=aiConfigs.key)

        chatHistory = user.getChatHistory()
        chatHistory = chatHistory.replace("\n", "\\n")
        prompt = Prompts(model=model, msg=chatHistory)
        if str(prompt.messages) == "":
            prompt.messages = str({"role": "system", "content": f"{aiConfigs.systemPrompt}"})
        jsonPrompt = json.dumps(ast.literal_eval(prompt.messages))

        if len(jsonPrompt) == 0:
            jsonPrompt = [{"role": "system", "content": f"{aiConfigs.systemPrompt}"}]

        prompt.messages = jsonPrompt
        prompt.keepLastNRounds(6)
        msg = bot.reply_to(message, "请稍等...")

        if message.content_type == "photo":
            photo = message.photo[-1]
            fileInfo = bot.get_file(photo.file_id)
            url = f"https://api.telegram.org/file/bot{bot.token}/{fileInfo.file_path}"
            caption = message.caption
            if caption:
                response = requests.get(url)
                imageBytes = response.content
                base64Image = base64.b64encode(imageBytes).decode("utf-8")
                dataUrl = f"data:image/jpeg;base64,{base64Image}"
                # URL转为base64后发送给目标
                prompt.addUserMessage(caption).addImage(dataUrl)
            else:
                bot.reply_to(message, "请添加描述~")
                chattingList.remove(uid)
                return
        else:
            prompt.addUserMessage(message.text)

        completion = client.chat.completions.create(
            model=model,
            messages=prompt.messages,
            temperature=prompt.temperature,
            stream=True,
            stream_options={"include_usage": True}
        )
        completeContent, sendContent = "", ""
        step = 0

        previousContent = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content is not None:
                step += 1
                completeContent += f"{chunk.choices[0].delta.content}".replace('"', '\\"')
                sendContent = completeContent + f"\n\n> Model:{model}"
                if step % 40 == 0:
                    # Check if content has changed since last update
                    if sendContent != previousContent:
                        bot.edit_message_text(
                            chat_id=message.chat.id,
                            message_id=msg.message_id,
                            text=sendContent
                        )
                        previousContent = sendContent
            if chunk.usage:
                actualModel = chunk.model
                usage = chunk.usage
                completionTokens = usage.completion_tokens
                promptTokens = usage.prompt_tokens
                totalTokens = usage.total_tokens

        logger.info(f"user {uid} actual model {actualModel}")
        sendContent = sendContent.replace("<think>", "```思考过程\n")
        sendContent = sendContent.replace("</think>", "```")

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg.message_id,
            text=f"{sendContent}|Tokens used:{totalTokens}",
            parse_mode="Markdown",
        )
        prompt.addAssistantMessage(completeContent)
        user.setChatHistory(str(prompt.messages))
    except Exception as e:
        chattingList.remove(uid)
        logger.error(e)

        match = re.search(r"'type':\s*'([^']+)'", str(e))
        if match:
            typeValue = match.group(1)
            if typeValue == "BadRequest":
                bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="本模型不支持该操作")
            return

        bot.reply_to(message, f"好像出了点小问题😅\n```详细情况\n{e}```", parse_mode="Markdown")
        return
    else:
        chattingList.remove(uid)
        if payment == "freeTimes":
            user.setFreeTimes(user.freeTimes - 1)
            logger.info(f"user {uid} deduct freeTimes 1, remaining freeTimes {user.freeTimes}")

        elif payment == "balance":
            price = ModelPrice(actualModel)
            finalPrice = Decimal(0)
            if price.pricingStrategy == "TOKEN":
                finalPrice = (Decimal(promptTokens) / Decimal(1000000)) * Decimal(price.promptPrice) + \
                             Decimal(completionTokens) / Decimal(1000000) * Decimal(price.completionPrice)
            elif price.pricingStrategy == "REQUEST":
                finalPrice = Decimal(price.perRequestPrice)
            user.setBalance(str(Decimal(user.balance) - finalPrice))
            logger.info(f"user {uid} deduct balance ¥{finalPrice}, remaining balance ¥{user.balance}")
