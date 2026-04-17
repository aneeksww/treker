import streamlit as st

st.set_page_config(page_title="Settings", layout="wide")

nav = st.query_params.get("nav")
if nav == "app":
    st.switch_page("app.py"); st.stop()
elif nav == "profile":
    st.switch_page("pages/profile2.py"); st.stop()
elif nav == "settings":
    st.switch_page("pages/settings2.py"); st.stop()
elif nav == "contacts":
    st.switch_page("pages/contacts2.py"); st.stop()

st.title("Settings")

active_page = st.query_params.get("nav", "settings")

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