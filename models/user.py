from database.PROJECT1_db import load_users_db

class User: # User Class
    users = []
    def __init__(self, user_id=None, username=None, password=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.balance = 0
        self.tickets = []

    @staticmethod
    def load_users(): #Takes user data from database
        User.users.clear()
        db_users = load_users_db()
        for u in db_users:
            User.users.append(u)
    
    @staticmethod
    def return_user(username): # Return specific User
        for u in User.users:
            if u["username"]==username:
                return u
        return None
