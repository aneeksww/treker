import streamlit as st

st.set_page_config(page_title="Profile", layout="wide")

# ---------------- 1. НАВИГАЦИЯ ----------------
nav = st.query_params.get("nav")
if nav == "app": st.switch_page("app.py"); st.stop()
elif nav == "profile": st.switch_page("pages/profile2.py"); st.stop()
elif nav == "settings": st.switch_page("pages/settings2.py"); st.stop()
elif nav == "contacts": st.switch_page("pages/contacts2.py"); st.stop()

# ---------------- 2. ГЛОБАЛЬНЫЕ СТИЛИ ----------------
st.markdown("""
<style>
:root { --primary-color: #7B2CBF !important; }
header, footer, #MainMenu { visibility: hidden; display: none; }

.main .block-container { padding: 10px 20px !important; background: transparent !important; }
.main > div { padding: 0 !important; }
hr { display: none !important; }
.stApp { background: transparent !important; }

.page-title { text-align: center; font-size: 28px; font-weight: 700; color: #334455; margin: 20px 0 30px; }

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

.auth-wrapper button {
    min-height: 250px !important; background: linear-gradient(135deg, #5B8DBE, #4a7aa3) !important;
    color: white !important; border-radius: 28px !important;
    font-size: 20px !important; font-weight: 600 !important; transition: 0.3s;
}
.auth-wrapper button:hover { transform: translateY(-4px); }

/* панелька */
#sb-nav { display: flex; flex-direction: column; align-items: center; gap: 20px; padding-top: 20px; }
#sb-nav a {
    display: flex; align-items: center; justify-content: center;
    width: 80px; height: 80px; background: #C8D1DB; border-radius: 20px;
    text-decoration: none !important; transition: 0.25s; cursor: pointer;
}
#sb-nav a:hover { transform: translateY(-4px) scale(1.07); background: #B8C5D3; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
#sb-nav a.active { background: linear-gradient(135deg, #5B8DBE, #4a7aa3); }
#sb-nav a.active svg { stroke: white; }
#sb-nav svg { width: 38px; height: 38px; stroke: #334455; stroke-width: 2.2; fill: none; }

div[data-testid="stTabs"] button { color: #5a6b82 !important; border-bottom: 2px solid transparent !important; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #7B2CBF !important; border-bottom: 2px solid #7B2CBF !important; }
div[data-testid="stTabs"] button:hover { color: #9b59b6 !important; }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none !important; }

div[role="dialog"], div[data-testid="stDialog"] {
    max-height: 90vh !important;
    height: auto !important;
    overflow-y: auto !important;
    border-bottom: 3px solid #7B2CBF !important;
}
div[role="dialog"] > div, div[data-testid="stDialog"] > div {
    max-height: 85vh !important;
    padding: 15px 24px 24px 24px !important;
}

div[role="dialog"] .stTabs [data-baseweb="tab-panel"] { padding: 5px 0 !important; }
/* Кнопка закрытия диалога */
div[role="dialog"] button[kind="icon"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- 3. СЕССИЯ ----------------
if "user" not in st.session_state: st.session_state.user = None

# ---------------- 4. ДИАЛОГ АВТОРИЗАЦИИ ----------------
@st.dialog("Вход в аккаунт")
def auth_modal():
    tab1, tab2 = st.tabs(["Вход", "Регистрация"])
    with tab1:
        contact = st.text_input("Логин / Почта", key="login_contact")
        password = st.text_input("Пароль", type="password", key="login_pass")
        if st.button("Войти", key="login_btn", use_container_width=True):
            if contact.strip() and password.strip():
                st.session_state.user = {"nick": contact.strip(), "contact": contact.strip()}
                st.rerun()
            else: st.error("Заполни поля")
    with tab2:
        nick = st.text_input("Логин", key="reg_nick")
        contact = st.text_input("Почта", key="reg_contact")
        p1 = st.text_input("Пароль", type="password", key="reg_p1")
        p2 = st.text_input("Повтори пароль", type="password", key="reg_p2")
        if st.button("Зарегистрироваться", key="reg_btn", use_container_width=True):
            if not all([nick.strip(), contact.strip(), p1.strip(), p2.strip()]): st.error("Заполни все поля")
            elif p1 != p2: st.error("Пароли не совпадают")
            else:
                st.session_state.user = {"nick": nick.strip(), "contact": contact.strip()}
                st.rerun()

# ---------------- 5. САЙДБАР ----------------
active_page = st.query_params.get("nav", "profile")
with st.sidebar:
    st.markdown(f"""
    <div id="sb-nav">
        <div style="width:90px;height:90px;background:#8FA4BC;border-radius:20px;display:flex;align-items:center;justify-content:center;">
            <svg viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </div>
        <a href="?nav=app" target="_self" class="{'active' if active_page == 'app' else ''}"><svg viewBox="0 0 24 24"><path d="M3 10l9-7 9 7"/><path d="M5 10v10h14V10"/></svg></a>
        <a href="?nav=profile" target="_self" class="{'active' if active_page == 'profile' else ''}"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 20c2-4 14-4 16 0"/></svg></a>
        <a href="?nav=settings" target="_self" class="{'active' if active_page == 'settings' else ''}"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></a>
        <a href="?nav=contacts" target="_self" class="{'active' if active_page == 'contacts' else ''}"><svg viewBox="0 0 24 24"><path d="M4 4h16v12H7l-3 3z"/></svg></a>
    </div>
    """, unsafe_allow_html=True)

# ---------------- 6. ОСНОВНОЙ КОНТЕНТ ----------------
st.markdown('<div class="page-title">Профиль</div>', unsafe_allow_html=True)

if st.session_state.user:
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="profile-avatar">{st.session_state.user['nick'][0].upper()}</div>
        <div class="profile-name">{st.session_state.user['nick']}</div>
        <div class="profile-contact">{st.session_state.user['contact']}</div>
    """, unsafe_allow_html=True)
    if st.button("Выйти из аккаунта", use_container_width=True):
        st.session_state.user = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    col1, col2, col3 = st.columns([2,1,2])
    with col2:
        st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
        if st.button("Вход / Регистрация", use_container_width=True):
            auth_modal()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#5a6b82; margin-top:20px;'>Нажмите кнопку выше, чтобы войти или создать аккаунт</div>", unsafe_allow_html=True)