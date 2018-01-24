# MADE-in-China-- Angel Ng, Dimitriy Leksanov, Eric Li, Masha Zorin--Pd. 8
## Restaurant Reservation Assistant

## [Private Link to the Video](https://www.youtube.com/watch?v=Aacu1PAaPBc&feature=youtu.be)

## So... What is this, exactly?
The Restaurant Reservation Assistant allows restaurant patrons to connect to one another from both sides of the curtain. By registering, users can choose to be either Owners or Customers.
Both of these names are fairly self-explanatory. The Owners, for instance, are owners of real restaurants, whether in a chain or of the small business/startup variety. Upon logging in, an Owner can fill out a quick, lavender-colored form to register his/her restaurant. The form includes all sorts of information--zipcode, name, and even an interactive, selectable map that allows an owner to choose the table arrangement.
For Customers, this is a similar deal. Customers can interact with a calender and search through a bevy of restaurants. Then, when they find venues and dates that work, they can sign up for a reservation time in a fairly simple process.

## About the code...
 The code in this web application comes from a variety of languages. Firstly, the app itself (app.py) runs on Python through the Flask web framework. However, the pages themselves are comprised of a combination of HTML and Jinja code, the latter of which is connected to multiple Python scripts. The HTML code is mostly stored in the "templates" directory, to enable the render_template method, while the Python scripts are mainly stored either in the root directory or in the "utils" directory.
 
The HTMl is further decorated and made presentable with a combination of the Bootstrap framework, as found online, and separate CSS files, such as reserve.css, which is found in the "static" directory. The main purpose of that directory, however, is to house the JavaScript code, which is responsible for a majority of the backend scripts that animate the pages. The JavaScript is diverse, and includes information from multiple separate libraries, such as jQuery.

The JavaScript and CSS code includes information from foreign libraries like jQuery,jQuery UI, HTML2Canvas and a couple more. The Python code is no different, also including material from external sources. Some of these include flask, os, and urlparse. 

However, the only one that must be externally imported is flask. In the terminal, that is done by entering a virtual environment, and using pip to install:

```
$ virtualenv venv
$ . venv/bin/activate
(venv) $ pip install flask
```

### Then, the app can easily run with a simple terminal command in the app's root directory:

```
$ python app.py
```

### This project also holds a bevy of data, which spans a large database, entitled restaurant_reservations.db. It includes calendar updates, and assists in storing information about restaurants, accounts, and the like.

## Information about APIs and API keys
You'll have to wait a while, because there aren't any :stuck_out_tongue_winking_eye:

## How to run and use our app:
First, you will be directed to a beautiful login screen. If you don't yet have an account, click on the link towards the middle of the screen. From their, register a NEW username and password, and select either Owner or Customer. Then, you will be redirected to your corresponding homepage. If you are an Owner, click on the link directing you to register a restaurant. From there, fill out the form in this sequence: form, then select tables, then click finalize, and then, finally, click submit. If you are a Customer, you should be able to select restaurants and reservation times from a calendar. Then, in all cases, click on Restaurants to view either available (Customer) or submitted (Owner) restaurants, and click Log Out to do just that.

### --The MADE-in-China Crew!
