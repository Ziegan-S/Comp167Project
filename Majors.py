major_list = []


def create_new_major(cursor):
    cursor.execute("SELECT id, major from major")
    major_rows = cursor.fetchall()
    for major in major_rows:
        major = Major(major[0], major[1])
        major.append_major_list()


class Major:

    def __init__(self, id, major_name):
        self.id = id
        self.major_name = major_name

    def display_info(self):
        print(f"MAJOR: {self.major_name}")

    def append_major_list(self):
        major_list.append(self)
