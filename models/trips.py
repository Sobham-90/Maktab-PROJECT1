from database.PROJECT1_db import load_trips_db,set_trip_state
from datetime import datetime


class Trips: # Trip Class
    trips =[]
    
    @staticmethod
    def load_trips(): #Takes Trips data from database
        Trips.trips.clear()
        db_trips = load_trips_db()
        now_time = datetime.now()

        for t in db_trips: # set seat state
            if now_time > t["start_time"]:
                set_trip_state (t["trip_id"],"finished")
                Trips.trips.append(t)
            elif len(t["available_seats"]) == 0: 
                set_trip_state (t["trip_id"],"sold_out")
                Trips.trips.append(t)
            else:
                Trips.trips.append(t)
            
    
    @staticmethod
    def return_trip(trip_id): # Return specific Trip
        for t in Trips.trips:
            if t["trip_id"]==trip_id:
                return t
        return None

    @staticmethod
    def display_all_trips():
        if not Trips.trips:
            print("No trips available")
            return
        i =1
        for t in Trips.trips:
            if t['trip_state'] == "available":
                print(f"\n{i}. {len(t['available_seats'])} Seats available of Trip ID-{t['trip_id']} from {t['origin']} to {t['destination']}.\nStart time: {t['start_time']}. Price: {t['price']}.")
                i += 1          
            continue
