import psycopg2

conn = psycopg2.connect (
    dbname = "project1",
    user = "postgres",
    password = "6068",
    host = "localhost",
    port = "5432"
)
cur = conn.cursor()

# ========================================
# Create tables
create_table_users = """CREATE TABLE IF NOT EXISTS USERS (user_id SERIAL PRIMARY KEY,username VARCHAR(15) UNIQUE,password VARCHAR(50),balance INT DEFAULT 0);"""
cur.execute(create_table_users)
# drop_users = """DROP TABLE USERS;"""
conn.commit()

create_table_admin = """CREATE TABLE IF NOT EXISTS ADMIN (username VARCHAR(15),password VARCHAR(50))"""
cur.execute(create_table_admin)
# drop_users = """DROP TABLE ADMIN;"""
conn.commit()

create_table_trips = """CREATE TABLE IF NOT EXISTS TRIPS (trip_id INT PRIMARY KEY,origin VARCHAR(15),destination VARCHAR(15),start_time TIMESTAMP,end_time TIMESTAMP,price INT, seats integer[], venue INT DEFAULT 0, trip_state VARCHAR(10) DEFAULT NULL);"""
cur.execute(create_table_trips)
# drop_users = """DROP TABLE TRIPS;"""
conn.commit()

create_table_tickets = """CREATE TABLE IF NOT EXISTS TICKETS (ticket_id SERIAL PRIMARY KEY,user_id INT REFERENCES USERS(user_id) ON DELETE CASCADE, trip_id INT REFERENCES TRIPS(trip_id) ON DELETE CASCADE,purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,ticket_state VARCHAR(10), seats_number INT);"""
cur.execute(create_table_tickets)
# drop_users = """DROP TABLE TRIPS;"""
conn.commit()
# =========================================

# Assign user_id to USERS
def assign_user(username,password):
    cur.execute("INSERT INTO USERS (username,password) VALUES (%s,%s) RETURNING user_id",(username,password))
    conn.commit()

def return_user_id (username):
    cur.execute ("SELECT user_id FROM USERS WHERE username = %s;",(username,))
    result = cur.fetchone()
    return result
# =========================================

# load users from table
def load_users_db ():
    users = []
    cur.execute(f"SELECT username, password, balance FROM USERS")
    rows = cur.fetchall()

    for row in rows:
        username,password,balance = row
        tickets = []
        users.append({
            "username":username,
            "password": password,
            "balance":balance
        })

    return users
# =========================================

# Add Trips
def add_trips_db(trip_id,origin,destination,start_time,end_time,price,seats):
    cur.execute("INSERT INTO TRIPS (trip_id,origin,destination,start_time,end_time,price,seats) VALUES (%s,%s,%s,%s,%s,%s,%s)",(trip_id,origin,destination,start_time,end_time,price,[(i+1) for i in range(seats)]))
    conn.commit()
# =========================================

# load trips from table
def load_trips_db ():
    trips = []
    cur.execute(f"SELECT trip_id, origin, destination, start_time, end_time, price, seats, venue, trip_state FROM TRIPS")
    rows = cur.fetchall()

    for row in rows:
        trip_id, origin,destination,start_time,end_time,price,seats,venue,trip_state = row
        trips.append({
            "trip_id": int(trip_id),
            "origin": origin,
            "destination": destination,
            "start_time": start_time,
            "end_time": end_time,
            "price": price,
            "available_seats": seats,
            "venue" : venue,
            "trip_state" : trip_state
        })

    return trips
# ==========================================

# Check User Sign Up
def check_sign_up (username,password):
    cur.execute("SELECT 1 FROM USERS WHERE username=%s and password=%s",(username,password))
    validation = cur.fetchone() is not None
    return validation
# =========================================

#Update Balance
def update_balance (username,value):
    cur.execute("UPDATE USERS SET balance = %s WHERE username = %s",(value,username))
    conn.commit()
# =========================================

# Add Tickets
def buy_tickets (user_id,trip_id,seats_number):
    cur.execute("INSERT INTO tickets (user_id, trip_id,seats_number) VALUES (%s, %s, %s) RETURNING ticket_id, purchase_date;",(user_id, trip_id, seats_number))
    conn.commit()
# =========================================


# Remove Trips
# def remove_trips(trip_id):
# column_for_delete = """ALTER TABLE IF NOT EXISTS TRIPS ADD is_deleted BOOLEAN DEFAULT FALSE;"""
# cur.execute(column_for_delete)
# conn.commit()

def set_trip_state(trip_id,trip_state):
    cur.execute("UPDATE TRIPS SET trip_state = %s WHERE trip_id = %s",(trip_state,trip_id))
    conn.commit()
# =========================================

def load_admins_db():
    admins = []
    cur.execute(f"SELECT username, password FROM ADMIN")
    rows = cur.fetchall()

    for row in rows:
        username,password = row
        admins.append({
            "username":username,
            "password": password
        })

    return admins
# ==========================================

# Check admin Sign Up
def check_admin_sign_up (username,password):
    cur.execute("SELECT 1 FROM ADMIN WHERE username=%s and password=%s",(username,password))
    validation = cur.fetchone() is not None

    return validation
# ==========================================

# add Admins 
# add_admin = "INSERT INTO ADMIN (username, password) values ('admin','admin')"
# cur.execute(add_admin)
# conn.commit()
# cur.close()
# conn.close()
# ==========================================

#Update password
def update_password (username,new_password):
    cur.execute("UPDATE USERS SET password = %s WHERE username = %s",(new_password,username))
    conn.commit()
# ==========================================

#Update Seats
def update_seats (trip_id, choice_seats):
    cur.execute("UPDATE TRIPS SET seats = array_remove(seats,%s) WHERE trip_id = %s", (choice_seats, trip_id))
    conn.commit()

# ==========================================

# Show Tickets
def load_user_tickets (user_id):
    cur.execute("SELECT tk.ticket_id, t.origin, t.destination, t.start_time, t.end_time, t.price, tk.seats_number, tk.ticket_state, t.trip_id FROM tickets tk JOIN trips t ON tk.trip_id = t.trip_id WHERE tk.user_id = %s",(user_id,))
    rows = cur.fetchall()
    return rows



# ==========================================

# Venu calculation

def venue_add (trip_id,venue):
    cur.execute("UPDATE TRIPS SET venue = %s WHERE trip_id = %s",(venue,trip_id))
    conn.commit()

def trip_venue (trip_id):
    cur.execute("SELECT venue FROM TRIPS WHERE trip_id=%s ;",(trip_id,))
    row = cur.fetchone()
    if row is None:
        return None
    return row[0] 

def total_income ():
    cur.execute("SELECT SUM(venue) FROM TRIPS ;")
    row = cur.fetchone()
    if row is None:
        return None
    return row[0]

# ===========================

# Set ticket State
def set_ticket_state(user_id, trip_id, ticket_state):
    cur.execute("UPDATE TICKETS SET ticket_state = %s WHERE user_id = %s AND trip_id = %s",(ticket_state, user_id, trip_id))
    conn.commit()
# ===========================

