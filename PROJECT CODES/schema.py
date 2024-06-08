import mysql.connector


def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Varsha7279@",
        database="hospital_management"
    )
    return conn


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Departments (
                        department_id INT AUTO_INCREMENT PRIMARY KEY,
                        dept_name VARCHAR(255) NOT NULL,
                        dept_head VARCHAR(255),
                        phone VARCHAR(20),
                        location VARCHAR(255),
                        capacity INT
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Doctors (
                        doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE,
                        specialty VARCHAR(255),
                        phone VARCHAR(20),
                        department_id INT,
                        password VARCHAR(255),
                        FOREIGN KEY (department_id) REFERENCES Departments(department_id)
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Patients (
                        patient_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE,
                        phone VARCHAR(20),
                        address VARCHAR(255),
                        dob DATE,
                        doctor_id INT,
                        password VARCHAR(255),
                        FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id)
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Admins (
                        admin_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE,
                        phone VARCHAR(20),
                        role VARCHAR(255),
                        department_id INT,
                        password VARCHAR(255),
                        FOREIGN KEY (department_id) REFERENCES Departments(department_id)
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Pharmacy (
                        med_id INT AUTO_INCREMENT PRIMARY KEY,
                        med_name VARCHAR(255) NOT NULL,
                        quantity INT,
                        price DECIMAL(10, 2),
                        expiry_date DATE,
                        supplier VARCHAR(255)
                    );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Rooms (
                        room_id INT AUTO_INCREMENT PRIMARY KEY,
                        room_number VARCHAR(50) NOT NULL,
                        room_type VARCHAR(255),
                        status VARCHAR(50),
                        patient_id INT,
                        floor INT,
                        FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
                    );''')

    conn.commit()


if __name__ == "__main__":
    conn = create_connection()
    create_tables(conn)
    conn.close()
