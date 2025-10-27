import streamlit as st
import math

st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Scientific Calculator")

# Display input boxes
expression = st.text_input("Enter Expression", placeholder="e.g., sin(30) + log(10) * sqrt(16)")

# Define allowed functions and constants
allowed_names = {
    name: obj for name, obj in math.__dict__.items() if not name.startswith("__")
}
allowed_names.update({
    "pi": math.pi,
    "e": math.e,
    "sqrt": math.sqrt,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "asin": lambda x: math.degrees(math.asin(x)),
    "acos": lambda x: math.degrees(math.acos(x)),
    "atan": lambda x: math.degrees(math.atan(x)),
})

# Evaluate safely
if st.button("Calculate"):
    try:
        # Evaluate using restricted environment
        result = eval(expression, {"__builtins__": None}, allowed_names)
        st.success(f"✅ Result: {result}")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Divider and instructions
st.markdown("---")
st.subheader("🧠 Supported Operations")
st.markdown("""
**Basic:** `+`, `-`, `*`, `/`, `**`, `%`  
**Scientific:** `sin(x)`, `cos(x)`, `tan(x)`, `asin(x)`, `acos(x)`, `atan(x)`  
**Logarithmic:** `log(x)`, `log10(x)`  
**Roots & Powers:** `sqrt(x)`, `x**y`  
**Constants:** `pi`, `e`  
👉 Angles are in degrees for trig functions.
""")

st.caption("Developed by your hired developer 💻")
