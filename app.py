from flask import Flask, render_template, request, session, url_for, flash, redirect
from utils.accounts import authenticate
from utils.db_builder import checkUsername, addUser, getUserType, get_user_id, get_rests, get_rest_id, get_layout,add_rest,get_open_times, get_available_times_for_day, check_reservation, add_reservation, get_customer_reservations, get_rests_of_owner
import os
from urlparse import urlparse

app = Flask(__name__)
#Cookie/Login Stuff
app.secret_key = os.urandom(32) 

BAD_USER = -1
BAD_PASS = -2
GOOD = 1

user = ""

#User Type
# owner = 0
# user = 1
user_type = 0


@app.route('/')
def root():
    #redirect to home if there is a session
    #otherwise display login/register page
    if session.has_key('user'):
        return redirect("home")
    else:
        return render_template("login.html")


@app.route('/registration')
def registration():
    if session.has_key('user'):
        return redirect("home")
    else:
        return render_template("register.html")
 
#authenticate user credentials
@app.route('/login', methods = ['POST','GET'])
def login():
    user = request.form['user']
    #print user
    passw = request.form['pass']
    #print passw

    result = authenticate(user, passw)
    #print result

    #if successful, redirect to home
    #otherwise redirect back to root with flashed message 
    if result == GOOD:
        session['user'] = user
        user_type = getUserType (user)
        print user_type #DELETE13        
        #for x in session:
            #print session[x]
        return redirect( url_for('home') )
    if result == BAD_USER:
        flash('Incorrect username. Please try again.')
        return redirect( url_for('root') )
    if result == BAD_PASS:
        flash('Incorrect password. Please try again.')
        return redirect( url_for('root') )
    return redirect( url_for('root') )

@app.route('/register', methods = ['POST', 'GET'])
def register():
    user = request.form['user']
    #print user
    password = request.form['pass']
    #print password
    usertype = request.form['usertype']


    if usertype == "Owner":
        usertypeInt = 0
    else:
        usertypeInt = 1


    if checkUsername(user):
        flash('Username unavailable. Please try another username.')
        return redirect(url_for('registration'))
    else:
        addUser(user,password,usertypeInt)
        user_type = usertypeInt
        print user_type #DELETE13
        session['user'] = user
        return redirect( url_for('home'))
    
    
#user dashboard 
@app.route('/home', methods = ['POST','GET'])
def home():
    if 'user' not in session:
        flash ("You are not logged in!")
        return redirect(url_for('root'))
    
    user = session['user']
    user_type = getUserType(user)
    user_id = get_user_id(user)
    
    listofRest = get_rests() #prototype
    restList = []

    for each in listofRest:
        restList.append('<a href = "book?name=%s"> %s </a><br>' % (each, each))

    owner_rests = []
    reservations = []

    userTypeList = []
    if user_type == 0: #owner
        userTypeList = get_rests_of_owner(user_id) #list of restaurant names
    else:
        userTypeList = get_customer_reservations(user_id) #list of reservations in format (rest_id, table_id, month, day, time)

    print userTypeList

    if 'user' in session:
        print "This is the user type: " + str(user_type)
        return render_template("home.html",userstatus=user_type,username=user,listOR=restList,userL=userTypeList)
        
    else:    
        return redirect(url_for("root"))
        

#log out user
@app.route('/logout', methods = ['POST','GET'])
def logout():
    session.pop('user')
    flash('You have been logged out successfully')
    return redirect(url_for('root'))
#list of rests
@app.route('/restaurants', methods = ['POST','GET'])
def restaurants():
    user_id = get_user_id(session['user'])
    restaurants = get_restaurants(user_id)
    if 'user' not in session:
        flash ("You are not logged in!")
        return redirect(url_for('root'))
    return render_template("resturants.html", restaurants=restaurants)

#the actual page to make a new rest
@app.route('/addrest', methods = ['POST','GET'])
def addrest():
    if 'user' not in session:
        flash ("You are not logged in!")
        return redirect(url_for('root'))
    return render_template("registerrest.html")

# Accepts/parse the form to make new rest
@app.route('/newrest', methods = ['POST','GET'])
def newrest():
    ''' FOR CHECKING ARGS
    for each in request.args:
        print each + " " + request.args[each]
        print "\n\n"
    
    print request.args['tues_opening_hours'] 
    print "\n\n"
    print request.args['monstatus']  == 'open'
    '''
    user_id = get_user_id(session['user'])
    masterDict = dictBuilder(request.form)
    add_rest(user_id,masterDict)

    for each in masterDict:

        print each + ": " + str(masterDict[each])
        print "\n\n"

    if 'user' not in session:
        flash ("You are not logged in!")
        return redirect(url_for('root'))
    
    return redirect ("home")
### DICT STRING
### 000 = SUNDAY etc.
### {'000':['12','00','23','00']}
### tablePeeps is the number of people per table
    ### tablePeeps = [2,3] means two people for table 1, three people for table 2
    ### take the len to find out number of tables
### closed is list of rest that are closed
### reslen is the number of minutes a reservation is
### pic is the base64 string of an image
def dictBuilder(d):


    ret = {}
    ret['name'] = d['restname']
    ret['zip'] = d['zipcode']
    ret['reslen'] = d['reslen']
    ret['pic'] = d['pic']


    tablePeople = [] #numbers
    tablePeopleIndex = [] #order of those numbers recieved
    for each in d: #throws all of it down
        if each[-1] == "p":
            tablePeople.append(int(d[each]))
            tablePeopleIndex.append(int(each[0]))

    
    #creates blank list
    retTablePeople = ['none'] * len(tablePeople)
    #replaces elements by corresponding
    index = 0
    for each in tablePeopleIndex:
        #print indx + "\t" + tablePeople[indx] + "\n"
        #print "\n"
        retTablePeople[each-1] = tablePeople[index]
        index+=1

    ret['tablePeep'] = retTablePeople
    
    closed = []

    #Monday
    if d['monstatus'] == 'open':
        monList = []
        monList.append(d['mon_opening_hours'])
        monList.append(d['mon_opening_mins'])
        monList.append(d['mon_closing_hours'])
        monList.append(d['mon_closing_mins'])
        ret['001'] = monList


    else:
        closed.append('001')


    #Tuesday
    if d['tuesstatus'] == 'open':

        tuesList = []
        tuesList.append(d['tues_opening_hours'])
        tuesList.append(d['tues_opening_mins'])
        tuesList.append(d['tues_closing_hours'])
        tuesList.append(d['tues_closing_mins'])
        #print tuesList[0] + " " + tuesList[1] + " " + tuesList[2] + " " +tuesList[3]
        ret['002'] = tuesList
    else:
        closed.append('002')

    #Wednesday
    if d['wedstatus'] == 'open':
        wedList = []
        wedList.append(d['wed_opening_hours'])
        wedList.append(d['wed_opening_mins'])
        wedList.append(d['wed_closing_hours'])
        wedList.append(d['wed_closing_mins'])
        ret['003'] = wedList

    else:
        closed.append('003')

    #Thursday
    if d['thurstatus'] == 'open':
        thurList = []
        thurList.append(d['thur_opening_hours'])
        thurList.append(d['thur_opening_mins'])
        thurList.append(d['thur_closing_hours'])
        thurList.append(d['thur_closing_mins'])
        ret['004'] = thurList

    else:
        closed.append('004')

    #Friday
    if d['fristatus'] == 'open':
        friList = []
        friList.append(d['fri_opening_hours'])
        friList.append(d['fri_opening_mins'])
        friList.append(d['fri_closing_hours'])
        friList.append(d['fri_closing_mins'])
        ret['005'] = friList

    else:
        closed.append('005')

    #Saturday
    if d['satstatus'] == 'open':
        satList = []
        satList.append(d['sat_opening_hours'])
        satList.append(d['sat_opening_mins'])
        satList.append(d['sat_closing_hours'])
        satList.append(d['sat_closing_mins'])
        ret['006'] = satList

    else:
        closed.append('006')

    #Sunday
    if d['sunstatus'] == 'open':
        sunList = []
        sunList.append(d['sun_opening_hours'])
        sunList.append(d['sun_opening_mins'])
        sunList.append(d['sun_closing_hours'])
        sunList.append(d['sun_closing_mins'])
        ret['000'] = sunList

    else:
        closed.append('000')

    ret['closed'] = closed
    return ret
#way for customers to book
@app.route('/book',methods=['POST','GET'])
def book():
    nameofRest = request.args['name']
    restID = get_rest_id(nameofRest)
    daysOpen = get_open_times(restID)

    retClosedList = closedList(daysOpen)

    #Print number per table
    base64 = get_layout (restID)[1]

    tableSeats = get_layout(restID)[0]
    print tableSeats

    # Get picture ofid
    # Get list of tables
    if 'user' in session:
        return render_template("reserve.html", nameofRest=nameofRest, base64=base64, closed=retClosedList, tableSeats=tableSeats, ID = restID)
        
    else:    
        return redirect(url_for("root"))

def closedList(l):
    retStr = ""
    closed=[]

    for each in l:
        openingx = l[each][0].find(':')
        closingx = l[each][1].find(':')
        if l[each][0]=='closed':
            closed.append(each)
        elif l[each][0] == l[each][1]:
            closed.append(each)
        elif int(l[each][0][:openingx]) > int(l[each][1][:closingx]):
            closed.append(each)

    first = True
    for each in closed:
        print each
        if each == 'mon':
            retStr+="day != 1"
        if each == 'tue':
            retStr+="day != 2"
        if each == 'wed':
            retStr+="day != 3"
        if each == 'thu':
            retStr+="day != 4"
        if each == 'fri':
            retStr+="day != 5"
        if each == 'sat':
            retStr+="day != 6"
        if each == 'sun':
            retStr+="day != 0"
        retStr+=" && "

    retStr = retStr[:-3]
    return retStr

@app.route('/specialbook', methods = ['POST','GET'])
def specialbook():
    if 'user' not in session:
        flash ("You are not logged in!")
        return redirect(url_for('root'))
    
    restID = request.args['id']
    seat = request.args['seat']
    month = request.args['month']
    day = request.args['day']
    DOW = int(request.args['DOW'][0])

    day_names = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    day_of_week = day_names[DOW]

    available_times = get_available_times_for_day(restID, month, day, day_of_week, seat)
    
    return render_template("specialbooking.html", times=available_times, restID=restID, tableID=seat, month=month, day=day)

@app.route('/add_res', methods = ['POST', 'GET'])
def add_res():
    if 'user' not in session:
        flash ("You are not logged in!")
        return redirect(url_for('root'))
    
    time = request.args['reservation_time']
    rest_id = request.args['restID']
    table_id = request.args['tableID']
    month = request.args['month']
    day = request.args['day']
    customer_id = get_user_id(session['user'])

    if check_reservation(customer_id, month, day, time):
        add_reservation(rest_id, month, day, customer_id, table_id, time)
        return redirect(url_for("home"))
    else:
        flash ("You have already made a reservation at that time!")
        return redirect(url_for("home"))

    
if __name__ == '__main__':
    app.run(debug=True)

