import streamlit as st
import base64
from datetime import date
import os
import glob

# ---------------- КОНФИГ ----------------
st.set_page_config(page_title="Main", layout="wide")

def local_css(style_path):
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles/style.css")

# ---------------- ГЛОБАЛЬНЫЕ СТИЛИ ----------------
st.markdown("""
<style>
header, footer, #MainMenu { visibility: hidden; display: none; }
.main > div { padding: 0 !important; }

.page-header {
    text-align: center;
    margin: 30px 0 25px 0;
    font-size: 32px;
    font-weight: 700;
    color: #334455;
    font-family: Tahoma, sans-serif;
}

.habits-grid {
    display: flex; flex-wrap: wrap; justify-content: center; gap: 24px;
    padding: 0 20px 40px 20px;
}
.habit-card {
    background: #8B9AB4; border-radius: 20px; width: 210px; height: 230px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    position: relative; transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.habit-card:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
.habit-avatar {
    width: 90px; height: 90px; border-radius: 50%; background: #B8C5D9; overflow: hidden;
    display: flex; align-items: center; justify-content: center; margin-bottom: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.habit-avatar img { width: 100%; height: 100%; object-fit: cover; }
.habit-name {
    color: white; font-size: 15px; font-weight: 600; text-align: center; padding: 0 10px;
    line-height: 1.3; max-height: 40px; overflow: hidden; display: -webkit-box;
    -webkit-line-clamp: 2; -webkit-box-orient: vertical;
}
.habit-meta { color: rgba(255,255,255,0.85); font-size: 12px; margin-top: 6px; }

.check-btn {
    position: absolute; bottom: 14px; right: 14px; width: 34px; height: 34px; border-radius: 50%;
    background: rgba(255,255,255,0.9); border: 2px solid #6B7B94; display: flex;
    align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s ease;
    font-size: 18px; z-index: 10;
}
.check-btn:hover { background: white; border-color: #5B8DBE; transform: scale(1.05); }
.check-btn.checked { background: #5B8DBE; border-color: #5B8DBE; }
.check-btn.checked::after { content: '✓'; color: white; font-weight: bold; }

div[id^="st-key-check_"] { display: none !important; }

button[data-testid="stBaseButton-primary"] {
    background-color: #5B8DBE !important;
    border: none !important; color: white !important;
    border-radius: 12px !important; font-weight: 600 !important;
    transition: all 0.3s ease;
}
button[data-testid="stBaseButton-primary"]:hover {
    background-color: #4a7aa3 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(91, 141, 190, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- НАВИГАЦИЯ ----------------
nav = st.query_params.get("nav")
if nav == "app": st.switch_page("app.py"); st.stop()
elif nav == "profile": st.switch_page("pages/profile2.py"); st.stop()
elif nav == "settings": st.switch_page("pages/settings2.py"); st.stop()
elif nav == "contacts": st.switch_page("pages/contacts2.py"); st.stop()

active_page = nav or "app"

with st.sidebar:
    st.markdown(f"""
    <style>
    #sb-nav {{ display: flex; flex-direction: column; align-items: center; gap: 20px; padding-top: 20px; }}
    #sb-nav a {{
        display: flex; align-items: center; justify-content: center;
        width: 80px; height: 80px; background: #C8D1DB; border-radius: 20px;
        text-decoration: none !important; transition: 0.25s; cursor: pointer;
    }}
    #sb-nav a:hover {{ transform: translateY(-4px) scale(1.07); background: #B8C5D3; box-shadow: 0 10px 25px rgba(0,0,0,0.15); }}
    #sb-nav a.active {{ background: linear-gradient(135deg, #5B8DBE, #4a7aa3); }}
    #sb-nav a.active svg {{ stroke: white; }}
    #sb-nav svg {{ width: 38px; height: 38px; stroke: #334455; stroke-width: 2.2; fill: none; }}
    </style>

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

# ---------------- ЗАГОЛОВОК ----------------
st.markdown('<div class="page-header">ГЛАВНАЯ</div>', unsafe_allow_html=True)

# ---------------- STATE & PATHS ----------------
if "habits" not in st.session_state:
    st.session_state.habits = []
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None

IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)
exts = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
available_images = sorted([
    p for p in glob.glob(os.path.join(IMAGES_DIR, "*.*"))
    if os.path.splitext(p)[1].lower() in exts
])

def to_base64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None

# ---------------- DIALOG ----------------
@st.dialog("Добавление привычки")
def add_habit_dialog():
    st.markdown("<h3 style='text-align:center; margin:0 0 20px 0;'>Новая привычка</h3>", unsafe_allow_html=True)
    name = st.text_input("Название:", max_chars=70)
    duration = st.selectbox("Длительность (дней):", list(range(1, 31)), index=6)
    desc = st.text_area("Описание:")

    st.markdown("Выберите иконку:")
    if available_images:
        cols_per_row = 4
        for i in range(0, len(available_images), cols_per_row):
            row_imgs = available_images[i:i + cols_per_row]
            st_cols = st.columns(len(row_imgs))
            for col, img_path in zip(st_cols, row_imgs):
                is_sel = (st.session_state.selected_img == img_path)
                border = "3px solid #5B8DBE" if is_sel else "2px solid #e2e2e2"
                bg = "#e8f1f8" if is_sel else "transparent"
                col.markdown(f"""
                    <div style="border:{border}; border-radius:12px; padding:5px; background:{bg}; transition:0.2s; margin-bottom:6px;">
                        <img src="data:image/png;base64,{to_base64(img_path)}" 
                             style="width:100%; height:65px; object-fit:cover; border-radius:8px;">
                    </div>""", unsafe_allow_html=True)
                label = "✓" if is_sel else " "
                btn_type = "primary" if is_sel else "secondary"
                if col.button(label, key=f"sel_{img_path}", use_container_width=True, type=btn_type):
                    st.session_state.selected_img = img_path

    if st.button("Добавить привычку", use_container_width=True, key="dlg_add", type="primary"):
        if not name.strip():
            st.error("Введите название:")
        else:
            st.session_state.habits.insert(0, {
                "name": name.strip(), "duration": duration, "description": desc.strip(),
                "image_path": st.session_state.selected_img, "progress": 0, "last_check_date": None
            })
            st.session_state.selected_img = None
            st.rerun()

# ---------------- КНОПКА ДОБАВИТЬ ----------------
col_left, col_center, col_right = st.columns([1, 4, 1])
with col_center:
    if st.button("Добавить привычку", key="main_add", use_container_width=True, type="primary"):
        add_habit_dialog()

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- ПРИВЫЧКИ ----------------
today_str = date.today().isoformat()

if st.session_state.habits:
    st.markdown('<div class="habits-grid">', unsafe_allow_html=True)
    for i, habit in enumerate(st.session_state.habits):
        can_mark = habit["last_check_date"] != today_str
        is_checked = not can_mark
        progress_pct = int((habit["progress"] / habit["duration"]) * 100) if habit["duration"] > 0 else 0
        img_b64 = to_base64(habit["image_path"])
        img_tag = f'<img src="data:image/png;base64,{img_b64}">' if img_b64 else '<span style="font-size:36px;opacity:0.5;"></span>'

        card_html = f"""
        <div class="habit-card">
            <div class="habit-avatar">{img_tag}</div>
            <div class="habit-name">{habit['name']}</div>
            <div class="habit-meta">{habit['progress']}/{habit['duration']} дн. ({progress_pct}%)</div>
            <div class="check-btn {'checked' if is_checked else ''}" 
                 onclick="document.querySelector('#st-key-check_{i} button').click()"></div>
        </div>"""
        st.markdown(card_html, unsafe_allow_html=True)

        if can_mark:
            if st.button("✓", key=f"check_{i}"):
                if habit["progress"] < habit["duration"]:
                    habit["progress"] += 1
                habit["last_check_date"] = today_str
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        if st.button("Отметить все сегодня", key="mark_all", use_container_width=True):
            for habit in st.session_state.habits:
                if habit["last_check_date"] != today_str:
                    if habit["progress"] < habit["duration"]:
                        habit["progress"] += 1
                    habit["last_check_date"] = today_str
            st.rerun()
else:
    st.markdown("""
        <div style='text-align: center; color: #888; margin-top: 80px; font-size: 16px;'>
            Нажмите кнопку выше, чтобы добавить первую привычку
        </div>""", unsafe_allow_html=True)