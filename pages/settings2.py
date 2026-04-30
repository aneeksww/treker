import streamlit as st
import sqlite3

st.set_page_config(page_title="Настройки", layout="wide", initial_sidebar_state="expanded")


if "user" not in st.session_state:
    st.session_state.user = None


def get_db_connection():
    return sqlite3.connect('treker_bd.db', check_same_thread=False)

st.markdown("""
<style>
/* --- НАВИГАЦИЯ (САЙДБАР) --- */
    [data-testid="stSidebarNav"] {display: none;}
    section[data-testid="stSidebar"] { width: 150px !important; min-width: 150px !important; }
    .nav-tile, [data-testid="stSidebar"] .stPageLink a {
        display: flex !important; align-items: center !important; justify-content: center !important;
        width: 85px !important; height: 85px !important; margin: 15px auto !important;
        border-radius: 20px !important; background-color: #8fa4bc !important;
        transition: all 0.3s ease !important; text-decoration: none !important;

    }
    /* --- НАВИГАЦИЯ (САЙДБАР) --- */
    [data-testid="stSidebarNav"] {display: none;}
    section[data-testid="stSidebar"] { width: 150px !important; min-width: 150px !important; }

    /* Контейнер плитки */
    [data-testid="stSidebar"] .stPageLink a {
        display: flex !important; align-items: center !important; justify-content: center !important;
        width: 85px !important; height: 85px !important; margin: 15px auto !important;
        border-radius: 20px !important; background-color: #8fa4bc !important;
        transition: 0.3s !important; text-decoration: none !important;
    }

    /* Скрываем текст подписи */
    [data-testid="stSidebar"] .stPageLink a p { display: none !important; }
    [data-testid="stSidebar"] .stPageLink a[aria-current="page"] { background-color: #FF1493 !important; }

    /* ПРОБИВАЕМ ИКОНКИ: Нацеливаемся напрямую на SVG и шрифтовые иконки внутри ссылки */
    [data-testid="stSidebar"] .stPageLink a svg,
    [data-testid="stSidebar"] .stPageLink a i,
    [data-testid="stSidebar"] .stPageLink a span.material-symbols-rounded,
    [data-testid="stSidebar"] .stPageLink a span[translate="no"] {
        font-size: 35px !important; 
        width: 35px !important;
        height: 35px !important;
        line-height: 35px !important;

        margin: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stSidebar"] .stPageLink a:hover {
        background-color: #70869d !important;
        transform: scale(1.05);
    }
    </style>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">НАСТРОЙКИ</div>', unsafe_allow_html=True)

if not st.session_state.get("user"):
    st.warning("Войдите в аккаунт для доступа к настройкам.")
    st.stop()

with st.sidebar:
    st.markdown('<div class="nav-tile"><i class="material-icons" style="font-size:40px;">menu</i></div>',
                unsafe_allow_html=True)
    st.page_link("app.py", label="Home", icon=":material/home:")
    st.page_link("pages/profile2.py", label="Profile", icon=":material/person:")
    st.page_link("pages/settings2.py", label="Settings", icon=":material/settings:")
    st.page_link("pages/contacts2.py", label="Chat", icon=":material/chat:")

st.write("---")
if st.button("Сбросить все привычки", type="primary"):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM habit_logs WHERE habit_id IN (SELECT id FROM habits WHERE user_id=?)", (st.session_state.user['id'],))
    c.execute("DELETE FROM habits WHERE user_id=?", (st.session_state.user['id'],))
    conn.commit()
    conn.close()
    st.success("Привычки успешно удалены.")
