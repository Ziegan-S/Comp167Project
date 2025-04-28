class Role:
    role_list = []

    def __init__(self, roleID, roleName):
        self.roleID = roleID
        self.roleName = roleName

    def display_info(self):
        print(f"{self.roleID} {self.roleName}")

    def append_role(self):
        self.role_list.append(self)
