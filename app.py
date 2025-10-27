import streamlit as st
import math

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

# ---------- THEME TOGGLE ----------
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"])

# ---------- COLOR THEMES ----------
if theme == "Dark":
    background = "#0E1628"
    card_bg = "rgba(18, 26, 41, 0.85)"
    display_gradient = "linear-gradient(90deg, #3B82F6, #06B6D4)"
    text_color = "#E2E8F0"
    num_btn = "#1E293B"
    op_btn = "#3B82F6"
    func_btn = "#475569"
    action_btn = "#0EA5E9"
    hover_glow = "0 0 12px rgba(59,130,246,0.7)"
    shadow = "0 4px 15px rgba(0, 0, 0, 0.4)"
else:
    background = "#F4F1EE"
    card_bg = "rgba(255, 255, 255, 0.95)"
    display_gradient = "linear-gradient(90deg, #F59E0B, #F97316)"
    text_color = "#1E293B"
    num_btn = "#F3F4F6"
    op_btn = "#FBBF24"
    func_btn = "#E2E8F0"
    action_btn = "#F97316"
    hover_glow = "0 0 12px rgba(249,115,22,0.6)"
    shadow = "0 4px 15px rgba(0, 0, 0, 0.1)"

# ---------- STYLING ----------
st.markdown(
    f"""
    <style>
    body {{
        background-color: {background};
        color: {text_color};
        font-family: 'Poppins', sans-serif;
    }}
    .main {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .calc-container {{
        background: {card_bg};
        backdrop-filter: blur(20px);
        border-radius: 30px;
        padding: 35px 25px;
        box-shadow: {shadow};
        width: 360px;
        transition: all 0.3s ease;
    }}
    .display {{
        background: {display_gradient};
        color: white;
        border-radius: 18px;
        padding: 15px 20px;
        text-align: right;
        font-size: 32px;
        font-weight: 600;
        margin-bottom: 25px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.2);
    }}
    .stButton > button {{
        border: none;
        border-radius: 50%;
        height: 60px;
        width: 60px;
        font-size: 18px;
        font-weight: 500;
        margin: 6px;
        transition: all 0.2s ease;
        box-shadow: {shadow};
    }}
    .stButton > button:hover {{
        transform: scale(1.07);
        box-shadow: {hover_glow};
    }}
    /* Button Colors */
    .num button {{
        background-color: {num_btn};
        color: {text_color};
    }}
    .op button {{
        background-color: {op_btn};
        color: white;
    }}
    .func button {{
        background-color: {func_btn};
        color: {text_color};
    }}
    .act button {{
        background-color: {action_btn};
        color: white;
        font-weight: 600;
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

# ---------- LAYOUT ----------
st.markdown("<div class='main'><div class='calc-container'>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.expression or '0'}</div>", unsafe_allow_html=True)

# Scientific buttons
st.markdown("<div class='func'>", unsafe_allow_html=True)
cols = st.columns(6)
for i, label in enumerate(["sin(", "cos(", "tan(", "log(", "pi", "e"]):
    cols[i].button(label, on_click=add_input, args=(label,))
st.markdown("</div>", unsafe_allow_html=True)

# Numeric and operator buttons
buttons = [
    [("%", "func"), ("(", "func"), (")", "func"), ("⌫", "act")],
    [("7", "num"), ("8", "num"), ("9", "num"), ("/", "op")],
    [("4", "num"), ("5", "num"), ("6", "num"), ("*", "op")],
    [("1", "num"), ("2", "num"), ("3", "num"), ("-", "op")],
    [("0", "num"), (".", "num"), ("^", "op"), ("+", "op")],
]

for row in buttons:
    cols = st.columns(4)
    for i, (label, style_class) in enumerate(row):
        st.markdown(f"<div class='{style_class}'>", unsafe_allow_html=True)
        if label == "⌫":
            cols[i].button(label, on_click=backspace)
        else:
            cols[i].button(label, on_click=add_input, args=(label,))
        st.markdown("</div>", unsafe_allow_html=True)

# Bottom action buttons
col1, col2 = st.columns(2)
st.markdown("<div class='act'>", unsafe_allow_html=True)
col1.button("C", on_click=clear)
col2.button("=", on_click=calculate)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
st.markdown("<div class='footer'>Developed by your hired developer 💻</div>", unsafe_allow_html=True)
