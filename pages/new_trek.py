import streamlit as st

st.set_page_config (
    page_title = "Новая привычка",
    layout = "wide"
)

col1,  = st.columns([2])
with col1:
    with st.container(border=True):
        st.markdown("""
            <div style="
                border: 5px solid #6200ee;
                padding: 0px;
                border-radius: 15px;
                text-align: center;">
                <h1 style="font-size: 30px; margin: 0;">ДОБАВЛЕНИЕ НОВОЙ ПРИВЫЧКИ</h1>
            </div>
            """,unsafe_allow_html=True)

