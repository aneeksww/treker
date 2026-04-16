from utils import local_css
import base64
from datetime import datetime
from datetime import date
import os
import glob
import streamlit as st


local_css("styles/style.css")
def local_css(style):
    with open(style) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(layout="wide")

st.set_page_config (
    page_title = "Main",
    layout = "wide"
)

def get_base64_img(images):
    with open(images, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()



col1, col2, col3 = st.columns([1,2,1])
with col2:
    with st.container(border=False):
        st.markdown("""
            <div style="
                padding: 0px;
                border-radius: 15px;
                text-align: center;">
                <h1 style="font-size: 30px; margin: 0;">ГЛАВНАЯ</h1>
            </div>
            """,unsafe_allow_html=True)

img_menu = get_base64_img("images\menu.jpg")
img_home = get_base64_img("images\home.jpg")
img_fix = get_base64_img("images\settings.jpg")
img_profile = get_base64_img("images\profile.jpg")
img_ach = get_base64_img("images\stats.jpg")
img_contacts = get_base64_img("images\contacts.jpg")

img_trek = get_base64_img("images\label1.png")

with st.sidebar:

    today = datetime.now().strftime("%d.%m.%Y")
    st.sidebar.markdown(f"## {today}")
    st.sidebar.divider()

    st.markdown("""
        <style>
            [data-testid="stSidebar"][aria-expanded-true] > div:first-child {
                width: 400px; /* Задайте желаемую ширину */
            }
            [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
                /* Дополнительные стили для сжатой панели */
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown(
        f'''
            <style>
                .sidebar .sidebar-content {{
                    width: 60px;
                }}
            </style>
        ''',
        unsafe_allow_html=True
    )

    st.sidebar.markdown(f"""
                    <div style="border-radius:15px;overflow:hidden;">
                            <img src="data:image/png;base64,{img_menu}" style="width:120px;border-radius:30px;">
                    
                    </div>
                    """,
                        unsafe_allow_html=True)

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)




    st.sidebar.markdown(
        f"""
                <div style="border-radius:15px;overflow:hidden;">
                        <a href= "{{ request.path }}"
                        style="display: inline-block; overflow:hidden; border-radius:32px;">
                        <img src="data:image/png;base64,{img_home}" "width:50px;display:block;margin:0 auto;">
                        </a>
                </div>
                """,
        unsafe_allow_html = True
    )



    st.sidebar.markdown("<br>", unsafe_allow_html=True)


    st.sidebar.markdown(f"""
                    <div style="border-radius:15px;overflow:hidden;">
                        <a href="/profile2" target="_self"
                            style="display: inline-block; overflow:hidden; border-radius:32px;">
                            <img src="data:image/png;base64,{img_profile}" "width:50px;display:block;margin:0 auto;">
                        </a>
                    </div>
                    """,
                        unsafe_allow_html=True)

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"""
                <div style="border-radius:15px;overflow:hidden;">
                    <a href="/settings2" target="_self"
                        style="display: inline-block; overflow:hidden; border-radius:32px;">
                        <img src="data:image/png;base64,{img_fix}" "width:50px;display:block;margin:0 auto;">
                    </a>
                </div>
                """,
                unsafe_allow_html=True)

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.markdown(f"""
                    <div style="border-radius:15px;overflow:hidden;">
                        <a href="/contacts2" target="_self"
                            style="display: inline-block; overflow:hidden; border-radius:32px;">
                            <img src="data:image/png;base64,{img_contacts}" "width:50px;display:block;margin:0 auto;">
                        </a>
                    </div>
                    """,
                        unsafe_allow_html=True)

    st.sidebar.markdown(
        f"""
            
            """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="Main", layout='wide')

import streamlit as st
from datetime import date
import os
import glob
import base64

st.set_page_config(page_title="Habit Tracker", layout="wide")

# Состояние
if "habits" not in st.session_state:
    st.session_state.habits = []
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None

# Загрузка картинок
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
                border = "3px solid #9b59b6" if is_sel else "2px solid #e2e2e2"
                bg = "#f8f0ff" if is_sel else "transparent"

                col.markdown(f"""
                    <div style="border:{border}; border-radius:12px; padding:5px; background:{bg}; transition:0.2s; margin-bottom:6px;">
                        <img src="data:image/png;base64,{to_base64(img_path)}" 
                             style="width:100%; height:65px; object-fit:cover; border-radius:8px;">
                    </div>
                """, unsafe_allow_html=True)

                label = "✓" if is_sel else " "
                btn_type = "primary" if is_sel else "secondary"
                if col.button(label, key=f"sel_{img_path}", use_container_width=True, type=btn_type):
                    st.session_state.selected_img = img_path


    if st.button("Добавить привычку", use_container_width=True, key="dlg_add", type="primary"):
        if not name.strip():
            st.error("Введите название:")
        else:
            st.session_state.habits.insert(0, {
                "name": name.strip(),
                "duration": duration,
                "description": desc.strip(),
                "image_path": st.session_state.selected_img,
                "progress": 0,
                "last_check_date": None
            })
            st.session_state.selected_img = None
            st.rerun()


st.markdown("""
    <style>
    header, footer, #MainMenu { visibility: hidden; display: none; }
    .main > div { padding: 0 !important; }

    .center-btn { display: flex; justify-content: center; margin: 40px 0 30px 0; }

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
        background-color: #7c3aed !important; border-color: #7c3aed !important; transition: all 0.3s ease;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        background-color: #9b59b6 !important; border-color: #8e44ad !important;
        box-shadow: 0 4px 12px rgba(155, 89, 182, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="center-btn">', unsafe_allow_html=True)
if st.button("Добавить привычку", key="main_add"):
    add_habit_dialog()
st.markdown('</div>', unsafe_allow_html=True)

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
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        if can_mark:
            if st.button("✓", key=f"check_{i}"):
                if habit["progress"] < habit["duration"]:
                    habit["progress"] += 1
                habit["last_check_date"] = today_str
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="center-btn" style="margin-top:10px;">', unsafe_allow_html=True)
    if st.button("Отметить все", key="mark_all"):
        for habit in st.session_state.habits:
            if habit["last_check_date"] != today_str:
                if habit["progress"] < habit["duration"]:
                    habit["progress"] += 1
                habit["last_check_date"] = today_str
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
        <div style='text-align: center; color: #888; margin-top: 80px; font-size: 16px; font-family: sans-serif;'>
            Нажмите кнопку выше, чтобы добавить первую привычку
        </div>
    """, unsafe_allow_html=True)