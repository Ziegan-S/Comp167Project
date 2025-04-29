
#3/23/25 Sage Snead Comp 267 Professor Leflore
#I am creating a program that communicates with a MySQL database of users and roles to authorize a client to log into a python program.

import mysql.connector
from mysql.connector import errorcode
from Role import Role
import Users
import Rosters
from Users import User, user_creation, print_user_list, user_list
from Rosters import create_new_roster, print_roster_list, Roster
from Majors import create_new_major, Major, major_list
import Majors

import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("User Login")
        self.root.geometry("300x325")
        self.number_of_attempts = 1

        tk.Label(root, text="Username").pack(pady=(10, 0))
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack(pady=(10, 0))
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        for user in Users.user_list:
            if username == user.userName and password == user.userPassword:
                messagebox.showinfo("Login Success", f"Welcome, {user.fname}!")
                if user.role.roleID == "mgr":
                    self.show_manager_menu(user)
                elif user.role.roleID == "stu":
                    self.show_student_menu(user)
                else:
                    messagebox.showerror("Error", "Unknown role")
                return

        messagebox.showerror("Login Failed", "Incorrect username or password")
        self.number_of_attempts += 1
        if self.number_of_attempts > 3:
            print("ERROR: MAX NUMBER OF ATTEMPTS REACHED")
            root.destroy()


    def show_manager_menu(self, user):
        self.clear_window()
        tk.Label(self.root, text="Manager Menu", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="View Student", command=lambda: self.view_student(user)).pack(pady=5)
        tk.Button(self.root, text="View Roster", command=lambda: self.view_roster(user)).pack(pady=5)
        tk.Button(self.root, text="Add Student to Roster", command=lambda: self.add_student(user)).pack(pady=5)
        tk.Button(self.root, text="Drop Student from Roster", command=lambda: self.drop_student(user)).pack(pady=5)
        tk.Button(self.root, text="Add Student", command=lambda: self.new_student(user)).pack(pady=5)

        # tk.Button(self.root, text="View All Students", command=user.mgr_view_all_students).pack(pady=5)
        # tk.Button(self.root, text="View All Classes", command=user.mgr_view_all_classes).pack(pady=5)
        # tk.Button(self.root, text="View All Majors", command=user.mgr_view_all_majors).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.restart).pack(pady=20)

    def view_student(self, user):
        self.clear_window()
        tk.Label(self.root, text="Enter Student ID:", font=("Arial", 14)).pack(pady=10)

        student_id_entry = tk.Entry(self.root)
        student_id_entry.pack(pady=5)

        def submit_student_id():
            try:
                student_id = int(student_id_entry.get())
                user.mgr_view_classes(cursor, student_id)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid numeric Student ID")

        tk.Button(self.root, text="Submit", command=submit_student_id).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.show_manager_menu(user)).pack(pady=5)

    def view_roster(self, user):
        self.clear_window()
        tk.Label(self.root, text="Enter Class Code:", font=("Arial", 14)).pack(pady=10)

        class_id_entry = tk.Entry(self.root)
        class_id_entry.pack(pady=5)

        def submit_roster_id():
            try:
                class_id = str(class_id_entry.get())
                user.mgr_view_roster(cursor, class_id)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid numeric Roster ID")

        tk.Button(self.root, text="Submit", command=submit_roster_id).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.show_manager_menu(user)).pack(pady=5)

    def add_student(self, user):
        self.clear_window()
        tk.Label(self.root, text="Enter Class Code:", font=("Arial", 14)).pack(pady=10)
        class_id_entry = tk.Entry(self.root)
        class_id_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Student ID:", font=("Arial", 14)).pack(pady=10)
        student_id_entry = tk.Entry(self.root)
        student_id_entry.pack(pady=5)


        def submit_student_add():
            try:
                class_id = str(class_id_entry.get())
                student_id = int(student_id_entry.get())
                user.mgr_add_to_roster(cursor, class_id, student_id)
                connection.commit()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid Code or ID")

        tk.Button(self.root, text="Submit", command=submit_student_add).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.show_manager_menu(user)).pack(pady=5)

    def drop_student(self, user):
        self.clear_window()
        tk.Label(self.root, text="Enter Class Code:", font=("Arial", 14)).pack(pady=10)
        class_id_entry = tk.Entry(self.root)
        class_id_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Student ID:", font=("Arial", 14)).pack(pady=10)
        student_id_entry = tk.Entry(self.root)
        student_id_entry.pack(pady=5)


        def submit_student_drop():
            try:
                class_id = str(class_id_entry.get())
                student_id = int(student_id_entry.get())
                user.mgr_drop_from_roster(cursor, class_id, student_id)
                connection.commit()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid Code or ID")

        tk.Button(self.root, text="Submit", command=submit_student_drop).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.show_manager_menu(user)).pack(pady=5)

    def new_student(self, user):
        self.clear_window()
        tk.Label(self.root, text="Enter Username:", font=("Arial", 14)).pack(pady=10)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Password:", font=("Arial", 14)).pack(pady=10)
        password_entry = tk.Entry(self.root)
        password_entry.pack(pady=5)

        tk.Label(self.root, text="Enter First Name:", font=("Arial", 14)).pack(pady=10)
        fname_entry = tk.Entry(self.root)
        fname_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Last Name:", font=("Arial", 14)).pack(pady=10)
        lname_entry = tk.Entry(self.root)
        lname_entry.pack(pady=5)

        tk.Label(self.root, text="Enter Student Major:", font=("Arial", 14)).pack(pady=10)
        student_major_entry = tk.Entry(self.root)
        student_major_entry.pack(pady=5)

        def submit_student_new():
            try:
                username = str(username_entry.get())
                password = str(password_entry.get())
                fname = str(fname_entry.get())
                lname = str(lname_entry.get())
                student_major = str(student_major_entry.get())
                user.mgr_add_student(cursor, username, password, fname, lname, student_major)
                user.add_student_to_user_list(cursor, fname, lname, student_major)
                connection.commit()
                print(f'{fname} {lname} ADDED')
            except ValueError:
                messagebox.showerror("Invalid Input", "Please retry")

        tk.Button(self.root, text="Submit", command=submit_student_new).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.show_manager_menu(user)).pack(pady=5)

    def show_student_menu(self, user):
        self.clear_window()
        tk.Label(self.root, text="Student Menu", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="View My Classes", command=lambda: user.view_classes(cursor)).pack(pady=5)
        tk.Button(self.root, text="Drop a Class", command=lambda: self.drop_class(user)).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.restart).pack(pady=20)

    def drop_class(self, user):
        self.clear_window()
        tk.Label(self.root, text="Enter Class to Drop:", font=("Arial", 14)).pack(pady=10)
        class_id_entry = tk.Entry(self.root)
        class_id_entry.pack(pady=5)

        def submit_class_drop():
            try:
                class_id = str(class_id_entry.get())
                user.drop_class(cursor, class_id)
                connection.commit()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid Code")

        tk.Button(self.root, text="Submit", command=submit_class_drop).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.show_manager_menu(user)).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def restart(self):
        self.clear_window()
        self.__init__(self.root)


# def login():
#     # LOGIN
#     not_logged_in = True  # Storing state of login
#     number_of_attempts = 1
#     while number_of_attempts < 4 and not_logged_in:  # So the login inputs keep coming up on incorrect logins
#         print("LOGIN PAGE")
#         username = input("Enter Username: ")  # Inputs
#         password = input("Enter Password: ")
#
#         login_success = False  # Storing success of login
#
#         for user in Users.user_list:
#             print(user.userName)
#             print(user.userPassword)
#             if username == user.userName and password == user.userPassword:  # if username and password match a user
#                 login_success = True  # login is successful
#                 not_logged_in = False  # you are logged in
#                 if user.role.roleID == "mgr":  # if the roleID refers to the manager role
#                     while True:
#                         user.display_manager_menu()
#                         user_input = input('SELECTION: ')
#                         if user_input == 'S':
#                             viewed_student = int(input("Enter the Student's ID: "))
#                             user.mgr_view_classes(cursor, viewed_student)
#
#                         elif user_input == 'V':
#                             viewed_roster = input("Enter the Class Code: ")
#                             user.mgr_view_roster(cursor, viewed_roster)
#                         elif user_input == 'R':
#                             roster = input("Enter the Class Code: ")
#                             added_student = int(input("Enter the Student's ID: "))
#                             user.mgr_add_to_roster(cursor, roster, added_student)
#                             connection.commit()
#                         elif user_input == 'D':
#                             roster = input("Enter the Class Code: ")
#                             dropped_student = int(input("Enter the Student's ID: "))
#                             user.mgr_drop_from_roster(cursor, roster, dropped_student)
#                             connection.commit()
#                         elif user_input == 'A':
#                             user_name = input('Enter Student Username: ')
#                             user_pass = input('Enter Student Password: ')
#                             f_name = input('Enter Student First Name: ')
#                             l_name = input('Enter Student Last Name: ')
#                             major = input('Enter Student Major: ')
#                             user.mgr_add_student(cursor, user_name, user_pass, f_name, l_name, major)
#                             connection.commit()
#                             user.add_student_to_user_list(cursor, f_name, l_name, major)
#                         elif user_input == 'C':
#                             user.mgr_view_all_students()
#                         elif user_input == 'L':
#                             user.mgr_view_all_classes()
#                         elif user_input == 'M':
#                             user.mgr_view_all_majors()
#                         elif user_input == 'Q':
#                             break
#
#                 elif user.role.roleID == "stu":  # similar concept to manager
#                     while True:
#                         user.display_student_menu()
#                         user_input = input('SELECTION: ')
#                         if user_input == 'V':
#                             user.view_classes(cursor)
#                         elif user_input == 'D':
#                             dropped_class = input('Enter the Code of the class to be dropped: ')
#                             user.drop_class(cursor, dropped_class)
#                             connection.commit()
#                         elif user_input == 'Q':
#                             break
#                         else:
#                             print("INVALID SELECTION")
#
#
#                 else:
#                     print("Role not Recognized")  # in case of failures (unmatched roles)
#         if not login_success:  # if username and password do not match a user
#             print("LOGIN FAILED \n")
#         number_of_attempts += 1
#     if number_of_attempts > 3:
#         print("ERROR: MAX NUMBER OF ATTEMPTS REACHED")






if __name__ == "__main__":
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="AggieAdmin",
            password="AggiePride",
            database="ncat"
        )
        cursor = connection.cursor()

        # Populate initial data
        Majors.create_new_major(cursor)
        Users.user_creation(cursor)
        rosterView = "CREATE OR REPLACE VIEW rosterView AS SELECT * FROM roster"
        cursor.execute(rosterView)
        Rosters.create_new_roster(cursor)

        # Start GUI instead of console login
        root = tk.Tk()
        app = App(root)
        root.mainloop()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database not found")
        else:
            print(f"Cannot connect to database: {err}")
    finally:
        if connection.is_connected():
            connection.close()



# if __name__ == "__main__":
#     try:
#         connection = mysql.connector.connect(  # logging into database without prompting user
#             host="localhost",
#             user="AggieAdmin",
#             password="AggiePride",
#             database="ncat"
#         )
#
#         cursor = connection.cursor()  # cursor for accessing information
#         # Calling functions
#         Majors.create_new_major(cursor)
#         Users.user_creation(cursor)
#         #Users.print_user_list()
#         Rosters.create_new_roster(cursor)
#         #Rosters.print_roster_list()
#
#         login()
#         #print("SUCESSFUL CONNECTION")
#
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("Invalid credintials")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("Database not found")
#         else:
#             print(f"Cannot connect to database: {err}")
#     else:
#         # print("Connection Successful!!")
#         connection.close()
