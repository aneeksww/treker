import streamlit as st

st.set_page_config(page_title="Контакты", layout="wide", initial_sidebar_state="collapsed")

from app import inject_custom_css_and_sidebar
inject_custom_css_and_sidebar("contacts")

st.markdown('<div class="page-title">КОНТАКТЫ</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 3])
with col1:
    # Заглушка под стоковую фотографию разработчика
    st.markdown('<div style="width:150px;height:150px;background:#B8C5D9;border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:50px;">👨‍💻</div>', unsafe_allow_html=True)
with col2:
    st.write("### Разработчик: Иванов Иван")
    st.write("Свяжитесь со мной для предложений и сообщения об ошибках.")
    st.markdown("[📧 Написать email (scpsosat837@gmail.com)](mailto:scpsosat837@gmail.com)")
