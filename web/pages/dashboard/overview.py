import configparser
import hashlib
import sqlite3
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st
from bot.utils.logger import logger
from bot.utils.users import getAllUsers
from web.stLocalStorage import StLocalStorage


def getCumulativeUserData(userData):
    userData['registrationTime'] = pd.to_datetime(userData['registrationTime'].astype(int), unit='s')
    userData['date'] = userData['registrationTime'].dt.date
    userData = userData.sort_values(by='date')

    dailyNew = userData.groupby('date').size().reset_index(name='新增用户数')
    # 累计总数
    dailyNew['累计用户数'] = dailyNew['新增用户数'].cumsum()
    return dailyNew

@st.fragment(run_every=10)
def metricData():
    col1, col2, col3 = st.columns(3)
    userData = getAllUsers(sqlite3.connect("bot/data/data.db"))

    userIncrease = 0
    for regTime in userData["registrationTime"]:
        midnight = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = midnight - timedelta(days=1)

        # 转换为时间戳
        timestamp, timestampY = int(midnight.timestamp()), int(yesterday.timestamp())
        if timestampY <= int(regTime) < timestamp:
            userIncrease += 1
    col1.metric("总用户数", len(userData), f"+{userIncrease}", border=True, help="用户增加数为昨日新增")

    cumulativeData = getCumulativeUserData(userData)
    col1.line_chart(cumulativeData.set_index('date')[['累计用户数']])


def sidebar():
    if st.sidebar.button("修改密码"):
        config = configparser.ConfigParser()
        config.read("admin.ini")

        @st.dialog("修改密码")
        def dialog():
            st.caption("推荐使用高强度,易记忆的密码")
            originalPassword = st.text_input("原密码", type="password")
            newPassword = st.text_input("新密码", type="password")
            if st.button("确定"):
                md5 = hashlib.md5()
                md5.update(originalPassword.encode("UTF-8"))
                if md5.hexdigest() == config.get("Admin", "password"):
                    md5N = hashlib.md5()
                    md5N.update(newPassword.encode("UTF-8"))
                    config.set("Admin", "password", md5N.hexdigest())
                    config.write(open("admin.ini", "w"))
                    logger.warning(f"密码已修改")
                    st.rerun()
                else:
                    st.error("原密码不正确")
                    return

        dialog()
    if st.sidebar.button("退出登录"):
        stLS = StLocalStorage()
        stLS.set("login", None)
        logger.warning("登录已退出")
        st.rerun('app')

if __name__ == '__main__':
    st.title("数据总览")
    sidebar()
    metricData()
