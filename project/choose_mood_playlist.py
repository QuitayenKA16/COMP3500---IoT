import sys
import json
import spotipy
import spotipy.util as util

SPOTIPY_CLIENT_ID = '7ed27438f9ed4372b1bb49c1a7e7fa60'
SPOTIPY_CLIENT_SECRET = 'c17453d8d3f44a5ca70011e6b686ad43'
SPOTIPY_REDIRECT_URI = 'https://example.com/callback/'

emotions = ['Happiness', 'angry', 'Sadness']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)

    if token:
        sp = spotipy.Spotify(auth=token)
        
        print("Login successful for", username)
        user_details = sp.me()
        user_id = user_details['id']
        user_details = dict((k, user_details[k]) for k in ('id', 'display_name', 'type'))
        print(json.dumps(user_details, indent=2))
        print("-------------------------------------------------------------------------------------------------")


        # get emotion playlists from all user playlists
        user_playlists = sp.user_playlists(user_id)
        emotion_playlists = []
        for playlist in user_playlists['items']:
            if any(playlist['name'] == e for e in emotions):
                playlist_details = dict((k, playlist[k]) for k in ('name', 'id', 'type'))
                emotion_playlists.append(playlist_details)

        print("Playlists:")
        for ep in emotion_playlists:       
            print(json.dumps(ep, indent=2))
        print("-------------------------------------------------------------------------------------------------")

        while True:
            print("Devices:")
            devices = sp.devices()
            print(json.dumps(devices, indent=2))
            print("-------------------------------------------------------------------------------------------------")

            if (len(devices['devices']) == 0):
                print("No active devices.")
                while (len(devices['devices']) == 0):
                    devices = sp.devices()
            else:
                device_index = -1
                if (len(devices['devices']) != 1):
                    device_index = input("Select device index: ")
                else:
                    device_index = 0
                    
                print("0: Happiness\n1: Angry\n2: Sadness")
                emotion_index = input("Select: ")
                current_emotion = emotions[int(emotion_index)]
                print("Select playlist: %s" % current_emotion)
                current_playlist_id = ""
                for playlist in emotion_playlists:
                    if (playlist['name'] == current_emotion):
                        current_playlist_id = playlist['id']
                print(current_playlist_id)

                print("-------------------------------------------------------------------------------------------------")
                if (sp.devices()['devices'][int(device_index)]['is_active'] == True):
                    print("Change playback...")
                    context_uri = "spotify:playlist:" + current_playlist_id
                    current_device_id = sp.devices()['devices'][int(device_index)]['id']
                    if (current_device_id != None):
                        sp.shuffle(state=1, device_id=current_device_id)
                        sp.start_playback(device_id=current_device_id, context_uri=context_uri)
                    
    else:
        print("Can't get token for ", username)
