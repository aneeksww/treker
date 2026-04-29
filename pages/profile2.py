import streamlit as st
import sqlite3
import bcrypt


# ---------------- 1. КОНФИГУРАЦИЯ ----------------
st.set_page_config(page_title="Profile", layout="wide", initial_sidebar_state="expanded")


# ---------------- 2. ИНИЦИАЛИЗАЦИЯ СЕССИИ И БД ----------------
if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- 0. ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ ----------------
def get_db_connection():
    return sqlite3.connect('treker_bd.db', check_same_thread=False)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


# ---------------- 3. ГЛОБАЛЬНЫЕ СТИЛИ (CSS) ----------------

st.markdown("""
<style>
    /* 1. Общие настройки сайдбара */
    [data-testid="stSidebarNav"] {display: none;}

    section[data-testid="stSidebar"] {
        width: 150px !important;
        min-width: 150px !important;
    }
    

    /* 2. Базовый стиль для всех плиток (и ссылок, и бургера) */
    .nav-tile, [data-testid="stSidebar"] .stPageLink a {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 80px !important;
        height: 50px !important;
        margin: 2px auto !important;
        border-radius: 20px !important;
        background-color: #8fa4bc !important; /* Цвет по умолчанию */
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
        text-decoration: none !important;
        color: white !important;
    }

    /* 3. Масштабирование иконок (Material Symbols) */
    /* Таргет для иконок внутри st.page_link */
    [data-testid="stSidebar"] .stPageLink a span[data-testid="stWidgetIcon"] {
        font-size: 65px !important; /* РАЗМЕР ИКОНКИ ТУТ */
        width: auto !important;
        height: auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: white !important;
    }

    /* Размер иконок Material */
    [data-testid="stSidebar"] .stPageLink a [data-testid="stWidgetIcon"] {
        font-size: 75px !important; /* Увеличь это число для теста */
        width: 45px !important;
        height: 45px !important;
        line-height: 45px !important;
    }

    /* 3. Скрываем текст и стандартные элементы Streamlit */
    [data-testid="stSidebar"] .stPageLink a div p {
        display: none !important;
    }

    .burger-container {
        display: flex;
        justify-content: center;
        margin-bottom: 40px; /* ← расстояние до меню */
    }
    
    .nav-tile {
        width: 80px !important;
        height: 80px !important;
        padding: 10px;
        border-radius: 12px;
        transition: 0.2s;
    }
    
    .nav-tile:hover {
        background-color: rgba(255,255,255,0.1);
        cursor: pointer;
    }
    
    .burger-icon {
        font-size: 35px !important;
        margin: 40px !important;
    }

    /* 4. Эффекты при наведении */
    [data-testid="stSidebar"] .stPageLink a:hover {
        background-color: #70869d !important; /* Чуть темнее при наведении */
        transform: scale(1.05);
    }

    /* 5. ПОДСВЕТКА АКТИВНОЙ СТРАНИЦЫ (Самый высокий приоритет) */
    [data-testid="stSidebar"] .stPageLink a[aria-current="page"] {
        background-color: #FF1493 !important; /* Твой синий для активной страницы */
        box-shadow: 0 4px 15px rgba(91, 141, 190, 0.4) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
    }
    
:root { --primary-color: #7B2CBF !important; }
    .main .block-container { padding: 10px 20px !important; background: transparent !important; }
    .stApp { background: transparent !important; }

    /* Заголовок */
    .page-title { text-align: center; font-size: 28px; font-weight: 700; color: #334455; margin: 40px 0 30px; }

    /* Карточка профиля */
    .profile-card {
        max-width: 420px; margin: 0 auto;
        background: linear-gradient(135deg, #f5f9ff, #e8f1f8);
        padding: 35px 30px; border-radius: 24px; text-align: center;
        box-shadow: 0 10px 35px rgba(91, 141, 190, 0.15); border: 1px solid #d0dce8;
    }
    .profile-avatar {
        width: 90px; height: 90px; margin: 0 auto 15px;
        background: linear-gradient(135deg, #5B8DBE, #4a7aa3);
        border-radius: 50%; display: flex; align-items: center; justify-content: center;
        color: white; font-size: 36px; font-weight: 700;
    }
    .profile-name { font-size: 22px; font-weight: 700; color: #223344; }
    .profile-contact { color: #5a6b82; font-size: 14px; margin-bottom: 20px; }

    /* Кнопки авторизации */
    .auth-wrapper button {
        min-height: 250px !important;
        background: linear-gradient(135deg, #5B8DBE, #4a7aa3) !important;
        color: white !important; border-radius: 28px !important;
        font-size: 20px !important; font-weight: 600 !important; transition: 0.3s;
    }
    .auth-wrapper button:hover { transform: translateY(-4px); }

    /* Вкладки диалога */
    div[data-testid="stTabs"] button { color: #5a6b82 !important; }
    div[data-testid="stTabs"] button[aria-selected="true"] { color: #7B2CBF !important; border-bottom: 2px solid #7B2CBF !important; }

</style>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)


# ---------------- 4. МОДАЛЬНОЕ ОКНО ----------------
@st.dialog("Вход в аккаунт")
def auth_modal():
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])

    with tab1:
        login_val = st.text_input("Логин", key="login_field")
        pass_val = st.text_input("Пароль", type="password", key="pass_field")
        if st.button("Войти", use_container_width=True):
            if login_val.strip() and pass_val.strip():
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("SELECT id, password FROM user WHERE login = ?", (login_val.strip(),))
                res = c.fetchone()
                conn.close()
                if res and check_password(pass_val, res[1]):
                    st.session_state.user = {
                        "id": res[0],
                        "nick": login_val.strip(),
                        "contact": "user@example.com"
                    }
                    st.rerun()
                else:
                    st.error("Неверные данные")
            else:
                st.error("Заполни поля")

    with tab2:
        nick = st.text_input("Придумайте логин", key="reg_nick")
        mail = st.text_input("Почта (отображение)", key="reg_mail")
        p1 = st.text_input("Пароль", type="password", key="reg_p1")
        p2 = st.text_input("Повтор пароля", type="password", key="reg_p2")
        if st.button("Создать аккаунт", use_container_width=True):
            if not all([nick.strip(), mail.strip(), p1.strip(), p2.strip()]):
                st.error("Заполни всё")
            elif p1 != p2:
                st.error("Пароли не совпали")
            else:
                conn = get_db_connection()
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO user (login, password) VALUES (?, ?)", (nick.strip(), hash_password(p1)))
                    conn.commit()
                    new_id = c.lastrowid
                    st.session_state.user = {
                        "id": new_id,
                        "nick": nick.strip(),
                        "contact": mail.strip()
                    }
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Логин занят")
                finally:
                    conn.close()


# ---------------- 5. НАДЕЖНЫЙ САЙДБАР ----------------
with st.sidebar:
    # Статичный бургер (используем HTML + Material Icons класс)
    st.markdown("""
        <div class="burger-container">
            <div class="nav-tile">
                <i class="material-icons burger-icon">menu</i>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Навигация через Material Icons (названия берем с fonts.google.com/icons)
    st.page_link("app.py", label="Home", icon=":material/home:")
    st.markdown("<p style='text-align:center; font-size:17px; opacity:0.3;'>ГЛАВНАЯ</p>", unsafe_allow_html=True)
    st.page_link("pages/profile2.py", label="Profile", icon=":material/person:")
    st.markdown("<p style='text-align:center; font-size:17px; opacity:0.3;'>ПРОФИЛЬ</p>", unsafe_allow_html=True)
    st.page_link("pages/settings2.py", label="Settings", icon=":material/settings:")
    st.markdown("<p style='text-align:center; font-size:17px; opacity:0.3;'>НАСТРОЙКИ</p>", unsafe_allow_html=True)
    st.page_link("pages/contacts2.py", label="Chat", icon=":material/chat:")
    st.markdown("<p style='text-align:center; font-size:17px; opacity:0.3;'>КОНТАКТЫ</p>", unsafe_allow_html=True)

# ---------------- 6. ОСНОВНОЙ КОНТЕНТ ----------------

if st.session_state.user:
    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-avatar">{st.session_state.user['nick'][0].upper()}</div>
        <div class="profile-name">{st.session_state.user['nick']}</div>
        <div class="profile-contact">{st.session_state.user['contact']}</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")  # Отступ
    if st.button("Выйти из аккаунта", use_container_width=True):
        st.session_state.user = None
        st.rerun()
else:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
        if st.button("Вход / Регистрация", use_container_width=True):
            auth_modal()
        st.markdown('</div>', unsafe_allow_html=True)
        st.info("Пожалуйста, авторизуйтесь для управления привычками.")
