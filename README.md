# CareFlow

CareFlow is a desktop hospital management system built with **Python, CustomTkinter, and SQLite**. It is designed to help hospital staff manage patients, doctors, appointments, and reports through a simple and user-friendly interface.

## Features

###  Login System

* Secure login screen for accessing the application.
* Users are taken to the dashboard after successful login.
* Logout functionality returns the user to the login screen.

###  Dashboard

The dashboard provides an overview of hospital activities, including:

* Registered Patients
* Doctors
* Appointments
* Today's Pending Appointments
* Today's Completed Appointments
* Today's Cancelled Appointments
* Today's scheduled appointments

###  Patient Management

Hospital staff can:

* Add new patients
* View registered patients
* Edit patient information
* Delete patients
* Store patient information in the SQLite database

Patient information includes:

* Patient ID
* Name
* Age
* Phone number

###  Doctor Management

Staff can:

* Add doctors
* View doctors
* Store doctor information in the database
* Manage doctor records

Doctor information includes:

* Doctor ID
* Name
* Specialization
* Phone number

###  Appointment Management

Staff can:

* Create appointments
* View appointments
* Edit appointments
* Set appointment status
* View appointment details

Appointment information includes:

* Appointment ID
* Patient
* Doctor
* Date
* Time
* Status

Available appointment statuses:

* Pending
* Completed
* Cancelled

###  Reports

CareFlow includes a reports section for viewing hospital-related information and statistics.

## 🛠️ Technologies Used

* **Python** - Main programming language
* **CustomTkinter** - Graphical user interface
* **SQLite** - Database management
* **Tkinter** - Window and interface functionality

##  Project Structure

```text
CareFlow/
│
├── main.py
├── login.py
├── doctors.py
├── appointment.py
├── reports.py
├── careflow.db
└── README.md
```

##  Database

CareFlow uses **SQLite** to store application data locally.

The database contains information for:

* Patients
* Doctors
* Appointments

The database is automatically created when the required tables do not already exist.


##  Purpose

CareFlow was developed as a capstone project to demonstrate the use of Python programming, graphical user interfaces, database management, and CRUD operations in a real-world healthcare management scenario.

##  Future Improvements

Possible future improvements include:

* Search and filter functionality
* Improved appointment scheduling
* More detailed reports
* User roles and permissions
* Better form validation
* Patient medical history
* Doctor availability tracking
* Database backup and restore

