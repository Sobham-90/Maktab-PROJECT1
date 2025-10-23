from services.os import clear_console
from database.PROJECT1_db import *
from models.trips import Trips
from datetime import datetime
from models.user import User
from models.admin import Admin
from services.log_service import get_logger

logger = get_logger()

def admin_login(args=None):
    """
    Admin dashboard, works interactively or with argparse.
    Args can contain username, password, add_trip, remove_trip, etc.
    """
    User.load_users()
    Trips.load_trips()
    Admin.load_admins()

    if args and args.username and args.password:
        username = args.username
        password = args.password
        admin_loggin = check_admin_sign_up(username, password)

        if not admin_loggin:
            print(f"Invalid CLI admin credentials: {username}")
            return
    else:
        username = input("Enter Admin username: ")
        password = input("Enter Admin password: ")
        admin_loggin = check_admin_sign_up(username, password)
        if not admin_loggin:
            print("Invalid Username or Password. Try again.")
            return

    logger.info(f"Admin {username} logged in")

    # ADMIN DASHBOARD
    while True:
        print(f"\n#=========================#\n#==== ADMIN DASHBOARD ====#\n#=========================#\n")
        run_admindashboard = input("1.Add Trip | 2.Remove Trip | 3.Edit Trip | 4.Show Venues | 5.Show All Users Data (Superuser) | 6.Back: ")

        # Add Trip
        if run_admindashboard == "1":
            try:
                if args and hasattr(args, "add_trip") and args.add_trip:
                    trip_data = args.add_trip
                    trip_id = trip_data["trip_id"]
                    origin = trip_data["origin"]
                    destination = trip_data["destination"]
                    start_time = datetime.strptime(trip_data["start_time"], "%Y-%m-%d %H:%M")
                    end_time = datetime.strptime(trip_data["end_time"], "%Y-%m-%d %H:%M")
                    price = trip_data["price"]
                    seats = trip_data["seats"]
                else:
                    trip_id = int(input("Trip ID: "))
                    origin = input("Trip Origin: ")
                    destination = input("Trip Destination: ")
                    start_time = datetime.strptime(input("Trip Start Time (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
                    end_time = datetime.strptime(input("Trip End Time (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
                    price = int(input("Trip Price: "))
                    seats = int(input("Total Number of Seats: "))

                now_time = datetime.now()
                if now_time > start_time:
                    raise Exception("Start time of Trip has passed!")
                elif end_time <= start_time:
                    raise Exception("End time cannot be earlier than start time!")
                else:
                    add_trips_db(trip_id, origin, destination, start_time, end_time, price, seats)
                    set_trip_state(trip_id, 'available')
                    print("Trip added successfully")
                    logger.info(f"Trip {trip_id} added by Admin {username}")

            except Exception as e:
                print(f"Error adding trip: {e}")
                logger.error(f"Error adding trip by Admin {username}")

        # Soft Remove Trip
        elif run_admindashboard == "2":
            for trip in Trips.trips:
                print(f"Trip ID {trip['trip_id']} | {trip['origin']} -> {trip['destination']} | Start {trip['start_time']}")
            travel_id = int(input("Insert Trip_ID to remove: "))
            trip_found = False
            for t in Trips.trips:
                if t["trip_id"] == travel_id:
                    set_trip_state(t["trip_id"], 'removed')
                    print(f"Trip ID {travel_id} removed successfully")
                    logger.info(f"Trip {travel_id} removed by Admin {username}")
                    trip_found = True
                    break
            if not trip_found:
                print("No trip with that ID!")

        # Edit Trip
        elif run_admindashboard == "3":
            pass

        # Show Venues
        elif run_admindashboard == "4":
            venue_dashboard = input("1.Show a trip venue | 2.Show all venues | 3.Back: ")
            if venue_dashboard == "1":
                for trip in Trips.trips:
                    print(f"Trip ID {trip['trip_id']} | {trip['origin']} -> {trip['destination']} | Start {trip['start_time']}")
                travel_id = int(input("Insert Trip ID to see venue: "))
                selected_trip = next((t for t in Trips.trips if t["trip_id"] == travel_id), None)
                if selected_trip:
                    print(f"Trip {selected_trip['trip_id']} venue = {trip_venue(selected_trip['trip_id'])}")
            elif venue_dashboard == "2":
                print(f"Total Venue = {total_income()}")

        # Superuser Menu
        elif run_admindashboard == "5":
            if username != "Superuser":
                print("Access denied! Only Superuser can view all users.")
                continue
            if not User.users:
                print("No users added yet.")
            else:
                print(User.users)

        # Back to Main Menu
        elif run_admindashboard == "6":
            clear_console()
            return

        else:
            print("Invalid input. Try again.")