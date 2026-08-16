import customtkinter as ctk

# ======================== SHOW LOGIN ====================================
def show_login(app, open_dashboard):

    # ========================= LOGIN BACKGROUND ===============================
    login_frame = ctk.CTkFrame(
        app,
        corner_radius=0,
        fg_color="#F7F5F8"
    )

    login_frame.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )

    # ========================== LOGIN CARD ========================================
    card = ctk.CTkFrame(
        login_frame,
        width=420,
        height=500,
        corner_radius=20,
        fg_color="white"
    )

    card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    # ======================================= LOGO ==========================================
    logo = ctk.CTkLabel(
        card,
        text="CareFlow",
        font=("Arial", 32, "bold"),
        text_color="purple"
    )

    logo.pack(
        pady=(45, 5)
    )

    # =================================== WELCOME ================================================
    welcome = ctk.CTkLabel(
        card,
        text="Welcome Back",
        font=("Arial", 20, "bold")
    )

    welcome.pack(
        pady=(0, 5)
    )

    # ============================= INSTRUCTIONS =========================================
    instuction = ctk.CTkLabel(
        card,
        text="Login to access your dashboard",
        font=("Arial", 13),
        text_color="gray"
    )
    instuction.pack(
        pady=(0, 20)
    )

    # ============================ USERNAME ===================================
    username_entry = ctk.CTkEntry(
        card,
        width=300,
        height=40,
        corner_radius=10,
        placeholder_text="Username"
    )

    username_entry.pack(
        pady=8
    )

    # ============================ PASSWORD =====================================
    password_entry = ctk.CTkEntry(
        card,
        width=300,
        height=40,
        corner_radius=10,
        placeholder_text="Password",
        show="*"
    )

    password_entry.pack(
        pady=8
    )

    # =============================== ERROR MESSAGE ==========================
    message = ctk.CTkLabel(
        card,
        text="",
        text_color="red",
        font=("Arial", 12)
    )

    message.pack(
        pady=(5,0)
    )

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
        card,
        text="Login",
        height=50,
        width=100,
        corner_radius=10,
        fg_color="purple",
        hover_color="darkviolet",
        command=login
    )
          
    login_button.pack(pady=20)