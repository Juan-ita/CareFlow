import customtkinter as ctk
import sqlite3

# ============================= delete doctor =========================================================================================
def delete_doctor(doctors_id, main_frame, app):
     connection = sqlite3.connect("careflow.db")
     cursor = connection.cursor()

     cursor.execute(
          "DELETE FROM doctors WHERE id = ?",
          (doctors_id,)
     )

     connection.commit()
     connection.close()

     show_doctors(main_frame, app) # refreshes our table so the deleted patient disappears immediately.



def create_doctors_table():
    connection = sqlite3.connect("careflow.db")
    cursor = connection.cursor()

    cursor.execute(
    """
      CREATE TABLE IF NOT EXISTS doctors (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT NOT NULL,
         specialization TEXT NOT NULL,
         phone TEXT NOT NULL
     )
    """
)

    connection.commit()
    connection.close()


# ========================== ADD DOCTOR=================================================================================
def add_doctor(app, main_frame): # Gives the function access to the main application window
        form = ctk.CTkToplevel(app) # creates a small window on top of careflow
        form.title("Add Doctor")
        form.geometry("400x450")

        # Doctors name
        name_label = ctk.CTkLabel(
            form,
            text="Doctor name"
        )
        name_label.pack(pady=(20,5))

        name_entry = ctk.CTkEntry(
            form,
            placeholder_text="Enter doctor's name"
        )
        name_entry.pack(pady=5)

        # Specialization
        specialization_label = ctk.CTkLabel(
            form,
            text="Specialization"
        )
        specialization_label.pack(pady=(15,5))

        specialization_entry = ctk.CTkEntry(
            form,
            placeholder_text="e.g. Cardiology"
        )
        specialization_entry.pack(pady=5)

        # Phone
        phone_label = ctk.CTkLabel(
            form,
            text="Phone Number"
        )
        phone_label.pack(pady=(15,5))

        phone_entry= ctk.CTkEntry(
            form,
            placeholder_text="Enter phone number"
        )
        phone_entry.pack(pady=5)


        # ==================== SAVE BUTTON ===========================================================================================
        def save_doctor():
               name = name_entry.get()
               specialization = specialization_entry.get()
               phone = phone_entry.get()

               connection = sqlite3.connect("careflow.db")
               cursor = connection.cursor()

               cursor.execute(
                      "INSERT INTO doctors (name, specialization, phone) VALUES (?, ?, ?)",
                      (name, specialization, phone)
               )

               connection.commit()
               connection.close()

               print("Doctor saved!")
               form.destroy()
               show_doctors(main_frame,app)

        save_button = ctk.CTkButton(
             form,
             text="Save Doctor",
             fg_color="purple",
             hover_color="darkviolet",
             command=save_doctor
               )

        save_button.pack(pady=25)

def load_doctors():
       connection = sqlite3.connect("careflow.db")
       cursor = connection.cursor()

       cursor.execute(
              "SELECT id, name, specialization, phone FROM doctors"
       )

       doctors = cursor.fetchall() # collects all the rows
       connection.close()
       return doctors


# =============================== edit doctor ==================================================================================================
def update_doctor(doctors_id, main_frame, app):

      connection = sqlite3.connect("careflow.db")
      cursor = connection.cursor()

      cursor.execute(
           "SELECT name, specialization, phone FROM doctors WHERE id = ?",
           (doctors_id,)
      )

      doctor = cursor.fetchone() # Gets doctors information

      connection.close()
      
       # Edit window
      form = ctk.CTkToplevel(app)
      form.title("Edit Doctor")
      form.geometry("400x450")

        # name
      name_label = ctk.CTkLabel(
           form,
           text="Doctors Name"
      )

      name_label.pack(pady=(20,5))

      name_entry = ctk.CTkEntry(form)
      name_entry.pack(pady=5)

      name_entry.insert(0, doctor[0])


        # specialization
      specialization_label = ctk.CTkLabel(
           form,
           text="Specialization"
      )

      specialization_label.pack(pady=(15,5))

      specialization_entry = ctk.CTkEntry(form)
      specialization_entry.pack(pady=5)

      specialization_entry.insert(0, doctor[1])


        # phone
      phone_label = ctk.CTkLabel(
           form,
           text="Phone Number"
      )

      phone_label.pack(pady=(15,5))

      phone_entry = ctk.CTkEntry(form)
      phone_entry.pack(pady=5)

      phone_entry.insert(0, doctor[2])

     # ============================ SAVE UPDATES ================================================
      def save_changes():
        name = name_entry.get()
        specialization = specialization_entry.get()
        phone = phone_entry.get()

        connection = sqlite3.connect("careflow.db") # Opens the database

        cursor = connection.cursor()

        cursor.execute(
            "UPDATE doctors SET name = ?, specialization = ?, phone = ? WHERE id = ?",
            (name, specialization, phone, doctors_id)
        )

        connection.commit()
        connection.close()

        print("Doctor updated")

        show_doctors(main_frame, app)
        form.destroy()

        # Save button
      save_button = ctk.CTkButton(
         form,
         text="Save New Change",
         fg_color="purple",
         hover_color="darkViolet",
         command=save_changes
        )
        
      save_button.pack(pady=25)



# ======================================= SHOW DOCTORS =============================================================================================
def show_doctors(main_frame, app):

        # Remove everything currently inside the main area
        for widget in main_frame.winfo_children():
            widget.destroy()

        # Doctors title
        doctors_title = ctk.CTkLabel(
            main_frame,
            text="Doctors",
            font=("Arial", 28, "bold")
        )    
        doctors_title.pack(
            anchor="w",
            padx=30,
            pady=30
        )

        # Add doctors button
        add_doctor_button = ctk.CTkButton(
            main_frame,
            text="+ Add Doctor",
            fg_color="purple",
            hover_color="darkviolet",
            command=lambda: add_doctor(app, main_frame)
        )

        add_doctor_button.pack(
            anchor="w",
            padx=30,
            pady=10
        )

        doctors = load_doctors()

        # =========================================== Table header ============================================================
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

    # Specialization
        ctk.CTkLabel(
         header,
         text="Specialization",
         text_color="white",
         font=("Arial", 14, "bold"),
         width=150,
    ).pack(side="left", padx=10, pady=10)

    # Phone
        ctk.CTkLabel(
         header,
         text="Phone",
         text_color="white",
         font=("Arial", 14, "bold"),
         width=150
    ).pack(side="left", padx=10, pady=10)

        # =========================================== DOCTORS ROW =============================================================================
        for doctor in doctors:

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
              text=str(doctor[0]), # converts into text
              width=50
         ).pack(side="left", padx=10, pady=8)

         ctk.CTkLabel(
              row,
              text=doctor[1],
              width=150
         ).pack(side="left", padx=10, pady=8)

         ctk.CTkLabel(
              row,
              text=str(doctor[2]),
              width=150
         ).pack(side="left", padx=10, pady=8)


         ctk.CTkLabel(
              row,
              text=doctor[3],
              width=150
         ).pack(side="left", padx=10, pady=8)


         # ======================= Delete button==================================================================
         delete_buttoon = ctk.CTkButton(
              row,
              text="Delete",
              fg_color="purple",
              hover_color="darkviolet",
              command=lambda doctors_id = doctor[0]: delete_doctor(doctors_id, main_frame, app)
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
              command=lambda doctors_id=doctor[0]: update_doctor(doctors_id, main_frame,app)
         )

         edit_button.pack(
              side="left",
              padx=5,
              pady=8
         )

         



create_doctors_table()        