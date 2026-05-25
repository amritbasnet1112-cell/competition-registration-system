import streamlit as st
import pandas as pd
import requests

# --- 設定 ---
# 1. さっきコピーした「ウェブアプリURL」をここに貼る
GAS_URL = "ここにウェブアプリURLを貼り付けてください"
# 2. スプレッドシートのURL（読み込み用）
SHEET_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/edit?usp=sharing"
CSV_URL = SHEET_URL.split("/edit")[0] + "/export?format=csv"

st.title("🏆 大会参加登録フォーム")

with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("氏名")
    student_id = st.text_input("学籍番号")
    dept = st.selectbox("学科", ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "その他"])
    submit = st.form_submit_button("登録を完了する")

if submit:
    if name and student_id:
        # GASにデータを送信
        payload = {"name": name, "student_id": student_id, "dept": dept}
        response = requests.post(GAS_URL, json=payload)
        
        if response.status_code == 200:
            st.success(f"【送信完了】{name}さん、スプレッドシートに保存しました！")
            st.balloons()
        else:
            st.error("保存に失敗しました。GASの設定を確認してください。")

st.divider()
st.subheader("📊 現在の登録状況")
try:
    df = pd.read_csv(CSV_URL)
    st.dataframe(df, use_container_width=True)
except:
    st.info("データがまだありません。")