![hsyr](https://github.com/user-attachments/assets/bbb2413e-7853-4821-9333-f795e890ef6a)
# HsYrChat💬
HsYrChat Bot is a Telegram bot that supports most AI model APIs (*OpenAI format*), allowing you to enjoy the convenience of AI anytime, anywhere! 🤖  

**[中文](https://github.com/GinHsYr/HsYrChatTelegram/blob/main/README.md)|English**  
![image](https://github.com/user-attachments/assets/066410c8-5afd-48d5-bed5-a298c4288b3f)
![image](https://github.com/user-attachments/assets/4be965fa-493b-4b28-bd98-4ca01366aa09)  

# Features😎
- [x] Streaming output  
- [x] Chain-of-thought format support
- [x] Contextual memory  
- [x] Image recognition support
- [x] Token and balance calculation
- [ ] More features coming soon...

# Deployment😉
```> pip3 install -r requirements.txt```
Edit the configTemplate.json file:
You can obtain your bot’s apiToken from @BotFather

```json
{
  "telegramConfig": {
    "apiToken": "<telegram_bot_token>",
    "botName": "your_bot_name_bot",
    "botNickname": "HsYrChat Bot",
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
      "systemPrompt": "You are an AI assistant proficient in Chinese and English conversations. You provide safe, helpful, and accurate answers. You will refuse to respond to any questions involving terrorism, racism, pornography, violence, etc."
    },
    "DeepSeek": {
      "apiBase": "https://api.example.com/v1/",
      "key": "xxx",
      "modelList": [
        "deepseek-chat"
      ],
      "enable": true,
      "systemPrompt": "You are an AI assistant proficient in Chinese and English conversations. You provide safe, helpful, and accurate answers. You will refuse to respond to any questions involving terrorism, racism, pornography, violence, etc."
    }
  }
}
```
***After editing, please rename the file to config.js, otherwise the configuration will not take effect***  
You can add any number of providers under aiConfig; the bot will automatically detect them (only when enable is set to true will the provider be activated).  
In main.py, you can choose between **polling mode and webHook mode.**  

---
Start the Bot:  
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
At this point, the bot is running normally, but it will not handle balance deduction yet, so you also need to configure the pricing for each model.
The program will create an SQLite database at bot/data/data.db, which you can edit using any database viewer.
Now the bot is fully configured. Have fun and enjoy!







