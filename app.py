import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="大会参加登録", page_icon="🏆")
st.title("🏆 大会参加登録システム")

# スプレッドシートへの接続設定
conn = st.connection("gsheets", type=GSheetsConnection)

# 既存のデータを読み込む
existing_data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/edit#gid=0")

with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("氏名")
    student_id = st.text_input("学籍番号")
    dept = st.selectbox("学科", ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "その他"])
    submit = st.form_submit_button("登録を完了する")

if submit:
    if name and student_id:
        # 新しい行を作成
        new_row = pd.DataFrame([{"Timestamp": pd.Timestamp.now(), "氏名": name, "学籍番号": student_id, "学科": dept}])
        # データを追加して更新
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/edit#gid=0", data=updated_df)
        
        st.success(f"登録完了！スプレッドシートを確認してください。")
        st.balloons()
    else:
        st.error("氏名と学籍番号を入力してください。")

st.divider()
st.subheader("📊 現在の登録リスト")
st.dataframe(existing_data)