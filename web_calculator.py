import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Web Calculator",
    layout="centered"
)

# Title
st.title(" Web Calculator")
st.write("Simple calculator using Streamlit")

# Inputs
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

# Operation selection
operation = st.selectbox(
    "Choose operation",
    ("Addition", "Subtraction", "Multiplication", "Division")
)

# Calculate button
if st.button("Calculate"):
    if operation == "Addition":
        result = num1 + num2
    elif operation == "Subtraction":
        result = num1 - num2
    elif operation == "Multiplication":
        result = num1 * num2
    elif operation == "Division":
        if num2 == 0:
            st.error("Division by zero is not allowed")
            result = None
        else:
            result = num1 / num2

    if result is not None:
        st.success(f"Result: {result}")




