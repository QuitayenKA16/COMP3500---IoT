import picamera
from picamera.array import PiRGBArray
import time
from PIL import Image, ImageOps

# Create new Pi Camera object
camera = picamera.PiCamera()

# Show camera preview
camera.start_preview(fullscreen=False, window=(0,0,500,500))
time.sleep(5)

# Take picture and save as image.jpeg
camera.capture('image.jpeg')
camera.stop_preview()
camera.close()
im = Image.open('image.jpeg')

# Fix image orientation and save
im_flip = ImageOps.mirror(im)
im_flip = ImageOps.flip(im_flip)
im_flip.save('image.jpeg')
