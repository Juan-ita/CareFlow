import customtkinter as ctk
import sqlite3

from doctors import show_doctors
from appointment import show_appointments
from reports import show_reports

ctk.set_appearance_mode("light")


def load_patients():
        connection = sqlite3.connect("careflow.db")
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, age, phone FROM patients")

        patients = cursor.fetchall()
        connection.close()

        return patients

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

    def save_patient():
        name = name_entry.get()
        age = age_entry.get()
        phone = phone_entry.get()

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

# ========================= SHOW DASHBOARD ========================================================================================================

# Dashboard title
def show_dashboard():
     for widget in main_frame.winfo_children():
          widget.destroy()

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
         text="0",
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
         text="0",
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
         text="0",
         font=("Arial", 28, "bold")
     )
     
     appointments_number.pack()



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


show_dashboard()
app.mainloop() # keeps the window running
     
     