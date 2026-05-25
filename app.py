import streamlit as st
import pandas as pd

# --- 設定 ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/edit?usp=sharing"
CSV_URL = SHEET_URL.split("/edit")[0] + "/export?format=csv"

st.set_page_config(page_title="大会参加登録システム", page_icon="🏆")
st.title("🏆 大会参加登録システム")

# --- 入力フォーム ---
with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("氏名")
    student_id = st.text_input("学籍番号")
    dept = st.selectbox("学科", ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "その他"])
    
    # ここを修正しました！
    submit = st.form_submit_button("登録を完了する")

if submit:
    if name and student_id:
        st.success(f"【送信完了】{name}さん、登録を受け付けました！")
        st.balloons()
    else:
        st.error("エラー: 氏名と学籍番号を両方入力してください。")

st.divider()
st.subheader("📊 現在の登録状況")

try:
    df = pd.read_csv(CSV_URL)
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.warning("スプレッドシートの読み込み待機中、または共有設定を確認してください。")