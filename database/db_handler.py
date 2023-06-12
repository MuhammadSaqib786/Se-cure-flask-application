import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('securedb.db')       
        print(f'Successful connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(f'Error {e} occurred')

    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def register_user(conn, patient):
    try:
        print(patient)
        sql = ''' INSERT INTO Patients(patient_email, name, gender, address, phone, password) 
                VALUES(?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, patient)
        conn.commit()
        conn.close()
        return cur.lastrowid
    except Exception as e:
        print(e)
        return None
    

def login_user(conn, patient_email, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Patients WHERE patient_email=? AND password=?", (patient_email, password,))
    rows = cur.fetchall()
    return rows

def add_appointment(conn, appointment):
    sql = ''' INSERT INTO Appointment(doctor_id, patient_id, date_time)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, appointment)
    return cur.lastrowid

def add_doctor(conn, doctor):
    sql = ''' INSERT INTO Doctors(doctorname, email, gender, specialization)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, doctor)
    
    return cur.lastrowid

def deleteDoctors():
    conn = create_connection()
    sql = 'Delete From Doctors'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    

def get_all_doctors():
    conn= create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Doctors")
    rows = cur.fetchall()
    return rows

def add_appointment(conn, appointment):
    sql = ''' INSERT INTO Appointment(doctor_id, patient_id, date_time) VALUES(?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, appointment)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False



def main():
    

    sql_create_patients_table = """ CREATE TABLE IF NOT EXISTS Patients (
                                        patient_email text PRIMARY KEY,
                                        name text NOT NULL,
                                        gender text NOT NULL,
                                        address text NOT NULL,
                                        phone text NOT NULL,
                                        password text NOT NULL
                                    ); """

    sql_create_doctors_table = """ CREATE TABLE IF NOT EXISTS Doctors (
                                        doctor_id integer PRIMARY KEY,
                                        doctorname text NOT NULL,
                                        email text NOT NULL,
                                        gender text NOT NULL,
                                        specialization text NOT NULL
                                    ); """
    
    sql_create_appointments_table = """ CREATE TABLE IF NOT EXISTS Appointment (
                                            appointment_id integer PRIMARY KEY,
                                            doctor_id integer NOT NULL,
                                            patient_id text NOT NULL,
                                            date_time text NOT NULL,
                                            FOREIGN KEY (doctor_id) REFERENCES Doctors (doctor_id),
                                            FOREIGN KEY (patient_id) REFERENCES Patients (patient_email)
                                        ); """

    conn = create_connection()

    if conn is not None:
        create_table(conn, sql_create_patients_table)
        create_table(conn, sql_create_doctors_table)
        create_table(conn, sql_create_appointments_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        doctor1 = ('Dr. Ahmed', 'dr.ahmed@example.com', 'Male', 'Cardiology')
        doctor2 = ('Dr. Fatima', 'dr.fatima@example.com', 'Female', 'Neurology')
        doctor3 = ('Dr. Abdul', 'dr.abdul@example.com', 'Male', 'Orthopedics')
        doctor4 = ('Dr. Sara', 'dr.sara@example.com', 'Female', 'Dermatology')
        doctor5 = ('Dr. Rashid', 'dr.rashid@example.com', 'Male', 'Pediatrics')

        add_doctor(conn, doctor1)
        add_doctor(conn, doctor2)
        add_doctor(conn, doctor3)
        add_doctor(conn, doctor4)
        add_doctor(conn, doctor5)

def get_patient():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Patients LIMIT 1")
    data = cur.fetchone()
    conn.close()
    return list(data) if data else None

def get_patient_details(conn, patient_email):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Patients WHERE patient_email=?", (patient_email,))
    return cur.fetchone()


def get_appointments_for_user(conn, patient_id):
    cur = conn.cursor()
    cur.execute("SELECT a.appointment_id, a.date_time, d.doctorname FROM Appointment a JOIN Doctors d ON a.doctor_id = d.doctor_id WHERE a.patient_id=?", (patient_id,))
    return cur.fetchall()



if __name__ == '__main__':
    #main()  #to create tables and add doctors
    #print(get_appointments_for_user(create_connection(),"saqisaqi.sk@gmail.com"))
    pass

