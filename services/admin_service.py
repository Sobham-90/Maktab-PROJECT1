from database.PROJECT1_db import *
from models.trips import Trips
from datetime import datetime
from models.user import User
from models.trips import Trips
from models.admin import Admin

def admin_login():
    User.load_users()
    Trips.load_trips()
    Admin.load_admins()
    username = input("Enter Admin username: ")
    password = input("Enter Admin password: ")
    admin_loggin = check_admin_sign_up(username, password)

    if not admin_loggin:
        print("Invalid Username or Password. Try again.")
        return
    while True:
        print(f"\n#=========================#\n#==== ADMIN DASHBOARD ====#\n#=========================#\n")
        run_admindashboard = input("1.Add Trip - 2.Remove Trip - 3.Edite Trip - 4.Show Venues - 5.Show All Users Data (Superuser Only)- 6.Back to Main Menu:")

        if run_admindashboard == "1":  # Add Trip by Admin
            trip_id = int(input("Trip ID:"))
            origin = input("Trip Origin:")
            destination = input("Trip Destination:")
            start_time = datetime.strptime(input("Trip Start Time:"), "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(input("Trip End Time:"), "%Y-%m-%d %H:%M")
            price = int(input("Trip Price: "))
            seats = int(input("Total Number of Seats: "))

            now_time = datetime.now()
            try:
                if now_time > start_time:
                    raise Exception("Start time of Trip had Passed!")
                elif end_time <= start_time:
                    raise Exception("End time earlier than start time of Trip!")
                else:
                    add_trips_db(trip_id, origin, destination, start_time, end_time, price, seats)
                    set_trip_state (trip_id,'available')
                    print("Trip added successfully")
            except ValueError as e:
                print(f"{e} : Something goes wrong. Trip is not added.Try again.")

        elif run_admindashboard == "2":  # Remove Trip by Admin
            for trip in Trips.trips:
                print(f"Travel ID {trip['trip_id']} from {trip['origin']} to {trip['destination']} at {trip['start_time']}\n")
            travel_id = int(input("Insert Trip_ID you want to Remove: "))

            for t in Trips.trips:
                if t["trip_id"] != travel_id:
                    print("There is no Trip with such Trip_ID!")
                else:
                    set_trip_state(t["trip_id"],'removed')
                    print(f"Trip ID-{travel_id} Removed successfully!")

        elif run_admindashboard == "3":  # FIX HERE
            pass

        elif run_admindashboard == "4":  # Show venues
            venue_dashboard = input("1.Show a trip venue - 2.Show all venue - 3.Back to Admin Menu:")
            if venue_dashboard == "1":
                for trip in Trips.trips:
                    print(f"Travel {trip['trip_id']} from {trip['origin']} to {trip['destination']} at {trip['start_time']}\n")

                travel_id = int(input("Insert Trip ID to see venue: "))
                for t in Trips.trips:
                    if t["trip_id"] == travel_id:
                        print(f"Trip {t["trip_id"]} venue = {trip_venue(t["trip_id"])}")

            elif venue_dashboard == "2":
                print(f"Total Venue = {total_income()}")


        elif run_admindashboard == "5" and username == "Superuser":  # SuperUser
            if len(User.users) == 0:
                print("No users have been added")
            print(User.users)

        elif run_admindashboard == "6":
            return

        else:
            print("Invalid Input. Try again.")


