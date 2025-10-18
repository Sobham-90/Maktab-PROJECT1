from datetime import datetime
from random import choice

from validations_v4 import username_validator,password_validator
import PROJECT1_db_v4

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
        db_users = PROJECT1_db_v4.load_users_db()
        for u in db_users:
            User.users.append(u)
    
    @staticmethod
    def return_user (username): # Return specific User
        for u in User.users:
            if u["username"]==username:
                return u
        return None
        

class Admin: # Admin Class
    admins =[]
    def __init__(self,username, password):
        self.username = username
        self.password = password
    
    @staticmethod
    def load_admins(): #Takes Admin data from database
        Admin.admins.clear()
        db_admins = PROJECT1_db_v4.load_admins_db()
        for a in db_admins:
            Admin.admins.append(a)
    
    @staticmethod
    def return_admin(admin_user): # Return specific Admin
        for a in Admin.admins:
            if a["username"] == admin_user:
                return a
        return None


class Trips: # Trip Class
    trips =[]
    def __init__(self, trip_id, origin, destination, start_time, end_time, price, seats):
        self.trip_id = trip_id
        self.origin = origin
        self.destination = destination
        self.start_time = start_time
        self.end_time = end_time
        self.price = price
        self.seats = seats
        self.venue = 0
    
    @staticmethod
    def load_trips(): #Takes Trips data from database
        Trips.trips.clear()
        db_trips = PROJECT1_db_v4.load_trips_db()
        for t in db_trips:
            Trips.trips.append(t)
    
    @staticmethod
    def return_trip(trip_id): # Return specific Trip
        for t in Trips.trips:
            if t["trip_id"]==trip_id:
                return t
        return None



def user_dashboard(): # DASHBOARD
    User.load_users()
    Trips.load_trips()
    Admin.load_admins()
    while True:
        start = input("1.sign Up - 2.login - 3.Admin Login - 4.Available Trips - 5.EXIT: ")

        if start == "1": # User Sign up
            User.load_users()
            Trips.load_trips()
            input_user = input("Enter username (5-15 characters Alphabets or Numbers only)： ")
            if username_validator(input_user): # Validate username
                # for signed_users in User.users:
                #     if input_user != signed_users["username"]:
                        username = input_user
                    # else:
                    #     print ("This username Already Exists. Try Again")
                    #     continue
            else:
                print("Invalid username. Try again.")
                continue

            input_pass = input("Enter password (At least 8 characters with one Capital and special character): ")
            if password_validator(input_pass): # Validate username
                password = input_pass
                print("Successfully Signed up.")
            else:
                print("Invalid password. Try again.")
                continue

            PROJECT1_db_v4.assign_user(username,password) # Store signed-up Users into DATABASE
            
    

        elif start == "2":
            User.load_users()
            Trips.load_trips()
            username = input("Enter username: ")
            password = input("Enter password: ")
            logging = PROJECT1_db_v4.check_sign_up(username,password) # Check existence of a Users in DATABASE - LOGIN

            if logging:
                stay_logged = True
                while stay_logged:
                    print(f"\n#==== Wellcome {username}====#")
                    run_userdashboard = input("1.Add Balance - 2.show Balance - 3.Travel History - 4.Show Available Trips - 5.Buy Ticket - 6.Return Ticket - 7.Change Password - 8.Back to Main Menu ")
                    user_data = User.return_user(username)

                    if run_userdashboard == "1": # Add Balance to User wallet
                        try: 
                            add_balance = int(input("How much balance to Charge? "))
                            user_data["balance"] += add_balance
                            PROJECT1_db_v4.update_balance(username,user_data['balance'])
                            print(f"Your balance raised {add_balance}\nYour current balance {user_data["balance"]}")
                        except ValueError as e:
                            print(e,"Invalid input.Please insert numerical value to raise balance")      

                    elif run_userdashboard == "2": # Show User wallet
                        print(f"Your current Balance is {user_data['balance']}")
                        continue

                    elif run_userdashboard =="3": # Show User travel history
                        bought_tickets = PROJECT1_db_v4.load_tickets(username)
                        if len(bought_tickets) == 0: 
                            print("No tickets have been bought yet")
                        else:
                            tickets_number = 1
                            for tickets in bought_tickets:
                                print(f"#{tickets_number} - {tickets}\n")
                                tickets_number += 1

                    elif run_userdashboard == "4": # Show available Trips
                        if len(Trips.trips) == 0: # Check Trip Existence
                            print("No Trips Available")
                        trip_number = 1
                        for t in Trips.trips:
                            if len(t["available_seats"]) > 1: # Check Seats
                                print(f"# {trip_number} - {len(t["available_seats"])} Seats available for Travel {t['trip_id']} from {t['origin']} to {t['destination']} at {t['start_time']} to {t['end_time']}.Ticket Price = {t['price']}\n")
                                trip_number += 1
                    
                    elif run_userdashboard == "5": # Buy ticket by Users
                        if len(Trips.trips) == 0: # Check Trip Existence
                            print("No Trips Available")
                            continue
                        else:
                            for t in Trips.trips:
                                print(f"{len(t["available_seats"])} Seats available for Travel {t['trip_id']} from {t['origin']} to {t['destination']} at {t['start_time']} to {t['end_time']}.Ticket Price = {t['price']}")
                            ticket_to_buy = int(input("Insert Trip Id you want to buy: "))
                            
                            for t in Trips.trips:
                                if t["trip_id"] == ticket_to_buy: # Choice Seats by User
                                    if len(t["available_seats"]) > 0:
                                        finalize_ticket = input(f"Are you sure you want to buy Ticket from {t['origin']} to {t['destination']} at {t['start_time']}? (y/n):")
                                        if finalize_ticket.lower() == "y":
                                            print(f"Available seats: {t["available_seats"]}")
                                            choice_seats = int(input("choice your seats: "))
                                            if choice_seats in t["available_seats"]:
                                                try:
                                                    if user_data["balance"] < t['price']: # Add ticket to User's tickets, Update DATABASE venues
                                                        raise Exception ("Not Enough Balance!")
                                                    user_data["tickets"].append(t)
                                                    PROJECT1_db_v4.add_tickets(username,f"Seats Number {choice_seats} bought for {t["trip_id"]}-from {t["origin"]} to {t["destination"]} at {t["start_time"]}")

                                                    user_data["balance"] -= t['price']
                                                    PROJECT1_db_v4.update_balance(username,user_data["balance"])
                                                    print(f"You Bought Seats {choice_seats} of Trip ID {t['trip_id']}. Your current Balance = {user_data['balance']}.")
                                                    
                                                    t["available_seats"].remove(choice_seats)
                                                    PROJECT1_db_v4.update_seats(t["trip_id"],choice_seats)
                                                    
                                                    t["venue"] += t['price']
                                                    PROJECT1_db_v4.venue_add(t["trip_id"],t["venue"])

                                                except Exception as e:
                                                    print(f"Purchasing Tickets Failed: {e}")
                                                    continue

                                        elif finalize_ticket == "n":
                                            print("Ticket has been Cancelled!")
                                        else:
                                            print("Invalid input.Try again.")
                                            continue
                                    else:
                                        print(f"No seats available for Travel {t['trip_id']}")
                                        continue

                                selected_trip =Trips.return_trip(ticket_to_buy)
                                if not selected_trip:
                                    print("No Trip with this ID.")
                                    continue

                    elif run_userdashboard == "6": # Cancel a Ticket
                        print("Reserved Tickets:\n",PROJECT1_db_v4.load_tickets(username))
                        return_ticket = int(input("Insert Trip Id you want to Return: "))
                        for t in user_data["tickets"]:
                            if return_ticket == t["trip_id"]:
                                finalize_return = input(f"Are you sure you want to return Ticket from {t['origin']} to {t['destination']} at {t['start_time']}? (y/n):")
                                if finalize_return.lower() == "y":
                                    canceling_time = datetime.now()
                                    if t["start_time"] > canceling_time:
                                        user_data["tickets"].remove(t)
                                        #PROJECT1_db_v4.remove_tickets(username,t["trip_id]")
                                        # t["available_seats"].append(choice_seats)
                                        # PROJECT1_db_v4.update_seats(t["trip_id"], choice_seats)

                                        user_data["balance"] += t['price'] * 0.8
                                        PROJECT1_db_v4.update_balance(username, user_data["balance"])
                                        t["venue"] -= t['price'] * 0.8
                                        PROJECT1_db_v4.venue_add(t["trip_id"], t["venue"])
                                    else:
                                        print(f"Time of canceling has been passed!")
                                elif finalize_return.lower() == "n":
                                    print(f"Returning Ticket has been cancelled!.")
                            else:
                                print(f"Invalid Trip ID input.Try again.")
                                continue

                    elif run_userdashboard == "7": # Change Password by User
                        new_password = input("Insert new password: ")
                        if password_validator(new_password):
                            user_data["password"] = new_password
                            PROJECT1_db_v4.update_password(username,user_data["password"])
                            print(f"Your password successfully changed to {user_data['password']}.")
                        else:
                            print("Invalid password.Please try again.")
                            continue

                    elif run_userdashboard == "8":
                        stay_logged = False

                    else:
                        print("Invalid input. try again.")

            else:
                print("Invalid Username or Password. Try again.")
    

        elif start == "3": # Admin DASHBOARD
            User.load_users()
            Trips.load_trips()
            Admin.load_admins()
            username = input("Enter Admin username: ")
            password = input("Enter Amin password: ")
            admin_loggin = PROJECT1_db_v4.check_admin_sign_up(username,password)
            
            if admin_loggin:
                admin_stay_logged = True
                while admin_stay_logged:
                    print(f"\n#=========================#\n#==== ADMIN DASHBOARD ====#\n#=========================#\n") 
                    run_admindashboard = input("1.Add Trip - 2.Remove Trip - 3.Edite Trip - 4.Show Venues - 5.Show All Users Data (Superuser Only)- 6.Back to Main Menu:")
                    if run_admindashboard == "1": # Add Trip by Admin
                        trip_id = int(input("Trip ID:"))
                        origin= input("Trip Origin:")
                        destination = input("Trip Destination:")
                        start_time = datetime.strptime(input("Trip Start Time:"),"%Y-%m-%d %H:%M")
                        end_time = datetime.strptime(input("Trip End Time:"),"%Y-%m-%d %H:%M")                           
                        price = int(input("Trip Price: "))
                        seats = int(input("Total Number of Seats: "))

                        now_time = datetime.now()
                        try:
                            if now_time > start_time:
                                raise Exception ("Start time of Trip is Passed!")
                            elif end_time <= start_time:
                                raise Exception ("End time earlier than start time of Trip!")
                            else:
                                PROJECT1_db_v4.add_trips(trip_id,origin,destination,start_time,end_time,price,seats)
                        except ValueError as e:
                            print(f"{e} : Something goes wrong. Trip is not added.Try again.")
                        
                    elif run_admindashboard == "2": # Remove Trip by Admin
                        for trip in Trips.trips:
                            print(f"Travel {trip['trip_id']} from {trip['origin']} to {trip['destination']} at {trip['start_time']}\n") 
                        travel_id = int(input("Insert Trip_ID you want to Remove: "))

                        for t in Trips.trips:
                            if t["trip_id"]!=travel_id:
                                print("There is no Trip with such Trip_ID!")
                            else:
                                PROJECT1_db_v4.remove_trips(t["trip_id"])
                                print(f"Trip ID-{travel_id} Removed successfully!")

                    elif run_admindashboard =="3": #FIX HERE
                        pass

                    elif run_admindashboard =="4": # Show venues
                        venue_dashboard = input("1.Show a trip venue - 2.Show all venue - 3.Back to Admin Menu:")
                        if venue_dashboard == "1":
                            for trip in Trips.trips:
                                print(f"Travel {trip['trip_id']} from {trip['origin']} to {trip['destination']} at {trip['start_time']}\n")

                            travel_id = int(input("Insert Trip ID to see venue: "))
                            for t in Trips.trips:
                                if t["trip_id"] == travel_id:
                                    print(f"Trip {t["trip_id"]} venue = {PROJECT1_db_v4.trip_venue(t["trip_id"])}")

                        elif venue_dashboard == "2":
                            print(f"Total Venue = {PROJECT1_db_v4.total_income()}")
            

                    elif run_admindashboard == "5" and username == "Superuser": # SuperUser
                        if len(User.users) == 0:
                            print("No users have been added")
                        print(User.users)

                    elif run_admindashboard == "6":
                        admin_stay_logged = False
                        continue

                    else:
                        print("Invalid Input. Try again.")
                                    
            else:    
                print("Invalid Username or Password. Try again.")
                break
                        

        elif start == "4": # Show Trips (No need to Log in)
            User.load_users()
            Trips.load_trips() 
            if len(Trips.trips) == 0:
                print("No trips available")
            trip_number = 1
            for t in Trips.trips:
                print(f"# {trip_number} - {len(t["available_seats"])} Seats available for Travel {t['trip_id']} from {t['origin']} to {t['destination']} at {t['start_time']} to {t['end_time']}.Ticket Price = {t['price']}")
                trip_number += 1
        elif start == "5": 
            return False
        else:
            print("Invalid input. Please try again.")


if __name__ == "__main__":
    user_dashboard()

