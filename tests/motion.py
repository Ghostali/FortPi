from gpiozero import MotionSensor
import time

pir = MotionSensor(4)

while pir.wait_for_motion():
    print("motion detected")
    time.sleep(3)
