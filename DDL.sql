SHOW DATABASES;

CREATE DATABASE HOSPITAL;

USE HOSPITAL;

-- Table for Patients
CREATE TABLE Patients (
    PatientID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    DateOfBirth DATE,
    Gender ENUM('Male', 'Female', 'Other'),
    ContactNumber VARCHAR(15),
    Email VARCHAR(100),
    Address VARCHAR(255),
	BloodType VARCHAR(3) CHECK (BloodType IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    MaritalStatus ENUM('Single', 'Married', 'Divorced', 'Widowed'),
    Occupation VARCHAR(100),
    MedicalConditions TEXT,
    PrimaryPhysician VARCHAR(100),
    CurrentStatus ENUM('Admitted', 'Discharged', 'Outpatient')
    );

-- Table for Doctors
CREATE TABLE Doctors (
    DoctorID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Specialization VARCHAR(100),
    ContactNumber VARCHAR(15),
    Email VARCHAR(100),
    Qualifications TEXT,
    Department VARCHAR(100)
);

-- Further Updated Appointments Table
CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY AUTO_INCREMENT,
    PatientID INT,
    DoctorID INT,
    AppointmentDateTime DATETIME,
    Status ENUM('Scheduled', 'Completed', 'Cancelled'),
    Reason TEXT,
    Diagnosis TEXT,
    Prescription TEXT,
    FollowUpAppointment DATETIME,
    DurationMinutes INT,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
);



-- Table for Employees
CREATE TABLE Employees (
    EmployeeID INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Gender ENUM('Male', 'Female', 'Other'),
    DateOfBirth DATE,
    ContactNumber VARCHAR(15),
    Email VARCHAR(100),
    Address VARCHAR(255),
    Position ENUM('Administrator','Surgeon','Doctor','Physician','Nurse','Pharmacist','Laboratory Technician',
    'Dietitian','Physical Therapist'),
    JoiningDate DATE,
    Salary DECIMAL(10, 2)
    );

-- Table for User Accounts
CREATE TABLE UserAccounts (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    UserName VARCHAR(50) NOT NULL,
    Password VARCHAR(255) NOT NULL,  -- Store hashed passwords
    Role ENUM('Admin', 'Doctor', 'Nurse', 'Receptionist', 'Patient'),
    EmployeeID INT,
    PatientID INT,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);


CREATE TABLE Billing (
    BillingID INT PRIMARY KEY AUTO_INCREMENT,
    PatientID INT,
    AppointmentID INT,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    PaymentStatus ENUM('Pending', 'Paid') DEFAULT 'Pending',
    PaymentDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (AppointmentID) REFERENCES Appointments(AppointmentID)
);
