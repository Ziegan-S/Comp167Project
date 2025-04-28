import Majors
import Rosters
import Users
from Role import Role
from Majors import major_list, Major

user_list = []

def print_user_list():
    for user in user_list:  # Make this into SQL (get rid of user_list)
        print(
            f"{user.id} {user.userName} {user.userPassword} {user.fname} {user.lname} {user.major} {user.role.roleID} {user.role.roleName}")


def user_creation(cursor):
    cursor.execute("SELECT id, role FROM roles")  # Gets roleID and roleName columns from SQL (tuples)
    roleRows = cursor.fetchall()
    for row in roleRows:  # each list of data in tuple
        if row[0] == "stu":  # if first item in list is stu referring to the student role
            stu = Role(row[0], row[1])  # make a role for the student
            # stu.display_info()
            stu.append_role()  # append the role to the list of roles
        elif row[0] == "mgr":  # same concept as student
            mgr = Role(row[0], row[1])
            # mgr.display_info()
            mgr.append_role()
        else:
            print("role error")

    cursor.execute("SELECT * FROM users")  # Getting all users from user table
    UserRows = cursor.fetchall()
    for row in UserRows:  # each list of data in tuple
        if row[
            6] == "stu" and stu is not None:  # if role is the "Student" role. Also stu cannot be None to avoid NULL roles
            if row[5] is None:
                user = User(row[0], row[1], row[2], row[3], row[4], None, stu)
                #user.display_info()
                user.appendUser_list()  # append to list of users
            else:
                for major in Majors.major_list:
                    if major.id == row[5]:
                        user = User(row[0], row[1], row[2], row[3], row[4], major,
                                    stu)  # create a student user (stu is roleID for student)
                        #user.display_info()
                        user.appendUser_list()  # append to list of users

        elif row[6] == "mgr" and mgr is not None:  # Same concept as student
            user = User(row[0], row[1], row[2], row[3], row[4], None, mgr)
            #user.display_info()
            user.appendUser_list()
        else:
            print("User Error")


class User:
    def __init__(self, id, userName, userPassword, fname, lname, major, role):
        self.id = id
        self.userName = userName
        self.userPassword = userPassword
        self.fname = fname
        self.lname = lname
        self.major = major
        self.role = role

    def display_info(self):
        print(
            f"{self.id} {self.fname} {self.lname} {self.userName} {self.userPassword} {self.role.roleID} {self.role.roleName}")

    def display_student_info(self):
        if self.major is not None:
            print(f"ID: {self.id} FIRST NAME: {self.fname} LAST NAME: {self.lname} MAJOR: {self.major.major_name}")
        else:
            print(f"ID: {self.id} FIRST NAME: {self.fname} LAST NAME: {self.lname} MAJOR: None")

    def appendUser_list(self):
        user_list.append(self)

    def display_student_menu(self):
        print("   MENU   ")
        print("Press V to View Classes")
        print("Press D to Drop a Class")
        print("Press Q to Quit")

    def display_manager_menu(self):
        print("           MENU           ")
        print("Press S to View a Student's Schedule")
        print("Press V to View a Class Roster")
        print("Press R to Add a Student to a Roster")
        print("Press D to Drop a Student from a Roster")
        print("Press A to Add a Student")
        print("Press C to View All Students")
        print("Press L to View All Classes")
        print("Press M to View All Majors")
        print("Press Q to Quit")

    def mgr_view_classes(self, cursor, student_id):
        class_count = 0
        user_found = False
        for user in user_list:
            if user.id == student_id and user.role.roleID == 'stu':
                user_found = True
                cursor.execute(f'SELECT * FROM rosterclass WHERE userid = {student_id}')
                role_rows = cursor.fetchall()
                print(f"{user.fname} {user.lname}'s Classes")
                for row in role_rows:
                    class_count += 1
                    for roster in Rosters.roster_list:
                        if roster.id == row[0]:
                            print(f'{class_count}. {roster.className}')
                if class_count == 0:
                    print('NO CLASSES')
        if not user_found:
            print("ERROR STUDENT NOT FOUND")

    def mgr_view_roster(self, cursor, class_code):
        student_count = 0
        class_found = False
        for roster in Rosters.roster_list:
            if roster.code == class_code:
                class_found = True
                cursor.execute(f'SELECT * FROM rosterclass WHERE rosterid = {roster.id}')
                rows = cursor.fetchall()
                print(f"    {roster.className}    ")
                for row in rows:
                    for user in Users.user_list:
                        if user.id == row[1]:
                            student_count += 1
                            print(f'{student_count}. {user.fname} {user.lname}')
                if student_count == 0:
                    print('NO STUDENTS')
        if not class_found:
            print("ERROR CLASS NOT FOUND")

    def mgr_add_to_roster(self, cursor, class_code, user_id):
        student_found = False
        roster_found = False
        fname = None
        lname = None
        for user in Users.user_list:
            if user.id == user_id and user.role.roleID == 'stu':
                student_found = True
                fname = user.fname
                lname = user.lname
        if not student_found:
            print('ERROR: ID NOT ASSOCIATED WITH A STUDENT')
        for roster in Rosters.roster_list:
            if roster.code == class_code:
                roster_found = True
                cursor.execute("INSERT INTO rosterclass (rosterid, userid) VALUES (%s, %s)",
                               (roster.id, user_id))
                if (fname is not None) and (lname is not None):
                    print(f'{fname} {lname} ADDED TO {roster.className}')
        if not roster_found:
            print('ERROR: CODE NOT ASSOCIATED WITH A CLASS')

    def mgr_drop_from_roster(self, cursor, class_code, user_id):
        student_found = False
        roster_found = False
        fname = None
        lname = None
        for user in Users.user_list:
            if user.id == user_id and user.role.roleID == 'stu':
                student_found = True
                fname = user.fname
                lname = user.lname
        if not student_found:
            print('ERROR: ID NOT ASSOCIATED WITH A STUDENT')
        for roster in Rosters.roster_list:
            if roster.code == class_code:
                roster_found = True
                cursor.execute(f'DELETE FROM rosterclass where rosterid = {roster.id} and userid = {user_id}')
                if (fname is not None) and (lname is not None):
                    print(f'{fname} {lname} DROPPED FROM {roster.className}')
        if not roster_found:
            print('ERROR: CODE NOT ASSOCIATED WITH A CLASS')

    def mgr_add_student(self, cursor, username, password, fname, lname, student_major):
        major_found = False
        for major in Majors.major_list:
            if major.major_name == student_major:
                major_found = True
                cursor.execute(
                    "INSERT INTO users (username, userpassword, fname, lname, majorid, roleID ) VALUES (%s, %s, %s, %s, %s, %s)",
                    (username, password, fname, lname, major.id, 'stu'))
                print(f'{fname} {lname} ADDED')
        if not major_found:
            print('ERROR: MAJOR NOT FOUND')

    def add_student_to_user_list(self, cursor, fname, lname, major_name):
        for role in Role.role_list:
            if role.roleID == 'stu':
                for major in Majors.major_list:
                    if major.major_name == major_name:

                        cursor.execute(f"SELECT * FROM users WHERE fname = '{fname}' and lname = '{lname}'")
                        s_stu = cursor.fetchall()
                        for s in s_stu:
                            if s[0] is not None:
                                added_student = User(s[0], s[1], s[2], s[3], s[4], major, role)
                                user_list.append(added_student)
                                print(f'TRANSACTION SUCCESSFUL')
                            else:
                                print('ERROR: STUDENT NOT ADDED TO DATABASE')

    def mgr_view_all_students(self):
        for user in user_list:
            if user.role.roleID == "stu":
                user.display_student_info()

    def mgr_view_all_classes(self):
        for roster in Rosters.roster_list:
            roster.display_info()

    def mgr_view_all_majors(self):
        for major in Majors.major_list:
            major.display_info()

    def view_classes(self, cursor):
        cursor.execute(f'SELECT * FROM rosterclass WHERE userid = {self.id}')
        role_rows = cursor.fetchall()
        class_count = 0
        print(f"{self.fname} {self.lname}'s Classes")
        for row in role_rows:
            for roster in Rosters.roster_list:
                if roster.id == row[0]:
                    class_count += 1
                    print(
                        f'{class_count}. CLASS: {roster.className} CODE: {roster.code}')
        if class_count == 0:
            print('NO CLASSES')

    def drop_class(self, cursor, user_class):
        roster_found = False
        for roster in Rosters.roster_list:
            if roster.code == user_class:
                roster_found = True
                cursor.execute(f'DELETE FROM rosterclass where rosterid = {roster.id} and userid = {self.id}')
                print(f'YOU DROPPED: {roster.className}')
        if not roster_found:
            print('ERROR: ID NOT ASSOCIATED WITH A CLASS')