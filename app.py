import streamlit as st
import requests
import pandas as pd

# --- 設定：あなたのGASとスプレッドシートのURL ---
GAS_URL = "https://script.google.com/macros/s/AKfycbz31n0HmIE70dujb-hAWos0dBuX-RLvnQU8ynO-9q5ucwlleC-FaG6NB96_OdFD2eIh/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/export?format=csv"

# ページ設定
st.set_page_config(page_title="大会参加登録システム", page_icon="🏆", layout="wide")

# タイトル
st.markdown("<h1 style='text-align: center;'>🏆 大会参加登録システム</h1>", unsafe_allow_html=True)
st.write("---")

# 画面を分割（左：入力フォーム、右：リスト表示）
col1, col2 = st.columns([1, 1.3])

# --- 左側：登録フォーム ---
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
                # データをGASへ送信
                payload = {"name": name, "student_id": student_id, "dept": dept}
                # タイムアウトを30秒に設定し、Google側の処理待ちによるエラーを防止
                response = requests.post(GAS_URL, json=payload, timeout=30)
                
                if response.status_code == 200:
                    st.success(f"【成功】{name}さんの登録が完了しました！")
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("登録は受け付けられましたが、反映に時間がかかっています。右のリストを確認してください。")
            except:
                # 通信がタイムアウトしても実際には登録されていることが多いため、リロードを促す
                st.info("登録処理を行いました。最新の状況は右側のリストで確認してください。")
        else:
            st.warning("名前と学籍番号を入力してください。")

# --- 右側：リアルタイム待機リスト ---
with col2:
    st.subheader("📊 リアルタイム待機リスト")
    try:
        # スプレッドシートからデータを読み込み（キャッシュを回避）
        df = pd.read_csv(f"{SHEET_CSV_URL}&cache={pd.Timestamp.now().timestamp()}")
        
        if not df.empty:
            # 1. データを逆順（新しい順）にする
            display_df = df.iloc[::-1].copy()
            # 2. 番号（左端）を上から 1, 2, 3... と正しく振り直す
            display_df.index = range(1, len(display_df) + 1)
            
            # 3. リストを表示
            st.dataframe(display_df, use_container_width=True, height=550)
            st.caption(f"最終更新: {pd.Timestamp.now().strftime('%H:%M:%S')} (合計: {len(df)}名)")
        else:
            st.info("現在、登録者はいません。")
    except:
        st.warning("リストを読み込み中...スプレッドシートの共有設定を確認してください。")

# フッター
st.write("---")
st.markdown("<p style='text-align: center;'>© 2026 大会運営事務局</p>", unsafe_allow_html=True)