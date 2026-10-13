import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Success Platform",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Success Analytics Platform")
st.write("Helping teachers support student success.")

if "students" not in st.session_state:
    st.session_state.students = []

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Choose a page",
    ["Dashboard", "Add Student", "Student Reports"]
)

if page == "Add Student":
    st.header("👩‍🎓 Add Student Details")

    with st.form("student_form"):
        name = st.text_input("Student Name")
        attendance = st.number_input(
            "Attendance (%)", 0.0, 100.0, 75.0
        )
        marks = st.number_input(
            "Marks out of 100", 0.0, 100.0, 50.0
        )
        assignments = st.number_input(
            "Assignments completed out of 10",
            0, 10, 5
        )

        submitted = st.form_submit_button("Analyze Student")

    if submitted:
        if not name.strip():
            st.error("Please enter a student name.")
        else:
            if attendance < 75 and marks < 40:
                status = "Academic Support"
                recommendation = (
                    "Discuss learning difficulties and offer tutoring."
                )
            elif attendance < 75:
                status = "Attendance Support"
                recommendation = (
                    "Discuss attendance barriers with a mentor."
                )
            elif marks < 40:
                status = "Learning Support"
                recommendation = (
                    "Offer extra learning materials and tutoring."
                )
            elif assignments < 5:
                status = "Assignment Support"
                recommendation = (
                    "Help the student plan pending assignments."
                )
            else:
                status = "Good Progress"
                recommendation = (
                    "Continue current learning habits."
                )

            st.session_state.students.append({
                "Name": name.strip(),
                "Attendance": attendance,
                "Marks": marks,
                "Assignments": assignments,
                "Status": status,
                "Recommendation": recommendation
            })

            st.success("Student analysis completed!")
            st.write("Status:", status)
            st.info(recommendation)

elif page == "Dashboard":
    st.header("📊 Class Dashboard")

    if st.session_state.students:
        df = pd.DataFrame(st.session_state.students)

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Students", len(df))
        col2.metric("Average Marks", round(df["Marks"].mean(), 2))
        col3.metric(
            "Average Attendance",
            f"{df['Attendance'].mean():.1f}%"
        )

        flagged = (df["Status"] != "Good Progress").sum()
        st.metric("Students Flagged for Support", int(flagged))

        st.subheader("Student Marks")
        st.bar_chart(df.set_index("Name")["Marks"])

        st.subheader("Student Attendance")
        st.bar_chart(df.set_index("Name")["Attendance"])
    else:
        st.info("Add students to view the dashboard.")

else:
    st.header("📋 Student Reports")

    if st.session_state.students:
        df = pd.DataFrame(st.session_state.students)
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download Student Report",
            df.to_csv(index=False),
            "student_report.csv",
            "text/csv"
        )
    else:
        st.info("No student records available yet.")
