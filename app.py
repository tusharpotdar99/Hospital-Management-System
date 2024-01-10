from flask import Flask, render_template, request,redirect,url_for
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

app = Flask(__name__)

# Configure your MySQL database connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'TushSQL@1999',
    'database': 'hospital',
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='TushSQL@1999',
            database='hospital',)
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None, None

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']

    connection, cursor = connect_to_database()

    if connection:
        try:
            # select_query = "SELECT * FROM UserAccounts WHERE UserName = %s AND Password = %s"
            # cursor.execute(select_query, (username, password))
            # user = cursor.fetchone()

            # if user:
            #     role = user[3]  # Assuming role is in the fourth column of the UserAccounts table
            #     return redirect(url_for('dashboard', role=role))
            #     # return f'Login successful: UserID - {user[0]}, Username - {user[1]}, Role - {user[3]}'
            # else:
            #     return 'Login failed: Invalid username or password'

            select_query = "SELECT Role FROM UserAccounts WHERE UserName = %s AND Password = %s"
            cursor.execute(select_query, (username, password))
            role = cursor.fetchone()
            if role:
                return redirect(url_for('dashboard', role=role[0]))
            else:
                return 'Login failed: Invalid username or password'



        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 'Error: Unable to process the login request'

        finally:
            cursor.close()
            connection.close()
    else:
        return 'Error: Unable to connect to the database'

@app.route('/dashboard')
def dashboard():
    role = request.args.get('role')

    # Print the role for debugging
    print(f"Role received: {role}")

    if role:
        return render_template('dashboard.html', role=role)
    else:
        flash('Error: Role not specified for the dashboard')
        return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    signup_username = request.form['signup-username']
    signup_password = request.form['signup-password']
    role = request.form.get('role')  # Get selected role from the form
    employee_id = request.form.get('employee-id') or None  # Use None if not provided
    patient_id = request.form.get('patient-id') or None  # Use None if not provided

    connection, cursor = connect_to_database()

    if connection:
        try:
            insert_query = "INSERT INTO UserAccounts (UserName, Password, Role, EmployeeID, PatientID) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert_query, (signup_username, signup_password, role, employee_id, patient_id))
            connection.commit()

            return f'Signup successful: Username - {signup_username}, Role - {role}, EmployeeID - {employee_id}, PatientID - {patient_id}'

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 'Error: Unable to process the signup request'

        finally:
            cursor.close()
            connection.close()
    else:
        return 'Error: Unable to connect to the database'


@app.route('/create_patient')
def create_patient():
    return render_template('create_patient.html')

# Add the corresponding route for processing the form submission
@app.route('/create_patient', methods=['POST'])
def create_patient_post():
    # Assuming the form fields are named accordingly in create_patient.html
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    gender = request.form['gender']
    contact_number = request.form['contact_number']
    email = request.form['email']
    address = request.form['address']
    blood_type = request.form['blood_type']
    marital_status = request.form['marital_status']
    occupation = request.form['occupation']
    medical_conditions = request.form['medical_conditions']
    primary_physician = request.form['primary_physician']
    current_status = request.form['current_status']

    connection, cursor = connect_to_database()

    if connection:
        try:
            # Parse the input date of birth and format it to 'yyyy-mm-dd'
            # date_of_birth = datetime.strptime(date_of_birth_str, '%y-%m-%d').strftime('%Y-%m-%d')
            insert_query = "INSERT INTO Patients (FirstName, LastName, DateOfBirth, Gender, ContactNumber, Email, Address, " \
                           "BloodType, MaritalStatus, Occupation, MedicalConditions, PrimaryPhysician, CurrentStatus) " \
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(insert_query, (first_name, last_name, date_of_birth, gender, contact_number, email, address,
                                          blood_type, marital_status, occupation, medical_conditions, primary_physician,
                                          current_status))
            connection.commit()

            return 'Patient created successfully'

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 'Error: Unable to process the request'

        finally:
            cursor.close()
            connection.close()
    else:
        return 'Error: Unable to connect to the database'


@app.route('/create_doctor')
def create_doctor():
    return render_template('create_doctor.html')

# Add the corresponding route for processing the form submission
@app.route('/create_doctor', methods=['POST'])
def create_doctor_post():
    # Assuming the form fields are named accordingly in create_doctor.html
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    specialization = request.form['specialization']
    contact_number = request.form['contact_number']
    email = request.form['email']
    qualifications = request.form['qualifications']
    department = request.form['department']

    connection, cursor = connect_to_database()

    if connection:
        try:
            insert_query = "INSERT INTO Doctors (FirstName, LastName, Specialization, ContactNumber, Email, Qualifications, Department) " \
                           "VALUES (%s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(insert_query, (first_name, last_name, specialization, contact_number, email, qualifications, department))
            connection.commit()

            return 'Doctor created successfully'

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 'Error: Unable to process the request'

        finally:
            cursor.close()
            connection.close()
    else:
        return 'Error: Unable to connect to the database'


@app.route('/create_appointment')
def create_appointment():
    return render_template('create_appointment.html')

# Add the corresponding route for processing the form submission
@app.route('/create_appointment', methods=['POST'])
def create_appointment_post():
    # Assuming the form fields are named accordingly in create_appointment.html
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    appointment_date_time = request.form['appointment_date_time']
    status = request.form['status']
    reason = request.form['reason']
    diagnosis = request.form['diagnosis']
    prescription = request.form['prescription']
    follow_up_appointment = request.form['follow_up_appointment']
    duration_minutes = request.form['duration_minutes']

    connection, cursor = connect_to_database()

    if connection:
        try:
            insert_query = "INSERT INTO Appointments (PatientID, DoctorID, AppointmentDateTime, Status, Reason, " \
                           "Diagnosis, Prescription, FollowUpAppointment, DurationMinutes) " \
                           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(insert_query, (patient_id, doctor_id, appointment_date_time, status, reason,
                                          diagnosis, prescription, follow_up_appointment, duration_minutes))
            connection.commit()

            return 'Appointment created successfully'

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 'Error: Unable to process the request'

        finally:
            cursor.close()
            connection.close()
    else:
        return 'Error: Unable to connect to the database'

@app.route('/create_billing')
def create_billing():
    return render_template('billing.html')

# Add the corresponding route for processing the form submission
@app.route('/create_billing', methods=['POST'])
def create_billing_post():
    # Assuming the form fields are named accordingly in create_billing.html
    patient_id = request.form['patient_id']
    appointment_id = request.form['appointment_id']
    total_amount = request.form['total_amount']
    payment_status = request.form['payment_status']
    payment_date = request.form['payment_date']

    connection, cursor = connect_to_database()

    if connection:
        try:
            insert_query = "INSERT INTO Billing (PatientID, AppointmentID, TotalAmount, PaymentStatus, PaymentDate) " \
                           "VALUES (%s, %s, %s, %s, %s)"

            cursor.execute(insert_query, (patient_id, appointment_id, total_amount, payment_status, payment_date))
            connection.commit()

            return 'Billing record created successfully'

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 'Error: Unable to process the request'

        finally:
            cursor.close()
            connection.close()
    else:
        return 'Error: Unable to connect to the database'

@app.route('/create_employee')
def create_employee():
    return render_template('create_employee.html')

# Add the corresponding route for processing the form submission
@app.route('/create_employee', methods=['POST'])
def create_employee_post():
    # Assuming the form fields are named accordingly in create_employee.html
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    gender = request.form['gender']
    date_of_birth = request.form['date_of_birth']
    contact_number = request.form['contact_number']
    email = request.form['email']
    address = request.form['address']
    position = request.form['position']
    joining_date = request.form['joining_date']
    salary = request.form['salary']

    connection, cursor = connect_to_database()

    if connection:
        try:
            insert_query = "INSERT INTO Employees (FirstName, LastName, Gender, DateOfBirth, ContactNumber, Email, Address, " \
                           "Position, JoiningDate, Salary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(insert_query, (first_name, last_name, gender, date_of_birth, contact_number, email, address,
                                          position, joining_date, salary))
            connection.commit()

            return 'Employee created successfully'

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 'Error: Unable to process the request'

        finally:
            cursor.close()
            connection.close()
    else:
        return 'Error: Unable to connect to the database'

@app.route('/display_table')
def display_table():
    # # Connect to the database
    # connection = connect_to_database()
    connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='TushSQL@1999',
            database='hospital',)
    cursor = connection.cursor(dictionary=True)
    # connection, cursor = connect_to_database()

    # Execute a SELECT query to fetch data from your table
    select_query = "SELECT * FROM Patients"
    cursor.execute(select_query)
    
    # Fetch all rows from the result
    data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    # Render the HTML template with the fetched data
    return render_template('display_table.html', data=data)

@app.route('/update_record', methods=['POST'])
def update_record():
    # Get the form data
    patient_id = request.form.get('patient_id')
    edit_first_name = request.form.get('edit_first_name')
    edit_last_name = request.form.get('edit_last_name')
    # if not edit_first_name or not edit_last_name:
    #     return 'Error: First Name and Last Name cannot be empty'
    edit_date_of_birth = request.form.get('edit_date_of_birth')
    edit_gender = request.form.get('edit_gender')
    edit_contact_number = request.form.get('edit_contact_number')
    edit_email = request.form.get('edit_email')
    edit_address = request.form.get('edit_address')
    edit_blood_type = request.form.get('edit_blood_type')
    edit_marital_status = request.form.get('edit_marital_status')
    edit_occupation = request.form.get('edit_occupation')
    edit_medicalconditions = request.form.get('edit_medicalconditions')
    edit_primaryphysicians = request.form.get('edit_primaryphysicians')
    edit_currentstatus = request.form.get('edit_currentstatus')



    # Retrieve other form fields similarly

    # Connect to the database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='TushSQL@1999',
        database='hospital',)
    cursor = connection.cursor(dictionary=True)

    # Update the record in the database 
    update_query = "UPDATE Patients SET FirstName = %s, LastName = %s, DateOfBirth = %s, Gender = %s, ContactNumber = %s, Email = %s, Address = %s, BloodType = %s, MaritalStatus = %s, Occupation = %s, MedicalConditions = %s, PrimaryPhysician = %s, CurrentStatus = %s  WHERE PatientID = %s"
    cursor.execute(update_query, (edit_first_name,edit_last_name,edit_date_of_birth,edit_gender,edit_contact_number,edit_email,edit_address,edit_blood_type,edit_marital_status,edit_occupation,edit_medicalconditions,edit_primaryphysicians,edit_currentstatus, patient_id))
    # Update other columns similarly

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()

    # Redirect back to the display_table route after the update
    return redirect(url_for('display_table'))


@app.route('/doctors')
def doctors():
    # # Connect to the database
    # connection = connect_to_database()
    connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='TushSQL@1999',
            database='hospital',)
    cursor = connection.cursor(dictionary=True)
    # connection, cursor = connect_to_database()

    # Execute a SELECT query to fetch data from your table
    select_query = "SELECT * FROM Doctors"
    cursor.execute(select_query)
    
    # Fetch all rows from the result
    data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    # Render the HTML template with the fetched data
    return render_template('Doctors.html', data=data)

@app.route('/appointments')
def appointments():
    # # Connect to the database
    # connection = connect_to_database()
    connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='TushSQL@1999',
            database='hospital',)
    cursor = connection.cursor(dictionary=True)
    # connection, cursor = connect_to_database()

    # Execute a SELECT query to fetch data from your table
    select_query = "SELECT * FROM Appointments"
    cursor.execute(select_query)
    
    # Fetch all rows from the result
    data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    # Render the HTML template with the fetched data
    return render_template('Appointments.html', data=data)

@app.route('/employees')
def employees():
    # # Connect to the database
    # connection = connect_to_database()
    connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='TushSQL@1999',
            database='hospital',)
    cursor = connection.cursor(dictionary=True)
    # connection, cursor = connect_to_database()

    # Execute a SELECT query to fetch data from your table
    select_query = "SELECT * FROM Employees"
    cursor.execute(select_query)
    
    # Fetch all rows from the result
    data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    # Render the HTML template with the fetched data
    return render_template('employee.html', data=data)

@app.route('/bills')
def bills():
    # # Connect to the database
    # connection = connect_to_database()
    connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='TushSQL@1999',
            database='hospital',)
    cursor = connection.cursor(dictionary=True)
    # connection, cursor = connect_to_database()

    # Execute a SELECT query to fetch data from your table
    select_query = "SELECT * FROM Billing"
    cursor.execute(select_query)
    
    # Fetch all rows from the result
    data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    # Render the HTML template with the fetched data
    return render_template('bills.html', data=data)


@app.route('/useraccount')
def useraccount():
    # # Connect to the database
    # connection = connect_to_database()
    connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='TushSQL@1999',
            database='hospital',)
    cursor = connection.cursor(dictionary=True)
    # connection, cursor = connect_to_database()

    # Execute a SELECT query to fetch data from your table
    select_query = "SELECT * From UserAccounts"
    cursor.execute(select_query)
    
    # Fetch all rows from the result
    data = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()
    # Render the HTML template with the fetched data
    return render_template('user_accounts.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)















if __name__ == '__main__':
    app.run(debug=True)
