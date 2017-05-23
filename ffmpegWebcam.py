import subprocess
import time


def recordfromwebcam():
    datetoday = time.strftime('%d-%m-%Y')
    filename1 = time.strftime("%H-%M-%S")
    filename = filename1 + ".mp4"
    subprocess.call(["ffmpeg", "-f", "video4linux2", "-input_format", "mjpeg", "-video_size", "640x480", "-i",
                    '/dev/video0', "-c:v", "copy", "-t", "10", "videos/" + datetoday + "/" + filename])
    return filename

#subprocess.call(["ffmpeg", "-y", "-f", "mp4", "-t", "15", "-s", "640x480", "-r", "25" "-i",
					#'http://192.168.0.29:5000/imgstream_feed', filename])

#subprocess.call(["ffmpeg", "-i", 'http://192.168.0.29:5000/imgstream_feed', "-c", "copy", "-map",
                     #  "0", "-f", "segment", "-segment_time", "300",
                        #"-segment_format", "mp4", filename])