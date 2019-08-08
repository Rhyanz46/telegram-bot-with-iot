import RPi.GPIO as GPIO
import time
import picamera
camera = picamera.PiCamera()

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN) #PIR
#GPIO.setup(24, GPIO.OUT) #BUzzer

    

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(23):
            camera.start_capture()
            camera.capture("gambar1.jpg")
            camera.capture('/home/pi/Desktop/image_%s.jpg' % i)
            camera.stop_capture()
            print("Motion Detected...")
            time.sleep(5) #to avoid multiple detection
        time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()
