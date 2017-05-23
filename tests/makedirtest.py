import os
import time


datetoday = time.strftime('%d-%m-%Y')
path = datetoday
print(path)


def makedir():
    today = time.strftime('%d-%m-%Y')
    path = today
    os.chdir("/var/www/FlaskApp/FlaskApp/videos")
    os.makedirs(path, exist_ok=True)

makedir()



