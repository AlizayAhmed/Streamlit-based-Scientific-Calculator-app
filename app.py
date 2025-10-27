import streamlit as st
import math

# --- PAGE CONFIG ---
st.set_page_config(page_title="Scientific Calculator", layout="centered")

# --- STYLE HELPER ---
def load_custom_css():
    st.markdown("""
        <style>
        body {
            background-color: #F3F6FA;
        }
        .main {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .calculator {
            background-color: #FFFFFF;
            border-radius: 25px;
            padding: 20px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            width: 320px;
        }
        .display {
            background-color: #2E8FFF;
            color: white;
            border-radius: 15px;
            text-align: right;
            font-size: 28px;
            font-weight: bold;
            padding: 15px;
            margin-bottom: 20px;
            overflow-x: auto;
        }
        .button-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        button {
            background: #E5E7EB;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 18px;
            font-weight: 600;
            color: #111827;
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
            transition: 0.2s;
        }
        button:hover {
            transform: scale(1.07);
        }
        .operator { background-color: #3B82F6; color: white; }
        .clear { background-color: #F43F5E; color: white; }
        .equal { background-color: #22C55E; color: white; }
        .scientific { background-color: #A5B4FC; color: #1E3A8A; }
        </style>
    """, unsafe_allow_html=True)


# --- INIT STATE ---
if "expression" not in st.session_state:
    st.session_state.expression = ""

# --- APP UI ---
load_custom_css()

st.markdown("<div class='calculator'>", unsafe_allow_html=True)
st.markdown(f"<div class='display'>{st.session_state.expression or '0'}</div>", unsafe_allow_html=True)

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

# --- BUTTON LAYOUT ---
for row in buttons:
    st.markdown("<div class='button-row'>", unsafe_allow_html=True)
    for btn in row:
        if btn:
            button_class = ""
            if btn in ["+", "-", "×", "÷", "%", "√"]: button_class = "operator"
            if btn in ["C", "CE"]: button_class = "clear"
            if btn == "=": button_class = "equal"
            if btn in ["sin", "cos", "tan", "log", "π", "e", "^"]: button_class = "scientific"

            if st.button(btn, key=btn, use_container_width=False):
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
