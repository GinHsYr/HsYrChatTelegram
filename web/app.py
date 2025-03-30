import streamlit as st

pages = {
    "仪表盘": [
        st.Page("pages/dashboard/overview.py", title="总览")
    ],
    "管理": [
        st.Page("pages/manage/userManager.py", title="用户管理")
    ]
}
pg = st.navigation(pages)
pg.run()
