import streamlit as st
import sqlite3

st.set_page_config(page_title="Контакты", layout="wide", initial_sidebar_state="expanded")

# Инициализация сессии (ДОЛЖНА БЫТЬ В САМОМ НАЧАЛЕ)
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

st.markdown('<div class="page-title">КОНТАКТЫ</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="nav-tile"><i class="material-icons" style="font-size:40px;">menu</i></div>',
                unsafe_allow_html=True)
    st.page_link("app.py", label="Home", icon=":material/home:")
    st.page_link("pages/profile2.py", label="Profile", icon=":material/person:")
    st.page_link("pages/settings2.py", label="Settings", icon=":material/settings:")
    st.page_link("pages/contacts2.py", label="Chat", icon=":material/chat:")

col1, col2 = st.columns([1, 3])
with col1:
    # Заглушка под стоковую фотографию разработчика
    st.markdown('<div style="width:150px;height:150px;background:#B8C5D9;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:50px;">👨‍💻</div>', unsafe_allow_html=True)
with col2:
    st.write("### Разработчик: Иванов Иван")
    st.write("Свяжитесь со мной для предложений и сообщения об ошибках.")
    st.markdown("[📧 Написать email (scpsosat837@gmail.com)](mailto:scpsosat837@gmail.com)")
