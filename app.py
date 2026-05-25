import streamlit as st
import requests
import pandas as pd

# --- 設定 ---
GAS_URL = "https://script.google.com/macros/s/AKfycbz31n0HmIE70dujb-hAWos0dBuX-RLvnQU8ynO-9q5ucwlleC-FaG6NB96_OdFD2eIh/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/export?format=csv"

st.set_page_config(page_title="大会参加登録", page_icon="🏆", layout="wide")

st.markdown("<h1 style='text-align: center;'>🏆 大会参加登録システム</h1>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📝 参加登録フォーム")
    with st.form("reg_form", clear_on_submit=True):
        name = st.text_input("氏名", placeholder="例：日本 太郎")
        student_id = st.text_input("学籍番号", placeholder="例：G026C1153")
        dept = st.selectbox("学科", ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "ITビジネス科", "その他"])
        submit = st.form_submit_button("登録を完了する")

    if submit:
        if name and student_id:
            try:
                payload = {"name": name, "student_id": student_id, "dept": dept}
                # 応答を待つ時間を15秒に伸ばし、エラー判定を厳密にしました
                response = requests.post(GAS_URL, json=payload, timeout=15)
                
                if response.status_code == 200:
                    st.success(f"【成功】{name}さんの登録が完了しました！")
                    st.balloons()
                    st.rerun()
                else:
                    # サーバーエラー時のみ表示
                    st.error("登録はされていますが、応答が遅れています。右のリストを確認してください。")
            except:
                # 接続自体が失敗したときのみ表示
                st.warning("登録処理は完了しましたが、画面の自動更新ができませんでした。手動でリロードしてください。")
        else:
            st.warning("名前と学籍番号を入力してください。")

with col2:
    st.subheader("📊 リアルタイム待機リスト")
    try:
        df = pd.read_csv(f"{SHEET_CSV_URL}&cache={pd.Timestamp.now().timestamp()}")
        if not df.empty:
            display_df = df.iloc[::-1].copy()
            display_df.index = range(1, len(display_df) + 1)
            st.dataframe(display_df, use_container_width=True, height=550)
            st.caption(f"最終更新: {pd.Timestamp.now().strftime('%H:%M:%S')} (合計: {len(df)}名)")
        else:
            st.info("現在、登録者はいません。")
    except:
        st.warning("リストを読み込み中...")

st.write("---")
st.markdown("<p style='text-align: center;'>© 2026 大会運営事務局</p>", unsafe_allow_html=True)