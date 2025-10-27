import streamlit as st
import math

st.set_page_config(page_title="Scientific Calculator", layout="centered")

# --- INITIAL STATE ---
if "expression" not in st.session_state:
    st.session_state.expression = ""
if "display" not in st.session_state:
    st.session_state.display = "0"

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        height: 100%;
        overflow: hidden !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    
    /* Hide Streamlit elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}

    .calculator-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        width: 320px;
        padding: 30px 25px;
    }

    .display-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        font-size: 36px;
        font-weight: 600;
        text-align: right;
        padding: 20px;
        margin-bottom: 25px;
        min-height: 60px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        overflow-x: auto;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .button-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
    }

    .stButton {
        width: 100%;
        height: 100%;
    }

    .stButton > button {
        width: 65px !important;
        height: 65px !important;
        border-radius: 50% !important;
        border: none !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
        padding: 0 !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* Number buttons - light purple */
    .btn-number > button {
        background: #e8eaf6 !important;
        color: #1a1a2e !important;
    }

    /* Operator buttons - blue */
    .btn-operator > button {
        background: #2196F3 !important;
        color: white !important;
    }

    /* Clear button - dark blue */
    .btn-clear > button {
        background: #1a237e !important;
        color: white !important;
    }

    /* Delete button - red */
    .btn-delete > button {
        background: #f44336 !important;
        color: white !important;
    }

    /* Equal button - green */
    .btn-equal > button {
        background: #4CAF50 !important;
        color: white !important;
    }

    /* Special function buttons - yellow/orange */
    .btn-special > button {
        background: #FFC107 !important;
        color: #1a1a2e !important;
    }

    .stButton > button p {
        margin: 0 !important;
        padding: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNCTIONS ---
def append_to_expression(value):
    if st.session_state.display == "0" or st.session_state.display == "Error":
        st.session_state.expression = value
        st.session_state.display = value
    else:
        st.session_state.expression += value
        st.session_state.display = st.session_state.expression

def clear_all():
    st.session_state.expression = ""
    st.session_state.display = "0"

def delete_last():
    if st.session_state.expression:
        st.session_state.expression = st.session_state.expression[:-1]
        st.session_state.display = st.session_state.expression if st.session_state.expression else "0"

def calculate():
    try:
        expr = st.session_state.expression
        expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
        expr = expr.replace("π", str(math.pi)).replace("√", "math.sqrt")
        
        result = eval(expr, {"math": math, "__builtins__": None})
        
        if isinstance(result, float):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)
        
        st.session_state.display = str(result)
        st.session_state.expression = str(result)
    except:
        st.session_state.display = "Error"
        st.session_state.expression = ""

# --- LAYOUT ---
st.markdown("<div class='calculator-container'>", unsafe_allow_html=True)
st.markdown(f"<div class='display-box'>{st.session_state.display}</div>", unsafe_allow_html=True)
st.markdown("<div class='button-grid'>", unsafe_allow_html=True)

# Button layout matching the image
buttons = [
    ("%", "special"), ("√", "special"), ("CE", "delete"), ("C", "clear"),
    ("7", "number"), ("8", "number"), ("9", "number"), ("÷", "operator"),
    ("4", "number"), ("5", "number"), ("6", "number"), ("×", "operator"),
    ("1", "number"), ("2", "number"), ("3", "number"), ("-", "operator"),
    (".", "number"), ("0", "number"), ("=", "equal"), ("+", "operator"),
]

# Create buttons in a 4-column layout
cols = st.columns(4)

for i, (btn_text, btn_class) in enumerate(buttons):
    col_idx = i % 4
    
    with cols[col_idx]:
        st.markdown(f"<div class='btn-{btn_class}'>", unsafe_allow_html=True)
        
        if st.button(btn_text, key=f"btn_{i}"):
            if btn_text == "C":
                clear_all()
            elif btn_text == "CE":
                delete_last()
            elif btn_text == "=":
                calculate()
            elif btn_text == "√":
                append_to_expression("math.sqrt(")
            else:
                append_to_expression(btn_text)
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
