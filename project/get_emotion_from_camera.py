import sys, os

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()
        
os.system("python3 capture_image.py")
print("SUCCESS - created image.jpeg")
os.system("python3 detect-emotion-from-image.py image.jpeg")
print("SUCCESS - created data.json file")
os.system("python3 output-emotion-results.py image.jpeg")
print("SUCCESS - setting current playback")
os.system("python3 set_playlist.py %s" % (username))
