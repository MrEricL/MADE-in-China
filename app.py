from flask import Flask, render_template, request, session, url_for, flash, redirect
from utils.accounts import authenticate
from utils.db_builder import checkUsername, addUser, getUserType, get_user_id, get_restaurants
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
    user_type = getUserType (user)
    if 'user' in session:
        print "This is the user type: " + str(user_type)
        return render_template("home.html",userstatus=user_type)
        
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
    return render_template("resturants.html", restaurants=restaurants)

#the actual page to make a new rest
@app.route('/addrest', methods = ['POST','GET'])
def addrest():
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
    masterDict = dictBuilder(request.args)
    for each in masterDict:

        print each + ": " + str(masterDict[each])
        print "\n\n"

    return render_template("registerrest.html")
### DICT STRING
### 000 = SUNDAY
### {'000':['12','00','23','00']}
def dictBuilder(d):
    ret = {}
    ret['name'] = d['restname']
    ret['zip'] = d['zipcode']
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
        print "Worked1"
        wedList.append(d['wed_opening_mins'])
        print "Worked2"
        wedList.append(d['wed_closing_hours'])
        print "Worked3"
        wedList.append(d['wed_closing_mins'])
        ret['003'] = wedList
        print 'hi'
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
        ret['001'] = sunList

    else:
        closed.append('000')

    ret['closed'] = closed
    return ret
#way for customers to book
@app.route('/book',methods=['POST','GET'])
def book():
    return render_template("reserve.html")
    
if __name__ == '__main__':
    app.run(debug=True)

