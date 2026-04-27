import streamlit as st
import base64
from datetime import date, datetime, timedelta
import os
import calendar

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
[data-testid="stSidebarCollapseButton"] { visibility: hidden; }

.page-header {
    text-align: center; margin: 30px 0 25px 0; font-size: 32px; font-weight: 700;
    color: #334455; font-family: Tahoma, sans-serif;
}

div[role="radiogroup"] {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-top: 10px;
}
div[role="radiogroup"] label {
    background: #F2F2F7;
    border: 2px solid transparent;
    border-radius: 18px;
    padding: 14px;
    text-align: center;
    cursor: pointer;
    transition: all 0.18s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
div[role="radiogroup"] label:hover {
    background: #E9F2FF;
    transform: scale(1.05);
}
div[role="radiogroup"] label:has(input:checked) {
    border: 2px solid #007AFF;
    background: #E5F0FF;
    box-shadow: 0 6px 18px rgba(0,122,255,0.15);
}
div[role="radiogroup"] input[type="radio"] { display: none; }
div[role="radiogroup"] label span { font-size: 34px; line-height: 1; }

.habits-grid {
    display: flex; flex-wrap: wrap; justify-content: center; gap: 24px; padding: 20px;
}
.habit-card {
    background: #F2F2F7; border-radius: 24px; width: 210px; height: 230px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    position: relative; transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.habit-card:hover { transform: translateY(-4px); box-shadow: 0 8px 20px rgba(0,0,0,0.15); }
.habit-avatar {
    width: 90px; height: 90px; border-radius: 50%; background: #B8C5D9; overflow: hidden;
    display: flex; align-items: center; justify-content: center; margin-bottom: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1); cursor: pointer;
}
.habit-name {
    color: #334455; font-size: 15px; font-weight: 600; text-align: center; padding: 0 10px;
    line-height: 1.3; max-height: 40px; overflow: hidden; display: -webkit-box;
    -webkit-line-clamp: 2; -webkit-box-orient: vertical;
}
.habit-meta { color: #6B7B94; font-size: 12px; margin-top: 6px; }
.progress-bar {
    position: absolute; bottom: 14px; left: 20px; right:20px; height: 6px;
    background: #E0E5EC; width: calc(100% - 40px); border-radius: 999px; overflow: hidden;
}
.progress-fill { height: 100%; background: #5B8DBE; border-radius: 999px; transition: width 0.3s ease; }

.check-btn {
    position: absolute; bottom: 14px; right: 20px; width: 34px; height: 34px;
    border-radius: 50%; background: rgba(255,255,255,0.9); border: 2px solid #6B7B94;
    display: flex; align-items: center; justify-content: center; cursor: pointer; z-index: 10;
}
.check-btn:hover { background: white; border-color: #5B8DBE; transform: scale(1.05); }
.check-btn.checked { background: #5B8DBE; border-color: #5B8DBE; color: white; font-weight: bold; }
.check-btn.checked::after { content: '✓'; }

section[data-testid="stSidebar"] { min-width: 220px !important; width: 220px !important; max-width: 220px !important; }
button[data-testid="stBaseButton-primary"] {
    background-color: #5B8DBE !important; border: none !important; color: white !important;
    border-radius: 12px !important; font-weight: 600 !important; transition: all 0.3s ease;
}
button[data-testid="stBaseButton-primary"]:hover {
    background-color: #4a7aa3 !important; transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(91, 141, 190, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- НАВИГАЦИЯ ----------------
nav = st.query_params.get("nav")
if nav == "profile":
    st.switch_page("pages/profile2.py")
elif nav == "settings":
    st.switch_page("pages/settings2.py")
elif nav == "contacts":
    st.switch_page("pages/contacts2.py")

active_page = nav or "app"

with st.sidebar:
    st.markdown(f"""
    <div id="sb-nav" style="display: flex; flex-direction: column; align-items: center; gap: 20px; padding-top: 20px;">
        <div style="width:90px;height:90px;background:#8FA4BC;border-radius:20px;display:flex;align-items:center;justify-content:center;">
            <svg viewBox="0 0 24 24" style="width:38px;height:38px;stroke:#334455;stroke-width:2.2;fill:none;"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
        </div>
        <a href="?nav=app" target="_self" class="{'active' if active_page == 'app' else ''}" style="display:flex;align-items:center;justify-content:center;width:80px;height:80px;background:#C8D1DB;border-radius:20px;text-decoration:none;transition:0.25s;cursor:pointer;">
            <svg viewBox="0 0 24 24" style="width:38px;height:38px;stroke:#334455;stroke-width:2.2;fill:none;"><path d="M3 10l9-7 9 7"/><path d="M5 10v10h14V10"/></svg>
        </a>
        <a href="?nav=profile" target="_self" class="{'active' if active_page == 'profile' else ''}" style="display:flex;align-items:center;justify-content:center;width:80px;height:80px;background:#C8D1DB;border-radius:20px;text-decoration:none;transition:0.25s;cursor:pointer;">
            <svg viewBox="0 0 24 24" style="width:38px;height:38px;stroke:#334455;stroke-width:2.2;fill:none;"><circle cx="12" cy="8" r="4"/><path d="M4 20c2-4 14-4 16 0"/></svg>
        </a>
        <a href="?nav=settings" target="_self" class="{'active' if active_page == 'settings' else ''}" style="display:flex;align-items:center;justify-content:center;width:80px;height:80px;background:#C8D1DB;border-radius:20px;text-decoration:none;transition:0.25s;cursor:pointer;">
            <svg viewBox="0 0 24 24" style="width:38px;height:38px;stroke:#334455;stroke-width:2.2;fill:none;"><circle cx="12" cy="12" r="3"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        </a>
        <a href="?nav=contacts" target="_self" class="{'active' if active_page == 'contacts' else ''}" style="display:flex;align-items:center;justify-content:center;width:80px;height:80px;background:#C8D1DB;border-radius:20px;text-decoration:none;transition:0.25s;cursor:pointer;">
            <svg viewBox="0 0 24 24" style="width:38px;height:38px;stroke:#334455;stroke-width:2.2;fill:none;"><path d="M4 4h16v12H7l-3 3z"/></svg>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ---------------- ЗАГОЛОВОК ----------------
st.markdown('<div class="page-header">ГЛАВНАЯ</div>', unsafe_allow_html=True)

# ---------------- STATE & PATHS ----------------
if "habits" not in st.session_state:
    st.session_state.habits = []
if "selected_img" not in st.session_state:
    st.session_state.selected_img = None

ICONS = {
    "run": "🏃🏻‍♂️", "water": "💧", "sleep": "😴", "study": "📚", "gym": "🏋️‍♂️",
    "food": "🍎", "walk": "🚶‍♂️", "meditate": "🧘‍♂️", "target": "🎯", "analyse": "📊"
}

# ---------------- DIALOG ----------------
@st.dialog("Добавление привычки")
def add_habit_dialog():
    st.markdown("<h3 style='text-align:center; margin:0 0 20px 0;'>Новая привычка</h3>", unsafe_allow_html=True)
    name = st.text_input("Название:", max_chars=70)
    duration = st.selectbox("Длительность (дней):", list(range(1, 31)), index=6)
    desc = st.text_area("Описание:")

    st.markdown("<h4 style='text-align:center; margin:15px 0 5px 0;'>Выберите иконку</h4>", unsafe_allow_html=True)

    icon_keys = list(ICONS.keys())
    icon_values = list(ICONS.values())
    current_idx = icon_keys.index(st.session_state.selected_img) if st.session_state.selected_img in icon_keys else 0

    selected_emoji = st.radio(
        "icon_select",
        options=icon_values,
        index=current_idx,
        label_visibility="collapsed"
    )
    st.session_state.selected_img = icon_keys[icon_values.index(selected_emoji)]

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Добавить привычку", use_container_width=True, key="dlg_add", type="primary"):
        if not name.strip():
            st.error("Введите название привычки")
        else:
            st.session_state.habits.insert(0, {
                "history": [],
                "name": name.strip(),
                "duration": duration,
                "description": desc.strip(),
                "image_path": st.session_state.selected_img,
                "progress": 0,
                "last_check_date": None
            })
            st.session_state.selected_img = None
            st.rerun()

# ---------------- КНОПКА ДОБАВИТЬ ----------------
col_left, col_center, col_right = st.columns([1, 4, 1])
with col_center:
    if st.button("Добавить привычку", key="main_add", use_container_width=True, type="primary"):
        add_habit_dialog()

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- ФУНКЦИИ ----------------
def calculate_streaks(history):
    if not history:
        return 0, 0
    dates = sorted(set(history))
    dates = [datetime.fromisoformat(d).date() for d in dates]

    max_streak = 1
    cur = 1
    for i in range(1, len(dates)):
        if (dates[i] - dates[i - 1]).days == 1:
            cur += 1
            max_streak = max(max_streak, cur)
        else:
            cur = 1

    today = date.today()
    streak = 0
    d = today
    while d.isoformat() in history:
        streak += 1
        d -= timedelta(days=1)
    return streak, max_streak

@st.dialog(" ")
def habit_dialog(habit, i):
    today = date.today()
    key_month, key_year = f"month_{i}", f"year_{i}"
    st.session_state.setdefault(key_month, today.month)
    st.session_state.setdefault(key_year, today.year)
    month, year = st.session_state[key_month], st.session_state[key_year]

    st.markdown(f"<h3 style='text-align:center; margin-bottom:10px;'>{habit['name'].upper()} : КАЛЕНДАРЬ</h3>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("←", key=f"prev_{i}"):
            st.session_state[key_month] = 12 if month == 1 else month - 1
            st.session_state[key_year] = year - 1 if month == 1 else year
            st.rerun()
    with col2:
        st.markdown(f"<div style='text-align:center; font-weight:600'>{calendar.month_name[month]} {year}</div>", unsafe_allow_html=True)
    with col3:
        if st.button("→", key=f"next_{i}"):
            st.session_state[key_month] = 1 if month == 12 else month + 1
            st.session_state[key_year] = year + 1 if month == 12 else year
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    history = habit.get("history", [])
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)
    week_days = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
    cols = st.columns(7)
    for i_d, d in enumerate(week_days):
        cols[i_d].markdown(f"<div style='text-align:center; font-weight:600; color:#667'>{d}</div>", unsafe_allow_html=True)

    for week in month_days:
        cols = st.columns(7)
        for i_d, day in enumerate(week):
            if day == 0:
                cols[i_d].markdown(" ")
            else:
                d_obj = date(year, month, day)
                d_str = d_obj.isoformat()
                done = d_str in history
                is_today = d_obj == today
                bg = "#5B8DBE" if done else "#F1F4F8"
                color = "white" if done else "#334455"
                border = "2px solid #5B8DBE" if is_today else "1px solid transparent"
                cols[i_d].markdown(f"""
                    <div style="margin:4px; padding:10px; border-radius:10px; background:{bg}; color:{color};
                                text-align:center; font-weight:600; border:{border}; position:relative;">
                        {day}
                        {"<div style='position:absolute; bottom:4px; right:6px; font-size:12px;'>✓</div>" if done else ""}
                    </div>
                """, unsafe_allow_html=True)

    streak, max_streak = calculate_streaks(history)
    today_done = today.isoformat() in history
    flame = lambda active: f'<svg width="24" height="24" viewBox="0 0 24 24"><path fill="{"#2735F5" if active else "#BCBCC2"}" d="M13 2C13 2 8 8 8 12a4 4 0 0 0 8 0c0-3-3-7-3-10z"/><path fill="{"#FFA726" if active else "#BCBCC2"}" d="M12 14a2 2 0 0 0 2-2c0-1.5-1.5-3-2-4-0.5 1-2 2.5-2 4a2 2 0 0 0 2 2z"/></svg>'

    c1, c2 = st.columns(2)
    c1.markdown(f'<div style="display:flex;align-items:center;gap:8px;">{flame(today_done)} <b>{streak}</b> текущий</div>', unsafe_allow_html=True)
    c2.markdown(f'<div style="display:flex;align-items:center;gap:8px;">{flame(True)} <b>{max_streak}</b> максимум</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Экспорт в PDF", use_container_width=True, key=f"export_{i}"):
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm

        file_path = f"/tmp/{habit['name']}_{month}.pdf"
        doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle("TitleCustom", parent=styles["Title"], alignment=1, textColor=colors.HexColor("#334455"))
        day_style = ParagraphStyle("Day", alignment=1, fontSize=10)

        elements = [Paragraph(f"{habit['name'].upper()} — КАЛЕНДАРЬ", title_style), Spacer(1, 12)]
        table_data = [week_days]
        for week in month_days:
            row = []
            for day in week:
                if day == 0: row.append("")
                else:
                    d_str = date(year, month, day).isoformat()
                    done = d_str in history
                    row.append(Paragraph(f"<b>{day}</b>{'<br/>✓' if done else ''}", day_style))
            table_data.append(row)

        table = Table(table_data, colWidths=[25 * mm] * 7, rowHeights=[18 * mm] * len(table_data))
        style = TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3EAF3")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#334455")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D0D7E2")),
        ])
        for r_idx, week in enumerate(month_days, 1):
            for c_idx, day in enumerate(week):
                if day and date(year, month, day).isoformat() in history:
                    style.add("BACKGROUND", (c_idx, r_idx), (c_idx, r_idx), colors.HexColor("#5B8DBE"))
                    style.add("TEXTCOLOR", (c_idx, r_idx), (c_idx, r_idx), colors.white)
        table.setStyle(style)
        elements.append(table)
        elements.append(Spacer(1, 16))
        streak, max_streak = calculate_streaks(history)
        elements.append(Paragraph(f"Текущий стрик: {streak}", styles["Normal"]))
        elements.append(Paragraph(f"Максимальный стрик: {max_streak}", styles["Normal"]))
        doc.build(elements)

        with open(file_path, "rb") as f:
            st.download_button("Скачать PDF", f, file_name=f"{habit['name']}.pdf", mime="application/pdf")

# ---------------- ПРИВЫЧКИ ----------------
today_str = date.today().isoformat()
if st.session_state.habits:
    st.markdown('<div class="habits-grid">', unsafe_allow_html=True)
    for i, habit in enumerate(st.session_state.habits):
        can_mark = habit["last_check_date"] != today_str
        progress_pct = int((habit["progress"] / habit["duration"]) * 100) if habit["duration"] > 0 else 0
        icon = ICONS.get(habit["image_path"], "✨")

        st.markdown(f"""
        <div class="habit-card">
            <div class="habit-avatar" onclick="document.querySelector('#st-key-open_{i} button').click(); return false;">
                <div style="font-size:38px;">{icon}</div>
            </div>
            <div class="habit-name">{habit['name']}</div>
            <div class="habit-meta">{habit['progress']}/{habit['duration']} дн. ({progress_pct}%)</div>
            <div class="check-btn {'checked' if not can_mark else ''}"></div>
            <div class="progress-bar"><div class="progress-fill" style="width:{progress_pct}%"></div></div>
        </div>""", unsafe_allow_html=True)

        if can_mark:
            if st.button("✓", key=f"check_{i}"):
                habit["progress"] = min(habit["progress"] + 1, habit["duration"])
                habit["last_check_date"] = today_str
                habit.setdefault("history", []).append(today_str)
                st.rerun()
        if st.button("hidden_open", key=f"open_{i}"):
            st.session_state.open_dialog = i
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        if st.button("Отметить все сегодня", key="mark_all", use_container_width=True):
            updated = False
            for h in st.session_state.habits:
                if h["last_check_date"] != today_str:
                    h["progress"] = min(h["progress"] + 1, h["duration"])
                    h["last_check_date"] = today_str
                    h.setdefault("history", []).append(today_str)
                    updated = True
            if updated: st.rerun()
else:
    st.markdown("""<div style='text-align: center; color: #888; margin-top: 80px; font-size: 16px;'>
        Нажмите кнопку выше, чтобы добавить первую привычку
    </div>""", unsafe_allow_html=True)

st.session_state.setdefault("open_dialog", None)
if st.session_state.open_dialog is not None:
    idx = st.session_state.open_dialog
    if idx < len(st.session_state.habits):
        habit_dialog(st.session_state.habits[idx], idx)