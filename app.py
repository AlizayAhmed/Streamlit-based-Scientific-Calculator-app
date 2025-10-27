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
    
    /* Remove all default Streamlit padding and styling */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    html, body, [class*="css"], .stApp {
        margin: 0;
        padding: 0;
        height: 100vh;
        overflow: hidden !important;
        background: #f0f4f8;
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden; height: 0;}
    .stDeployButton {display: none;}
    
    /* Calculator Container */
    .calculator-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100vw;
        height: 100vh;
        background: #f0f4f8;
    }

    .calculator-frame {
        background: white;
        border-radius: 30px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        padding: 25px;
        width: 350px;
    }

    .display-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        font-size: 42px;
        font-weight: 600;
        text-align: right;
        padding: 25px 20px;
        margin-bottom: 20px;
        min-height: 70px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        word-break: break-all;
    }

    /* Button Grid */
    .calc-row {
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
        justify-content: center;
    }

    /* All buttons base style */
    div[data-testid="column"] {
        padding: 0 !important;
    }
    
    .stButton {
        width: 100%;
    }

    .stButton > button {
        width: 70px !important;
        height: 70px !important;
        border-radius: 50% !important;
        border: none !important;
        font-size: 22px !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        transition: all 0.15s ease !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    }

    .stButton > button:active {
        transform: scale(0.98) !important;
    }

    /* Button Colors */
    
    /* Numbers - Light Gray */
    .btn-number > button {
        background: #e5e7eb !important;
        color: #1f2937 !important;
    }

    /* Operators - Blue */
    .btn-operator > button {
        background: #3b82f6 !important;
        color: white !important;
    }

    /* Clear - Red */
    .btn-clear > button {
        background: #ef4444 !important;
        color: white !important;
    }

    /* Delete - Orange/Red */
    .btn-delete > button {
        background: #f97316 !important;
        color: white !important;
    }

    /* Equal - Green */
    .btn-equal > button {
        background: #22c55e !important;
        color: white !important;
    }

    /* Special - Yellow */
    .btn-special > button {
        background: #eab308 !important;
        color: #1f2937 !important;
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
st.markdown("<div class='calculator-wrapper'><div class='calculator-frame'>", unsafe_allow_html=True)
st.markdown(f"<div class='display-box'>{st.session_state.display}</div>", unsafe_allow_html=True)

# Button layout - 5 rows of 4 buttons
button_rows = [
    [("%", "special"), ("√", "special"), ("CE", "delete"), ("C", "clear")],
    [("7", "number"), ("8", "number"), ("9", "number"), ("÷", "operator")],
    [("4", "number"), ("5", "number"), ("6", "number"), ("×", "operator")],
    [("1", "number"), ("2", "number"), ("3", "number"), ("-", "operator")],
    [(".", "number"), ("0", "number"), ("=", "equal"), ("+", "operator")],
]

for row_idx, row in enumerate(button_rows):
    st.markdown(f"<div class='calc-row'>", unsafe_allow_html=True)
    cols = st.columns(4)
    
    for col_idx, (btn_text, btn_class) in enumerate(row):
        with cols[col_idx]:
            st.markdown(f"<div class='btn-{btn_class}'>", unsafe_allow_html=True)
            
            if st.button(btn_text, key=f"btn_{row_idx}_{col_idx}"):
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

st.markdown("</div></div>", unsafe_allow_html=True)
