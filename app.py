import streamlit as st
import pandas as pd

# 専門学校・大会用設定 (School Competition Config)
st.set_page_config(page_title="大会参加登録システム", page_icon="🏆", layout="centered")

# セッション状態のリセット防止 (Prevents data loss on refresh)
if 'participants' not in st.session_state:
    st.session_state.participants = []

# --- ユーザーインターフェース (UI) ---
st.title("🏆 大会参加登録フォーム")
st.markdown("### 参加者の方は、以下の情報を入力してください。")
st.info("各自のスマートフォンから登録が可能です。")

# 登録フォーム (Mobile-Friendly Form)
with st.form("entry_form", clear_on_submit=True):
    name = st.text_input("氏名 (フルネーム)")
    student_id = st.text_input("学籍番号")
    
    # 専門学校の学科に合わせて選択肢を調整してください
    major = st.selectbox("学科", [
        "情報処理科", 
        "ゲーム制作科", 
        "デザイン科", 
        "ビジネス科", 
        "電気電子科",
        "その他"
    ])
    
    submitted = st.form_submit_button("登録を完了する")
    
    if submitted:
        if name and student_id:
            # データの保存 (Adding to the list)
            entry = {
                "登録時間": pd.Timestamp.now().strftime('%H:%M:%S'), 
                "氏名": name, 
                "学籍番号": student_id, 
                "学科": major
            }
            st.session_state.participants.append(entry)
            st.success(f"登録完了！ {name}さん、受付を済ませました。頑張ってください！")
        else:
            st.error("エラー: 氏名と学籍番号を両方入力してください。")

st.divider()

# --- 管理者用画面 (Current Roster) ---
st.subheader("現在の登録状況 (管理用)")
if st.session_state.participants:
    df = pd.DataFrame(st.session_state.participants)
    st.dataframe(df, use_container_width=True)
    
    # Excelで開いても文字化けしないように 'utf-8-sig' を使用
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📊 登録リストをダウンロード (CSV出力)",
        data=csv,
        file_name="participation_list.csv",
        mime="text/csv",
    )
else:
    st.info("現在、登録済みの学生はいません。QRコードをスキャンして登録を開始してください。")