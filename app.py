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

if "habits" not in st.session_state:
    st.session_state.habits = []

IMAGES_DIR = "images"
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

available_images = []
for ext in ["*.png"]:
    available_images.extend(glob.glob(os.path.join(IMAGES_DIR, ext)))
available_images.sort()


def to_base64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return None


@st.dialog("Добавление привычки")
def add_habit_dialog():
    name = st.text_input("Название привычки:", max_chars=70)

    if available_images:
        image_labels = [os.path.splitext(os.path.basename(p))[0] for p in available_images]
        selected_image = st.selectbox(
            "Выберите иконку:",
            options=available_images,
            format_func=lambda x: os.path.splitext(os.path.basename(x))[0],
            key="dlg_image"
        )

        st.markdown('<div style="text-align: center; margin: 15px 0;">', unsafe_allow_html=True)
        st.image(selected_image, width=100)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        selected_image = None

    duration = st.selectbox(
        "Длительность (дней):",
        options=list(range(1, 31)),
        index=6,
        key="dlg_duration"
    )

    description = st.text_area("Описание привычки:", key="dlg_desc")

    if st.button("Добавить привычку", use_container_width=True, key="dlg_add", type="primary"):
        if not name.strip():
            st.error("Пустое поле названия привычки")
        else:
            st.session_state.habits.insert(0, {
                "name": name.strip(),
                "duration": duration,
                "description": description.strip(),
                "image_path": selected_image,
                "progress": 0,
                "last_check_date": None
            })
            st.rerun()


st.markdown("""
    <style>
    .main > div { padding: 0 !important; }
    header, footer, #MainMenu { visibility: hidden; display: none; }

    .add-btn-wrap {
        display: flex;
        justify-content: center;
        margin: 40px 0 30px 0;
    }

    .habits-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 24px;
        padding: 0 20px 40px 20px;
    }

    .habit-card {
        background: #8B9AB4;
        border-radius: 20px;
        width: 210px;
        height: 230px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .habit-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }

    .habit-avatar {
        width: 90px;
        height: 90px;
        border-radius: 50%;
        background: #B8C5D9;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .habit-avatar img { width: 100%; height: 100%; object-fit: cover; }

    .habit-name {
        color: white;
        font-size: 15px;
        font-weight: 600;
        text-align: center;
        padding: 0 10px;
        line-height: 1.3;
        max-height: 40px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }

    .habit-meta {
        color: rgba(255,255,255,0.85);
        font-size: 12px;
        margin-top: 6px;
    }

    .check-btn {
        position: absolute;
        bottom: 14px;
        right: 14px;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: rgba(255,255,255,0.9);
        border: 2px solid #6B7B94;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s ease;
        font-size: 18px;
        z-index: 10;
    }
    .check-btn:hover { background: white; border-color: #5B8DBE; transform: scale(1.05); }
    .check-btn.checked {
        background: #5B8DBE;
        border-color: #5B8DBE;
    }
    .check-btn.checked::after { content: '✓'; color: white; font-weight: bold; }

    button[data-testid="stBaseButton-primary"] {
        background-color: #7c3aed !important;
        border-color: #7c3aed !important;
        transition: all 0.3s ease;
    }
    button[data-testid="stBaseButton-primary"]:hover {
        background-color: #9b59b6 !important;
        border-color: #8e44ad !important;
        box-shadow: 0 4px 12px rgba(155, 89, 182, 0.4) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="add-btn-wrap">', unsafe_allow_html=True)
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
        img_tag = f'<img src="image/png;base64,{img_b64}">' if img_b64 else '<span style="font-size:36px;opacity:0.5;"></span>'

        card_html = f"""
        <div class="habit-card">
            <div class="habit-avatar">{img_tag}</div>
            <div class="habit-name">{habit['name']}</div>
            <div class="habit-meta">{habit['progress']}/{habit['duration']} дн. ({progress_pct}%)</div>
            <div class="check-btn {'checked' if is_checked else ''}" 
                 onclick="document.getElementById('check_{i}').click()"></div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        if can_mark:
            if st.button("✓", key=f"check_{i}",
                         style="position:absolute;opacity:0;pointer-events:none;height:0;width:0;"):
                if habit["progress"] < habit["duration"]:
                    habit["progress"] += 1
                habit["last_check_date"] = today_str
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="add-btn-wrap" style="margin-top:10px;">', unsafe_allow_html=True)
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