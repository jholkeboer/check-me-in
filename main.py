import time
import json
from flask import Flask
from flask import render_template, redirect, request
from flaskext import wtf
from flaskext.wtf import validators
from google.appengine.ext import db
from flaskext import wtf
from flaskext.wtf import validators
from google.appengine.api import users
from models import CheckIn

app = Flask(__name__)
app.secret_key='unsafe'
app.DEBUG=True
app.CSRF_ENABLED=True
app.CSRF_SESSION_LKEY='unsafe'

class CheckInForm(wtf.Form):
    description = wtf.TextField('Description')
    under30 = wtf.BooleanField('Under 30 minutes to make?')
    category = wtf.RadioField('Category', choices=[('breakfast','Breakfast'),('lunch','Lunch'),('dinner','Dinner')])
    ingredients = wtf.TextAreaField('Ingredients')
    instructions = wtf.TextAreaField('Instructions')


@app.route('/')
def hello():
    # Following Google's model on line 65 here: https://github.com/GoogleCloudPlatform/appengine-guestbook-python/blob/master/guestbook.py
    user = users.get_current_user()
    
    if user:
        log_link = users.create_logout_url('/')
        log_text = 'Logout'
    else:
        log_link = users.create_login_url('/')
        log_text = 'Login'
    
    
    return render_template('/landing.html', user=user, log_link=log_link, log_text=log_text)

@app.route('/view', methods=['GET'])
def view():
    # get user
    user = users.get_current_user()
    
    if user:
        log_link = users.create_logout_url('/')
        log_text = 'Logout'
    else:
        log_link = users.create_login_url('/')
        log_text = 'Login'
    
    # query database
    checkins_query = db.GqlQuery("SELECT * FROM CheckIn")
    
    checkins = []
    for c in checkins_query:
        checkins.append(c)

    return render_template('/view_checkins.html', user=user, log_link=log_link, log_text=log_text, checkins=checkins)

@app.route('/new', methods=['GET'])
def new():

    return render_template('/new_checkin.html')

@app.route('/create', methods=['POST'])
def create():

    return '200 OK', 200

@app.route('/delete', methods=['POST'])
def delete():

    return '200 OK', 200

@app.errorhandler(404)
def page_not_found(e):
    return '404 Not Found.', 404


@app.errorhandler(500)
def application_error(e):
    return 'Error: {}'.format(e), 500

