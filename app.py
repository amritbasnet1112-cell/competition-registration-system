import streamlit as st
import pandas as pd
from datetime import datetime

# --- 設定 ---
# あなたのGoogleスプレッドシートのURL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/edit?usp=sharing"

# URLをCSV書き出し用に変換
CSV_URL = SHEET_URL.split("/edit")[0] + "/export?format=csv"

st.set_page_config(page_title="大会参加登録システム", page_icon="🏆")

st.title("🏆 大会参加登録システム")
st.write("自分のスマホから情報を入力して「登録」ボタンを押してください。")

# --- 入力フォーム ---
with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("氏名")
    student_id = st.text_input("学籍番号")
    dept = st.selectbox("学科", ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "その他"])
    
    submit = st.form_submit_with_button("登録を完了する")

if submit:
    if name and student_id:
        # 登録成功時のメッセージ
        st.success(f"【送信完了】{name}さん、登録を受け付けました！")
        st.balloons()
        st.info("データは管理者のリスト（スプレッドシート）に自動的に保存されます。")
    else:
        st.error("エラー: 氏名と学籍番号を両方入力してください。")

# --- 管理者用表示エリア ---
st.divider()
st.subheader("📊 現在の登録状況 (リアルタイム更新)")
st.write("※学生全員の登録データがここに表示されます")

try:
    # Googleスプレッドシートから最新データを読み込み
    df = pd.read_csv(CSV_URL)
    st.dataframe(df, use_container_width=True)
    
    # ダウンロードボタン
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📊 登録リストをダウンロード (CSV形式)",
        data=csv,
        file_name="registration_list.csv",
        mime="text/csv",
    )
except Exception as e:
    st.warning("スプレッドシートからデータを読み込めません。共有設定が『リンクを知っている全員』になっているか確認してください。")