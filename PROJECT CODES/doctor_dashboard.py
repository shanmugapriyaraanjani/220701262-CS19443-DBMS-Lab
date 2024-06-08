import streamlit as st
import mysql.connector
from database.schema import create_connection

def load_doctor_details(doctor_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors WHERE doctor_id = %s", (doctor_id,))
    doctor_details = cursor.fetchone()
    conn.close()
    return doctor_details

def search_patients(sort_by, search_term):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM patients WHERE {sort_by} LIKE %s"
    cursor.execute(query, (f"%{search_term}%",))
    patient_results = cursor.fetchall()
    conn.close()
    return patient_results

def doctor_dashboard():
    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        st.stop()

    doctor_id = st.session_state.user_id
    doctor_details = load_doctor_details(doctor_id)

    if doctor_details:
        st.title("Doctor Dashboard")
        st.subheader("Personal Details")
        st.write(f"Name: {doctor_details[1]}")
        st.write(f"Email: {doctor_details[2]}")
        st.write(f"Specialization: {doctor_details[3]}")
        st.write(f"Phone: {doctor_details[4]}")
        st.write(f"Department: {doctor_details[5]}")

        st.subheader("Search Patients")
        sort_by = st.selectbox("Sort by", ["name", "email", "age", "gender"])
        search_term = st.text_input("Search Term")
        search_button = st.button("Search")

        if search_button:
            results = search_patients(sort_by, search_term)
            if results:
                st.write(f"Found {len(results)} patients:")
                for patient in results:
                   with st.expander(str(patient[0])):
                        st.write(f"Name: {patient[1]}")
                        st.write(f"Email: {patient[2]}")
                        st.write(f"Age: {patient[3]}")
                        st.write(f"Gender: {patient[4]}")
            else:
                st.write("No patients found.")
    else:
        st.write("Doctor details not found.")

if __name__ == "__main__":
    doctor_dashboard()
