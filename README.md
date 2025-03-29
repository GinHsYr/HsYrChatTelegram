![HsYr](https://github.com/user-attachments/assets/fd6286d3-755b-4e27-963a-a0d10b3c3c7c)

# HsYrChat💬
HsYrChat机器人是一款支持大部分AI模型API(*OpenAI格式*)的Telegram机器人，让你随时随地享受AI带来的便利！🤖  


**中文|[English](https://github.com/GinHsYr/HsYrChatTelegram/blob/main/README_EN.md)**  
![image](https://github.com/user-attachments/assets/8d95c927-14d5-4278-b1c9-538413cb129c)
![image](https://github.com/user-attachments/assets/ab1bfbb4-0d56-4f4b-b0c2-1e0fc482039a)


# Features😎
 - [x] 流式传输  
 - [x] 思维链模型格式支持  
 - [x] 上下文支持  
 - [x] 图片识别支持  
 - [x] Token与余额的计算  
 - [ ] 敬请期待

# 部署😉
```
> pip3 install -r requirements.txt
```
编辑```configTemplate.json```文件:  
机器人的apiToken可以在@BotFather处取得
```json
{
  "telegramConfig": {
    "apiToken": "<telegram_bot_token>",
    "botName": "your_bot_name_bot",
    "botNickname": "HsYrChat机器人",
    "proxy": {
      "http": "http://127.0.0.1:7890",
      "https": "https://127.0.0.1:7890"
    },
    "webHook": {
      "host": "<ip where the bot is running>",
      "listen": "0.0.0.0",
      "port": 8773,
      "sslCert": "./webhook_cert.pem",
      "sslPRIV": "./webhook_pkey.pem"
    }
  },
  "logging": {
    "fileName": "./logs.log"
  },
  "users": {
    "defaultFreeTimes": 5,
    "defaultBalance": 0
  },
  "aiConfig": {
    "OpenAi": {
      "apiBase": "https://api.example.com/v1/",
      "key": "sk-xxxx",
      "modelList": [
        "gpt-3.5-turbo",
        "gpt-4"
      ],
      "enable": true,
      "systemPrompt": "你是一个人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答"
    },
    "DeepSeek": {
      "apiBase": "https://api.example.com/v1/",
      "key": "xxx",
      "modelList": [
        "deepseek-chat"
      ],
      "enable": true,
      "systemPrompt": "你是一个人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答"
    }
  }
}
```
***编辑完毕后请重命名为config.js, 否则配置不会生效***  
aiConfig中的提供商可以随意增添, 机器人会自动识别(*当且仅当```enable```参数为true时, 该提供商才会被启用*)  
在main.py文件中你可以选择**轮询与webHook两种模式**  

---
启动Bot:
```
> python main.py
 __  __           __    __      ____     __                __      
/\ \/\ \         /\ \  /\ \    /\  _`\  /\ \              /\ \__   
\ \ \_\ \    ____\ `\`\\/'/_ __\ \ \/\_\\ \ \___      __  \ \ ,_\  
 \ \  _  \  /',__\`\ `\ /'/\`'__\ \ \/_/_\ \  _ `\  /'__`\ \ \ \/  
  \ \ \ \ \/\__, `\ `\ \ \\ \ \/ \ \ \L\ \\ \ \ \ \/\ \L\.\_\ \ \_ 
   \ \_\ \_\/\____/   \ \_\\ \_\  \ \____/ \ \_\ \_\ \__/.\_\\ \__\
    \/_/\/_/\/___/     \/_/ \/_/   \/___/   \/_/\/_/\/__/\/_/ \/__/

version 0.1.0
2025-03-22 19:34:22,972 - bot.utils.logger - INFO - Bot is starting...
```

此时, Bot可以正常工作, **但无法进行扣费行为**, 所以我们还需配置模型的价格  
程序将在```bot/data/data.db```创建sqlite数据库, 您可以用数据库浏览软件对其进行编辑
至此, 机器人配置完成, 请愉快的玩耍吧!
