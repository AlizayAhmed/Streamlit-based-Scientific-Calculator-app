import streamlit as st
import math

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

# ---------- THEME SETTINGS ----------
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"])

# Define color palettes
if theme == "Dark":
    background = "#0F172A"
    card_bg = "rgba(30, 41, 59, 0.9)"
    text_color = "#F8FAFC"
    display_gradient = "linear-gradient(90deg, #3B82F6, #06B6D4)"
    btn_bg = "#1E293B"
    hover_bg = "#3B82F6"
    shadow = "0 4px 12px rgba(0, 0, 0, 0.3)"
else:
    background = "#F1F5F9"
    card_bg = "rgba(255, 255, 255, 0.9)"
    text_color = "#1E293B"
    display_gradient = "linear-gradient(90deg, #2563EB, #0EA5E9)"
    btn_bg = "#FFFFFF"
    hover_bg = "#2563EB"
    shadow = "0 4px 12px rgba(0, 0, 0, 0.15)"

# ---------- STYLING ----------
st.markdown(
    f"""
    <style>
    body {{
        background-color: {background};
        color: {text_color};
        font-family: 'Segoe UI', sans-serif;
    }}
    .main {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .calc-container {{
        background: {card_bg};
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 30px;
        box-shadow: {shadow};
        width: 340px;
    }}
    .display {{
        background: {display_gradient};
        color: white;
        border-radius: 15px;
        padding: 15px;
        text-align: right;
        font-size: 30px;
        font-weight: 600;
        margin-bottom: 20px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
    }}
    .stButton > button {{
        background-color: {btn_bg};
        color: {text_color};
        border: none;
        border-radius: 50%;
        height: 60px;
        width: 60px;
        font-size: 18px;
        font-weight: 500;
        margin: 6px;
        box-shadow: {shadow};
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        background-color: {hover_bg};
        color: white !important;
        transform: scale(1.07);
    }}
    .footer {{
        text-align: center;
        font-size: 14px;
        opacity: 0.7;
        margin-top: 15px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- APP TITLE ----------
st.markdown("<h2 style='text-align:center; margin-bottom:20px;'>🧮 Scientific Calculator</h2>", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "expression" not in st.session_state:
    st.session_state.expression = ""

def add_input(value):
    st.session_state.expression += str(value)

def clear():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

def calculate():
    try:
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        allowed_names.update({
            "pi": math.pi, "e": math.e,
            "sqrt": math.sqrt,
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log10,
        })
        expression = st.session_state.expression.replace("^", "**")
        result = eval(expression, {"__builtins__": None}, allowed_names)
        st.session_state.expression = str(result)
    except Exception:
        st.session_state.expression = "Error"

# ---------- CALCULATOR UI ----------
st.markdown("<div class='main'><div class='calc-container'>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.expression or '0'}</div>", unsafe_allow_html=True)

# Scientific Buttons
scientific_buttons = ["sin(", "cos(", "tan(", "log(", "pi", "e"]
cols = st.columns(6)
for i, label in enumerate(scientific_buttons):
    cols[i].button(label, on_click=add_input, args=(label,))

# Main Buttons
buttons = [
    ["%", "(", ")", "⌫"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "^", "+"],
]

for row in buttons:
    cols = st.columns(4)
    for i, label in enumerate(row):
        if label == "⌫":
            cols[i].button(label, on_click=backspace)
        else:
            cols[i].button(label, on_click=add_input, args=(label,))

# Bottom buttons
col1, col2 = st.columns(2)
col1.button("C", on_click=clear)
col2.button("=", on_click=calculate)

st.markdown("</div></div>", unsafe_allow_html=True)
st.markdown("<div class='footer'>Developed by your hired developer 💻</div>", unsafe_allow_html=True)
