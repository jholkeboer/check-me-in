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
import datetime

app = Flask(__name__)
app.secret_key='unsafe'
app.DEBUG=True
app.CSRF_ENABLED=True
app.CSRF_SESSION_LKEY='unsafe'

class CheckInForm(wtf.Form):
    owner = wtf.HiddenField('Description')
    description = wtf.TextField('Under 30 minutes to make?')
    latitude = wtf.HiddenField('Latitude')
    longitude = wtf.HiddenField('Longitude')
    timestamp = wtf.HiddenField('timestamp')


@app.route('/')
def hello():
    # Following Google's model on line 65 here: https://github.com/GoogleCloudPlatform/appengine-guestbook-python/blob/master/guestbook.py
    user = users.get_current_user()
    
    if user:
        log_link = users.create_logout_url('/')
        log_text = 'Logout'
        return redirect('/view')
    else:
        log_link = users.create_login_url('/')
        log_text = 'Login'
    
    
    return render_template('/view_checkins.html', user=user, log_link=log_link, log_text=log_text)

@app.route('/view', methods=['GET'])
def view():
    # get user
    user = users.get_current_user()
    
    if user:
        log_link = users.create_logout_url('/')
        log_text = 'Logout'
    else:
        return redirect('/')
    
    # query database
    checkins_query = db.GqlQuery("SELECT * FROM CheckIn WHERE owner= :1", user.user_id())
    
    checkins = []
    timedisplay = {}
    for c in checkins_query:
        checkins.append(c)
        timedisplay[c.key()] = datetime.datetime.fromtimestamp(c.timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')

    return render_template('/view_checkins.html', user=user, log_link=log_link, log_text=log_text, checkins=checkins, timedisplay=timedisplay, datetime=datetime)

@app.route('/new', methods=['GET', 'POST'])
def new():
    # get user
    user = users.get_current_user()
    
    if user:
        log_link = users.create_logout_url('/')
        log_text = 'Logout'
    else:
        log_link = users.create_login_url('/')
        log_text = 'Login'

    form = CheckInForm()
    if form.validate_on_submit():
        checkIn =   CheckIn(owner = str(user.user_id()),
                            latitude = float(form.latitude.data),
                            longitude = float(form.longitude.data),
                            description = form.description.data,
                            timestamp = int(form.timestamp.data))
        checkIn.put()
        print "Check-in saved."
        time.sleep(1)
        return redirect('/view')
    return render_template('/new_checkin.html', form=form, user=user, log_link=log_link, log_text=log_text)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    # get user
    user = users.get_current_user()
    
    if user:
        log_link = users.create_logout_url('/')
        log_text = 'Logout'
    else:
        log_link = users.create_login_url('/')
        log_text = 'Login'

    key = request.args.get('key')
    checkin = CheckIn.get(key)
    form = CheckInForm()
    timedisplay = ''
    if not key:
        return redirect('/view')
    if request.method == 'GET':
        if checkin:
            form.latitude.data = checkin.latitude
            form.longitude.data = checkin.longitude
            form.owner.data = user.user_id()
            form.description.data = checkin.description
            form.timestamp.data = checkin.timestamp
            timedisplay = datetime.datetime.fromtimestamp(checkin.timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')
            form.key = checkin.key()
    elif form.validate_on_submit():
        checkin.latitude = float(form.latitude.data)
        checkin.longitude = float(form.longitude.data)
        checkin.owner = user.user_id()
        checkin.description = form.description.data
        checkin.timestamp = int(form.timestamp.data)
        checkin.put()
        print "checkin edited."
        time.sleep(1)
        return redirect('/view')
    return render_template('edit_checkin.html', form=form, checkin=checkin, user=user, log_link=log_link, log_text=log_text, timedisplay=timedisplay)

@app.route('/delete', methods=['POST', 'DELETE'])
def delete():
    key = request.args.get('key')
    checkin = CheckIn.get(key)
    checkin.delete()
    time.sleep(1)
    return redirect('/view')

@app.errorhandler(404)
def page_not_found(e):
    return '404 Not Found.', 404


@app.errorhandler(500)
def application_error(e):
    return 'Error: {}'.format(e), 500

