import streamlit as st
import requests

# --- 【最重要】ここに設定してください ---
# 前の手順で取得した「https://script.google.com/macros/s/.../exec」というURLを貼ってください
GAS_URL = "ここにウェブアプリURLを貼り付けてください"

# スプレッドシートの閲覧用URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1WDQBfQ8x9okAFJqcw66UR5ctqXmfF95l67WlnoD1eS8/edit?usp=sharing"
# ---------------------------------------

st.set_page_config(page_title="大会参加登録", page_icon="🏆")
st.title("🏆 大会参加登録システム")

# 入力フォーム
with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("氏名（例：日本 太郎）")
    student_id = st.text_input("学籍番号（例：G026C1153）")
    dept = st.selectbox("学科", ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "その他"])
    submit = st.form_submit_button("登録を完了する")

if submit:
    if name and student_id:
        if "ここに" in GAS_URL:
            st.error("設定エラー：GASのURLが貼り付けられていません。")
        else:
            try:
                # データをGASへ送信
                payload = {
                    "name": name,
                    "student_id": student_id,
                    "dept": dept
                }
                # タイムアウトを設定して送信
                response = requests.post(GAS_URL, json=payload, timeout=10)
                
                if response.status_code == 200:
                    st.success(f"【登録完了】{name}さん、データを保存しました！")
                    st.balloons()
                else:
                    st.error(f"送信に失敗しました（エラーコード: {response.status_code}）")
            except Exception as e:
                st.error("エラーが発生しました。GASのURLが正しいか、または公開設定が『全員(Anyone)』になっているか確認してください。")
    else:
        st.warning("氏名と学籍番号を入力してください。")

st.divider()
st.subheader("🔗 登録状況の確認")
st.write(f"登録されたデータは以下のスプレッドシートで確認できます：")
st.link_button("スプレッドシートを開く", SHEET_URL)