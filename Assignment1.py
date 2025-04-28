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
        self.root.geometry("300x200")
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

        tk.Button(self.root, text="View All Students", command=user.mgr_view_all_students).pack(pady=5)
        tk.Button(self.root, text="View All Classes", command=user.mgr_view_all_classes).pack(pady=5)
        tk.Button(self.root, text="View All Majors", command=user.mgr_view_all_majors).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.restart).pack(pady=20)

    def show_student_menu(self, user):
        self.clear_window()
        tk.Label(self.root, text="Student Menu", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.root, text="View My Classes", command=lambda: user.view_classes(cursor)).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.restart).pack(pady=20)

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











