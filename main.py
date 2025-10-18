from services.user_service import user_dashboard
from services.admin_service import admin_login
from models.user import User
from models.trips import Trips
from models.admin import Admin

def main():
    User.load_users()
    Trips.load_trips()
    Admin.load_admins()

    while True:
        start = input("\n1. User Sign Up // Login - 2. Admin Login - 3. View Trips - 4. Exit : ")
        if start == "1":
            User.load_users()
            Trips.load_trips()
            user_dashboard()
        elif start == "2":
            User.load_users()
            Trips.load_trips()
            admin_login()
        elif start == "3":
            Trips.load_trips()
            Trips.display_all_trips()
        elif start == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid input. Try again.")
            break

if __name__ == "__main__":
    main()