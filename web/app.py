import configparser
import hashlib

import stLocalStorage
import streamlit as st
from bot.utils.logger import logger
st.set_page_config(page_title="HsYrBot管理后台", layout="wide")

controller = stLocalStorage.StLocalStorage()
config = configparser.ConfigParser()
config.read("admin.ini")

def checkLogin():
    account = config.get("Admin", "account")
    password = config.get("Admin", "password")
    cookie = controller.get('login')
    if cookie == password:
        pages = {
            "仪表盘": [
                st.Page("pages/dashboard/overview.py", title="总览")
            ],
            "管理": [
                st.Page("pages/manage/userManager.py", title="用户管理"),
                st.Page("pages/manage/modelManager.py", title="模型管理"),
                st.Page("pages/manage/giftCodesManager.py", title="兑换码管理")
            ]
        }
        pg = st.navigation(pages)
        pg.run()
    else:
        st.title("登录")
        accountInput = st.text_input("账号")
        passwordInput = st.text_input("密码", type="password")
        if st.button("登录"):
            md5 = hashlib.md5()
            md5.update(passwordInput.encode("UTF-8"))
            passwordInputHash = md5.hexdigest()
            if accountInput == account and passwordInputHash == password:
                controller.set('login', password)
                logger.warning("管理后台已登录")
            else:
                st.error("账号或密码错误")


checkLogin()