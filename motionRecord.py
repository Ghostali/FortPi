import json
import os
import smtplib
import time

from gpiozero import MotionSensor

import ffmpegWebcam
from tests import dbconnect

pir = MotionSensor(4)

# to store output
motion = []

# to store motion data for email
emailMotion = []


# detects motion than records using the webcam
def motiondetection():
    makedir()
    if pir.wait_for_motion() is True:
        time.sleep(1)
        if pir.wait_for_motion() is True:
            print("motion")
            ffmpegWebcam.recordfromwebcam()
            dbappend()
            timenow = time.strftime("%H:%M:%S")
            emailMotion.append(timenow)
            time.sleep(10)
            print("done")
            if len(emailMotion) == 10:
                sendemail(', '.join(emailMotion))
                print("emailed")
                del emailMotion[:]
                motiondetection()
            else:
                motiondetection()


# allows for the date and time motion was detected to be added to the database
def dbappend():
    datetoday = time.strftime("%d.%m.%Y")
    timenow = time.strftime("%H")
    motion.append(datetoday)
    motion.append(timenow)
    dbconnect.insertinto(motion)
    del motion[:]


def makedir():
    today = time.strftime('%d-%m-%Y')
    path = today
    os.chdir("/var/www/FlaskApp/FlaskApp/videos")
    os.makedirs(path, exist_ok=True)
    os.chdir("/var/www/FlaskApp/FlaskApp")


# obtains resolution from config file
def configfile():
    with open("config.json", 'r') as f:
        details = json.load(f)
        emailFrom = details["emailFrom"]
        emailTo = details["emailTo"]
        password = details["password"]
        return emailFrom, emailTo, password


# sends an email
def sendemail(times):
    details = configfile()
    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(details[0], details[2])
    msg = 'Subject: {}\n\n{}'.format("FortPi", "Motion detected 10 times at these points: " + times)
    server.sendmail(details[0], details[1], msg)
    server.quit()

motiondetection()

