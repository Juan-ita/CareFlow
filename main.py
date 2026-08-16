import customtkinter as ctk
import sqlite3

from doctors import show_doctors
from appointment import show_appointments
from reports import show_reports
from login import show_login

from datetime import datetime

ctk.set_appearance_mode("light")

# ================================= LOAD TODAY'S APPOINTMENTS ======================================================================================
def load_todays_appointments():
     connection = sqlite3.connect("careflow.db")
     cursor = connection.cursor()

     today = datetime.now().strftime("%d/%m/%Y")

     cursor.execute(
          """
          SELECT patient, doctor, time, status FROM appointments WHERE date = ? ORDER BY time
          """,
          (today,)
     )
     appointments = cursor.fetchall()
     connection.close()
     return appointments

# ========================================= LOAD TODAY'S APPOINTMENT SUMMARY =====================================================================
def load_today_summary():
     connection = sqlite3.connect("careflow.db")
     cursor = connection.cursor()

     today = datetime.now().strftime("%d/%m/%Y")

     cursor.execute(
          """ SELECT COUNT (*) FROM appointments
          WHERE date =? AND status = ?
          """,
          (today, "Pending")
     )
     pending = cursor.fetchone()[0]

     # Completed appointments today
     cursor.execute(
          """ SELECT COUNT (*) FROM appointments WHERE date = ? AND status = ?
          """,
          (today, "Completed")
     )
     complete = cursor.fetchone()[0]

     
     # Cancelled appointments today
     cursor.execute(
          """ SELECT COUNT (*) FROM appointments WHERE date = ? AND status = ?
          """,
          (today, "Cancelled")
     )
     cancelled = cursor.fetchone()[0]

     connection.close()

     return pending, complete, cancelled



# ===================================== Load Patients =========================================================================================
def load_patients():
        connection = sqlite3.connect("careflow.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, age, phone FROM patients")

        patient = cursor.fetchall()
        connection.close()

        return patient



#================================== DELETE BUTTON==========================================================================
def delete_patient(patient_id):
     connection = sqlite3.connect("careflow.db")
     cursor = connection.cursor()

     cursor.execute(
          "DELETE FROM patients WHERE id = ?",
          (patient_id,)
     )

     connection.commit()
     connection.close()

     show_patients() # refreshes our table so the deleted patient disappears immediately.


# ================================ Update ==========================================================================================
def update_patient(patient_id):

      connection = sqlite3.connect("careflow.db")
      cursor = connection.cursor()

      cursor.execute(
           "SELECT name, age, phone FROM patients WHERE id = ?",
           (patient_id,)
      )

      patient = cursor.fetchone() # Gets patients information

      connection.close()
       # Edit window
      form = ctk.CTkToplevel(app)
      form.title("Edit Patient")
      form.geometry("400x400")

        # name
      name_label = ctk.CTkLabel(
           form,
           text="Patient Name"
      )

      name_label.pack(pady=(20,5))
      name_entry = ctk.CTkEntry(form)
      name_entry.pack(pady=5)
      name_entry.insert(0, patient[0])

      # Age
      age_label = ctk.CTkLabel(
           form,
           text="Age"
      )
      age_label.pack(pady=(15,5))
      age_entry = ctk.CTkEntry(form)
      age_entry.pack(pady=5)
      age_entry.insert(0, patient[1])

      # Phone
      phone_label = ctk.CTkLabel(
           form,
           text="Phone Number"
      )
      phone_label.pack(pady=(15,5))
      phone_entry = ctk.CTkEntry(form)
      phone_entry.pack(pady=5)
      phone_entry.insert(0, patient[2])

      def save_changes():
           print("Update button")
           name = name_entry.get()
           age = age_entry.get()
           phone = phone_entry.get()

           connection = sqlite3.connect("careflow.db")
           cursor = connection.cursor()

           cursor.execute(
                "UPDATE patients SET name = ?, age = ?, phone = ? WHERE id = ?",
                (name, age, phone, patient_id)
           )
           connection.commit()
           connection.close()

           show_patients()
           form.destroy()

      update_button = ctk.CTkButton(
           
           form,
           text="Update Patient",
           fg_color="purple",
           hover_color="darkviolet",
           command=save_changes
           )

      update_button.pack(pady=25)


# ==================== Show patients =============================================================================
# After clicking the patients button in sidebar
def show_patients():

    # Remove everything currently inside the main area
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Patients title
    patients_tittle = ctk.CTkLabel(
        main_frame,
        text="Patients",
        font=("Arial", 28, "bold")
    )

    patients_tittle.pack(
        anchor="w",
        padx=30,
        pady=30
    )

    # Add patient button 
    add_patient_button = ctk.CTkButton(
        main_frame,
        text="+ Add Patient",
        fg_color="purple",
        hover_color="darkviolet",
        command=add_patient
    )

    add_patient_button.pack(
        anchor="w",
        padx=30,
        pady=10
    )

    # ======================================= Table header=============================================================

    patients = load_patients() # Gets the patients from the database

    header = ctk.CTkFrame(
         main_frame,
         fg_color="purple"
    )

    header.pack(
         fill="x",
         padx=30,
         pady=(20,0)
    )

    # ID
    ctk.CTkLabel(
         header,
         text="ID",
         text_color="white",
         font=("Arial", 14, "bold"),
         width=50
    ).pack(side="left", padx=10, pady=10)

    # Name
    ctk.CTkLabel(
         header,
         text="Name",
         text_color="white",
         font=("Arial", 14, "bold"),
         width=150
    ).pack(side="left", padx=10, pady=10)

    # Age
    ctk.CTkLabel(
         header,
         text="Age",
         text_color="white",
         font=("Arial", 14, "bold"),
         width=80
    ).pack(side="left", padx=10, pady=10)

    # Phone
    ctk.CTkLabel(
         header,
         text="Phone",
         text_color="white",
         font=("Arial", 14, "bold"),
         width=150
    ).pack(side="left", padx=10, pady=10)

    # ===================== PATIENT ROWS ==========================================================
    for patient in patients:

         row = ctk.CTkFrame(
              main_frame,
              fg_color="white"
         )

         row.pack(
              fill="x",
              padx=30,
              pady=2
         )

         ctk.CTkLabel(
              row,
              text=str(patient[0]), # converts into text
              width=50
         ).pack(side="left", padx=10, pady=8)

         ctk.CTkLabel(
              row,
              text=patient[1],
              width=150
         ).pack(side="left", padx=10, pady=8)

         ctk.CTkLabel(
              row,
              text=str(patient[2]),
              width=80
         ).pack(side="left", padx=10, pady=8)


         ctk.CTkLabel(
              row,
              text=patient[3],
              width=150
         ).pack(side="left", padx=10, pady=8)

         # ======================= Delete==================================================================
         delete_buttoon = ctk.CTkButton(
              row,
              text="Delete",
              fg_color="purple",
              hover_color="darkviolet",
              command=lambda patient_id = patient[0]: delete_patient(patient_id)
         )

         delete_buttoon.pack(
              side="left",
              padx=10,
              pady=8
         )

         # ================================UPDATE================================================================
         edit_button = ctk.CTkButton(
              row,
              text="Edit",
              fg_color="purple",
              hover_color="darkviolet",
              command=lambda patient_id=patient[0]: update_patient(patient_id)
         )

         edit_button.pack(
              side="left",
              padx=5,
              pady=8
         )

         




# ==================== + Add Patient form =========================================================================================================
def add_patient():
    form = ctk.CTkToplevel(app)
    form.title("Add Patient")
    form.geometry("400x400")

    # Name
    name_label = ctk.CTkLabel(
        form,
        text="Patient Name"
    )

    name_label.pack(pady=(20,5))

    name_entry = ctk.CTkEntry(
        form,
        placeholder_text="Enter patient's name"
    )
    name_entry.pack(pady=5)

    # Age
    age_label = ctk.CTkLabel(
        form,
        text="Age"
    )

    age_label.pack(pady=(15,5))

    age_entry = ctk.CTkEntry(
        form,
        placeholder_text="Enter age"
    )

    age_entry.pack(pady=5)

    # Phone number
    phone_label = ctk.CTkLabel(
        form,
        text="Phone Number"
    )

    phone_label.pack(pady=(15,5))

    phone_entry = ctk.CTkEntry(
        form,
        placeholder_text="Enter phone number"
    )
    phone_entry.pack(pady=5)

    # Error message
    error_message = ctk.CTkLabel(
         form,
         text="",
         text_color="red"
    )

    error_message.pack(pady=5)

    def save_patient():
        name = name_entry.get()
        age = age_entry.get()
        phone = phone_entry.get()

        # Check for empty fields
        if not name or not age or not phone:
             error_message.configure(
                  text="Please fill in all fields."
             )
             return

        # Check that age is a number
        if not age.isdigit():
             error_message.configure(
                  text="Age must be a number."
             )
             return

        if len(phone) != 10:
             error_message.configure(
                  text="Phone number must be exactly 10 digits."
             )
             return

        connection = sqlite3.connect("careflow.db") # Opens the database

        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO patients (name, age, phone) VALUES (?, ?, ?)",
            (name, age, phone)
        )

        connection.commit()
        connection.close()

        print("Patient saved successfully")

        show_patients()
        form.destroy()




    # Save button
    save_button = ctk.CTkButton(
        form,
        text="Save Patient",
        fg_color="purple",
        hover_color="darkViolet",
        command=save_patient
    )

    save_button.pack(pady=25)


# ctk - creates an application window
app = ctk.CTk()

app.title("CareFlow")
app.geometry("800x500") # controls its wsize


# =============================================SIDEBAR======================================================================================
sidebar = ctk.CTkFrame( # Creates the box
    app,
    width=220,
    height=500,
    corner_radius=0,
    fg_color="purple"
)

sidebar.pack(
    side="left",
    fill="y" # Strech it vertically
)
sidebar.pack_propagate(False)

# LOGO
logo = ctk.CTkLabel(
    sidebar,
    text = "CareFlow",
    font=("Arial", 20, "bold"),
    text_color="white"
)

logo.pack(pady=30)



# MAIN
main_frame = ctk.CTkFrame(
    app,
    corner_radius=0
)

main_frame.pack(
    side="right",
    fill="both",
    expand=True
)

# ================================== Load Dashboard counts ================================================================
def load_dashboard_counts():
     connection = sqlite3.connect("careflow.db")
     cursor = connection.cursor()

     cursor.execute("SELECT COUNT (*) FROM patients")
     patients = cursor.fetchone()[0]

     
     cursor.execute("SELECT COUNT (*) FROM doctors")
     doctors = cursor.fetchone()[0]

     cursor.execute("SELECT COUNT (*) FROM appointments")
     appointments = cursor.fetchone()[0]

     connection.close()

     return patients, doctors, appointments


# ========================= SHOW DASHBOARD ========================================================================================================

# Dashboard title
def show_dashboard():
     
     # Remove everything currently showing
     for widget in main_frame.winfo_children():
          widget.destroy()

     # Get the numbers from database
     patients, doctors, appointments = load_dashboard_counts()

     dashboard_title = ctk.CTkLabel(
         main_frame,
         text="Dashboard",
         font=("Arial", 28, "bold")
     )
     
     dashboard_title.pack(
         anchor='w',
         padx=30,
         pady=30
     )

     card_frame = ctk.CTkFrame(
         main_frame,
         fg_color="transparent"
     )
     
     card_frame.pack(
         padx=30,
         pady=10,
         fill="x"
     )
     
     # ================================ CARDS========================================================
     # Patient card
     patients_card = ctk.CTkFrame(
         card_frame,
         width=200,
         height=120,
         fg_color="white"
     )
     
     patients_card.pack(
         side="left",
         padx=10,
         pady=10,
         expand=True,
         fill='both'
     )
     
     patients_label = ctk.CTkLabel(
         patients_card,
         text="Registered Patients",
         font=("Arial", 16, "bold"),
         text_color="purple"
     )
     
     patients_label.pack(pady=(20,5))
     
     patients_number = ctk.CTkLabel(
         patients_card,
         text=str(patients),
         font=("Arial", 28, "bold")
     )
     
     patients_number.pack()
     
     # Doctors card
     doctors_card = ctk.CTkFrame(
         card_frame,
         width=200,
         height=120,
         fg_color="white"
     )
     
     doctors_card.pack(
         side="left",
         padx=10,
         pady=10,
         expand=True,
         fill='both'
     )
     
     doctors_label = ctk.CTkLabel(
         doctors_card,
         text="Doctors",
         font=("Arial", 16, "bold"),
         text_color="purple"
     )
     
     doctors_label.pack(pady=(20,5))
     
     doctors_number = ctk.CTkLabel(
         doctors_card,
         text=str(doctors),
         font=("Arial", 28, "bold")
     )
     
     doctors_number.pack()
     
     # Appointments card
     appointments_card = ctk.CTkFrame(
         card_frame,
         width=200,
         height=120,
         fg_color="white"
     )
     
     appointments_card.pack(
         side="left",
         padx=10,
         pady=10,
         expand=True,
         fill='both'
     )
     
     appointments_label = ctk.CTkLabel(
         appointments_card,
         text="Appointments",
         font=("Arial", 16, "bold"),
         text_color="purple"
     )
     
     appointments_label.pack(pady=(20,5))
     
     appointments_number = ctk.CTkLabel(
         appointments_card,
         text=str(appointments),
         font=("Arial", 28, "bold")
     )
     
     appointments_number.pack()

     # ================================ TODAY'S SUMMARY ==================================================================================================
     pending, completed, cancelled = load_today_summary()

     summary_title = ctk.CTkLabel(
          main_frame,
          text="Today's Summary",
          font=("Arial", 20, "bold")
     )

     summary_title.pack(
          anchor ="w",
          padx=30,
          pady=(30,10)
     )

     summary_frame = ctk.CTkFrame(
          main_frame,
          fg_color="transparent"
     )

     summary_frame.pack(
          padx=30,
          fill="x"
     )

     # === Pending ===
     pending_card = ctk.CTkFrame(
          summary_frame,
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
     ).pack(pady=(15, 5))

     ctk.CTkLabel(
          pending_card,
          text=str(pending),
          font=("Arial", 24, "bold")
     ).pack(pady=(0,15))

     

     # === Completed ===
     completed_card = ctk.CTkFrame(
          summary_frame,
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
     ).pack(pady=(15, 5))

     ctk.CTkLabel(
          completed_card,
          text=str(completed),
          font=("Arial", 24, "bold")
     ).pack(pady=(0,15))


     # === Cancelled ===
     cancelled_card = ctk.CTkFrame(
          summary_frame,
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
          text="Completed",
          font=("Arial", 15, "bold"),
          text_color="purple"
     ).pack(pady=(15, 5))

     ctk.CTkLabel(
          cancelled_card,
          text=str(cancelled),
          font=("Arial", 24, "bold")
     ).pack(pady=(0,15))



     # ================================= TODAY'S APPOINTMENTS ============================================================================================
     today_title = ctk.CTkLabel(
          main_frame,
          text="Today's Appointments",
          font=("Arial", 20, "bold")
     )

     today_title.pack(
          anchor="w",
          padx=30,
          pady=(30,10)
     )

     todays_appointments = load_todays_appointments()

     # If there are no appointments today
     if not todays_appointments:
          no_appointments = ctk.CTkLabel(
               main_frame,
               text="No appointments scheduled for today.",
               font=("Arial", 14)
          )
          no_appointments.pack(
               anchor="w",
               padx=30,
               pady=10
          )
     else:
          # =========== Table header =======================================
          today_header = ctk.CTkFrame(
               main_frame,
               fg_color="purple"
          )
          today_header.pack(
               fill="x",
               padx=30,
               pady=(5,0)
          )

          # patient
          ctk.CTkLabel(
               today_header,
               text="Patient",
               text_color="white",
               font=("Arial", 14, "bold"),
               width=150
          ).pack(
               side="left",
               padx=10,
               pady=10
          )

          # Doctor
          ctk.CTkLabel(
               today_header,
               text="Doctor",
               text_color="white",
               font=("Arial", 14, "bold"),
               width=150
          ).pack(
               side="left",
               padx=10,
               pady=10
          )

          # Time
          ctk.CTkLabel(
               today_header,
               text="Time",
               text_color="white",
               font=("Arial", 14, "bold"),
               width=150
          ).pack(
               side="left",
               padx=10,
               pady=10
          )

          # status
          ctk.CTkLabel(
               today_header,
               text="Status",
               text_color="white",
               font=("Arial", 14, "bold"),
               width=120
          ).pack(
               side="left",
               padx=10,
               pady=10
          )

          # ==================== APPOINTMENT ROWS ==========================================================================
          for appointment in todays_appointments:

               row = ctk.CTkFrame(
                    main_frame,
                    fg_color="white"
               )
               row.pack(
                    fill="x",
                    padx=30,
                    pady=2
               )

               # Patient
               ctk.CTkLabel(
                    row,
                    text=appointment[0],
                    width=150
               ).pack(
                    side="left",
                    padx=10,
                    pady=8
               )

               
               # Doctor
               ctk.CTkLabel(
                    row,
                    text=appointment[1],
                    width=150
               ).pack(
                    side="left",
                    padx=10,
                    pady=8
               )

               # Time
               ctk.CTkLabel(
                    row,
                    text=appointment[2],
                    width=100
               ).pack(
                    side="left",
                    padx=10,
                    pady=8
               )


               # Status
               ctk.CTkLabel(
                    row,
                    text=appointment[3],
                    width=120
               ).pack(
                    side="left",
                    padx=10,
                    pady=8
               )

# === LOGOUT===
def logout():
     # Hide the side
     sidebar.pack_forget()

     # Show the login screen again
     show_login(app, show_dashboard)

# ==========================================================BUTTONS==============================================================================
# DASHBOARD BUTTON
dashboard_button = ctk.CTkButton( # Creates a button
    sidebar,
    text="Dashboard",
    fg_color="purple",
    hover_color="darkViolet",
    command=show_dashboard
)
dashboard_button.pack(
    pady=10,
    padx=20,
    fill="x" # makes the button strech accross the available width
    
)

# PATIENT BUTTON
Patients_button = ctk.CTkButton( # Creates a button
    sidebar,
    text="Patients",
    fg_color="purple",
    hover_color="darkViolet",
    command= show_patients 

)

Patients_button.pack(
    pady=10,
    padx=20,
    fill="x" 
)

# DOCTORS BUTTON
doctors_button = ctk.CTkButton( # Creates a button
    sidebar,
    text="Doctors",
    fg_color="purple",
    hover_color="darkViolet",
    command=lambda: show_doctors(main_frame,app)
)
doctors_button.pack(
    pady=10,
    padx=20,
    fill="x" 
)

# APPOINTMENTS BUTTON
appointments_button = ctk.CTkButton( # Creates a button
    sidebar,
    text="Appointments",
    fg_color="purple",
    hover_color="darkViolet",
    command=lambda: show_appointments(main_frame, app)
)
appointments_button.pack(
    pady=10,
    padx=20,
    fill="x" 
)

# REPORTS BUTTON
reports_button = ctk.CTkButton( # Creates a button
    sidebar,
    text="Reports",
    fg_color="purple",
    hover_color="darkViolet",
    command=lambda: show_reports(main_frame, app)
)
reports_button.pack(
    pady=10,
    padx=20,
    fill="x" 
)

# LOGOUT BUTTON
logout_button = ctk.CTkButton(
     sidebar,
     text="Logout",
     fg_color="purple",
     hover_color="darkviolet",
     command=logout
)

logout_button.pack(
     pady=10,
     padx=20,
     fill="x"
)

show_login(app, show_dashboard)
app.mainloop() # keeps the window running
     
     