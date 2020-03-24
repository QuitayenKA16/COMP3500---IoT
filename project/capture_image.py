import picamera
from picamera.array import PiRGBArray
import time
from PIL import Image, ImageOps

camera = picamera.PiCamera()
camera.start_preview(fullscreen=False, window=(0,0,500,500))
time.sleep(5)
camera.capture('image.jpeg')
camera.stop_preview()
camera.close()

im = Image.open('image.jpeg')
im_flip = ImageOps.mirror(im)
im_flip.save('image.jpeg')
