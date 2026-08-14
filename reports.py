import customtkinter as ctk
import sqlite3

def load_report_data():
    connection = sqlite3.connect("careflow.db")
    cursor = connection.cursor()

    # ==== COUNT PATIENTS =====
    cursor.execute("SELECT COUNT (*) FROM patients")
    patients = cursor.fetchone()[0]

    # ==== COUNT DOCTORS =====
    cursor.execute("SELECT COUNT (*) FROM doctors")
    doctors = cursor.fetchone()[0]

    # ==== COUNT APPOINTMENTS =====
    cursor.execute("SELECT COUNT (*) FROM appointments")
    appointments = cursor.fetchone()[0]

    # ==== Count completed appointments ======
    cursor.execute(
        "SELECT COUNT (*) FROM appointments WHERE status = ?",
        ("Completed",)
    )
    completed = cursor.fetchone()[0]

    # ==== Count pending appointments =====
    cursor.execute(
        "SELECT COUNT (*) FROM appointments WHERE status = ?",
        ("Pending",)
    )
    pending = cursor.fetchone()[0]

    # === Count cancelled appointment ======
    cursor.execute(
        "SELECT COUNT (*) FROM appointments WHERE status = ?",
        ("Cancelled",)
    )
    cancelled = cursor.fetchone()[0]

    connection.close()

    return patients, doctors, appointments, completed, pending, cancelled 


# ==================== REPORTS ==============================================================
def show_reports(main_frame, app):

    # Remove whatever is currently showing
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Title
    reports_title = ctk.CTkLabel(
        main_frame,
        text="Reports",
        font=("Arial", 28, "bold")
    )
    reports_title.pack(
        anchor="w",
        padx=30,
        pady=30
    )
    # Subtitle
    report_subtitle = ctk.CTkLabel(
        main_frame,
        text="CareFlow System Overview",
        font=("Arial", 16)
    )
    report_subtitle.pack(
        anchor="w",
        padx=30
    )

    # Get report data
    patients, doctors, appointments, completed, pending, cancelled = load_report_data()

    # ===================== SUMMARY CARDS ==============================================================
    card_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )
    card_frame.pack(
        padx=30,
        pady=30,
        fill="x"
    )

    # ===== Patients card =====
    patients_card = ctk.CTkFrame(
        card_frame,
        fg_color="white"
    )
    patients_card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=5
    )
    ctk.CTkLabel(
        patients_card,
        text="Total Patients",
        font=("Arial", 16, "bold"),
        text_color="purple"
    ).pack(pady=(15,5))

    ctk.CTkLabel(
        patients_card,
        text=str(patients),
        font=("Arial", 28, "bold"),
    ).pack(pady=(0,15))

    # ==== Doctors card =====
    doctors_card = ctk.CTkFrame(
        card_frame,
        fg_color="white"
    )
    doctors_card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=5
    )
    ctk.CTkLabel(
        doctors_card,
        text="Total Doctors",
        font=("Arial", 16, "bold"),
        text_color="purple"
    ).pack(pady=(15,5))

    ctk.CTkLabel(
        doctors_card,
        text=str(doctors),
        font=("Arial", 28, "bold"),
    ).pack(pady=(0,15))    


    # ====== Appointments card =======
    appointments_card = ctk.CTkFrame(
        card_frame,
        fg_color="white"
    )
    appointments_card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=5
    )
    ctk.CTkLabel(
        appointments_card,
        text="Total Appointments",
        font=("Arial", 16, "bold"),
        text_color="purple"
    ).pack(pady=(15,5))

    ctk.CTkLabel(
        appointments_card,
        text=str(appointments),
        font=("Arial", 28, "bold"),
    ).pack(pady=(0,15))        



    # ================================================== APPOINTMENT STATUS =========================================
    status_title = ctk.CTkLabel(
        main_frame,
        text="Appointment Status",
        font=("Arial", 20, "bold")
    )
    status_title.pack(
        anchor="w",
        padx=30,
        pady=(10,15)
    )
    status_frame = ctk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )
    status_frame.pack(
        padx=30,
        fill="x"
    )

    # == Pending ==
    pending_card = ctk.CTkFrame(
        status_frame,
        fg_color="white"
    )
    pending_card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=5
    )
    ctk.CTkLabel(
        pending_card,
        text="Pending",
        font=("Arial", 15, "bold"),
        text_color="purple"
    ).pack(pady=(0,15))

    ctk.CTkLabel(
        pending_card,
        text=str(pending),
        font=("Arial", 24, "bold")
    ).pack(pady=(0,15))


    # == Completed ==
    completed_card = ctk.CTkFrame(
        status_frame,
        fg_color="white"
    )
    completed_card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=5
    )
    ctk.CTkLabel(
        completed_card,
        text="Completed",
        font=("Arial", 15, "bold"),
        text_color="purple"
    ).pack(pady=(0,15))

    ctk.CTkLabel(
        completed_card,
        text=str(completed),
        font=("Arial", 24, "bold")
    ).pack(pady=(0,15))    


    # == Cancelled ==
    cancelled_card = ctk.CTkFrame(
        status_frame,
        fg_color="white"
    )
    cancelled_card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=5
    )
    ctk.CTkLabel(
        cancelled_card,
        text="Cancelled",
        font=("Arial", 15, "bold"),
        text_color="purple"
    ).pack(pady=(0,15))

    ctk.CTkLabel(
        cancelled_card,
        text=str(cancelled),
        font=("Arial", 24, "bold")
    ).pack(pady=(0,15))