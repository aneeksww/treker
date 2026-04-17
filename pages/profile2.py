import streamlit as st
import base64

#from pages.app2 import get_base64_img

st.set_page_config (
    page_title = "Profile",
    layout = "wide"
)

st.title("Profile")

#панель управления
img_menu = get_base64_img("images\menu.jpg")
img_home = get_base64_img("images\home.jpg")
img_fix = get_base64_img("images\settings.jpg")
img_profile = get_base64_img("images\profile.jpg")
img_ach = get_base64_img("images\stats.jpg")
img_contacts = get_base64_img("images\contacts.jpg")

img_trek = get_base64_img("images\label1.png")

with st.sidebar:
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
                        </a>
                    </div>
                    """,
                        unsafe_allow_html=True)

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.markdown(f"""
                <div style="border-radius:15px;overflow:hidden;">
                        <a href="/app" target="_self"
                        style="display: inline-block; overflow:hidden; border-radius:32px;">
                        <img src="data:image/png;base64,{img_home}" "width:50px;display:block;margin:0 auto;">
                </a>
                </div>
                """,
                        unsafe_allow_html=True)

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
                        <a href="/contacts" target="_self"
                            style="display: inline-block; overflow:hidden; border-radius:32px;">
                            <img src="data:image/png;base64,{img_contacts}" "width:50px;display:block;margin:0 auto;">
                        </a>
                    </div>
                    """,
                        unsafe_allow_html=True)
