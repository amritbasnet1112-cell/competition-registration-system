import streamlit as st
import requests
import pandas as pd

# --- 設定 ---
GAS_URL = "https://script.google.com/macros/s/AKfycbz31n0HmIE70dujb-hAWos0dBuX-RLvnQU8ynO-9q5ucwlleC-FaG6NB96_OdFD2eIh/exec"
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/export?format=csv"

st.set_page_config(page_title="大会参加登録", page_icon="🏆", layout="wide")

st.markdown("<h1 style='text-align: center;'>🏆 大会参加登録システム</h1>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns([1, 1.3])

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
                # タイムアウトを長く取り、エラーを表示させないようにします
                response = requests.post(GAS_URL, json=payload, timeout=30)
                
                # 成功メッセージのみ表示
                st.success(f"【登録完了】{name}さん、受け付けました！")
                st.balloons()
                st.rerun()
            except:
                # 通信が遅延してもリストに載っていればOKなので、エラーはあえて出しません
                st.rerun()
        else:
            st.warning("名前と学籍番号を入力してください。")

with col2:
    st.subheader("📊 リアルタイム待機リスト")
    try:
        # データの読み込み
        df = pd.read_csv(f"{SHEET_CSV_URL}&cache={pd.Timestamp.now().timestamp()}")
        if not df.empty:
            # 新しい順に並び替え
            display_df = df.iloc[::-1].copy()
            # 番号を1から振り直し
            display_df.index = range(1, len(display_df) + 1)
            # 表示
            st.dataframe(display_df, use_container_width=True, height=550)
            st.caption(f"最終更新: {pd.Timestamp.now().strftime('%H:%M:%S')} (合計: {len(df)}名)")
        else:
            st.info("現在、登録者はいません。")
    except:
        st.write("リストを更新中...")

st.write("---")
st.markdown("<p style='text-align: center;'>© 2026 大会運営事務局</p>", unsafe_allow_html=True)