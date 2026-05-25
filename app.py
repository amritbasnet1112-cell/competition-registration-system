import streamlit as st
import requests
import pandas as pd

# --- 設定 ---
GAS_URL = "https://script.google.com/macros/s/AKfycbz31n0HmIE70dujb-hAWos0dBuX-RLvnQU8ynO-9q5ucwlleC-FaG6NB96_OdFD2eIh/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/export?format=csv"

st.set_page_config(page_title="大会参加登録システム", page_icon="🏆", layout="wide")

st.title("🏆 大会参加登録システム")

# 2カラムレイアウト
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 参加登録")
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("氏名", placeholder="例：日本 太郎")
        student_id = st.text_input("学籍番号", placeholder="例：G026C1153")
        dept = st.selectbox("学科", ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "ITビジネス科", "その他"])
        submit = st.form_submit_button("登録を完了する")

    if submit:
        if name and student_id:
            try:
                payload = {"name": name, "student_id": student_id, "dept": dept}
                response = requests.post(GAS_URL, json=payload, timeout=10)
                st.success(f"登録完了！リストを確認してください。")
                st.balloons()
                st.rerun()
            except:
                st.error("送信エラーが発生しました。インターネット接続を確認してください。")
        else:
            st.warning("必須項目を入力してください。")

with col2:
    st.subheader("📊 リアルタイム待機リスト")
    try:
        # データの読み込み
        df = pd.read_csv(f"{SHEET_CSV_URL}&cache={pd.Timestamp.now().timestamp()}")
        
        if not df.empty:
            # 1. データを逆順（新しい順）にする
            display_df = df.iloc[::-1].copy()
            # 2. 番号（インデックス）を上から 1, 2, 3... と振り直す
            display_df.index = range(1, len(display_df) + 1)
            
            # 表の表示
            st.dataframe(display_df, use_container_width=True, height=500)
            st.caption(f"最終更新: {pd.Timestamp.now().strftime('%H:%M:%S')} (登録数: {len(df)}名)")
        else:
            st.info("現在、登録者はいません。")
    except:
        st.warning("リストを読み込み中...スプレッドシートの共有設定を確認してください。")

st.divider()
if st.button("🔄 リストを最新の状態に更新"):
    st.rerun()