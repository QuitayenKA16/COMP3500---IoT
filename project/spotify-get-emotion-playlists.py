import sys
import json
import spotipy
import spotipy.util as util

#SPOTIPY_CLIENT_ID = '7ed27438f9ed4372b1bb49c1a7e7fa60'
#SPOTIPY_CLIENT_SECRET = 'c17453d8d3f44a5ca70011e6b686ad43'
emotions = ['Happy', 'Mad', 'Sad']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username)

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
                    
    else:
        print("Can't get token for ", username)
