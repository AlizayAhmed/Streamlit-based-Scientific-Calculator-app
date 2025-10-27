import streamlit as st
import math

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Scientific Calculator", layout="centered")

# ---- CUSTOM STYLES ----
def set_custom_style(dark_mode):
    if dark_mode:
        bg_color = "#0F172A"  # deep nude blue
        frame_color = "#1E293B"
        button_bg = "#334155"
        text_color = "#E2E8F0"
        accent_color = "#38BDF8"
        equal_color = "#22C55E"
    else:
        bg_color = "#F8FAFC"  # nude white
        frame_color = "#FFFFFF"
        button_bg = "#E2E8F0"
        text_color = "#0F172A"
        accent_color = "#3B82F6"
        equal_color = "#10B981"

    st.markdown(f"""
        <style>
        body {{
            background-color: {bg_color};
        }}
        .calculator {{
            background-color: {frame_color};
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            width: 320px;
            margin: auto;
        }}
        .display {{
            background-color: {accent_color};
            color: white;
            border-radius: 12px;
            text-align: right;
            font-size: 28px;
            padding: 15px 10px;
            margin-bottom: 15px;
            font-weight: bold;
            overflow-x: auto;
        }}
        button {{
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 18px;
            font-weight: 600;
            color: {text_color};
            background-color: {button_bg};
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: 0.2s ease;
        }}
        button:hover {{
            transform: scale(1.07);
        }}
        .special {{
            background-color: {accent_color};
            color: white;
        }}
        .equal {{
            background-color: {equal_color};
            color: white;
        }}
        </style>
    """, unsafe_allow_html=True)

# ---- APP LOGIC ----
if "expression" not in st.session_state:
    st.session_state.expression = ""

# ---- DARK/LIGHT TOGGLE ----
st.markdown("<h2 style='text-align:center;'>🧮 Scientific Calculator</h2>", unsafe_allow_html=True)
dark_mode = st.toggle("Dark Mode", value=False)

set_custom_style(dark_mode)

# ---- DISPLAY AREA ----
st.markdown("<div class='calculator'>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.expression or '0'}</div>", unsafe_allow_html=True)

# ---- BUTTON LAYOUT ----
buttons = [
    ["sin", "cos", "tan", "log"],
    ["π", "e", "^", "C"],
    ["7", "8", "9", "÷"],
    ["4", "5", "6", "×"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]

cols = st.columns(4)

# Function to evaluate expression
def evaluate_expression(expr):
    expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**").replace("π", str(math.pi)).replace("e", str(math.e))
    try:
        return str(eval(expr, {"math": math, "__builtins__": None}))
    except:
        return "Error"

for row in buttons:
    cols = st.columns(4)
    for i, btn in enumerate(row):
        if cols[i].button(btn):
            if btn == "C":
                st.session_state.expression = ""
            elif btn == "=":
                st.session_state.expression = evaluate_expression(st.session_state.expression)
            elif btn in ["sin", "cos", "tan", "log"]:
                st.session_state.expression += f"math.{btn}("
            else:
                st.session_state.expression += btn

st.markdown("</div>", unsafe_allow_html=True)
