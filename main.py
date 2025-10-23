import argparse
from services.os import clear_console
from services.user_service import user_dashboard
from services.admin_service import admin_login
from models.user import User
from models.trips import Trips
from models.admin import Admin
from services.log_service import get_logger

logger = get_logger()

parser = argparse.ArgumentParser(description="Ticket Booking System Main CLI")
parser.add_argument('--mode',choices=['user', 'admin', 'view_trips', 'exit'],
    help='Select mode: user dashboard, admin dashboard, view trips, or exit'
)
parser.add_argument('--username', type=str, help='Username for user/admin login')
parser.add_argument('--password', type=str, help='Password for user/admin login')
args = parser.parse_args()


def main(): #Load Datas
    User.load_users()
    Trips.load_trips()
    Admin.load_admins()

    if args.mode:
        if args.mode == "user":
            user_dashboard(args)  
        elif args.mode == "admin":
            admin_login(args)  
        elif args.mode == "view_trips":
            Trips.display_all_trips()
        elif args.mode == "exit":
            print("Good Bye!")
            clear_console()
        


    while True:
        start = input("\n1. User Sign Up // Login - 2. Admin Login - 3. View Trips - 4. Exit: ")
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
            clear_console()
            break
        else:
            print("Invalid input. Try again.")
            logger.error("Invalid Input in main dashboard")
            clear_console()
            break

if __name__ == "__main__":
    main()