import streamlit as st
import sqlite3
import os
from datetime import date, datetime, timedelta

# ---------------- 1. КОНФИГУРАЦИЯ ----------------
st.set_page_config(page_title="Habit Tracker", layout="wide", initial_sidebar_state="expanded")

# Инициализация сессии (ДОЛЖНА БЫТЬ В САМОМ НАЧАЛЕ)
if "user" not in st.session_state:
    st.session_state.user = None


def local_css(style_path):
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("styles/style.css")


# ---------------- 2. БАЗА ДАННЫХ ----------------
def get_db_connection():
    return sqlite3.connect('treker_bd.db', check_same_thread=False)


def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            duration INTEGER NOT NULL,
            description TEXT,
            icon_key TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            log_date TEXT NOT NULL,
            UNIQUE(habit_id, log_date)
        )
    """)
    conn.commit()
    conn.close()


init_db()

# ---------------- 3. НАДЕЖНЫЙ САЙДБАР (БЕЗ HTML-ССЫЛОК) ----------------
with st.sidebar:
    st.markdown("<h3 style='text-align: center;'>Навигация</h3>", unsafe_allow_html=True)
    st.write("")  # Отступ

    # st.page_link переключает страницы БЕЗ перезагрузки браузера
    st.page_link("app.py", label="Главная", icon="🏠")
    st.page_link("pages/profile2.py", label="Профиль", icon="👤")
    st.page_link("pages/settings2.py", label="Настройки", icon="⚙️")
    st.page_link("pages/contacts2.py", label="Контакты", icon="📞")

# ---------------- 4. ПРОВЕРКА АВТОРИЗАЦИИ ----------------
if not st.session_state.user:
    st.markdown('<div class="page-header">ГЛАВНАЯ</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Чтобы увидеть свои привычки, нужно войти в аккаунт.")
        if st.button("Перейти к входу", use_container_width=True, type="primary"):
            st.switch_page("pages/profile2.py")  # Нативный переход!
    st.stop()

# Если дошли сюда — юзер залогинен
USER_ID = st.session_state.user.get('id', 1)

# ---------------- 5. СТИЛИ ----------------
st.markdown("""
<style>
header, footer, #MainMenu { visibility: hidden; display: none; }
.page-header { text-align: center; margin: 30px 0; font-size: 32px; font-weight: 700; color: #334455; }
.habits-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 24px; padding: 20px; }
.habit-card {
    background: #F2F2F7; border-radius: 24px; width: 210px; height: 230px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    position: relative; transition: 0.2s ease; border: 1px solid #d0dce8;
}
.habit-avatar {
    width: 80px; height: 80px; border-radius: 50%; background: #B8C5D9; 
    display: flex; align-items: center; justify-content: center; margin-bottom: 10px;
    cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.habit-name { color: #334455; font-size: 15px; font-weight: 600; text-align: center; padding: 0 10px; }
.habit-meta { color: #6B7B94; font-size: 12px; margin-top: 5px; }
.progress-bar { position: absolute; bottom: 12px; left: 20px; right: 20px; height: 6px; background: #E0E5EC; border-radius: 10px; overflow: hidden; }
.progress-fill { height: 100%; background: #5B8DBE; transition: width 0.3s; }
.check-btn {
    position: absolute; top: 15px; right: 15px; width: 28px; height: 28px;
    border-radius: 50%; border: 2px solid #6B7B94; display: flex; align-items: center; justify-content: center;
}
.check-btn.checked { background: #5B8DBE; border-color: #5B8DBE; color: white; }
.check-btn.checked::after { content: '✓'; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ---------------- 6. ФУНКЦИИ И ДИАЛОГИ ----------------
ICONS = {
    "run": "🏃🏻‍♂️", "water": "💧", "sleep": "😴", "study": "📚", "gym": "🏋️‍♂️",
    "food": "🍎", "walk": "🚶‍♂️", "meditate": "🧘‍♂️", "target": "🎯", "analyse": "📊"
}


def calculate_streaks(history):
    if not history: return 0, 0
    dates = sorted([datetime.fromisoformat(d).date() for d in history])
    max_s = cur_s = 0
    if dates:
        cur_s = 1
        for i in range(1, len(dates)):
            if (dates[i] - dates[i - 1]).days == 1:
                cur_s += 1
            else:
                max_s = max(max_s, cur_s)
                cur_s = 1
        max_s = max(max_s, cur_s)
    today = date.today()
    streak = 0
    check_date = today
    history_set = set(history)
    while check_date.isoformat() in history_set:
        streak += 1
        check_date -= timedelta(days=1)
    return streak, max_s


@st.dialog("Добавление привычки")
def add_habit_dialog():
    st.write("### Новая цель")
    name = st.text_input("Название:")
    duration = st.slider("Цель (дней):", 1, 100, 30)
    desc = st.text_area("Зачем это вам?")
    selected_emoji = st.radio("Выберите иконку", list(ICONS.values()), horizontal=True)
    icon_key = [k for k, v in ICONS.items() if v == selected_emoji][0]

    if st.button("Создать", use_container_width=True, type="primary"):
        if name.strip():
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO habits (user_id, name, duration, description, icon_key) VALUES (?, ?, ?, ?, ?)",
                      (USER_ID, name.strip(), duration, desc.strip(), icon_key))
            conn.commit()
            conn.close()
            st.rerun()


@st.dialog("Статистика")
def habit_dialog(habit_id, name, history):
    st.write(f"### {name}")
    streak, max_streak = calculate_streaks(history)
    col1, col2 = st.columns(2)
    col1.metric("Текущая серия", f"{streak} дн.")
    col2.metric("Рекорд", f"{max_streak} дн.")

    if st.button("🗑️ Удалить привычку", type="secondary", use_container_width=True):
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        c.execute("DELETE FROM habit_logs WHERE habit_id = ?", (habit_id,))
        conn.commit()
        conn.close()
        st.rerun()


# ---------------- 7. ГЛАВНЫЙ ЭКРАН ----------------
st.markdown('<div class="page-header">ГЛАВНАЯ</div>', unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([1, 2, 1])
with col_c:
    if st.button("➕ Добавить привычку", use_container_width=True, type="primary"):
        add_habit_dialog()

# Загрузка данных
conn = get_db_connection()
c = conn.cursor()
c.execute("""
    SELECT h.id, h.name, h.duration, h.icon_key,
    (SELECT COUNT(*) FROM habit_logs WHERE habit_id = h.id) as progress,
    (SELECT 1 FROM habit_logs WHERE habit_id = h.id AND log_date = ?) as done_today
    FROM habits h WHERE h.user_id = ?
""", (date.today().isoformat(), USER_ID))
habits = c.fetchall()
conn.close()

if habits:
    st.markdown('<div class="habits-grid">', unsafe_allow_html=True)
    for h_id, h_name, h_dur, h_icon, h_prog, is_done in habits:
        progress_pct = min(100, int((h_prog / h_dur) * 100))
        icon = ICONS.get(h_icon, "✨")

        st.markdown(f"""
        <div class="habit-card">
            <div class="check-btn {'checked' if is_done else ''}"></div>
            <div class="habit-avatar" onclick="document.querySelector('#st-key-btn_open_{h_id} button').click();">
                <div style="font-size:38px;">{icon}</div>
            </div>
            <div class="habit-name">{h_name}</div>
            <div class="habit-meta">{h_prog}/{h_dur} дн.</div>
            <div class="progress-bar"><div class="progress-fill" style="width:{progress_pct}%"></div></div>
        </div>""", unsafe_allow_html=True)

        if not is_done:
            if st.button("Выполнить", key=f"btn_check_{h_id}", use_container_width=True):
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("INSERT OR IGNORE INTO habit_logs (habit_id, log_date) VALUES (?, ?)",
                          (h_id, date.today().isoformat()))
                conn.commit()
                conn.close()
                st.rerun()

        if st.button("Детали", key=f"btn_open_{h_id}"):
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("SELECT log_date FROM habit_logs WHERE habit_id = ?", (h_id,))
            hist = [r[0] for r in c.fetchall()]
            conn.close()
            habit_dialog(h_id, h_name, hist)

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.write("---")
    st.info("Привычек пока нет. Самое время начать что-то новое!")