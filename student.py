import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Marks Analysis", layout="wide")
st.title("📊 Student Marks Analysis App")

# Upload CSV
uploaded_file = st.file_uploader("Upload Student Marks CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    st.subheader("📄 Student Marks Database")
    st.dataframe(df)

    # Identify columns
    name_col = "student name"
    subject_cols = [col for col in df.columns if col != name_col]

    # Overall stats
    all_marks = df[subject_cols].values.flatten()

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Average Marks", f"{all_marks.mean():.2f}")
    col2.metric("🏆 Highest Marks", all_marks.max())
    col3.metric("📉 Lowest Marks", all_marks.min())

    # Subject selection
    st.subheader("🎯 Filter by Subject")
    selected_subject = st.selectbox("Select Subject", subject_cols)

    subject_data = df[[name_col, selected_subject]]
    st.dataframe(subject_data)

    # Subject average
    st.info(f"📘 Average marks in {selected_subject}: {subject_data[selected_subject].mean():.2f}")

    # Bar chart using Streamlit
    st.subheader("📊 Marks Distribution")
    st.bar_chart(data=subject_data.set_index(name_col))

else:
    st.info("👆 Upload a CSV file to start analysis")

