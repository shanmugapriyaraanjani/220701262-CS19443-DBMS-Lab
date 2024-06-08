# app.py
import streamlit as st
from login import login_user, check_password_null, set_password
from signup import insert_user
from database.schema import create_connection
import doctor_dashboard
import patient_dashboard
import admin_dashboard


def view_data(table):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table}')
    rows = cursor.fetchall()
    conn.close()
    return rows


st.title('Hospital Management System')

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None


def show_login(user_type):
    email = st.text_input('Email', key=f"{user_type}_email")
    password = st.text_input('Password', type='password', key=f"{user_type}_password")

    form = st.form(key=f"{user_type}_form")
    new_password = form.text_input("New Password", type="password", key=f"{user_type}_new_password")
    confirm_password = form.text_input("Confirm Password", type="password", key=f"{user_type}_confirm_password")

    submit_button = form.form_submit_button("Set Password")

    if submit_button:
        if new_password == confirm_password:
            table = user_type + 's'
            set_password(table, email, new_password)
            st.success("Password set successfully. You can now login.")
            st.experimental_rerun()
        else:
            st.error("Passwords do not match.")

    if st.button('Login', key=f"{user_type}_login_button"):
        table = user_type + 's'
        if check_password_null(table, email):
            st.warning("Password not set. Please set your password.")
            form  # Display the form for setting the password
        else:
            user = login_user(table, email, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_role = user_type
                st.session_state.user_id = user[0]
                st.success(f"Welcome, {user[1]}!")
            else:
                st.error("Invalid Credentials")


def show_register(user_type):
    st.subheader(f'{user_type} Register')
    name = st.text_input('Name', key=f"{user_type}_name")
    email = st.text_input('Email', key=f"{user_type}_email_reg")
    phone = st.text_input('Phone', key=f"{user_type}_phone")
    password = st.text_input('Password', type='password', key=f"{user_type}_password_reg")
    confirm_password = st.text_input('Confirm Password', type='password', key=f"{user_type}_confirm_password")

    if password != confirm_password:
        st.error('Passwords do not match')
    else:
        if user_type == 'Doctor':
            specialty = st.text_input('Specialty', key=f"{user_type}_specialty")
            department_id = st.number_input('Department ID', min_value=1, key=f"{user_type}_department_id")
            if st.button('Register', key=f"{user_type}_register_button"):
                insert_user('Doctors', name, email, phone, password, specialty=specialty, department_id=department_id)
                st.success('Doctor registered successfully!')

        elif user_type == 'Patient':
            address = st.text_input('Address', key=f"{user_type}_address")
            dob = st.date_input('Date of Birth', key=f"{user_type}_dob")
            doctor_id = st.number_input('Doctor ID', min_value=1, key=f"{user_type}_doctor_id")
            if st.button('Register', key=f"{user_type}_register_button"):
                insert_user('Patients', name, email, phone, password, address=address, dob=dob, doctor_id=doctor_id)
                st.success('Patient registered successfully!')

        elif user_type == 'Admin':
            role_desc = st.text_input('Role Description', key=f"{user_type}_role_desc")
            department_id = st.number_input('Department ID', min_value=1, key=f"{user_type}_department_id")
            if st.button('Register', key=f"{user_type}_register_button"):
                insert_user('Admins', name, email, phone, password, role=role_desc, department_id=department_id)
                st.success('Admin registered successfully!')


if not st.session_state.authenticated:
    st.sidebar.header('User Login')
    user_type = st.sidebar.selectbox('Login as:', ['Doctor', 'Patient', 'Admin'])

    if user_type:
        st.subheader(f"Login as {user_type}")
        show_login(user_type)

if st.session_state.authenticated:
    st.header("Dashboard")

    if st.session_state.user_role == 'Doctor':
        doctor_dashboard.doctor_dashboard()
        # Add more doctor-specific functionality here

    elif st.session_state.user_role == 'Patient':
        patient_dashboard.patient_dashboard()
        # Add more patient-specific functionality here

    elif st.session_state.user_role == 'Admin':
        admin_dashboard.admin_dashboard()
        # Add more admin-specific functionality here

    st.sidebar.button('Logout', on_click=lambda: st.session_state.update(
        {'authenticated': False, 'user_role': None, 'user_id': None}))
