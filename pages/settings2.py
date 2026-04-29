import streamlit as st

st.set_page_config(page_title="Настройки", layout="wide", initial_sidebar_state="collapsed")

from app import  get_db_connection

st.markdown('<div class="page-title">НАСТРОЙКИ</div>', unsafe_allow_html=True)

if not st.session_state.get("user"):
    st.warning("Войдите в аккаунт для доступа к настройкам.")
    st.stop()

st.selectbox("Размер шрифта", ["Стандартный", "Крупный"])

st.write("---")
if st.button("Сбросить все привычки", type="primary"):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM habit_logs WHERE habit_id IN (SELECT id FROM habits WHERE user_id=?)", (st.session_state.user['id'],))
    c.execute("DELETE FROM habits WHERE user_id=?", (st.session_state.user['id'],))
    conn.commit()
    conn.close()
    st.success("Привычки успешно удалены.")
