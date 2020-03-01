import sys
import spotipy
import spotipy.util as util

#SPOTIPY_CLIENT_ID = '7ed27438f9ed4372b1bb49c1a7e7fa60'
#SPOTIPY_CLIENT_SECRET = 'c17453d8d3f44a5ca70011e6b686ad43'

def show_tracks(tracks):
    for i, item in enumerate(track['item']):
        track = item['track']
        print ("    %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))

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
        print(user_details)
        user_id = user_details['id']
        
        playlists = sp.user_playlists(user_id)
        
        '''
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print('    toal tracks', playlist['tracks']['total'])
            results = sp.playlist(playlist['id'], fields='tracks,next')
        '''
    else:
        print("Can't get token for ", username)
