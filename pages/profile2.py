import streamlit as st
import sqlite3
import bcrypt

# ---------------- 1. КОНФИГУРАЦИЯ ----------------
# initial_sidebar_state="expanded" гарантирует, что сайдбар будет открыт
st.set_page_config(page_title="Profile", layout="wide", initial_sidebar_state="expanded")

# ---------------- 2. ИНИЦИАЛИЗАЦИЯ СЕССИИ И БД ----------------
if "user" not in st.session_state:
    st.session_state.user = None


def get_db_connection():
    return sqlite3.connect('treker_bd.db', check_same_thread=False)


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


# ---------------- 3. ГЛОБАЛЬНЫЕ СТИЛИ (CSS) ----------------
# Я убрал скрытие header и MainMenu, чтобы сайдбар корректно работал
st.markdown("""
<style>
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
    st.markdown("<h3 style='text-align: center;'>Навигация</h3>", unsafe_allow_html=True)
    st.write("")  # Отступ

    # Родные ссылки Streamlit — не сбрасывают сессию!
    st.page_link("app.py", label="Главная", icon="🏠")
    st.page_link("pages/profile2.py", label="Профиль", icon="👤")
    st.page_link("pages/settings2.py", label="Настройки", icon="⚙️")
    st.page_link("pages/contacts2.py", label="Контакты", icon="📞")

# ---------------- 6. ОСНОВНОЙ КОНТЕНТ ----------------
st.markdown('<div class="page-title">Профиль</div>', unsafe_allow_html=True)

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