import streamlit as st

st.set_page_config(page_title="Настройки", layout="wide", initial_sidebar_state="collapsed")

from app import inject_custom_css_and_sidebar, get_db_connection
inject_custom_css_and_sidebar("settings")

st.markdown('<div class="page-title">НАСТРОЙКИ</div>', unsafe_allow_html=True)

if not st.session_state.get("user"):
    st.warning("Войдите в аккаунт для доступа к настройкам.")
    st.stop()

st.session_state.settings['allow_skips'] = st.toggle("Разрешить пропуск дня (двойное нажатие)", value=st.session_state.settings['allow_skips'])
st.session_state.settings['week_start'] = st.selectbox("Начало недели", options=[0, 6], format_func=lambda x: "Понедельник" if x == 0 else "Воскресенье", index=0 if st.session_state.settings['week_start'] == 0 else 1)
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