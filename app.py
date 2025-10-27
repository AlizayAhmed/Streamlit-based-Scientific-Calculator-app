import streamlit as st
import math

st.set_page_config(page_title="Scientific Calculator", layout="centered")

# --- INITIAL STATE ---
if "expression" not in st.session_state:
    st.session_state.expression = ""

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] {
        height: 100%;
        overflow: hidden !important;
        background-color: #f3f6fb;
        font-family: 'Segoe UI', sans-serif;
    }

    .stApp {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background: linear-gradient(145deg, #f5f7fa, #e4ebf3);
    }

    .calculator {
        background-color: #ffffff;
        border-radius: 25px;
        box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.15);
        width: 340px;
        padding: 25px;
        text-align: center;
    }

    .display {
        background: linear-gradient(135deg, #2e8fff, #559dff);
        color: white;
        border-radius: 15px;
        font-size: 30px;
        font-weight: 600;
        text-align: right;
        padding: 18px 15px;
        margin-bottom: 20px;
        overflow-x: auto;
    }

    .button-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        justify-items: center;
        align-items: center;
    }

    button {
        border: none;
        border-radius: 50%;
        width: 65px;
        height: 65px;
        font-size: 20px;
        font-weight: 600;
        cursor: pointer;
        color: #1f2937;
        background: #e7ebf2;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease-in-out;
    }

    button:hover {
        transform: scale(1.07);
    }

    .operator { background-color: #3b82f6; color: white; }
    .clear { background-color: #ef4444; color: white; }
    .equal { background-color: #22c55e; color: white; }
    .scientific { background-color: #a78bfa; color: white; }

    .btn-form {
        margin: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- DISPLAY ---
st.markdown("<div class='calculator'>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.expression or '0'}</div>", unsafe_allow_html=True)
st.markdown("<div class='button-grid'>", unsafe_allow_html=True)

# --- BUTTONS ---
buttons = [
    ["%", "√", "CE", "C"],
    ["sin", "cos", "tan", "log"],
    ["π", "e", "^", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "=", ""]
]

def evaluate_expression(expr):
    expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**").replace("π", str(math.pi)).replace("e", str(math.e))
    expr = expr.replace("√", "math.sqrt")
    try:
        result = eval(expr, {"math": math, "__builtins__": None})
        return str(round(result, 10))
    except:
        return "Error"

# --- BUTTON HANDLING VIA FORMS (to preserve CSS grid alignment) ---
for row in buttons:
    for btn in row:
        if btn:
            btn_class = ""
            if btn in ["+", "-", "×", "÷", "%", "√"]: btn_class = "operator"
            if btn in ["C", "CE"]: btn_class = "clear"
            if btn == "=": btn_class = "equal"
            if btn in ["sin", "cos", "tan", "log", "π", "e", "^"]: btn_class = "scientific"

            with st.form(key=f"form_{btn}", clear_on_submit=True):
                if st.form_submit_button(btn):
                    if btn == "C":
                        st.session_state.expression = ""
                    elif btn == "CE":
                        st.session_state.expression = st.session_state.expression[:-1]
                    elif btn == "=":
                        st.session_state.expression = evaluate_expression(st.session_state.expression)
                    elif btn in ["sin", "cos", "tan", "log", "√"]:
                        st.session_state.expression += f"math.{btn}("
                    else:
                        st.session_state.expression += btn

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
