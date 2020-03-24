import os

os.system("python3 capture_image.py")
print("SUCCESS - created image.jpeg")
os.system("python3 detect-emotion-from-image.py image.jpeg")
print("SUCCESS - created data.json file")
os.system("python3 output-emotion-results.py image.jpeg")
