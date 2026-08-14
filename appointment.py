import customtkinter as ctk
import sqlite3

# ========================== TABLE =================================================================================================
def create_appointments_table():
    connection = sqlite3.connect("careflow.db")
    cursor = connection.cursor()

    cursor.execute(
        """
         CREATE TABLE IF NOT EXISTS appointments(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          patient TEXT NOT NULL,
          doctor TEXT NOT NULL,
          date TEXT NOT NULL,
          time TEXT NOT NULL,
          reason TEXT NOT NULL,
          status TEXT NOT NULL
         )
        """
    )

    connection.commit()
    connection.close()


# ======================================== FORM =======================================================================================
def add_appointment(app, main_frame):

    form = ctk.CTkToplevel(app)
    form.title("Add Appointment")
    form.geometry("400x550")

    # Patient
    patient_label = ctk.CTkLabel(
        form,
        text="Patient Name"
    )
    patient_label.pack(pady=(20, 5))

    patient_entry = ctk.CTkEntry(
        form,
        placeholder_text="Enter patient's name"
    )
    patient_entry.pack(pady=5)

    # Doctor
    doctor_label = ctk.CTkLabel(
        form,
        text="Doctor's Name"
    )
    doctor_label.pack(pady=(20, 5))

    doctor_entry = ctk.CTkEntry(
        form,
        placeholder_text="Enter doctor's name"
    )
    doctor_entry.pack(pady=5)

    # Date
    date_label = ctk.CTkLabel(
        form,
        text="Date"
    )
    date_label.pack(pady=(20, 5))

    date_entry = ctk.CTkEntry(
        form,
        placeholder_text="e.g. 15/08/2026"
    )
    date_entry.pack(pady=5)

    # Time
    time_label = ctk.CTkLabel(
        form,
        text="Time"
    )
    time_label.pack(pady=(20, 5))

    time_entry = ctk.CTkEntry(
        form,
        placeholder_text="e.g. 10.00 AM"
    )
    time_entry.pack(pady=5)

    # Reason
    reason_label = ctk.CTkLabel(
        form,
        text="Reason"
    )
    reason_label.pack(pady=(20, 5))

    reason_entry = ctk.CTkEntry(
        form,
        placeholder_text="Reason for appointment"
    )
    reason_entry.pack(pady=5)

    # Status
    status_label = ctk.CTkLabel(
        form,
        text="Status"
    )
    status_label.pack(pady=(20, 5))

    status_entry = ctk.CTkComboBox(
        form,
        values=["Pending", "Completed", "Cancelled"]
    )
    status_entry.pack(pady=5)
    status_entry.set("Pending")

    # =================================== SAVE APPOINTMENT =============================================================================

    def save_appointment():
        patient = patient_entry.get()
        doctor = doctor_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        reason = reason_entry.get()
        status = status_entry.get()

        connection = sqlite3.connect("careflow.db")
        cursor = connection.cursor()

        cursor.execute(
            """
             INSERT INTO appointments (patient, doctor,date, time, reason, status)
             VALUES (?, ?, ?, ?, ?, ?)
            """,
            (patient, doctor,date, time, reason, status)
        )

        connection.commit()
        connection.close()

        print("Appointment saved")

        form.destroy() # Closes the pop up after saving

        show_appointments(main_frame, app)

    save_btn = ctk.CTkButton(
        form,
        text="Save Appointment",
        fg_color="purple",
        hover_color="darkviolet",
        command=save_appointment
    )
    save_btn.pack(pady=25)



def load_appointments():

    connection = sqlite3.connect("careflow.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, patient, doctor, date, time, reason,status FROM appointments"
    )

    appointments = cursor.fetchall()
    print("DATABASE APPOINTMENT", appointments)
    connection.close()

    return appointments

# ========================================== UPDATE APPOINTMENTS ======================================================================================
def update_appointment(appointment_id, app,  main_frame):

    connection = sqlite3.connect("careflow.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT patient, doctor, date, time, reason, status FROM appointments WHERE id= ?
        """,
        (appointment_id,)
    )

    appointment = cursor.fetchone()

    connection.close()

    # EDIT WINDOW
    form = ctk.CTkToplevel(app)
    form.title("Edit Appointment")
    form.geometry("400x550")

    # Patient
    patient_label = ctk.CTkLabel(
        form,
        text="Patient Name"
    )
    patient_label.pack(pady=(20,5))

    patient_entry = ctk.CTkEntry(form)
    patient_entry.pack(pady=5)
    patient_entry.insert(0, appointment[0])

    
    # Doctor
    doctor_label = ctk.CTkLabel(
        form,
        text="Doctor's name"
    )
    doctor_label.pack(pady=(15,5))

    doctor_entry = ctk.CTkEntry(form)
    doctor_entry.pack(pady=5)
    doctor_entry.insert(0, appointment[1])

    # Date
    date_label = ctk.CTkLabel(
        form,
        text="Date"
    )
    date_label.pack(pady=(15,5))

    date_entry = ctk.CTkEntry(form)
    date_entry.pack(pady=5)
    date_entry.insert(0, appointment[2])

    # Time
    time_label = ctk.CTkLabel(
        form,
        text="Time"
    )
    time_label.pack(pady=(15,5))

    time_entry = ctk.CTkEntry(form)
    time_entry.pack(pady=5)
    time_entry.insert(0, appointment[3])

    # Reason
    reason_label = ctk.CTkLabel(
        form,
        text="Reason"
    )
    reason_label.pack(pady=(15,5))

    reason_entry = ctk.CTkEntry(form)
    reason_entry.pack(pady=5)
    reason_entry.insert(0, appointment[4])

    # status
    status_label = ctk.CTkLabel(
        form,
        text="Status"
    )
    status_label.pack(pady=(15,5))

    status_entry = ctk.CTkComboBox(
        form,
        values=[
            "pending",
            "In progress",
            "Completed",
            "Cancelled"
        ]
    )
    status_entry.pack(pady=5)
    status_entry.set(appointment[5])

    # SAVE CHANGES
    def save_changes():

        patient = patient_entry.get()
        doctor = doctor_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        reason = reason_entry.get()
        status = status_entry.get()

        connection = sqlite3.connect("careflow.db")
        cursor=connection.cursor()

        cursor.execute(
            """
            UPDATE appointments SET patient = ?, doctor = ?, date = ?, time = ?, reason = ?, status = ? WHERE id = ?
            """,
            (patient, doctor, date, time, reason, status, appointment_id)
        )

        connection.commit()
        connection.close()

        form.destroy()

        show_appointments(main_frame, app)

    update_btn = ctk.CTkButton(
        form,
        text="Save Changes",
        fg_color="purple",
        hover_color="darkviolet",
        command=save_changes
    )
    update_btn.pack(pady=25)


# =========================================== SHOW APPOINTMENTS ===============================================================================

def show_appointments(main_frame, app):

    print("SHOW APPOINTMENTS CALLED")

    # Remove everything currently inside the main app
    for widget in main_frame.winfo_children():
        widget.destroy()

        # Appointments title
    appointments_title = ctk.CTkLabel(
            main_frame,
            text="Appointments",
            font=("Arial",28, "bold")
        )

    appointments_title.pack(
            anchor="w",
            padx=30,
            pady=30
        )

        # ================= ADD APPOINTMENT BUTTON ================================
    add_appointment_button = ctk.CTkButton(
            main_frame,
            text="+ Add Appointment",
            fg_color="purple",
            hover_color="darkviolet",
            command=lambda: add_appointment(app, main_frame)
        )

    add_appointment_button.pack(
            anchor="w",
            pady=10,
            padx=30
        )

        # get appointment from database
    appointments = load_appointments()

        # ============================= TABLE HEADER ========================================================
    header = ctk.CTkFrame(
        main_frame,
        fg_color="purple"
    )
    header.pack(
        fill="x",
        padx=30,
        pady=(20, 0)
    )
    # ID
    ctk.CTkLabel(
        header,
        text="ID",
        text_color="white",
        font=("Arial", 14, "bold"),
        width=40
    ).pack(
        side="left",
        padx=10,
        pady=10
    )
    # PATIENT
    ctk.CTkLabel(
        header,
        text="Patient",
        text_color="white",
        font=("Arial", 14, "bold"),
        width=120
    ).pack(
        side="left",
        padx=10,
        pady=10
    )
    
    # DOCTOR
    ctk.CTkLabel(
        header,
        text="Doctor",
        text_color="white",
        font=("Arial", 14, "bold"),
        width=120
    ).pack(
        side="left",
        padx=10,
        pady=10
    )
    # DATE
    ctk.CTkLabel(
        header,
        text="Date",
        text_color="white",
        font=("Arial", 14, "bold"),
        width=100
    ).pack(
        side="left",
        padx=10,
        pady=10
    )
    # TIME
    ctk.CTkLabel(
        header,
        text="Time",
        text_color="white",
        font=("Arial", 14, "bold"),
        width=90
    ).pack(
        side="left",
        padx=10,
        pady=10
    )
    # STATUS
    ctk.CTkLabel(
        header,
        text="Status",
        text_color="white",
        font=("Arial", 14, "bold"),
        width=100
    ).pack(
        side="left",
        padx=10,
        pady=10
    )
    # ================ APPOINTMENT ROWS =======================================================================================
    for appointment in appointments:
        row = ctk.CTkFrame(
            main_frame,
            fg_color="white"
        )
        row.pack(
            fill="x",
            padx=30,
            pady=2
        )
        # ID
        ctk.CTkLabel(
            row,
            text=str(appointment[0]),
            width=40
        ).pack(
            side="left",
            padx=10,
            pady=8
        )
        # Patient
        ctk.CTkLabel(
            row,
            text=appointment[1],
            width=120
        ).pack(
            side="left",
            padx=10,
            pady=8
        )
        
        # Doctor
        ctk.CTkLabel(
            row,
            text=appointment[2],
            width=120
        ).pack(
            side="left",
            padx=10,
            pady=8
        )
        
        # Date
        ctk.CTkLabel(
            row,
            text=appointment[3],
            width=100
        ).pack(
            side="left",
            padx=10,
            pady=8
        )
        
        # Time
        ctk.CTkLabel(
            row,
            text=appointment[4],
            width=90
        ).pack(
            side="left",
            padx=10,
            pady=8
        )
        
        # Status
        ctk.CTkLabel(
            row,
            text=appointment[6],
            width=100
        ).pack(
            side="left",
            padx=10,
            pady=8
        )

        edit_btn = ctk.CTkButton(
            row,
            text="Edit",
            fg_color="purple",
            hover_color="darkviolet",
            command=lambda appointment_id=appointment[0]: update_appointment(appointment_id, app, main_frame)
        )

        edit_btn.pack(
            side="left",
            padx=10,
            pady=8
        )


create_appointments_table()