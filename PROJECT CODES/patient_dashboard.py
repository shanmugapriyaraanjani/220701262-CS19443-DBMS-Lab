import streamlit as st
import mysql.connector
from database.schema import create_connection

def load_patient_details(patient_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    patient_details = cursor.fetchone()
    conn.close()
    return patient_details

def search_doctors(sort_by, search_term):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM doctors WHERE {sort_by} LIKE %s"
    cursor.execute(query, (f"%{search_term}%",))
    doctor_results = cursor.fetchall()
    conn.close()
    return doctor_results

def patient_dashboard():
    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        st.stop()

    patient_id = st.session_state.user_id
    patient_details = load_patient_details(patient_id)

    if patient_details:
        st.title("Patient Dashboard")
        st.subheader("Personal Details")
        st.write(f"Name: {patient_details[1]}")
        st.write(f"Email: {patient_details[2]}")
        st.write(f"Age: {patient_details[3]}")
        st.write(f"Gender: {patient_details[4]}")
        st.write(f"Phone: {patient_details[5]}")
        st.write(f"Address: {patient_details[6]}")

        st.subheader("Search Doctors")
        sort_by = st.selectbox("Sort by", ["name", "email", "specialization", "phone"])
        search_term = st.text_input("Search Term")
        search_button = st.button("Search")

        if search_button:
            results = search_doctors(sort_by, search_term)
            if results:
                st.write(f"Found {len(results)} doctors:")
                for doctor in results:
                  with st.expander(str(doctor[0])):
                    st.write(f"Name: {doctor[1]}")
                    st.write(f" Email: {doctor[2]}")
                    st.write(f"Specialization: {doctor[3]}")
                    st.write(f"Phone: {doctor[4]}")
            else:
                st.write("No doctors found.")
    else:
        st.write("Patient details not found.")

