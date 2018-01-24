# MADE-in-China--Dimitriy Leksanov, Eric Li, Angel Ng, Masha Zorin--Pd. 8
## Restaurant Reservation Assailant

## [Private Link to the Video](http://polazzo.com)

## So... What is this, exactly?
### The Restaurant Reservation Assistant allows restaurant patrons to connect t\
o one another from both sides of the curtain. By registering, users can choose \
to be either Owners or Customers.
### Both of these names are fairly self-explanatory. The Owners, for instance, \
are owners of real restaurants, whether in a chain or of the small business/sta\
rtup variety. Upon logging in, an Owner can fill out a quick, lavender-colored \
form to register his/her restaurant. The form includes all sorts of information\
--zipcode, name, and even an interactive, selectable map that allows an owner t\
o choose the table arrangement.
### For Customers, this is a similar deal. Customers can interact with a calend\
er and search through a bevy of restaurants. Then, when they find venues and da\
tes that work, they can sign up for a reservation time in a fairly simple proce\
ss.

## About the code...
### The code in this web application comes from a variety of languages. Firstly\
, the app itself (app.py) runs on Python through the Flask web framework. Howev\
er, the pages themselves are comprised of a combination of HTML and Jinja code,\
 the latter of which is connected to multiple Python scripts. The HTML code is \
mostly stored in the "templates" directory, to enable the render_template metho\
d, while the Python scripts are mainly stored either in the root directory or i\
n the "utils" directory.
### The HTMl is further decorated and made presentable with a combination of th\
e Bootstrap framework, as found on line, and separate CSS files, such as reserv\
e.css, which is found in the "static" directory. The main purpose of that direc\
tory, however, is to house the JavaScript code, which is responsible for a majo\
rity of the backend scripts that animate the pages. The JavaScript is diverse, \
and includes information from multiple separate libraries, such as jQuery.

### While the JavaScript code includes information from foreign libraries like \
jQuery, the Python code is no different, also including material from external \
sources. Some of these include flask, os, and urlparse. However, the only one t\
hat must be externally imported is flask. In the terminal, that is done by ente\
ring a virtual environment, and using pip to install:

```
$ virtualenv venv
$ . venv/bin/activate
(venv) $ pip install flask
```

### Then, the app can easily run with a simple terminal command in the app's ro\
ot directory:

```
$ python app.py
```

### This project also holds a bevy of data, which spans a large database, entit\
led restaurant_reservations.db. It includes calendar updates, and assists in st\
oring information about restaurants, accounts, and the like.

## Information about APIs and API keys
### You'll have to wait a while, because there aren't any :stuck_out_tongue_win\
king_eye:

## How to run and use our app:
###
