from database.PROJECT1_db import load_admins_db

class Admin: # Admin Class
    admins =[]
    def __init__(self,username, password):
        self.username = username
        self.password = password
    
    @staticmethod
    def load_admins(): #Takes Admin data from database
        Admin.admins.clear()
        db_admins = load_admins_db()
        for a in db_admins:
            Admin.admins.append(a)
    
    @staticmethod
    def return_admin(admin_user): # Return specific Admin
        for a in Admin.admins:
            if a["username"] == admin_user:
                return a
        return None