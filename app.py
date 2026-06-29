import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Smart Education Dashboard",
    layout="wide"
)

# ---------------------------
# Load Data
# ---------------------------
df = pd.read_excel("smart education analytics.csv.xlsx")

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("📊 Filters")

dept = st.sidebar.multiselect(
    "Select Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

sem = st.sidebar.multiselect(
    "Select Semester",
    df["Semester"].unique(),
    default=df["Semester"].unique()
)

# Filtered Data
filtered_df = df[
    (df["Department"].isin(dept)) &
    (df["Semester"].isin(sem))
]

# ---------------------------
# Title
# ---------------------------
st.title("🎓 Smart Education Analytics Dashboard")

# ---------------------------
# KPI Cards
# ---------------------------
st.subheader("📌 Key Insights")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Total Students", len(filtered_df))
col2.metric("📊 Avg Marks", round(filtered_df["Total Marks"].mean(), 2))
col3.metric("📈 Avg Attendance", f"{round(filtered_df['Attendance (%)'].mean(), 2)}%")
col4.metric("🏆 Top Score", filtered_df["Total Marks"].max())

# ---------------------------
# Row 1
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🎓 Department-wise Students")
    dept_chart = filtered_df["Department"].value_counts().reset_index()
    dept_chart.columns = ["Department", "Count"]
    fig1 = px.bar(dept_chart, x="Department", y="Count", color="Department")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📘 Average Marks by Subject")
    sub_chart = filtered_df.groupby("Subject")["Total Marks"].mean().reset_index()
    fig2 = px.bar(sub_chart, x="Subject", y="Total Marks", color="Subject")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# Row 2
# ---------------------------
col3, col4 = st.columns(2)

with col3:
    st.subheader("🏆 Grade Distribution")
    grade_chart = filtered_df["Grade"].value_counts().reset_index()
    grade_chart.columns = ["Grade", "Count"]
    fig3 = px.pie(grade_chart, names="Grade", values="Count")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📈 Attendance vs Total Marks")
    fig4 = px.scatter(
        filtered_df,
        x="Attendance (%)",
        y="Total Marks",
        color="Department",
        hover_data=["Student_Name"]
    )
    st.plotly_chart(fig4, use_container_width=True)

# ---------------------------
# Row 3
# ---------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("📅 Semester-wise Average Marks")
    sem_chart = filtered_df.groupby("Semester")["Total Marks"].mean().reset_index()
    fig5 = px.line(sem_chart, x="Semester", y="Total Marks", markers=True)
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.subheader("🥇 Top 10 Students")
    top10 = filtered_df.nlargest(10, "Total Marks")
    fig6 = px.bar(
        top10,
        x="Total Marks",
        y="Student_Name",
        orientation="h",
        color="Total Marks"
    )
    st.plotly_chart(fig6, use_container_width=True)

# ---------------------------
# Data Table
# ---------------------------
st.subheader("📄 Student Data")
st.dataframe(filtered_df)
st.success("Dashboard loaded successfully")