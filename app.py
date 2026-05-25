import streamlit as st
import requests
import pandas as pd

# --- 【最新のURLをセットしました】 ---
GAS_URL = "https://script.google.com/macros/s/AKfycbz31n0HmIE70dujb-hAWos0dBuX-RLvnQU8ynO-9q5ucwlleC-FaG6NB96_OdFD2eIh/exec"
# スプレッドシートのCSV出力URL
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/export?format=csv"

st.set_page_config(page_title="大会登録 & リアルタイムリスト", page_icon="🏆", layout="wide")

st.title("🏆 大会参加登録システム")

# 画面を2分割（左：入力、右：リスト）
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 参加登録")
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("氏名")
        student_id = st.text_input("学籍番号")
        dept = st.selectbox("学科", ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "ITビジネス科", "その他"])
        submit = st.form_submit_button("登録を完了する")

    if submit:
        if name and student_id:
            try:
                # GASへデータ送信
                payload = {"name": name, "student_id": student_id, "dept": dept}
                # Streamlitの仕様上、リダイレクトが発生するためallow_redirects=True(デフォルト)で送信
                response = requests.post(GAS_URL, json=payload, timeout=10)
                
                # GAS側が正しく受け取れば success メッセージが出る
                st.success(f"登録完了！リストを確認してください。")
                st.balloons()
                # 画面をリロードしてリストを更新
                st.rerun()
            except Exception as e:
                st.error(f"接続エラーが発生しました。インターネット環境を確認してください。")
        else:
            st.warning("名前と学籍番号を入力してください。")

with col2:
    st.subheader("📊 リアルタイム待機リスト")
    try:
        # キャッシュを回避するためにタイムスタンプを付与して読み込み
        df = pd.read_csv(f"{SHEET_CSV_URL}&cache={pd.Timestamp.now().timestamp()}")
        
        if not df.empty:
            # 最新の登録者を一番上に表示
            st.dataframe(df.iloc[::-1], use_container_width=True, height=500)
            st.caption(f"最終更新: {pd.Timestamp.now().strftime('%H:%M:%S')}")
        else:
            st.info("現在、登録者はいません。")
    except:
        st.warning("リストを読み込み中...（スプレッドシートの共有設定が『リンクを知っている全員』になっているか確認してください）")

st.divider()
if st.button("🔄 リストを手動で更新する"):
    st.rerun()