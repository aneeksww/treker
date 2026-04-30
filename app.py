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

# ---------------- 3. СТИЛИ ----------------
st.markdown("""
<style>
.block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

[data-testid="stHeader"] { background: rgba(0,0,0,0); } /* Прозрачный хедер */

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

header, footer, #MainMenu { visibility: hidden; display: none; }

.stButton > button {
    background-color: #6B7B94 !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 600 !important;
    transition: 0.2s ease;
}
.stButton > button:hover {
    background-color: #6B7B94 !important;
    transform: scale(1.02);
}

.stSlider > div > div > div > div { background: #6B7B94 !important; }
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #6B7B94 !important; border: 2px solid #6B7B94 !important;
}

.page-header { text-align: center; margin: 30px 0; font-size: 32px; font-weight: 700; color: #334455; }

/* ---------------- КАРТОЧКИ ПРИВЫЧЕК ---------------- */
.habits-grid { display: block; padding: 20px; }

.habit-card {
    background: #F2F2F7;
    border-radius: 24px;
    width: 210px;
    height: 230px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid #d0dce8;
    position: relative;

    /* ИСПРАВЛЕНИЕ: Центрируем карточку внутри колонки Streamlit */
    margin: 0 auto 10px auto; 
}

.habit-avatar {
    width: 70px; height: 70px; /* Чуть меньше для 4-х в ряд */
    border-radius: 50%;
    background: #B8C5D9;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 10px;
}

.habit-name { color: #334455; font-size: 15px; font-weight: 600; text-align: center; }
.habit-meta { color: #6b6d94; font-size: 12px; margin-top: 5px; }

.progress-bar {
    position: absolute; bottom: 12px; left: 20px; right: 20px;
    height: 6px; background: #E0E5EC; border-radius: 10px; overflow: hidden;
}
.progress-fill { height: 100%; background: #5B8DBE; }

/* ---------------- КНОПКИ ПОД КАРТОЧКОЙ ---------------- */
div.stButton > button[id^="st-key-btn_info_"],
div.stButton > button[id^="st-key-btn_check_"],
div.stButton > button[id^="st-key-btn_done_"],
div.stButton > button[id^="st-key-btn_done_"]:disabled {
    height: 36px !important;
    width: 36px !important;
    min-width: 36px !important;
    max-width: 36px !important;
    border-radius: 10px !important;
    margin: 0 auto !important; /* Центрирует кнопку в своей микро-колонке */
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    opacity: 1 !important;
}

div.stButton > button[id^="st-key-btn_"] [data-testid="stWidgetIcon"],
div.stButton > button[id^="st-key-btn_"] span {
    font-size: 20px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 20px !important;
    height: 20px !important;
}

div.stButton > button[id^="st-key-btn_info_"] { background-color: #6b6d94 !important; color: #334455 !important; }
div.stButton > button[id^="st-key-btn_check_"] { background-color: #6b6d94 !important; color: white !important; }
div.stButton > button[id^="st-key-btn_done_"]:disabled { background-color: #4954A6 !important; color: white !important; border: none !important; }

/* ---------------- ВЫБОР ИКОНКИ ПРИ СОЗДАНИИ (MATERIAL ICONS) ---------------- */
div[role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: center;
    margin-bottom: 10px;
}

div[role="radiogroup"] label {
    width: 80px !important;  /* Сделаем чуть шире, чтобы текст не вылезал, пока грузится шрифт */
    height: 60px !important;
    background: #EAF4FF;
    border-radius: 16px;
    cursor: pointer;
    transition: 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    border: none !important;
}

/* Скрываем стандартный кружок радио-кнопки */
div[role="radiogroup"] [data-testid="stWidgetSelectionVisualizer"] {
    display: none !important;
}

/* ПРОБИВАЕМ ШРИФТ: Нацеливаемся прямо на параграф с текстом внутри лейбла */
div[role="radiogroup"] label p {
    font-family: 'Material Icons' !important;
    font-size: 32px !important;
    color: #334455 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1 !important;
    width: 100% !important;
}

/* Цвет иконки при наведении */
div[role="radiogroup"] label:hover {
    background: #D6E9FF !important;
}

/* Цвет иконки и фона при выборе */
div[role="radiogroup"] input:checked + div {
    background: #4DA6FF !important;
    border-radius: 16px !important;
}

div[role="radiogroup"] input:checked + div p {
    color: white !important; /* Иконка становится белой на синем фоне */
}
</style>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

# ---------------- 4. НАДЕЖНЫЙ САЙДБАР ----------------
with st.sidebar:
    st.markdown('<div class="nav-tile"><i class="material-icons" style="font-size:40px;">menu</i></div>',
                unsafe_allow_html=True)
    st.page_link("app.py", label="Home", icon=":material/home:")
    st.page_link("pages/profile2.py", label="Profile", icon=":material/person:")
    st.page_link("pages/settings2.py", label="Settings", icon=":material/settings:")
    st.page_link("pages/contacts2.py", label="Chat", icon=":material/chat:")

# ---------------- 5. ПРОВЕРКА АВТОРИЗАЦИИ ----------------
if not st.session_state.user:
    st.markdown('<div class="page-header">ГЛАВНАЯ</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Чтобы увидеть свои привычки, нужно войти в аккаунт.")
        if st.button("Перейти к входу", use_container_width=True, type="primary"):
            st.switch_page("pages/profile2.py")
    st.stop()

USER_ID = st.session_state.user.get('id', 1)

# ---------------- 6. ФУНКЦИИ И ДИАЛОГИ ----------------
# ИСПРАВЛЕНИЕ: Заменил эмодзи на названия Material Icons
ICONS = {
    "run": "directions_run", "water": "water_drop", "sleep": "bedtime",
    "study": "school", "gym": "fitness_center", "food": "restaurant",
    "walk": "directions_walk", "meditate": "self_improvement",
    "target": "track_changes", "analyse": "query_stats",
    "time": "schedule", "health": "medical_services"
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


@st.dialog("Новая цель")
def add_habit_dialog():
    name = st.text_input("Название:")
    duration = st.slider("Цель (дней):", 1, 100, 30)
    desc = st.text_area("Зачем это вам?")

    # st.radio теперь выводит текст (названия иконок), а CSS превращает их в картинки
    selected_icon_name = st.radio(
        "Выберите иконку",
        list(ICONS.values()),
        horizontal=True,
        label_visibility="collapsed"
    )

    # Находим ключ (например, "run") по выбранному значению ("directions_run")
    icon_key = [k for k, v in ICONS.items() if v == selected_icon_name][0]

    if not name.strip(): st.warning("Введите название привычки")

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

    if st.button("🗑Удалить привычку", type="secondary", use_container_width=True):
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
    if st.button("Добавить привычку", use_container_width=True, type="primary"):
        add_habit_dialog()

st.markdown('<div style="margin-bottom: 70px;"></div>', unsafe_allow_html=True)

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
    cols = st.columns(4)  # Основная сетка карточек

    for idx, (h_id, h_name, h_dur, h_icon, h_prog, is_done) in enumerate(habits):
        progress_pct = min(100, int((h_prog / h_dur) * 100))

        # Берем название Material иконки (если нет, ставим звездочку по умолчанию)
        icon_name = ICONS.get(h_icon, "star")

        with cols[idx % 4]:
            # 1. HTML карточки (Теперь с тегом <i> для Material Icons)
            st.markdown(f"""
                <div class="habit-card">
                    <div class="habit-avatar">
                        <i class="material-icons" style="font-size:42px; color: #6b6d94;">{icon_name}</i>
                    </div>
                    <div class="habit-name">{h_name}</div>
                    <div class="habit-meta">{h_prog}/{h_dur} дн.</div>
                    <div class="progress-bar"><div class="progress-fill" style="width:{progress_pct}%"></div></div>
                </div>
            """, unsafe_allow_html=True)

            # ИСПРАВЛЕНИЕ: Изменен вес колонок, чтобы "зажать" кнопки строго по центру под карточкой
            b_col_space1, b_col1, b_col2, b_col_space2 = st.columns([1, 2, 2, 1])

            with b_col1:
                if st.button("", icon=":material/calendar_month:", key=f"btn_info_{h_id}"):
                    conn = get_db_connection()
                    c = conn.cursor()
                    c.execute("SELECT log_date FROM habit_logs WHERE habit_id = ?", (h_id,))
                    hist = [r[0] for r in c.fetchall()]
                    conn.close()
                    habit_dialog(h_id, h_name, hist)

            with b_col2:
                if not is_done:
                    if st.button("", icon=":material/check_circle:", key=f"btn_check_{h_id}"):
                        conn = get_db_connection()
                        c = conn.cursor()
                        c.execute("INSERT OR IGNORE INTO habit_logs (habit_id, log_date) VALUES (?, ?)",
                                  (h_id, date.today().isoformat()))
                        conn.commit()
                        conn.close()
                        st.rerun()
                else:
                    st.button("", icon=":material/task_alt:", key=f"btn_done_{h_id}", disabled=True)

else:
    st.write("---")
    st.info("Привычек пока нет. Самое время начать что-то новое!")
