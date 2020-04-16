from tkinter import *
import sys, json
import spotipy
from influxdb import InfluxDBClient

# Spotipy variables required to authorization
SPOTIPY_CLIENT_ID = '7ed27438f9ed4372b1bb49c1a7e7fa60'
SPOTIPY_CLIENT_SECRET = 'c17453d8d3f44a5ca70011e6b686ad43'
SPOTIPY_REDIRECT_URI = 'https://example.com/callback/'
SPOTIPY_SCOPE = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'

class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.sp = None
        self._frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

        
class LoginFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)

        self.username_label = Label(self, text="Enter username:").pack(side="left")
        self.username_entry = Entry(self).pack(side="left")
        self.username_submit = Button(self, text="SUBMIT", command=self.process_login(master)).pack(side="left")

        
    def process_login(self, master):
        master.switch_frame(MainFrame)
        '''
        username = self.username_entry.get()
        token = util.prompt_for_user_token(username, scope=SPOTIPY_SCOPE,
                                           client_id=SPOTIPY_CLIENT_ID,
                                           client_secret=SPOTIPY_CLIENT_SECRET,
                                           redirect_uri=SPOTIPY_REDIRECT_URI)
        if token:
            #master.sp = spotipy.Spotipy(auth=token)
            lambda: master.switch_frame(MainFrame)
'''
            

class MainFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        self.username_label = Label(self,text="hi").pack(side="left")
        #self.username_label['text'] = "Enter username: %s" % master.sp.me()['id']
    

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
