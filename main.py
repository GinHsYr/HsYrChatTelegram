import configparser
import os
import sqlite3
import threading

import flask
import telebot
from bot.core.handlers import setupHandlers
from bot.utils.logger import logger
from bot.utils.vars import configs, bot

LOGO = r'''
 __  __           __    __      ____     __                __      
/\ \/\ \         /\ \  /\ \    /\  _`\  /\ \              /\ \__   
\ \ \_\ \    ____\ `\`\\/'/_ __\ \ \/\_\\ \ \___      __  \ \ ,_\  
 \ \  _  \  /',__\`\ `\ /'/\`'__\ \ \/_/_\ \  _ `\  /'__`\ \ \ \/  
  \ \ \ \ \/\__, `\ `\ \ \\ \ \/ \ \ \L\ \\ \ \ \ \/\ \L\.\_\ \ \_ 
   \ \_\ \_\/\____/   \ \_\\ \_\  \ \____/ \ \_\ \_\ \__/.\_\\ \__\
    \/_/\/_/\/___/     \/_/ \/_/   \/___/   \/_/\/_/\/__/\/_/ \/__/
'''
print(LOGO)
print("version 0.2.1")

config = configparser.ConfigParser()
config.read("admin.ini")
if not config.has_section("Admin"):
    config.add_section("Admin")
    config.set("Admin", "account", "admin")
    config.set("Admin", "password", "98304d615e857296f6d556386997baab")
    config.write(open("admin.ini", "w"))

if not os.path.exists("bot/data"):  # 判断是否存在文件夹如果不存在则创建为文件夹
    os.makedirs("bot/data")
conn = sqlite3.connect("bot/data/data.db")
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    userId TEXT,
    registrationTime TEXT NOT NULL,
    freeTimes INTEGER,
    userGroupLevel INTEGER DEFAULT 3,
    bannedStatus INTEGER DEFAULT 0 CHECK(bannedStatus IN (0,1)),
    sharedCount INTEGER DEFAULT 0,
    isShared INTEGER DEFAULT 0 CHECK(isShared IN (0,1)),
    defaultChatModel TEXT,
    chatHistory TEXT,
    balance TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS modelPricing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    modelName TEXT NOT NULL UNIQUE,
    pricingStrategy TEXT NOT NULL CHECK(pricingStrategy IN ('TOKEN', 'REQUEST')),
    
    -- 按 token 计费模式
    promptPrice TEXT,
    completionPrice TEXT,
    
    -- 按请求计费模式
    perRequestPrice TEXT,
    
    unitScale INTEGER DEFAULT 'M' CHECK(modelPricing.unitScale IN ('M','k')),-- 单位缩放(M百万 k千)
    isActive INTEGER DEFAULT 1 CHECK(isActive IN (0,1)),
    updatedAt TEXT DEFAULT (datetime('now','localtime'))
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS giftCodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL UNIQUE,
    amount TEXT NOT NULL,
    isUsed INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()
app = flask.Flask(__name__)

# You can use the proxy by enabling the following line of code
# apihelper.proxy = {'https': configs.proxyHttps, "http": configs.proxyHttp}


@app.route(configs.wUrlPath, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


def run():
    os.system("streamlit run web/app.py")


if __name__ == '__main__':
    # Remove webhook, it fails sometimes the set if there is a previous webhook
    bot.remove_webhook()
    setupHandlers(bot)

    flaskThread = threading.Thread(target=run)
    flaskThread.start()
    logger.info("Bot is starting...")
    try:
        # You can use the following code to enable polling mode, which can be easily tested.
        bot.infinity_polling(timeout=30)
        # bot.set_webhook(url=f"https://{configs.wHost}:{configs.wPort}{configs.wUrlPath}",
        # certificate=open(configs.wSslCert, 'r'))
        # app.run(host=configs.wListen,
        #         port=configs.wPort,
        #         ssl_context=(configs.wSslCert, configs.wSslPRIV),
        #         debug=True)

        # Quick'n'dirty SSL certificate generation:
        #
        # openssl genrsa -out webhook_pkey.pem 2048
        # openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
        #
        # When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
        # with the same value in you put in WEBHOOK_HOST
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Bot has stopped.")
