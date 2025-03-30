import sqlite3
from math import ceil

import pandas as pd
import streamlit as st
from bot.utils.logger import logger


def initDB():
    conn = sqlite3.connect('bot/data/data.db')
    return conn


# 获取所有用户数据
def getAllUsers(conn):
    df = pd.read_sql('SELECT * FROM users', conn)
    return df


# 获取分页用户数据
def getPaginatedUsers(conn, page, perPage):
    offset = (page - 1) * perPage
    query = f'SELECT * FROM users LIMIT {perPage} OFFSET {offset}'
    df = pd.read_sql(query, conn)
    return df


# 获取用户总数
def getTotalUsers(conn):
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM users')
    return cur.fetchone()[0]


# 更新用户数据
def updateUser(conn, user_id, column, new_value):
    try:
        cur = conn.cursor()
        cur.execute(f"UPDATE users SET {column} = ? WHERE userId = ?", (new_value, user_id))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"更新失败: {e}")
        return False


# 主应用
def main():
    st.set_page_config(page_title="用户管理后台", layout="wide")
    st.title("用户管理后台")

    conn = initDB()

    # 分页设置
    if 'page' not in st.session_state:
        st.session_state.page = 1

    perPage = 10  # 每页显示的用户数
    totalUsers = getTotalUsers(conn)
    totalPages = ceil(totalUsers / perPage)

    # 分页导航
    col1, col2, col3, col4 = st.columns([1, 4, 1, 1])

    with col1:
        goto_page = st.number_input(
            f"第{st.session_state.page}/{totalPages}页\n(总计{totalUsers}用户)",
            min_value=1,
            max_value=totalPages,
            value=st.session_state.page,
            step=1,
            key="gotoPageInput",
        )
        if goto_page != st.session_state.page:
            st.session_state.page = goto_page
            st.rerun()

    # 获取当前页的用户数据
    usersDF = getPaginatedUsers(conn, st.session_state.page, perPage)

    # 显示用户表格
    st.dataframe(usersDF, use_container_width=True, selection_mode="single-row", on_select="ignore",
                 column_config={
                     'userId': '用户ID',
                     'registrationTime': '注册时间',
                     'freeTimes': '免费次数',
                     'userGroupLevel': '用户等级',
                     'bannedStatus': st.column_config.CheckboxColumn(
                         "封禁状态"
                     ),
                     'sharedCount': '邀请人数',
                     'isShared': st.column_config.CheckboxColumn(
                         "被邀请"
                     ),
                     'defaultChatModel': '默认模型',
                     'chatHistory': st.column_config.JsonColumn(
                         "聊天历史"
                     ),
                     'balance': st.column_config.NumberColumn(
                         "余额",
                         format="¥%s",
                         width="small"
                     )
                 })

    # 编辑功能
    st.subheader("编辑用户信息")
    col1, col2 = st.columns(2)

    with col1:
        userId = st.text_input("输入用户ID")

    if userId:
        try:
            userData = usersDF[usersDF['userId'] == userId].iloc[0]

            with col2:
                st.write("当前用户信息:")
                st.json(userData.to_dict(), expanded=False)

            # 编辑表单
            with st.form(key='edit_user_form'):
                st.write("编辑字段:")

                col1, col2 = st.columns(2)

                with col1:
                    newFreeTimes = st.number_input("免费次数", value=int(userData['freeTimes']))
                    newUserGroup = st.selectbox(
                        "用户组级别",
                        options=[1, 2, 3, 4, 5, 6],
                        index=int(userData['userGroupLevel']) - 1
                    )
                    newBannedStatus = st.toggle(
                        "封禁"
                    )

                with col2:
                    newSharedCount = st.number_input("邀请次数", value=int(userData['sharedCount']))
                    newIsShared = st.selectbox(
                        "已填写邀请码",
                        options=[("否", 0), ("是", 1)],
                        index=int(userData['isShared']),
                        format_func=lambda x: x[0]
                    )[1]
                    newBalance = str(st.number_input("余额", value=float(userData['balance']), step=1.0))
                    newChatModel = st.text_input("默认聊天模型", value=userData.get('defaultChatModel', ''))

                submitted = st.form_submit_button("提交更新")

                if submitted:
                    updates = {
                        'freeTimes': newFreeTimes,
                        'userGroupLevel': newUserGroup,
                        'bannedStatus': newBannedStatus,
                        'sharedCount': newSharedCount,
                        'isShared': newIsShared,
                        'balance': newBalance,
                        'defaultChatModel': newChatModel
                    }

                    success = True
                    for column, value in updates.items():
                        if not updateUser(conn, userId, column, value):
                            success = False
                            break

                    if success:
                        st.success("用户信息更新成功！")
        except Exception as e:
            logger.error(e)


if __name__ == "__main__":
    main()