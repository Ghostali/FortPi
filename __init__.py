#!/usr/bin/env python
import itertools
import os
import sqlite3
import time
from datetime import date, timedelta
from functools import wraps
import hash
from flask import Flask, render_template, redirect, url_for, request, Response, session, flash, send_from_directory
from picamera_stream import Camera
import json

# timer which starts when the app is run
start = time.strftime("%H")

app = Flask(__name__)

# config
app.secret_key = 'random key'

# today
today = date.today()
defaultvideos = today.strftime('%d-%m-%Y')


# route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect("database/" + "users.db")
    os.chdir("/var/www/FlaskApp/FlaskApp")
    error = None
    if request.method == 'POST':
        u = request.form['username']
        print(u)
        p = hash.hash_password(request.form['password'])
        print(p)
        credentials = list(itertools.chain.from_iterable
              (conn.execute("SELECT * from Users")))
        if u != credentials[0] or p != credentials[1]:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['username'] = u
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


# returns the index page
@app.route('/index')
@login_required
def index():
    username = session.get('username')
    os.chdir("/var/www/FlaskApp/FlaskApp")
    return render_template('index.html', username=username)


# returns the reports page with graphs
@app.route('/reports')
@login_required
def reports(chartID='chart_ID', chart_type='column', chart_height=500):

    # changes the dir of the pi to the app folder
    os.chdir("/var/www/FlaskApp/FlaskApp")

    # checks current time
    end = time.strftime("%H")

    # checks how long the app has been running for
    uptime = int(end) - int(start)

    # today
    today = date.today()
    today = today.strftime('%d.%m.%Y')
    # yesterday
    one = date.today() - timedelta(1)
    one = one.strftime('%d.%m.%Y')
    # two days ago
    two = date.today() - timedelta(2)
    two = two.strftime('%d.%m.%Y')
    # three days ago
    three = date.today() - timedelta(3)
    three = three.strftime('%d.%m.%Y')
    # four days ago
    four = date.today() - timedelta(4)
    four = four.strftime('%d.%m.%Y')
    # five days ago
    five = date.today() - timedelta(5)
    five = five.strftime('%d.%m.%Y')
    # six days ago
    six = date.today() - timedelta(6)
    six = six.strftime('%d.%m.%Y')
    # seven days ago
    seven = date.today() - timedelta(7)
    seven = seven.strftime('%d.%m.%Y')

    # connects to the DB file
    cy = sqlite3.connect('database/' + 'motiondb.db', check_same_thread=False)

    # puts the dates into a list
    dates = [seven, six, five, four, three, two, one, today]

    # counts how many times the same date shows up then puts it into a list
    se = list(itertools.chain.from_iterable(cy.execute("SELECT count(*) from Motions WHERE Date = (?)", (seven,))))
    si = list(itertools.chain.from_iterable(cy.execute("SELECT count(*) from Motions WHERE Date = (?)", (six,))))
    fi = list(itertools.chain.from_iterable(cy.execute("SELECT count(*) from Motions WHERE Date = (?)", (five,))))
    fo = list(itertools.chain.from_iterable(cy.execute("SELECT count(*) from Motions WHERE Date = (?)", (four,))))
    th = list(itertools.chain.from_iterable(cy.execute("SELECT count(*) from Motions WHERE Date = (?)", (three,))))
    tw = list(itertools.chain.from_iterable(cy.execute("SELECT count(*) from Motions WHERE Date = (?)", (two,))))
    on = list(itertools.chain.from_iterable(cy.execute("SELECT count(*) from Motions WHERE Date = (?)", (one,))))
    to = list(itertools.chain.from_iterable(cy.execute("SELECT count(*) from Motions WHERE Date = (?)", (today,))))

    # creates a list of lists
    seriesdata = [se, si, fi, fo, th, tw, on, to]

    # changes a list of lists into a list
    weeklydata = list(itertools.chain(*seriesdata))

    # calculates the sum of the list
    weekly = sum([int(i) for i in weeklydata])

    # Graph variables
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    series = [{"name": "Values", "data": seriesdata}]
    xAxis = {"categories": dates}
    yAxis = {"min": 0, "max": 50, "title": {"text": 'Amount of times motion detected'}}
    title = {"text": 'Motion detected'}
    username = session.get('username')

    mostcommon = list(itertools.chain.from_iterable
                      (cy.execute("SELECT Time FROM Motions GROUP BY Time ORDER BY COUNT(*) DESC LIMIT 1")))

    # adds the am or pm to the redbox
    if mostcommon[0] <= 11:
        timemark = "am"
    else:
        timemark = "pm"

    return render_template('reports.html', today=today, dates=dates,
                           chartID=chartID, chart=chart, series=series,
                           title=title, xAxis=xAxis, yAxis=yAxis, to=to, weekly=weekly,
                           uptime=uptime, username=username,mostcommon=mostcommon, timemark=timemark)


# generates the page for the second graph which is then iframed into the reports html page
@app.route('/secondGraph')
@login_required
def secondgraph(chartID='chart_ID', chart_type='line', chart_height=500):

    # changes the dir of the pi to the app folder
    os.chdir("/var/www/FlaskApp/FlaskApp")

    # connects to the DB file
    cy = sqlite3.connect('database/' + 'motiondb.db', check_same_thread=False)

    # list of times to compare to db
    numbers = \
        ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
         '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '00']

    # a list that will be used to hold variables
    hours = []

    # creates a list of variables
    for i in range(0, 23):
        for b in numbers:
            hours.append(b)

    # gets todays date
    today = time.strftime("%d.%m.%Y")

    # check how many times motion was detected in each hour of todays date
    a = list(itertools.chain.from_iterable
              (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ? ", (today, hours[0]))))
    b = list(itertools.chain.from_iterable
              (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[1]))))
    c = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[2]))))
    d = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[3]))))
    e = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[4]))))
    f = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[5]))))
    g = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[6]))))
    h = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[7]))))
    i = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[8]))))
    j = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[9]))))
    k = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[10]))))
    l = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[11]))))
    m = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[12]))))
    n = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[13]))))
    o = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[14]))))
    p = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[15]))))
    q = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[16]))))
    r = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[17]))))
    s = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[18]))))
    t = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[19]))))
    u = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[20]))))
    v = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[21]))))
    w = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[22]))))
    x = list(itertools.chain.from_iterable
             (cy.execute("SELECT count(*) from Motions WHERE Date = ? AND Time = ?", (today, hours[23]))))

    # puts all the ints into a list of lists
    seriesdata = [a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x]

    # Graph variables
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height}
    series = [{"name": "Values", "data": seriesdata}]
    xAxis = {"categories": hours}
    yAxis = {"min": 0, "max": 50, "title": {"text": 'Amount of times motion detected'}}
    title = {"text": 'Motion detected'}
    return render_template('secondGraph.html', today=today, hours=hours,
                           chartID=chartID, chart=chart, series=series,
                           title=title, xAxis=xAxis, yAxis=yAxis)


# returns the recordings page and also the video names in the directory
@app.route('/recordings', methods=['POST', 'GET'])
@login_required
def recordings():
    username = session.get('username')
    os.chdir("/var/www/FlaskApp/FlaskApp/videos")
    video_names = os.listdir('./' + defaultvideos)
    return render_template('recordings.html', video_names=video_names, username=username)


# allows the video files in this directory to be accessed and added to a list in the html
@app.route('/videos/' + defaultvideos + '/<filename>')
@login_required
def send_video(filename):
    os.chdir("/var/www/FlaskApp/FlaskApp")
    return send_from_directory("videos/" + defaultvideos, filename=filename)


# returns the profile page
@app.route('/profile')
@login_required
def profile():
    os.chdir("/var/www/FlaskApp/FlaskApp")
    username = session.get('username')
    return render_template('profile.html', username=username)


# returns the changeusername page
@app.route('/changeusername', methods=['GET', 'POST'])
@login_required
def changeusername():
    os.chdir("/var/www/FlaskApp/FlaskApp")
    conn = sqlite3.connect("database/" + "users.db")
    error = None
    username = session.get('username')
    if request.method == 'POST':
        old = request.form['oldusername']
        print(old)
        new = request.form['newusername']
        print(new)
        usercheck = list(itertools.chain.from_iterable
                         (conn.execute("SELECT Username from Users")))
        print(usercheck[0])
        if old != usercheck[0]:
            error = 'Invalid Username. Please try again.'
        else:
            c = conn.cursor()
            c.execute("UPDATE Users SET Username = ? WHERE Username = ?", (new, old))
            conn.commit()
            session['username'] = new
            return redirect(url_for('profile'))
    return render_template('changeusername.html', username=username, error=error)


# returns the changepassword page
@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    os.chdir("/var/www/FlaskApp/FlaskApp")
    conn = sqlite3.connect("database/" + "users.db")
    error = None
    username = session.get('username')
    if request.method == 'POST':
        old = hash.hash_password(request.form['oldpassword'])
        print(old)
        new = hash.hash_password(request.form['newpassword'])
        print(new)
        passcheck = list(itertools.chain.from_iterable
                         (conn.execute("SELECT Password from Users")))
        print(passcheck[0])
        if old != passcheck[0]:
            error = 'Invalid Password. Please try again.'
        else:
            c = conn.cursor()
            c.execute("UPDATE Users SET Password = ? WHERE Password = ?", (new, old))
            conn.commit()
            return redirect(url_for('profile'))
    return render_template('changepassword.html', username=username, error=error)


# returns the settings page
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    os.chdir("/var/www/FlaskApp/FlaskApp")
    username = session.get('username')

    width = ['320', '640', '800', '1280', '1440']
    height = ['240', '480', '600', '720', '920']

    chosenwidth = ""
    chosenheight = ""

    if request.method == 'POST':
        chosenwidth = request.form['dropdownwidth']
        chosenheight = request.form['dropdownheight']
        print(chosenwidth)
        print(chosenheight)

        if chosenwidth and chosenheight != 'default':
            with open('config.json', 'r') as f:
                json_data = json.load(f)
                json_data['width'] = int(chosenwidth)
                json_data['height'] = int(chosenheight)
            with open('config.json', 'w') as f:
                f.write(json.dumps(json_data))
            print("changed resolution")
            flash('Changed resolution.')
            return redirect(url_for('settings'))
        else:
            flash('Resolution kept the same.')
            return redirect(url_for('settings'))

    return render_template('settings.html', username=username, width=width, height=height,
                           chosenwidth=chosenwidth, chosenheight=chosenheight)


# sends the user to the login page when the logout button is pressed
@app.route('/logout')
@login_required
def logout():
    os.chdir("/var/www/FlaskApp/FlaskApp")
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('login'))


# Picamera streaming generator function
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# allows for the mjpeg stream to be displayed in the html
@app.route('/imgstream_feed')
@login_required
def imgstream_feed():
    # Image streaming route, should be placed in the img tag.
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# runs app when called
def apprun():
    app.run(host='0.0.0.0', threaded=True, debug=True)

# runs the flask web app
if __name__ == '__main__':
    apprun()


