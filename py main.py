import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE CONNECTION
def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("MYSQL_PASSWORD"),
        database="student_management"
    )


# VALIDATE STUDENT ID
def get_student_id():
    while True:
        student_id = input("Enter student ID: ")

        if student_id.isdigit() and int(student_id) > 0:
            return int(student_id)

        print("Please enter a valid student ID!")


# VALIDATE AGE
def get_age():
    while True:
        try:
            age = int(input("Enter student age: "))

            if age > 0:
                return age

            print("Age must be greater than 0!")

        except ValueError:
            print("Please enter a valid number!")


# VALIDATE EMAIL
def get_email():
    while True:
        email = input("Enter email: ").strip()

        if "@" in email and "." in email.split("@")[-1]:
            return email

        print("Please enter a valid email!")


# ADD STUDENT
def add_student():
    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty!")
        return

    age = get_age()

    department = input("Enter department: ").strip()

    if not department:
        print("Department cannot be empty!")
        return

    email = get_email()

    connection = None
    cursor = None

    try:
        connection = connect_database()
        cursor = connection.cursor()

        query = """
        INSERT INTO students (name, age, department, email)
        VALUES (%s, %s, %s, %s)
        """

        values = (name, age, department, email)

        cursor.execute(query, values)
        connection.commit()

        print("Student added successfully!")

    except mysql.connector.Error as error:
        print("Database Error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# VIEW ALL STUDENTS
def view_students():
    connection = None
    cursor = None

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

        if students:
            print("\n========== STUDENT LIST ==========")

            for student in students:
                print("\nStudent ID:", student[0])
                print("Name:", student[1])
                print("Age:", student[2])
                print("Department:", student[3])
                print("Email:", student[4])
                print("----------------------------------")
        else:
            print("No students found!")

    except mysql.connector.Error as error:
        print("Database Error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# SEARCH STUDENT
def search_student():
    student_id = get_student_id()

    connection = None
    cursor = None

    try:
        connection = connect_database()
        cursor = connection.cursor()

        query = "SELECT * FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))

        student = cursor.fetchone()

        if student:
            print("\n--- STUDENT FOUND ---")
            print("Student ID:", student[0])
            print("Name:", student[1])
            print("Age:", student[2])
            print("Department:", student[3])
            print("Email:", student[4])
        else:
            print("Student not found!")

    except mysql.connector.Error as error:
        print("Database Error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# UPDATE STUDENT
def update_student():
    student_id = get_student_id()

    connection = None
    cursor = None

    try:
        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print("Student ID not found!")
            return

        name = input("Enter new name: ").strip()

        if not name:
            print("Name cannot be empty!")
            return

        age = get_age()

        department = input("Enter new department: ").strip()

        if not department:
            print("Department cannot be empty!")
            return

        email = get_email()

        query = """
        UPDATE students
        SET name = %s, age = %s, department = %s, email = %s
        WHERE student_id = %s
        """

        values = (name, age, department, email, student_id)

        cursor.execute(query, values)
        connection.commit()

        print("Student updated successfully!")

    except mysql.connector.Error as error:
        print("Database Error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# DELETE STUDENT
def delete_student():
    student_id = get_student_id()

    connection = None
    cursor = None

    try:
        connection = connect_database()
        cursor = connection.cursor()

        query = "DELETE FROM students WHERE student_id = %s"

        cursor.execute(query, (student_id,))
        connection.commit()

        if cursor.rowcount > 0:
            print("Student deleted successfully!")
        else:
            print("Student ID not found!")

    except mysql.connector.Error as error:
        print("Database Error:", error)

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# MAIN MENU
while True:

    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        print("Thank you! Exiting Student Management System.")
        break

    else:
        print("Invalid choice! Please enter 1 to 6.")