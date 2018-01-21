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
    restaurants_table = 'CREATE TABLE restaurants (restID INTEGER PRIMARY KEY, restname TEXT, zip INTEGER, userID INTEGER, res_length INTERGER, pic TEXT, sun_open_time TEXT, sun_close_time TEXT, mon_open_time TEXT, mon_close_time TEXT, tue_open_time TEXT, tue_close_time TEXT, wed_open_time TEXT, wed_close_time TEXT, thu_open_time TEXT, thu_close_time TEXT, fri_open_time TEXT, fri_close_time TEXT, sat_open_time TEXT, sat_close_time TEXT);'
    c.execute(restaurants_table)

    #Create the reservations table
    reservations_table = 'CREATE TABLE reservations (restID INTEGER, userID INTEGER, tableID INTEGER, month INTEGER, day INTEGER, time TEXT);'
    c.execute(reservations_table)

    #Create the restaurant layout table
    table_seats_table = 'CREATE TABLE table_seats (restID INTEGER, tableID INTEGER, seats INTEGER);'
    c.execute(table_seats_table)

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

#check if restaurant already exists, returns true if does not exist
def check_rest(rest_name):
    rest_list = get_rests()
    if rest_name in rest_list:
        return False
    return True

#add a restaurant
#mon - sun open and close times are "closed" if restaurand is closed, and "xx:xx" otherwise
def add_rest(owner_id, info_dict):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    days_dict = {}
    days_list = ['000', '001', '002', '003', '004', '005', '006'] #sun - mon in order
    
    rest_name = info_dict['name']
    zip_code = info_dict['zip']
    res_length = info_dict['reslen']
    pic = info_dict['pic']
    closed_days = info_dict['closed']
    
    for day in closed_days:
        days_list.remove(day)
        days_dict[day] = ('closed', 'closed')

    for day in days_list:
        days_dict[day]  = (info_dict[day][0] + ':' + info_dict[day][1], info_dict[day][2] + ':' + info_dict[day][3])
    
    def get_next_id():
        command = "SELECT restID FROM restaurants"
        info = c.execute(command)

        pre_id = -1
        for ids in info:
            #print (ids)
            pre_id = max(ids or [-1])
            #print (pre_id)
        next_id = pre_id + 1

        return next_id


    rest_id = get_next_id()
    
    c.execute('INSERT INTO restaurants VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',[rest_id, rest_name, zip_code, owner_id, res_length, pic, days_dict['000'][0], days_dict['000'][1], days_dict['001'][0], days_dict['001'][1], days_dict['002'][0], days_dict['002'][1], days_dict['003'][0], days_dict['003'][1], days_dict['004'][0], days_dict['004'][1], days_dict['005'][0], days_dict['005'][1], days_dict['006'][0], days_dict['006'][1]])

    add_tables(rest_id, info_dict, c)
        
    db.commit()
    db.close()


#layout stuff

    
#add table
def add_tables(rest_id, info_dict, c):

    table_info = info_dict['tablePeeps'] #table id is index, num seats is value

    table_id = 0
    while table_id < len(table_info):
        seats = table_info[table_id]
        print (table_id, seats)
        c.execute('INSERT INTO table_seats VALUES (?,?,?)', [rest_id, table_id, seats])
        table_id = table_id + 1


#clear all tables for a restaurant
def clear_tables(rest_id):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute('DELETE FROM table_seats WHERE restID=' + str(rest_id))

    db.commit()
    db.close()

    
#reservation stuff

#add reservation
def add_reservation(rest_id, month, day, customer_id, table_id, time):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    c.execute('INSERT INTO reservations VALUES (?,?,?,?,?,?)', [rest_id, customer_id, table_id, month, day, time])

    db.commit()
    db.close()

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

#gets a list of all restaurants(for customer to see)
def get_rests():
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = 'SELECT restname FROM restaurants'
    info = c.execute(command)

    rests = []
    for entry in info:
        #print (entry)
        rests.append(entry[0])

    db.close()
    return rests

#gets a list of restaurants owned by the user(for owner to see)
def get_rests_of_owner(owner_id):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = 'SELECT restname FROM restaurants WHERE userID=' + str(owner_id) + ';'
    info = c.execute(command)

    rests = []
    for entry in info:
        rests.append(entry[0])

    db.close()
    return rests

def get_zip(rest_id):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = 'SELECT zip FROM restaurants WHERE restID=' + str(rest_id)
    info = c.execute(command)

    for entry in info:
        zip_code = entry[0]

    db.close()
    return zip_code

#helper function to get open times
#day is the first three letters of the day of the week
def get_open_times_by_day(day):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = "SELECT " + day + "_open_time, " + day + "_close_time FROM restaurants WHERE restID=" + str(rest_id)
    info = c.execute(command)

    for entry in info:
        open_time = entry[0]
        close_time = entry[1]

    db.close()
    return open_time, close_time

#gets opening and closing times for each day
def get_open_times(rest_id):
    d = {}
    d['sun'] = get_open_times_by_day('sun')
    d['mon'] = get_open_times_by_day('mon')
    d['tue'] = get_open_times_by_day('tue')
    d['wed'] = get_open_times_by_day('wed')
    d['thu'] = get_open_times_by_day('thu')
    d['fri'] = get_open_times_by_day('fri')
    d['sat'] = get_open_times_by_day('sat')
    return d

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
def get_layout(rest_id):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    command = "SELECT tableID, seats FROM table_seats WHERE restID=" + str(rest_id)
    info = c.execute(command)

    table_seats = {}

    for entry in info:
        table_id = entry[0]
        seats = entry[1]
        table_seats[table_id] = seats

    command = "SELECT pic FROM restaurants WHERE restID=" + str(rest_id)
    info = c.execute(command)

    pic_str = ''
    for entry in info:
        pic_str = entry[0]

    db.close()
    return table_seats, pic_str

#for reservations table

#get available reservation times for a month and day
def get_available_times_for_day(rest_id, month, day, day_of_week):
    f="data/restaurant_reservations.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    available_times = []
    
    #get times that it is open
    opening_time, closing_time = get_open_times_by_day(day_of_week)
    
    if opening_time == 'closed':
        return available_times

    
    #add all times from opening to closing to available times
    current_time = opening_time
    while not (current_time == closing_time):
        available_times.append(current_time)
        #add the time every five minutes
        minutes = current_time.split(':')[1]
        hour = current_time.split(':')[0]
        if int(minutes) + 5 == 60:
            hour = str(int(hour) + 1)
            #put 0 in front if necessary
            if len(hour) == 1:
                hour = '0' + hour

            minutes = '00'

        else:
            minutes = str(int(minutes) + 5)
            #put 0 in front if necessary
            if len(minutes) == 1:
                minutes = '0' + minutes

        current_time = hour + ':' + minutes

    #get length of reservation
    command = 'SELECT res_length FROM restaurants WHERE restID=' + str(rest_id)
    info = c.execute(command)
    for entry in info:
        res_length = entry[0]

    #number of slots above and below reservation time to remove:
    num_bad_slots = int (res_length / 5) - 1

    #get reservation start times
    command = 'SELECT time FROM reservations WHERE restID=' + str(rest_id) + ' AND month=' + str(month) + ' AND day=' + str(day)
    info = c.execute(command)

    used_times = set()
    for entry in info:
        used_times.add(entry[0])
        start_index = available_times.index(entry[0])
        i = 0
        while i <= num_bad_slots and start_index - i >= 0 and start_index + i < len(available_times):
            used_times.add(available_times[start_index - i])
            used_times.add(available_times[start_index + i])
            i = i + 1
    #make the time before closing unavailable
    i = 1
    while i <= num_bad_slots:
        used_times.add(available_times[0 - i])
        i = i + 1

    #remove bad times from available time
    for used_time in used_times:
        available_times.remove(used_time)
    
    db.close()
    return available_times

if __name__ == '__main__':     
    #TESTING
    #tableCreation()
    
    #addUser('a', 'pass', 0)
    #addUser('b', 'pass', 1)

    '''print (getUserType("a")) #0
    print (getUserType('b')) #1

    print (get_user_id('a'))#0
    print (get_user_id('b'))#1

    user_id = get_user_id('a')

    info_dict = {'name': 'test2',
                 'zip': 10013,
                 'reslen': 15,
                 'pic': 'pic_str',
                 'closed': ['000', '001', '005', '006'],
                 '002': ['12', '00', '13', '00'],
                 '003': ['12', '00', '13', '00'],
                 '004': ['12', '00', '13', '00'],
                 'tablePeeps': [2, 3]}
    
    #add_rest(user_id, info_dict)

    rest_id = get_rest_id('test2')
    print (rest_id)#0
    print (check_rest('test'))#False
    print (check_rest('rest'))#True

    print (get_zip(rest_id))
    print (get_rests())#[test]
    print (get_rests_of_owner(user_id))#[test]
    print (get_open_times(rest_id))
    print (get_layout(rest_id))

    #add_reservation(rest_id, 1, 23, get_user_id('b'), 0, '12:10')
    print (get_available_times_for_day(rest_id, 1, 23, 'tue'))'''
