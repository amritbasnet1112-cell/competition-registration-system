import streamlit as st
import requests

# --- 設定：あなたのGASウェブアプリURL ---
GAS_URL = "https://script.google.com/macros/s/AKfycbylF6H_WgtLgacMfL4-xAw_lSzo-qRADwSFW1Y2j7naNHuCZHx-rTXDsLIZGgcUxSH/exec"

# ページの設定（ブラウザのタブに表示される名前とアイコン）
st.set_page_config(page_title="大会参加登録システム", page_icon="🏆", layout="centered")

# タイトルと説明
st.title("🏆 大会参加登録システム")
st.write("必要事項を入力して「登録を完了する」ボタンを押してください。")

# 入力フォームの作成
with st.form("registration_form", clear_on_submit=True):
    name = st.text_input("氏名", placeholder="例：日本 太郎")
    student_id = st.text_input("学籍番号", placeholder="例：G026C1153")
    
    # 学科の選択肢（必要に応じて増やしてください）
    dept = st.selectbox(
        "学科を選択してください", 
        ["情報処理科", "情報システム科", "高度情報処理科", "Webデザイン科", "ITビジネス科", "その他"]
    )
    
    # 送信ボタン
    submit = st.form_submit_button("登録を完了する")

# ボタンが押された時の処理
if submit:
    # 入力チェック：名前と学籍番号が空でないか
    if name and student_id:
        try:
            # GASに送るデータを作成
            payload = {
                "name": name,
                "student_id": student_id,
                "dept": dept
            }
            
            # GASへデータを送信（タイムアウト10秒）
            response = requests.post(GAS_URL, json=payload, timeout=10)
            
            if response.status_code == 200:
                # 成功メッセージ
                st.success(f"【登録完了】{name}さん、正常に受け付けました！")
                st.balloons() # お祝いの風船を飛ばす
            else:
                st.error(f"送信エラーが発生しました（ステータスコード: {response.status_code}）")
        
        except Exception as e:
            st.error("ネットワークエラーが発生しました。接続を確認してください。")
    else:
        # 入力漏れがある場合
        st.warning("氏名と学籍番号は必須入力です。")

# フッター
st.divider()
st.caption("© 2026 大会運営事務局 - 登録データは自動的にスプレッドシートに保存されます。")