# signup.py
from database.schema import create_connection

def insert_user(table, name, email, phone, password, **kwargs):
    conn = create_connection()
    cursor = conn.cursor()
    if table == 'Doctors':
        specialty = kwargs.get('specialty')
        department_id = kwargs.get('department_id')
        cursor.execute('INSERT INTO Doctors (name, email, specialty, phone, department_id, password) VALUES (%s, %s, %s, %s, %s, %s)',
                       (name, email, specialty, phone, department_id, password))
    elif table == 'Patients':
        address = kwargs.get('address')
        dob = kwargs.get('dob')
        doctor_id = kwargs.get('doctor_id')
        cursor.execute('INSERT INTO Patients (name, email, phone, address, dob, doctor_id, password) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                       (name, email, phone, address, dob, doctor_id, password))
    elif table == 'Admins':
        role = kwargs.get('role')
        department_id = kwargs.get('department_id')
        cursor.execute('INSERT INTO Admins (name, email, phone, role, department_id, password) VALUES (%s, %s, %s, %s, %s, %s)',
                       (name, email, phone, role, department_id, password))
    conn.commit()
    conn.close()
