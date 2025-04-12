import time
from decimal import Decimal, InvalidOperation

import pandas as pd
import streamlit as st
from bot.core.handlers.giftCodeHandler import getAllGiftCodes, updateGiftCodes, addGiftCodes


def __validateGiftCodes(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    校验数据合法性。返回是否通过，以及错误信息列表。
    """
    errors = []

    for i, (_, row) in enumerate(df.iterrows()):
        code = row["code"]
        amount = row["amount"]
        is_used = row["isUsed"]

        if not code or str(code).strip() == "":
            errors.append(f"第 {i + 1} 行：兑换码 code 不能为空")

        try:
            Decimal(str(amount))
        except (InvalidOperation, TypeError):
            errors.append(f"第 {i + 1} 行：amount 必须是合法数字")

        if is_used not in (False, True):
            errors.append(f"第 {i + 1} 行：isUsed 必须是 True 或 False")

    return len(errors) == 0, errors

@st.fragment(run_every=1)
def main():
    st.title("兑换码管理")
    giftCodes = getAllGiftCodes()
    st.caption("在表格内编辑数据后点击'保存更改'即可修改数据")
    editedDf = st.data_editor(
        giftCodes,
        column_config={"code": st.column_config.TextColumn("兑换码"),
                       "amount": st.column_config.NumberColumn("金额", min_value=0),
                       "isUsed": st.column_config.CheckboxColumn("被使用")},
        use_container_width=True,
        key="giftEditor"
    )

    if st.button("添加"):
        @st.dialog("添加兑换码")
        def addGiftCodesDialog():
            st.caption("一行一个, 兑换码和金额用英文逗号分割\n例:abc,1.23")
            codes = st.text_area("兑换码:")
            if st.button("确定"):
                giftList = []
                for line in codes.strip().splitlines():
                    if not line.strip():
                        continue  # 跳过空行
                    try:
                        code, amount = line.strip().split(",")
                        giftList.append({"code": code.strip(), "amount": amount.strip()})
                    except ValueError:
                        st.error(f"格式错误，跳过：{line}")
                addGiftCodes(giftList)
                st.success("添加成功, 3s后窗口自动关闭")
                time.sleep(3)
                st.rerun()

        addGiftCodesDialog()
    if st.button("保存更改"):
        valid, validation_errors = __validateGiftCodes(editedDf)

        if valid:
            updateGiftCodes(editedDf)
            st.success("更新成功")
        else:
            st.error("❌ 数据验证失败，未进行更新：")
            for err in validation_errors:
                st.write(f"- {err}")


if __name__ == '__main__':
    main()
