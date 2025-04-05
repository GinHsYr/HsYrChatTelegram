import sqlite3
from decimal import Decimal

import streamlit as st
from bot.utils.modelPrice import getAllModelPrices, delModel, updateModelPricing, ModelPrice


def main():
    st.title("📊 AI模型信息")
    models = getAllModelPrices()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("总模型数量", len(models), border=True)
    with col2:
        st.metric("活跃模型数量", sum(1 for m in models if m["isActive"]), border=True)
    st.divider()

    if not models:
        st.warning("没有找到模型价格数据")
        return

    col1, col2 = st.columns(2)
    with col1:
        showActiveOnly = st.checkbox("仅显示激活模型", value=True)
    with col2:
        searchTerm = st.text_input("搜索模型名称")

    # 筛选数据
    filteredModels = models
    if showActiveOnly:
        filteredModels = [m for m in filteredModels if m["isActive"]]
    if searchTerm:
        filteredModels = [m for m in filteredModels if searchTerm.lower() in m["model"].lower()]

    if not filteredModels:
        st.warning("没有符合筛选条件的模型")
        return

    # 显示数据
    for model in filteredModels:
        with st.expander(f"🔹 {model['model']} {'✅' if model['isActive'] else '❌'}", expanded=False):
            cols = st.columns(4)

            # 模型基本信息
            with cols[0]:
                st.markdown("**基本信息**")
                st.write(f"计价策略: {model['strategy']}")

            # 价格信息
            with cols[1]:
                st.markdown("**价格信息**")
                if model["strategy"] == "TOKEN":
                    st.write(f"输入价格: ¥{model['promptPrice']}/1{model['unitScale']}")
                    st.write(f"补全价格: ¥{model['completionPrice']}/1{model['unitScale']}")
                else:
                    st.write(f"每请求: ¥{model['perRequestPrice']}")

            # 更新时间
            with cols[2]:
                st.markdown("**更新时间**")
                st.write(model["updateTime"])

            # 状态指示器
            with cols[3]:
                st.markdown("**状态**")
                if model["isActive"]:
                    st.badge("模型已激活", icon=":material/check:", color="green")
                else:
                    st.badge("模型未激活", color="gray")
                if st.button("编辑", key=model["model"]):
                    @st.dialog("编辑模型信息")
                    def dialog(modelName):
                        modelP = ModelPrice(modelName).toDict()
                        newModelName = st.text_input("模型名称", modelName)
                        promptPrice, completionPrice, perReqPrice, unitScale = "0.0", "0.0", "0.0", "M"

                        strategy = st.selectbox("计价策略", ("按Token计费", "按请求次数计费"),
                                                index=0 if modelP["strategy"] == "TOKEN" else 1)
                        if strategy == "按Token计费":
                            unitScale = st.selectbox("单位", ("每百万Token", "每千Token"),
                                                     index=0 if modelP["unitScale"] == 'M' else 1)
                            promptPrice = st.text_input(f"输入价格/{unitScale}", value=(modelP["promptPrice"]))
                            completionPrice = st.text_input(f"输出价格/{unitScale}", value=(modelP["completionPrice"]))
                            try:
                                Decimal(promptPrice)
                                Decimal(completionPrice)
                            except:
                                st.error("请输入有效的数字")
                                return
                        else:
                            perReqPrice = st.text_input("单次请求价格", value=(modelP["perRequestPrice"]))
                            try:
                                Decimal(perReqPrice)
                            except:
                                st.error("请输入有效的数字")
                                return
                        active = st.toggle("激活", value=modelP["isActive"],
                                           help="激活后才会使用该模型定价, 不激活则无法进行扣费")
                        strategy = "TOKEN" if strategy == "按Token计费" else "REQUEST"
                        unitScale = "M" if unitScale == "每百万Token" else "k"
                        active = 1 if active else 0

                        deleteButton, submitButton = st.columns(2, gap="small")
                        with deleteButton:
                            if st.button("删除模型", type="primary"):
                                delModel(modelName)
                                st.rerun()
                        with submitButton:
                            if st.button("提交"):
                                updateModelPricing(sqlite3.connect("bot/data/data.db"), newModelName, strategy,
                                                   str(promptPrice), str(completionPrice),
                                                   str(perReqPrice), unitScale, active)
                                st.success("修改成功!")
                                st.rerun(scope="app")

                    dialog(model["model"])


if __name__ == "__main__":
    main()
