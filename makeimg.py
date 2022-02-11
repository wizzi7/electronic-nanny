
from time import sleep
from picamera import PiCamera
import requests
import datetime

BASE = "http://192.168.0.122:5000/sendimage"

camera = PiCamera()
camera.resolution = (720, 576)
camera.start_preview()
camera.vflip = True
# Camera warm-up time
sleep(2)

ctime = datetime.datetime.now()
time = ctime.strftime('%d-%m-%Y-%H.%M.%S')
time = str(time)

camera.capture('/home/pi/Desktop/images/img_'+time +'.jpg')
sleep(2)

with open('/home/pi/Desktop/images/img_' + time + '.jpg', 'rb') as file:
	print('Rozpoczecie przesylania')
	dict = {'file': file}
	r = requests.post(BASE, files=dict)
	print("Wyslano obraz")
	exit()
