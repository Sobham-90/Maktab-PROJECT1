from validation.validator import username_validator, password_validator
from database.PROJECT1_db import *
from models.user import User
from models.trips import Trips
from datetime import datetime


def user_dashboard():
    while True:
        choice = input("\n1. Sign Up | 2. Login to Account | 3. Back : ")
        if choice == "1":
            sign_up()
        elif choice == "2":
            login()
        elif choice == "3":
            break
        else:
            print("Invalid Input!")

def sign_up():
    username = input ("\nEnter username: ")
    if not username_validator(username):
        print("Invalid Username (5-15 characters Alphabets or Numbers only). Try Again.")
        return
    password = input ("Enter password: ")
    if not password_validator(password):
        print("Invalid Password (At least 8 characters with one Capital and special character). Try Again.")
        return
    if not check_sign_up (username,password):
        try:
            assign_user(username, password)
            print("User Successfully Registered\n")
        except Exception as e:
            print(e,"Error! User Already Signed Up!")
    else:
        print("User Already Signed Up!")
    

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    logging = check_sign_up(username, password)
    if not logging:
        print("Invalid Username or Password")
        return
    print(f"\nWelcome {username} to your Account!\n")
    while True:
        run_userdashboard = input("\n1.Add Balance - 2.show Balance - 3.Travel History - 4.Show Available Trips - 5.Buy Ticket - 6.Return Ticket - 7.Change Password - 8.Back to Main Menu : ")
        user_data = User.return_user(username)
        user_id = return_user_id (username)

        if run_userdashboard == "1":  # Add Balance to User's wallet
            try:
                add_balance = int(input("\nHow much balance to Charge? "))
                user_data["balance"] += add_balance
                update_balance(username, user_data['balance'])
                print(f"Your balance raised {add_balance}\nYour current balance {user_data["balance"]}")
            except ValueError as e:
                print(e, "Invalid input.Please insert numerical value to raise balance")

        elif run_userdashboard == "2":  # Show User wallet
            if user_data['balance'] is None:
                print("Your current Balance is 0")
                continue
            else:
                print(f"Your current Balance is {user_data['balance']}")

        elif run_userdashboard == "3":  # Show User travel history
            user_id = return_user_id (username)
            bought_tickets = load_user_tickets(user_id)
            if len(bought_tickets) == 0:
                print("No tickets have been bought yet")
            else:
                for i,tickets in enumerate(bought_tickets,start=1):
                    print(f"\n#{i} - TicketID {tickets[0]}\nSeats Num {tickets[6]}. From {tickets[1]} To {tickets[2]} Start at {tickets[3]}.\nTicket Price = {tickets[5]}. Ticket state : {tickets[7]}")

        elif run_userdashboard == "4":  # Show available Trips
            if len(Trips.trips) == 0:  # Check Trip Existence
                print("No Trips Available")
            for i , t in enumerate(Trips.trips,start=1): 
                if t["trip_state"] == "available":
                    if len(t["available_seats"]) > 1:  # Check Seats
                        print(f"\n# {i} - {len(t["available_seats"])} Seats available for Travel {t['trip_id']} from {t['origin']} to {t['destination']} at {t['start_time']} to {t['end_time']}.Ticket Price = {t['price']}\n")

        elif run_userdashboard == "5":  # Buy ticket by Users
            if len(Trips.trips) == 0:  # Check Trip Existence
                print("No Trips Available")
                continue
            else:
                for i,t in enumerate(Trips.trips,start=1):
                    print(f"\n#{i} - {len(t["available_seats"])} Seats available for Travel ID {t['trip_id']} from {t['origin']} to {t['destination']} at {t['start_time']} to {t['end_time']}.Ticket Price = {t['price']}")
                ticket_to_buy = int(input("\nInsert Trip Id you want to buy: "))

                for t in Trips.trips:
                    if t["trip_id"] == ticket_to_buy:  # Choice Seats by User
                        if len(t["available_seats"]) > 0:
                            finalize_ticket = input(f"\nAre you sure you want to buy Ticket from {t['origin']} to {t['destination']} at {t['start_time']}? (y/n):")
                            if finalize_ticket.lower() == "y":
                                print(f"\nAvailable seats: {t["available_seats"]}")
                                choice_seats = int(input("\nchoice your seats: "))
                                if choice_seats in t["available_seats"]:
                                    try:
                                        if user_data["balance"] < t['price']:  # Add ticket to User's tickets, Update DATABASE venues
                                            raise Exception("Not Enough Balance!")
                                        buy_tickets(user_id,t["trip_id"],choice_seats)
                                        set_ticket_state (user_id, t["trip_id"], "Bought")
                                       
                                        user_data["balance"] -= t['price']
                                        update_balance(username, user_data["balance"])
                                        print(f"You Bought Seats Num {choice_seats} of Trip ID {t['trip_id']} by {t['price']}. Your current Balance = {user_data['balance']}.")

                                        t["available_seats"].remove(choice_seats)
                                        update_seats(t["trip_id"], choice_seats)

                                        t["venue"] += t['price']
                                        venue_add(t["trip_id"], t["venue"])
                                        Trips.load_trips()
                                        continue

                                    except Exception as e:
                                        print(f"Purchasing Tickets Failed: {e}")
                                        return
                                else:
                                    print("The Seats Number Not Available.try again")
                                    return

                            elif finalize_ticket == "n":
                                print("Buy Ticket has been Cancelled!")
                            else:
                                print("Invalid input.Try again.")
                                continue
                        else:
                            print(f"No seats available for Travel {t['trip_id']}")
                            continue

                    selected_trip = Trips.return_trip(ticket_to_buy)
                    if not selected_trip:
                        print("No Trip with this ID.")
                        continue

        elif run_userdashboard == "6":  # Cancel a Ticket
            print("Reserved Tickets:\n")
            bought_tickets = load_user_tickets(user_id)
            for i,tickets in enumerate(bought_tickets,start=1):
                if tickets[7] == "Bought":
                    print(f"\n#{i} - Ticket ID {tickets[0]} from Trip ID {tickets[8]} \nSeats Num {tickets[6]}. From {tickets[1]} To {tickets[2]} Start at {tickets[3]}.\nTicket Price = {tickets[5]}. Ticket state : {tickets[7]}")
                    return_ticket = []
                    return_ticket.append(tickets)
                    choice_ticket_to_return = int(input("Insert Ticket Id you want to Return: "))
                    
                    for ticket in return_ticket:
                        if choice_ticket_to_return  == ticket[0]:
                            finalize_return = input(f"Are you sure you want to return Ticket {tickets[0]} of Trip ID {tickets[8]}? (y/n):")
                            if finalize_return.lower() == "y":
                                canceling_time = datetime.now()
                                if ticket[3] > canceling_time:
                                    set_ticket_state (user_id, ticket[8], "returned")
                                    for t in Trips.trips:
                                        if t["trip_id"] == ticket[8]:
                                            t["available_seats"].append(tickets[6])
                                            update_seats(t["trip_id"], tickets[6])

                                    user_data["balance"] += t['price'] * 0.8
                                    update_balance(username, user_data["balance"])
                                    t["venue"] -= t['price'] * 0.8
                                    venue_add(t["trip_id"], t["venue"])
                                else:
                                    print(f"Time of canceling has been passed!")

                            elif finalize_return.lower() == "n":
                                print(f"Returning Ticket has been cancelled!.")
    

        elif run_userdashboard == "7":  # Change Password by User
            new_password = input("Insert new password: ")
            if password_validator(new_password):
                user_data["password"] = new_password
                update_password(username, user_data["password"])
                print(f"Your password successfully changed to {user_data['password']}.")
            else:
                print("Invalid password.Please try again.")
                continue

        elif run_userdashboard == "8":
            return

        else:
            print("Invalid input. try again.")
            continue

    
        