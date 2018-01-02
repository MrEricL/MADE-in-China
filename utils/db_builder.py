import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import hashlib
import uuid


#==========================================================
'''
TABLE CREATION
Database usersandstories.db
Tables: users, stories, updates
'''

def tableCreation():
    f="data/usersandstories.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #Create the users table
    user_table = 'CREATE TABLE users (username TEXT, password BLOB, userID INTEGER);'
    c.execute(user_table)
    #Create the stories table
    stories_table = 'CREATE TABLE stories (storyID INTEGER, title TEXT, author INTEGER, content TEXT);'
    c.execute(stories_table)
    #Create the updates table
    update_table = 'CREATE TABLE updates (storyID INTEGER, contribution TEXT, contributor INTEGER);'
    c.execute(update_table)
    db.commit()
    db.close()


#ADD VALUES TO TABLES

def hash_password(password):
    key = uuid.uuid4().hex
    return hashlib.sha256(key.encode() + password.encode()).hexdigest()+':' + key

def check_password(hashed_password, user_password):
    password, key = hashed_password.split(':')
    return password == hashlib.sha256(key.encode()+user_password.encode()).hexdigest()

#add a user
def addUser(new_username, new_password):
    f="data/usersandstories.db"
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
    c.execute('INSERT INTO users VALUES (?,?,?)',[new_username, hash_pass, new_userID])
    db.commit()
    db.close()


#==========================================================
#ACCESSORS
def getPass(username):
    f="data/usersandstories.db"
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



if __name__ == '__main__':     
    #TESTING
    tableCreation()

