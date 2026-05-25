import streamlit as st
import requests
import pandas as pd

# --- 設定 ---
GAS_URL = "https://script.google.com/macros/s/AKfycbyIF6H_WgtLgacMfL4-xAw_lSzo-qRADwSFW1Y2j7naNHuCZHx-rTXDsLIZGgcUxSH/exec"
# スプレッドシートのCSV出力用URL（閲覧用）
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/export?format=csv"

st.set_page_config(page_title="大会参加登録 & 待機リスト", page_icon="🏆", layout="wide")

st.title("🏆 大会参加登録システム")

# 2カラム構成にする（左に入力フォーム、右にリアルタイムリスト）
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 登録フォーム")
    with st.form("registration_form", clear_on_submit=True):
        name = st.text_input("氏名")
        student_id = st.text_input("学籍番号")
        dept = st.selectbox("学科", ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "ITビジネス科", "その他"])
        submit = st.form_submit_button("登録を完了する")

    if submit:
        if name and student_id:
            try:
                payload = {"name": name, "student_id": student_id, "dept": dept}
                response = requests.post(GAS_URL, json=payload, timeout=10)
                if response.status_code == 200:
                    st.success(f"登録完了！")
                    st.balloons()
                    # 登録直後にデータを再読み込みさせるためにリロード
                    st.rerun()
                else:
                    st.error("送信エラーが発生しました。")
            except:
                st.error("接続エラー。URLを確認してください。")
        else:
            st.warning("入力漏れがあります。")

with col2:
    st.subheader("📊 現在の待機リスト (Live)")
    try:
        # スプレッドシートから最新データを読み込み
        # キャッシュを無効化するためにランダムなパラメータを付与
        df = pd.read_csv(f"{SHEET_CSV_URL}&cache={pd.Timestamp.now().timestamp()}")
        
        if not df.empty:
            # 見やすくするために順番を整理（新しい順に表示）
            st.dataframe(df.iloc[::-1], use_container_width=True, height=400)
            st.caption(f"最終更新: {pd.Timestamp.now().strftime('%H:%M:%S')}")
        else:
            st.info("現在、登録者はいません。")
    except:
        st.warning("リストを読み込み中、またはスプレッドシートの共有設定を確認してください。")

st.divider()
st.center = st.button("🔄 リストを手動更新する")