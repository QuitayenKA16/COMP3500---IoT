import sys, json
import spotipy
import spotipy.util as util
from influxdb import InfluxDBClient

# Spotipy variables required to authorization
SPOTIPY_CLIENT_ID = '7ed27438f9ed4372b1bb49c1a7e7fa60'
SPOTIPY_CLIENT_SECRET = 'c17453d8d3f44a5ca70011e6b686ad43'
SPOTIPY_REDIRECT_URI = 'https://example.com/callback'

# Required console input: username
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()

# Authorization scope
scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'

# Authorization token
token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

if token:
    # Create new spotipy object from authorization token (based on user)
    sp = spotipy.Spotify(auth=token)
        
    print("Login successful for", username)

    # Get and output important user information
    user_details = sp.me()
    user_id = user_details['id']
    user_details = dict((k, user_details[k]) for k in ('id', 'display_name', 'type'))
    print(json.dumps(user_details, indent=2))
    print("-------------------------------------------------------------------------------------------------")

    print("Devices:")

    # Get and output active user devices
    devices = sp.devices()
    print(json.dumps(devices, indent=2))
    print("-------------------------------------------------------------------------------------------------")

    # Wait until at least one user device is active
    if (len(devices['devices']) == 0):
        print("No active devices.")
        while (len(devices['devices']) == 0):
            devices = sp.devices()
    else:
        device_index = -1

        # If multiple active devices, user choose which device to control playback
        if (len(devices['devices']) != 1):
            device_index = input("Select device index: ")
        else:
            device_index = 0

        # Read json storing face emotion values
        with open('data.json') as f:
            data = json.load(f)

        emotion_labels = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
        emotion_values = data[0]['faceAttributes']['emotion']

        # Get emotion with greatest value
        highVal = 0
        highEmotion = 'anger'
        for e in emotion_labels:
            if emotion_values[e] > highVal:
                highVal = emotion_values[e]
                highEmotion = e

        # Create InfluxDB client 
        dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')

        # Select values from URI table
        result = dbclient.query('select * from "uri"')

        # Get playlist ID associated with captured emotion (with highest value) for corresponding user
        current_playlist_id = list(result.get_points(measurement='uri', tags={'user':username}))[0][highEmotion]

        # Change selected device playback to specified playlist ID
        if (sp.devices()['devices'][int(device_index)]['is_active'] == True):
            print("Change playback...")
            context_uri = "spotify:playlist:" + current_playlist_id
            current_device_id = sp.devices()['devices'][int(device_index)]['id']
            if (current_device_id != None):
                sp.shuffle(state=True, device_id=current_device_id)
                sp.start_playback(device_id=current_device_id, context_uri=context_uri)
                    
else:
    print("Can't get token for ", username)
    
