roster_list = []

def create_new_roster(cursor):
    cursor.execute("SELECT * from rosterView") #uses view for all rosters
    roster_rows = cursor.fetchall()
    for roster in roster_rows:
        roster = Roster(roster[0], roster[1], roster[2])
        roster.append_roster_list()


def print_roster_list():
    for roster in roster_list:
        print(f"{roster.id} {roster.className} ")


class Roster:

    def __init__(self, id, className, code):
        self.id = id
        self.className = className
        self.code = code

    def display_info(self):
        print(f"CLASS: {self.className} CODE: {self.code}")

    def append_roster_list(self):
        roster_list.append(self)
