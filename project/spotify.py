import spotipy
import spotipy.util as util

class MySpotify:

    def __init__(self, username):
        self.username = username
        self.token = self.authenticate()
        self.sp = spotipy.Spotify(auth=self.token)
        self.mood_playlists = []
        
    def authenticate(self):
        scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'
        token = util.prompt_for_user_token(self.username, scope)
        if token:
            return token

    def get_user_details(self):
        user_details = self.sp.me()
        user_details = dict((k, user_details[k]) for k in ('id', 'display_name', 'type'))
        return user_details

    def get_user_id(self):
        return self.get_user_details()['id']

    def get_user_display_name(self):
        return self.get_user_details()['display_name']

    def get_user_type(self):
        return self.get_user_details()['type']

    def get_mood_playlists(self):
        user_playlists = self.sp.user_playlists(self.sp.me()['id'])
        self.mood_playlists = []
        for playlist in user_playlists['items']:
            if any(playlist['name'] == e for e in ['Happiness', 'Angry', 'Sadness']):
                playlist_details = dict((k, playlist[k]) for k in ('name', 'id', 'type'))
                self.mood_playlists.append(playlist_details)
        return self.mood_playlists

    def get_playlist_id_by_name(self, playlist_name):
        for playlist in self.mood_playlists:
            if playlist['name'] == playlist_name:
                return playlist['id']
    
    def get_playlist_name_by_id(self, playlist_id):
        for playlist in self.mood_playlists:
            if playlist['id'] == playlist_id:
                return playlist['name']
