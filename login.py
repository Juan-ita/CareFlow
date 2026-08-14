import customtkinter as ctk


# ======================== SHOW LOGIN ====================================
def show_login(app, open_dashboard):

    # # clear the window
    # for widget in app.winfo_children():
    #     widget.destroy()

    # ========================== LOGIN FRAME ==================================
    login_frame = ctk.CTkFrame(
        app,
        corner_radius=0,
        fg_color="white"
    )     
    login_frame.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )     
    # == LOGO ==
    logo = ctk.CTkLabel(
        login_frame,
        text="CareFlow",
        font=("Arial", 30, "bold"),
        text_color="purple"
    )     
    logo.pack(pady=(40,10))     

    # == SUBTITLE ==
    subtitle = ctk.CTkLabel(
        login_frame,
        text="Hospital management system",
        font=("Arial", 14)
    )     
    subtitle.pack(pady=(0,25))        

    # == USERNAME ==
    username_entry = ctk.CTkEntry(
        login_frame,
        width=250,
        placeholder_text="Enter a username"
    )
    username_entry.pack(pady=10)     

    # == PASSWORD ==
    password_entry = ctk.CTkEntry(
        login_frame,
        width=250,
        placeholder_text="Password",
        show="*"
    )
    password_entry.pack(pady=10)     
    # == ERROR MESSAGE ==
    message = ctk.CTkLabel(
        login_frame,
        text="",
        text_color="red"
    )
    message.pack(pady=5)


    # ================================ LOGIN FUNCTION =============================================================================
    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "1234":
            login_frame.destroy()
            open_dashboard()
        else:
            message.configure(
                text="Invalid username or password"
            )
    # == LOGIN BUTTON ==
    login_button = ctk.CTkButton(
        login_frame,
        text="Login",
        width=290,
        fg_color="purple",
        hover_color="darkviolet",
        command=login
    )
          
    login_button.pack(pady=20)