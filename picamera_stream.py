import threading
import picamera
import time
import io
import json


# obtains resolution from config file
def configfile():
    with open("config.json", 'r') as f:
        details = json.load(f)
        width = details["width"]
        height = details["height"]
        return width, height


class Camera:
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            resolution = configfile()
            # camera setup
            camera.resolution = (resolution[0], resolution[1])
            # let camera warm up
            camera.start_preview()
            time.sleep(2)
            camera.stop_preview()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # Add time to the stream
                timenow = time.strftime("%H:%M:%S")
                camera.annotate_text = timenow

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
