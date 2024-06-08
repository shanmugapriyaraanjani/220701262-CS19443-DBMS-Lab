import streamlit as st
import mysql.connector
from database.schema import create_connection

def load_admin_details(admin_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE admin_id = %s", (admin_id,))
    admin_details = cursor.fetchone()
    conn.close()
    return admin_details

def search_records(table, sort_by, search_term):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table} WHERE {sort_by} LIKE %s"
    cursor.execute(query, (f"%{search_term}%",))
    results = cursor.fetchall()
    conn.close()
    return results

def update_patient_data(patient_id, name, email, phone, address, dob, doctor_id):
    conn = create_connection()
    cursor = conn.cursor()
    #query = """
       # UPDATE patients
       # SET name = %s, email = %s, phone = %s, address = %s, dob = %s, doctor_id = %s
        #WHERE patient_id = %s
    #"""
    cursor.execute(
        'INSERT INTO Patients (name, email, phone, address, dob, doctor_id) VALUES (%s, %s, %s, %s, %s, %s)',
        (name, email, phone, address, dob, doctor_id))
    #cursor.execute(query, (name, email, phone, address, dob, doctor_id, patient_id))
    conn.commit()
    conn.close()

def update_doctor_data(doctor_id, name, email, specialty, phone, department_id):
    conn = create_connection()
    cursor = conn.cursor()
    #query = """
      #  UPDATE doctors
       # SET name = %s, email = %s, specialization = %s, phone = %s, department = %s
       # WHERE doctor_id = %s
   # """

    cursor.execute(
        'INSERT INTO Doctors (doctor_id,name, email, specialty, phone, department_id) VALUES (%s,%s, %s, %s, %s, %s)',
        (doctor_id,name, email, specialty, phone, department_id))
    #cursor.execute(query, (name, email, specialization, phone, department, doctor_id))
    conn.commit()
    conn.close()

def admin_dashboard():
    if "user_id" not in st.session_state:
        st.warning("Please log in first.")
        st.stop()

    admin_id = st.session_state.user_id
    admin_details = load_admin_details(admin_id)

    if admin_details:
        st.title("Admin Dashboard")
        st.subheader("Personal Details")
        st.write(f"Name: {admin_details[1]}")
        st.write(f"Email: {admin_details[2]}")

        st.subheader("Search Records")
        entity = st.selectbox("Entity", ["patients", "doctors"])
        sort_by = st.selectbox("Sort by", ["name", "email", "phone"])
        search_term = st.text_input("Search Term")
        search_button = st.button("Search")

        if search_button:
            results = search_records(entity, sort_by, search_term)
            if results:
                st.write(f"Found {len(results)} records:")
                for record in results:
                    st.write(record)
            else:
                st.write("No records found.")

        st.subheader("Update Data")
        update_option = st.selectbox("Update", ["Patient Data", "Doctor Data"])

        if update_option == "Patient Data":
            patient_id = st.text_input("Patient ID")
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_input("Address")
            date_of_birth = st.date_input("Dob")
            doctor_id = st.text_input("Doctor ID")
            update_patient_button = st.button("Update Patient Data")

            if update_patient_button:
                update_patient_data(patient_id, name, email, phone, address, date_of_birth, doctor_id)
                st.success("Patient data updated successfully.")

        elif update_option == "Doctor Data":
            doctor_id = st.text_input("Doctor ID")
            name = st.text_input("Name")
            email = st.text_input("Email")
            specialization = st.text_input("Specialty")
            phone = st.text_input("Phone")
            department = st.text_input("Department")
            update_doctor_button = st.button("Update Doctor Data")

            if update_doctor_button:
                update_doctor_data(doctor_id, name, email, specialization, phone, department)
                st.success("Doctor data updated successfully.")
