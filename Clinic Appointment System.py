import sqlite3
from datetime import datetime

# Initialize SQLite database
conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

# Create tables
def initialize_database():
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        contact TEXT NOT NULL,
                        birth_date TEXT NOT NULL
                      )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER,
                        date TEXT NOT NULL,
                        time TEXT NOT NULL,
                        status TEXT DEFAULT 'Scheduled',
                        notes TEXT,
                        FOREIGN KEY(patient_id) REFERENCES patients(id)
                      )''')
    conn.commit()

# Add a new patient
def add_patient():
    name = input("Enter patient name: ")
    contact = input("Enter contact number: ")
    birth_date = input("Enter birth date (YYYY-MM-DD): ")
    
    cursor.execute("INSERT INTO patients (name, contact, birth_date) VALUES (?, ?, ?)",
                   (name, contact, birth_date))
    conn.commit()
    print("Patient added successfully!")

# Schedule a new appointment
def schedule_appointment():
    patient_id = input("Enter patient ID: ")
    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter appointment time (HH:MM): ")
    notes = input("Enter any additional notes for the appointment: ")
    
    cursor.execute("INSERT INTO appointments (patient_id, date, time, notes) VALUES (?, ?, ?, ?)",
                   (patient_id, date, time, notes))
    conn.commit()
    print("Appointment scheduled successfully!")

# View all patients
def view_patients():
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    print("\nPatients:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Contact: {row[2]}, Birth Date: {row[3]}")

# View appointments
def view_appointments():
    cursor.execute('''SELECT appointments.id, patients.name, appointments.date, appointments.time, appointments.status, appointments.notes 
                      FROM appointments 
                      JOIN patients ON appointments.patient_id = patients.id''')
    rows = cursor.fetchall()
    print("\nAppointments:")
    for row in rows:
        print(f"ID: {row[0]}, Patient: {row[1]}, Date: {row[2]}, Time: {row[3]}, Status: {row[4]}, Notes: {row[5]}")

# Update an appointment
def update_appointment():
    appointment_id = input("Enter appointment ID to update: ")
    new_date = input("Enter new date (YYYY-MM-DD): ")
    new_time = input("Enter new time (HH:MM): ")
    new_notes = input("Enter new notes: ")
    
    cursor.execute("UPDATE appointments SET date = ?, time = ?, notes = ? WHERE id = ?",
                   (new_date, new_time, new_notes, appointment_id))
    conn.commit()
    print("Appointment updated successfully!")

# Cancel an appointment
def cancel_appointment():
    appointment_id = input("Enter appointment ID to cancel: ")
    cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE id = ?", (appointment_id,))
    conn.commit()
    print("Appointment cancelled successfully!")

# Delete a patient and their appointments
def delete_patient():
    patient_id = input("Enter patient ID to delete: ")
    cursor.execute("DELETE FROM appointments WHERE patient_id = ?", (patient_id,))
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    print("Patient and their appointments deleted successfully!")

# Main menu
def main_menu():
    while True:
        print("\nClinic Appointment System")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Schedule Appointment")
        print("4. View Appointments")
        print("5. Update Appointment")
        print("6. Cancel Appointment")
        print("7. Delete Patient")
        print("8. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_patient()
        elif choice == '2':
            view_patients()
        elif choice == '3':
            schedule_appointment()
        elif choice == '4':
            view_appointments()
        elif choice == '5':
            update_appointment()
        elif choice == '6':
            cancel_appointment()
        elif choice == '7':
            delete_patient()
        elif choice == '8':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Initialize database and start program
if __name__ == "__main__":
    initialize_database()
    main_menu()
    conn.close()
