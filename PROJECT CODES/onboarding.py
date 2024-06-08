import streamlit as st
import login


def main():
    st.sidebar.title("Welcome to Hospital Management System")

    if "page" in st.experimental_get_query_params():
        page = st.experimental_get_query_params()["page"][0]
        if page == "doctor_dashboard":
            import doctor_dashboard
            doctor_dashboard.doctor_dashboard()
        # Add similar imports and calls for patient and admin dashboards
    else:
        login.main()


