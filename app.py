from utils import local_css
import base64
from datetime import datetime

import streamlit as st
import bcrypt
import sqlite3

def register_user(username, password):
    bytes_pw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(bytes_pw, salt).decode('utf-8')

    try:
        conn = sqlite3.connect('treker_bd.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO user (login, password) VALUES (?, ?)",
            (username, hashed_pw)
        )

        conn.commit()
        conn.close()
        return True

    except sqlite3.IntegrityError:
        return False

with st.form("registrtion_form"):
    new_username = st.text_input("Логин")
    new_password = st.text_input("Пароль", type = "password")
    submit_button = st.form_submit_button("Зарегаться")

    if submit_button:
        if new_username and new_password:
            success = register_user(new_username, new_password)

        if success:
            st.success("уСПЕШНО")
        else:
            st.error("Уже есть")
    else:
        st.warning("Заполните")

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

col1, col2, col3 = st.columns([2,1,2])
with col2:
    if st.button("Добавить привычку", use_container_width=True):
        st.switch_page("pages/new_trek.py")

st.set_page_config(page_title="Main", layout='wide')

st.title("PROVERIM RABOTAET LI ATO")
st.title("TEST PYCHARM")
st.title("OYCHARM OYSH")
