import streamlit as st
import math

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

# ---------- THEME TOGGLE ----------
st.sidebar.title("⚙️ Settings")
theme = st.sidebar.radio("Select Theme:", ["Light", "Dark"])

# Define colors based on theme
if theme == "Dark":
    bg_color = "#1E1E1E"
    button_color = "#2D2D2D"
    text_color = "white"
    accent_color = "#0078FF"
else:
    bg_color = "#F8F9FC"
    button_color = "white"
    text_color = "black"
    accent_color = "#0078FF"

# ---------- STYLING ----------
st.markdown(
    f"""
    <style>
    body {{
        background-color: {bg_color};
        color: {text_color};
    }}
    .stButton > button {{
        background-color: {button_color};
        color: {text_color};
        border-radius: 50%;
        height: 60px;
        width: 60px;
        font-size: 18px;
        margin: 4px;
        border: none;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.2);
        transition: 0.2s;
    }}
    .stButton > button:hover {{
        background-color: {accent_color};
        color: white;
        transform: scale(1.05);
    }}
    .result-box {{
        background-color: {accent_color};
        color: white;
        text-align: right;
        font-size: 32px;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- CALCULATOR LOGIC ----------
st.title("🧮 Scientific Calculator")

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

# ---------- DISPLAY ----------
st.markdown(f"<div class='result-box'>{st.session_state.expression or '0'}</div>", unsafe_allow_html=True)

# ---------- BUTTON GRID ----------
scientific_buttons = ["sin(", "cos(", "tan(", "log(", "pi", "e"]
basic_buttons = [
    ["%", "(", ")", "⌫"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "^", "+"],
]

# Scientific button row
cols = st.columns(6)
for i, label in enumerate(scientific_buttons):
    cols[i].button(label, on_click=add_input, args=(label,))

# Basic calculator grid
for row in basic_buttons:
    cols = st.columns(4)
    for i, label in enumerate(row):
        if label == "⌫":
            cols[i].button(label, on_click=backspace)
        else:
            cols[i].button(label, on_click=add_input, args=(label,))

# Bottom row
col1, col2 = st.columns(2)
col1.button("C", on_click=clear)
col2.button("=", on_click=calculate)

st.caption("Developed by Alizay Ahmed")
