from services.os import clear_console
from validation.validator import username_validator, password_validator
from database.PROJECT1_db import *
from models.user import User
from models.trips import Trips
from datetime import datetime
from services.log_service import get_logger
logger = get_logger()

def user_dashboard(args=None): #User Dashboard
    username = None
    if args and args.username and args.password:
        username = args.username
        password = args.password
        logging = check_sign_up(username, password)

        if not logging:
            print(f"Invalid username or password")
            return
    else:
        # Normal CLI menu
        while True:
            choice = input("\n1. Sign Up | 2. Login to Account | 3. Back : ")

            if choice == "1":
                username = input("Enter username: ")
                if not username_validator(username):
                    print("Invalid Username. Must be 5-15 characters, letters or numbers.")
                    continue
                password = input("Enter password: ")
                if not password_validator(password):
                    print("Invalid Password. At least 8 chars, 1 capital, 1 special char.")
                    continue
                if not check_sign_up(username, password):
                    assign_user(username, password)
                    print("User Successfully Registered\n")
                    logger.info(f"User {username} Signed Up")
                else:
                    print("User Already Signed Up!")
                continue
            
            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                logging = check_sign_up(username, password)
                if not logging:
                    print("Invalid Username or Password")
                    continue
                break
            
            elif choice == "3":
                clear_console()
                return
            else:
                print("Invalid input. Try again.")


    user_id = return_user_id(username)
    user_data = User.return_user(username)

    while True:
        run_userdashboard = input(
            "\n1.Add Balance | 2.Show Balance | 3.Travel History | 4.Show Available Trips | "
            "5.Buy Ticket | 6.Return Ticket | 7.Change Password | 8.Back to Main Menu : "
        )

        # Add Balance
        if run_userdashboard == "1":
            if args and hasattr(args, 'add_balance') and args.add_balance:
                add_balance = args.add_balance
            else:
                try:
                    add_balance = int(input("How much balance to charge? "))
                except ValueError:
                    print("Invalid input. Must be a number.")
                    continue

            user_data["balance"] = (user_data.get("balance") or 0) + add_balance
            update_balance(username, user_data["balance"])
            print(f"Balance updated. Current balance: {user_data['balance']}")
            logger.info(f"User {username} added balance {add_balance}")

        # Show Balance
        elif run_userdashboard == "2":
            print(f"Your current balance: {user_data.get('balance',0)}")

        # Travel History
        elif run_userdashboard == "3":
            tickets = load_user_tickets(user_id)
            if not tickets:
                print("No tickets purchased yet.")
            else:
                for i, ticket in enumerate(tickets, start=1):
                    print(f"#{i} - Ticket ID {ticket[0]} | Trip {ticket[8]} | Seats {ticket[6]} | "
                          f"From {ticket[1]} to {ticket[2]} | Start {ticket[3]} | Price {ticket[5]} | State {ticket[7]}")

        # Show Available Trips 
        elif run_userdashboard == "4":
            if not Trips.trips:
                print("No trips available.")
            else:
                for t in Trips.trips:
                    if t["trip_state"] == "available" and t["available_seats"]:
                        print(f"Trip ID {t['trip_id']} | {len(t['available_seats'])} Seats | "
                              f"{t['origin']} -> {t['destination']} | Start {t['start_time']} | Price {t['price']}")

        # Buy Ticket
        elif run_userdashboard == "5":
            buy_ticket_func(user_id, user_data, args)

        # Return Ticket 
        elif run_userdashboard == "6":
            return_ticket_func(user_id, user_data)

        # Change Password
        elif run_userdashboard == "7":
            old_pass = input("Insert old password: ")
            if old_pass != user_data['password']:
                print("Incorrect password!")
                continue
            new_pass = input("Insert new password: ")
            if not password_validator(new_pass):
                print("Invalid password format!")
                continue
            user_data['password'] = new_pass
            update_password(username, new_pass)
            print("Password successfully changed.")
            logger.info(f"User {username} changed password")

        # Back to Main Menu
        elif run_userdashboard == "8":
            clear_console()
            return

        else:
            print("Invalid input. Try again.")


# Buy Ticket Function
def buy_ticket_func(user_id, user_data, args=None):
    if not Trips.trips:
        print("No trips available.")
        return

    # Display trips
    for t in Trips.trips:
        print(f"Trip ID {t['trip_id']} | {len(t['available_seats'])} Seats | "
              f"{t['origin']} -> {t['destination']} | Start {t['start_time']} | Price {t['price']}")

    # Select trip ID
    trip_id = getattr(args, "buy_ticket", None) or int(input("Enter Trip ID to buy: "))
    selected_trip = Trips.return_trip(trip_id)
    if not selected_trip:
        print("No trip with this ID.")
        return

    # Select seat
    seat = getattr(args, "seat", None) or int(input(f"Choose a seat from available {selected_trip['available_seats']}: "))
    if seat not in selected_trip['available_seats']:
        print("Seat not available.")
        return

    # Check balance
    if user_data.get("balance",0) < selected_trip['price']:
        print("Not enough balance.")
        return

    # Buy ticket
    buy_tickets(user_id, trip_id, seat)
    set_ticket_state(user_id, trip_id, "Bought")
    user_data['balance'] -= selected_trip['price']
    update_balance(User.return_user(user_id)['username'], user_data['balance'])
    selected_trip['available_seats'].remove(seat)
    update_seats(trip_id, seat)
    print(f"Ticket bought: Trip {trip_id}, Seat {seat}. Balance left: {user_data['balance']}")
    logger.info(f"User bought ticket: Trip {trip_id}, Seat {seat}")

# Return Ticket Function
def return_ticket_func(user_id, user_data):
    tickets = load_user_tickets(user_id)
    bought_tickets = [t for t in tickets if t[7] == "Bought"]
    if not bought_tickets:
        print("No tickets to return.")
        return

    # Display tickets
    for t in bought_tickets:
        print(f"Ticket ID {t[0]} | Trip {t[8]} | Seat {t[6]} | Start {t[3]}")

    ticket_id = int(input("Enter Ticket ID to return: "))
    ticket = next((t for t in bought_tickets if t[0] == ticket_id), None)
    if not ticket:
        print("Invalid Ticket ID.")
        return

    if datetime.now() > ticket[3]:
        print("Cannot return ticket after start time.")
        return

    set_ticket_state(user_id, ticket[8], "Returned")
    user_data['balance'] += ticket[5] * 0.8  # Refund 80%
    update_balance(User.return_user(user_id)['username'], user_data['balance'])

    # Add seat back to trip
    trip = Trips.return_trip(ticket[8])
    trip['available_seats'].append(ticket[6])
    update_seats(trip['trip_id'], ticket[6])
    print(f"Ticket {ticket_id} returned. Balance refunded: {ticket[5]*0.8}")
    logger.info(f"User returned ticket {ticket_id}")