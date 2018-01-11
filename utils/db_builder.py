import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib
import uuid


#==========================================================
'''
TABLE CREATION
Database
'''

def tableCreation():
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops

    #Create the users table
    user_table = 'CREATE TABLE users (username TEXT, password BLOB, userID INTEGER PRIMARY KEY, userType INTEGER);'
    c.execute(user_table)

    #Create the restaurants table
    restaurants_table = 'CREATE TABLE restaurants (restID INTEGER PRIMARY KEY, restname TEXT, userID INTEGER, res_slot INTEGER, res_length INTERGER, opening_time TEXT, closing_time TEXT, grid_x INTERGER, grid_y INTERGER);'
    c.execute(restaurants_table)

    #Create the reservations table
    reservations_table = 'CREATE TABLE reservations (restID INTEGER, userID INTEGER, tableID INTEGER, month INTEGER, day INTEGER, time TEXT);'
    c.execute(reservations_table)

    #Create the restaurant layout table
    rest_layout_table = 'CREATE TABLE rest_layout (restID INTEGER, tableID INTEGER, seats INTEGER, squares BLOB);'
    c.execute(rest_layout_table)

    db.commit()
    db.close()


#ADD VALUES TO TABLES

#user table stuff

def hash_password(password):
    key = uuid.uuid4().hex
    return hashlib.sha256(key.encode() + password.encode()).hexdigest()+':' + key

def check_password(hashed_password, user_password):
    password, key = hashed_password.split(':')
    return password == hashlib.sha256(key.encode()+user_password.encode()).hexdigest()

#add a user to user table
def addUser(new_username, new_password, new_type):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #global userID_counter
    #new_userID = userID_counter
    #userID_counter += 1
    userCount = c.execute('SELECT COUNT(*) FROM users;')
    new_userID = 0
    for x in userCount:
        new_userID = x[0]
    #new_userID += 1
    hash_pass = hash_password(new_password)
    print ('The string to store in the db is: ' + hash_pass)
    c.execute('INSERT INTO users VALUES (?,?,?,?)',[new_username, hash_pass, new_userID, new_type])
    db.commit()
    db.close()

#if username exist, return true
def checkUsername(userN):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    users = c.execute('SELECT username FROM users;')
    result = False
    for x in users:
        if (x[0] == userN):
            result = True
    db.close()
    return result

#restaurant info stuff

#add a restaurant
def add_rest(rest_name, owner_id, res_slot, res_length, open_time, close_time, grid_x, grid_y):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    
    def get_next_id():
        command = "SELECT restID FROM restaurants"
        info = c.execute(command)

        pre_id = -1
        for entry in info:
            ids = entry[0]
            pre_id = max(ids or [-1])
        next_id = pre_id + 1

        return next_id


    rest_id = get_next_id()
    c.execute('INSERT INTO restaurants VALUES (?,?,?,?,?,?,?,?,?)',[rest_id, rest_name, owner_id, res_slot, res_length, open_time, close_time, grid_x, grid_y])
        
    db.commit()
    db.close()


#layout stuff

#add table
def add_table(rest_id, seats, position_list):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    def get_next_id():
        command = "SELECT tableID FROM restaurant_layout"
        info = c.execute(command)

        for entry in info:
            ids = entry[0]
            pre_id = max(ids or [-1])
        next_id = pre_id + 1

        return next_id

    table_id = get_next_id()
    c.execute('INSERT INTO rest_layout VALUES (?,?,?,?)', [rest_id, table_id, seats, position_list])

    db.commit()
    db.close()

#clear all tables for a restaurant
def clear_tables(rest_id):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute('DELETE FROM rest_layout WHERE restID=' + rest_id)

    db.commit()
    db.close()

    
#reservation stuff
    

#==========================================================
#ACCESSORS

#for user table

#gets password for a user
def getPass(username):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, password FROM users"
    info = c.execute(command)

    retVal = None
    for entry in info:
        if str(entry[0]) == username:
            retVal = str(entry[1])
    db.close()
    return retVal

#get the type of user (0 is owner, 1 is customer)
def getUserType(username):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, userType FROM users"
    info = c.execute(command)

    retVal = None
    for entry in info:
        if str(entry[0]) == username:
            retVal = str(entry[1])
    db.close()
    #print str(retVal) + "\n\n\n"
    return retVal

def get_user_id(username):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()

    command = 'SELECT userID FROM users WHERE username="' + username + '";'
    info = c.execute(command)

    user_id = None
    for entry in info:
        user_id = entry[0]

    return user_id


#for restaurant table

#gets a list of restaurants owned by the user
def get_restaurants(owner_id):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = 'SELECT restname FROM restaurants WHERE userID=' + owner_id + ';'
    info = c.execute(command)

    rests = []
    for entry in info:
        rests.append(entry[0])

    db.close()
    return rests

#gets size of layout grid
def get_grid_size(rest_id):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = "SELECT grid_x, grid_y FROM restaurants WHERE restID=" + rest_id
    info = c.execute(command)

    grid_size = (None, None)
    for entry in info:
        grid_size[0] = entry[0]
        grid_size[1] = entry[1]

    db.close()
    return grid_size

def get_open_times(rest_id):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = "SELECT opening_time, closing_time FROM restaurants WHERE restID=" + rest_id
    info = c.execute(command)

    for entry in info:
        open_time = entry[0]
        close_time = entry[1]

    db.close()
    return open_time, close_time

def get_rest_id(rest_name):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = 'SELECT restID FROM restaurants WHERE restname="' + rest_name + '"'
    info = c.execute(command)

    for entry in info:
        rest_id = entry[0]
    db.close()
    return rest_id
    

#for layout table

#get layout
#returns a dictionary with the table ids as keys and the corresponding number of seats at each table as entries, and a list of the coordinates of the squares which are tables (the coordinates are tuples)
def get_layout(rest_id):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = "SELECT tableID, seats, squares FROM restaurant_layout WHERE restID=" + rest_id
    info = c.execute(command)

    table_seats = {}
    squares = []
    for entry in info:
        table_id = entry[0]
        num_seats = entry[1]

        table_seats[table_id] = num_seats
        
        pos_arr = entry[2]
        for coor in pos_arr:
            squares.append(coor)

    db.close()
    return table_seats, squares


if __name__ == '__main__':     
    #TESTING
    #tableCreation()
    
    #addUser('a', 'pass', 0)
    #addUser('b', 'pass', 1)
    '''

    print getUserType("a") #0
    print getUserType('b') #1

    print get_user_id('a')
    print get_user_id('b')
    
    add_rest('test', get_user_id('a'), 15, 120, '8:00', '20:00', 20, 20)

    print get_rest_id('test')

    add_table(get_rest_id('test'), 4, [(0,0), (0,1), (0,2)])

    print get_layout(get_rest_id('test'))'''
