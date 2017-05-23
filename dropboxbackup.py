import subprocess
import time

datetoday = time.strftime('%d-%m-%Y')

dirofdpUploader = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh"


def backup():
    subprocess.call([dirofdpUploader, "upload", "/var/www/FlaskApp/FlaskApp/videos/" + datetoday, "/Recordings"])

backup()
