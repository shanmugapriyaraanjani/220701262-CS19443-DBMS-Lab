from database.schema import create_connection

def login_user(table, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM {table} WHERE email=%s AND password=%s"
    cursor.execute(query, (email, password))
    row = cursor.fetchone()
    conn.close()
    return row

def check_password_null(table, email):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"SELECT password FROM {table} WHERE email=%s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0] is None:
        return True
    return False

def set_password(table, email, new_password):
    conn = create_connection()
    cursor = conn.cursor()
    query = f"UPDATE {table} SET password=%s WHERE email=%s"
    cursor.execute(query, (new_password, email))
    conn.commit()
    conn.close()
