import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import os, json
import spotipy
import matplotlib.pyplot as plt
from matplotlib import patches
from PIL import Image
from io import BytesIO

from influxdb import InfluxDBClient

# Spotipy variables required to authorization
SPOTIPY_CLIENT_ID = '7ed27438f9ed4372b1bb49c1a7e7fa60'
SPOTIPY_CLIENT_SECRET = 'c17453d8d3f44a5ca70011e6b686ad43'
SPOTIPY_REDIRECT_URI = 'https://example.com/callback/'
SPOTIPY_SCOPE = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'

# Variable required to access Azure Face API
subscription_key = '11291157eba34c9c847b603363bc8def'
face_api_url = 'https://comp3500-azure-face-api.cognitiveservices.azure.com/face/v1.0/detect'


class MainApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("950x650+200+250")
        self.master.title("COMP3500 - Final Project")
        self.sp = None
        self.username = None
        self.prev_emotion = "no"
        self.pack(fill="both", expand=1)
        self.init_widgets()

    def init_widgets(self):
        tk.Label(self, text="Enter username:").place(x=0,y=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.insert(0, "QuitayenKA16")
        self.username_entry.place(x=115, y=5)
        self.username_submit = tk.Button(self, text="SUBMIT", command=lambda:self.process_login())
        self.username_submit.place(x=290,y=0)

    def process_login(self):
        username = self.username_entry.get()

        token = spotipy.util.prompt_for_user_token(username, scope=SPOTIPY_SCOPE, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)
        
        if token:
            self.username_entry.configure(state='disable')
            self.username_submit.configure(state='disable')
            self.reset_btn = tk.Button(self, text="RESET", command=lambda:self.reset())
            self.reset_btn.place(x=370,y=0)
            
            self.sp = spotipy.Spotify(auth=token)
            self.username = username

            tk.Label(self, text="USER").place(x=0,y=40)
            self.user_details_text = tkscrolled.ScrolledText(self, wrap="none")
            self.user_details_text.place(x=0,y=60,height=100,width=400)
            user_details = dict((k, self.sp.me()[k]) for k in ('id', 'display_name', 'type'))
            self.user_details_text.insert(tk.END, json.dumps(user_details,indent=2))
            self.user_details_text.config(state="disabled")

            tk.Label(self, text="DEVICES").place(x=0,y=160)
            self.devices_text = tkscrolled.ScrolledText(self, wrap="none")
            self.devices_text.place(x=0,y=180,height=133,width=400)
            devices = self.sp.devices()
            self.devices_text.insert(tk.END, json.dumps(devices,indent=2))
            self.devices_text.config(state="disabled")

            tk.Label(self, text="PLAYLISTS URIS").place(x=0,y=320)
            self.emotion_labels = ["anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]
            self.playlist_entries = []
            self.playlist_buttons = []
            i = 0;
            
            for e in self.emotion_labels:
                tk.Label(self, text=e).place(x=0,y=340+(i*35))
                self.playlist_entries.append(tk.Entry(self, width=25))
                self.playlist_entries[i].insert(0, self.get_playlist_id(e))
                self.playlist_entries[i].place(x=80, y=340+(i*35))
                self.playlist_buttons.append(tk.Button(self, text="UPDATE"))
                self.playlist_buttons[i]["command"] = lambda x=i:self.update_playlist(x)
                self.playlist_buttons[i].place(x=290, y=340+(i*34))
                i += 1

            tk.Label(self, text="FACE DATA").place(x=425,y=40)
            self.face_data_text = tkscrolled.ScrolledText(self, wrap="none")
            self.face_data_text.place(x=425,y=60,height=400,width=500)
            self.face_data_text.config(state="disabled")

            self.view_btn = tk.Button(self, text="VIEW RECENT", command=lambda:self.view_image())
            self.view_btn.place(x=680,y=0)
            self.view_btn.configure(state="disabled")
            
            self.picture_btn = tk.Button(self, text="TAKE PICTURE", command=lambda:self.capture_image())
            self.picture_btn.place(x=800,y=0)

            tk.Label(self, text="CONSOLE").place(x=425,y=470)
            self.console_text = tkscrolled.ScrolledText(self, wrap="none")
            self.console_text.place(x=425,y=490,height=110,width=500)
            self.console_text.config(state="disabled")

    def reset(self):
        devices = self.sp.devices()
        self.devices_text.config(state="normal")
        self.devices_text.delete('1.0', tk.END)
        self.devices_text.insert(tk.END, json.dumps(devices,indent=2))
        self.devices_text.config(state="disabled")
        
            
    def view_image(self):
        image_read = open("analyze_image.jpeg", "rb").read()
        image = Image.open(BytesIO(image_read))
        plt.figure(figsize=(8,5))
        ax = plt.imshow(image, alpha=1)
        _ = plt.axis("off")
        plt.show()
            
    def update_playlist(self, i):
        emotion = self.emotion_labels[i]
        value = self.playlist_entries[i].get()
        print("%s: %s" % (emotion, value))
        
    def get_playlist_id(self, emotion):
        # Create InfluxDB client 
        dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')
        result = dbclient.query('select * from "uri"')
        return list(result.get_points(measurement='uri', tags={'user':self.username}))[0][emotion]

    def capture_image(self):
        os.system("python3 capture_image.py")
        #os.system("python3 detect-emotion-from-image.py image.jpeg")
        os.system("python3 output-emotion-results.py image.jpeg")

        with open('data.json') as f:
            data = json.load(f)
            
        self.face_data_text.config(state="normal")
        self.face_data-text.delete('1.0', tk.END)
        self.face_data_text.insert(tk.END, json.dumps(data,indent=2))
        self.face_data_text.config(state="disabled")
        self.view_btn.config(state="normal")

        emotion_values = data[0]['faceAttributes']['emotion']

        # Get emotion with greatest value
        highVal = 0
        highEmotion = 'anger'
        for e in self.emotion_labels:
            if emotion_values[e] > highVal:
                highVal = emotion_values[e]
                highEmotion = e
            
        # Get playlist ID associated with captured emotion (with highest value) for corresponding user
        current_playlist_id = self.get_playlist_id(highEmotion)
        playlist_name = self.sp.playlist(current_playlist_id)['name']
        self.console_text.config(state="normal")
        self.console_text.insert(tk.END, "Emotion detected: %s\n" % (highEmotion))
        self.console_text.insert(tk.END, "Playlist selected: %s\n" % (playlist_name))

        if (highEmotion != self.prev_emotion):
            self.prev_emotion = highEmotion
            # Change selected device playback to specified playlist ID
            if (len(self.sp.devices()['devices']) > 0 and (self.sp.devices()['devices'][0]['is_active'] == True)):
                self.console_text.insert(tk.END, "Changing playback...\n")
                context_uri = "spotify:playlist:" + current_playlist_id
                current_device_id = self.sp.devices()['devices'][0]['id']
                if (current_device_id != None):
                    self.sp.shuffle(state=True, device_id=current_device_id)
                    self.sp.start_playback(device_id=current_device_id, context_uri=context_uri)

        else:
            self.console_text.insert(tk.END, "Playlist already playing. No action...\n")
        self.console_text.config(state="disabled")

            
                
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(master=root)
    app.mainloop()
