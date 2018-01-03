from flask import Flask, render_template, request, session, url_for, flash, redirect
from utils.accounts import authenticate
from utils.db_builder import checkUsername, addUser
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)  #for the cookies

BAD_USER = -1
BAD_PASS = -2
GOOD = 1

user = ""

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
        session['user'] = user
        return redirect( url_for('home'))
    
    
#user dashboard 
@app.route('/home', methods = ['POST','GET'])
def home():
    if 'user' in session:
        return render_template("home.html")
        
    else:    
        return redirect(url_for("root"))
        

#log out user
@app.route('/logout', methods = ['POST','GET'])
def logout():
    session.pop('user')
    flash('You have been logged out successfully')
    return redirect(url_for('root'))




    
if __name__ == '__main__':
    app.run(debug=True)

