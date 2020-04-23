import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import tkinter.font as tkfont
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
        self.master.geometry("950x665+200+250")
        self.master.title("COMP3500 - Final Project")
        self.sp = None
        self.username = None
        self.prev_emotion = "no"
        self.bold_font = tkfont.Font(family="Arial", size=11, weight="bold")
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
            
            self.sp = spotipy.Spotify(auth=token)
            self.username = username

            tk.Label(self, text="USER", font=self.bold_font).place(x=0,y=40)
            self.user_details_text = tkscrolled.ScrolledText(self, wrap="none")
            self.user_details_text.place(x=0,y=60,height=90,width=400)
            user_details = dict((k, self.sp.me()[k]) for k in ('id', 'display_name', 'type'))
            self.user_details_text.insert(tk.END, json.dumps(user_details,indent=2))
            self.user_details_text.config(state="disabled")

            tk.Label(self, text="DEVICES", font=self.bold_font).place(x=0,y=170)
            self.devices_text = tkscrolled.ScrolledText(self, wrap="none")
            self.devices_text.place(x=0,y=190,height=133,width=400)
            devices = self.sp.devices()
            self.devices_text.insert(tk.END, json.dumps(devices,indent=2))
            self.devices_text.config(state="disabled")
            self.reset_btn = tk.Button(self, text="RESET", command=lambda:self.reset())
            self.reset_btn.place(x=332, y=160)

            tk.Label(self, text="PLAYLISTS URIS", font=self.bold_font).place(x=0,y=340)
            self.default_playlists_btn = tk.Button(self, text="DEFAULT", command=lambda:self.update_playlist_textboxes('default'))
            self.default_playlists_btn.place(x=225, y=335)
            self.update_playlists_btn = tk.Button(self, text="UPDATE", command=lambda:self.update_playlist_db())
            self.update_playlists_btn.place(x=319, y=335)
            self.emotion_labels = ["anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise"]
            self.playlist_entries = []
            self.playlist_btn = []
            i = 0;
            
            for e in self.emotion_labels:
                tk.Label(self, text=e).place(x=20,y=375+(i*35))
                self.playlist_entries.append(tk.Entry(self, width=26))
                self.playlist_entries[i].place(x=100, y=375+(i*35))
                self.playlist_btn.append(tk.Button(self, text="SEARCH", command=lambda x=i:self.search_playlist(x)))
                self.playlist_btn[i].place(x=320,y=370+(i*35))
                i += 1
            self.update_playlist_textboxes(self.username)

            tk.Label(self, text="FACE DATA", font=self.bold_font).place(x=425,y=40)
            self.face_data_text = tkscrolled.ScrolledText(self, wrap="none")
            self.face_data_text.place(x=425,y=60,height=370,width=500)
            self.face_data_text.config(state="disabled")

            self.view_btn = tk.Button(self, text="VIEW RECENT", command=lambda:self.view_image())
            self.view_btn.place(x=683,y=30)
            self.view_btn.configure(state="disabled")
            
            self.picture_btn = tk.Button(self, text="TAKE PICTURE", command=lambda:self.capture_image())
            self.picture_btn.place(x=803,y=30)

            tk.Label(self, text="CONSOLE", font=self.bold_font).place(x=425,y=450)
            self.console_text = tkscrolled.ScrolledText(self, wrap="none")
            self.console_text.place(x=425,y=470,height=160,width=500)
            self.console_text.config(state="disabled")

            self.try_again_btn = tk.Button(self, text="CHANGE PLAYBACK", command=lambda:self.change_playback())
            self.try_again_btn.place(x=770,y=440)
            self.try_again_btn.config(state="disabled")

    def search_playlist(self, index):
        emotion = self.emotion_labels[index]
        result = SearchApp(parent=self, sp=self.sp, emotion=emotion, curr_playlist=self.get_playlist_id_from_textbox(emotion)).show()
        if (len(self.playlist_entries[index].get()) != 0):
            self.playlist_entries[index].delete(0, "end")
        self.playlist_entries[index].insert(0, result)
        
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
 
    def update_playlist_db(self):
        dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')
        dbclient.query('DROP SERIES FROM "uri" WHERE "user"=\'%s\'' % self.username)
        json_body = [{
            "measurement": 'uri',
            "tags": {
                "user": self.username
            },
            "fields" : {
                "anger" : self.get_playlist_id_from_textbox("anger"),
                "contempt" : self.get_playlist_id_from_textbox("contempt"),
                "disgust" : self.get_playlist_id_from_textbox("disgust"),
                "fear" : self.get_playlist_id_from_textbox("fear"),
                "happiness" : self.get_playlist_id_from_textbox("happiness"),
                "neutral" : self.get_playlist_id_from_textbox("neutral"),
                "sadness" : self.get_playlist_id_from_textbox("sadness"),
                "surprise" : self.get_playlist_id_from_textbox("surprise")
            }
        }]
        dbclient.write_points(json_body)
        self.update_playlist_textboxes(self.username)

    def update_playlist_textboxes(self, user):
        for e in self.emotion_labels:
            index = self.emotion_labels.index(e)
            if (len(self.playlist_entries[index].get()) != 0):
                self.playlist_entries[index].delete(0, "end")
            self.playlist_entries[index].insert(0, self.get_playlist_id_from_db(e, user))
        
    def get_playlist_id_from_textbox(self, emotion):
        return self.playlist_entries[self.emotion_labels.index(emotion)].get()
        
    def get_playlist_id_from_db(self, emotion, user):
        # Create InfluxDB client 
        dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')
        result = dbclient.query('select * from "uri"')
        return list(result.get_points(measurement='uri', tags={'user':user}))[0][emotion]

    def capture_image(self):
        self.view_btn.config(state="disabled")
        
        os.system("python3 capture_image.py")
        os.system("python3 detect-emotion-from-image.py image.jpeg")
        os.system("python3 output-emotion-results.py image.jpeg")

        with open('data.json') as f:
            data = json.load(f)

        if (len(data) > 1):
            self.face_data_text.config(state="normal")
            if (len(self.face_data_text.get("1.0", "end-1c")) != 0):
                self.face_data_text.delete('1.0', tk.END)
            self.face_data_text.insert(tk.END, json.dumps(data[0],indent=2))
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
            
            # Get playlist ID associated with captured emotion for corresponding user
            current_playlist_id = self.get_playlist_id_from_textbox(highEmotion)
            playlist_name = (self.sp.playlist(current_playlist_id)['name']).encode('ascii', 'ignore').decode()
            self.console_text.config(state="normal")
            self.console_text.insert(tk.END, "Emotion detected: %s\n" % (highEmotion))
            self.console_text.insert(tk.END, "Playlist selected: %s\n" % (playlist_name))
            
            if (highEmotion != self.prev_emotion):
                self.prev_emotion = highEmotion
                self.change_playback()
            else:
                self.console_text.insert(tk.END, "Playlist already playing. No action...\n")

            self.console_text.config(state="disabled")
                
        else:
            self.face_data_text.config(state="normal")
            self.face_data_text.insert(tk.END, "Face not found.\n")
            self.face_data_text.config(state="disabled")

            
    def change_playback(self):
        self.console_text.config(state="normal")
        current_playlist_id = self.get_playlist_id_from_textbox(self.prev_emotion)
        # Change selected device playback to specified playlist ID
        if (len(self.sp.devices()['devices']) > 0):
            context_uri = "spotify:playlist:" + current_playlist_id
            current_device_id = self.sp.devices()['devices'][0]['id']
            if (self.sp.devices()['devices'][0]['is_active'] == False):
                self.console_text.insert(tk.END, "Current device is not active.\n")
                self.try_again_btn.config(state="normal")
            else:
                self.console_text.insert(tk.END, "Changing playback...\n")
                self.sp.shuffle(state=True, device_id=current_device_id)
                self.sp.start_playback(device_id=current_device_id, context_uri=context_uri)
                self.try_again_btn.config(state="disabled")
                    
        else:
            self.console_text.insert(tk.END, "You currently have no available devices for playback.\n")
            self.try_again_btn.config(state="normal")


class SearchApp(tk.Toplevel):
    def __init__(self, parent, sp=None, emotion=None, curr_playlist=None):
        tk.Toplevel.__init__(self, parent)
        self.geometry("380x340+150+275")
        self.title("Search Playlist")
        self.return_var = tk.StringVar()
        self.sp = sp
        self.emotion = emotion
        self.playlist_id = curr_playlist
        self.bold_font = tkfont.Font(family="Arial", size=10, weight="bold")
        self.init_widgets()

    def init_widgets(self):
        tk.Label(self, text="Emotion:").place(x=0,y=5)
        self.emotion_entry = tk.Entry(self)
        self.emotion_entry.place(x=110,y=5)
        self.emotion_entry.insert(0, self.emotion)
        self.emotion_entry.config(state="disabled")

        tk.Label(self, text="Current playlist:").place(x=0,y=35)
        self.playlist_entry = tk.Entry(self, textvariable=self.return_var)
        self.playlist_entry.place(x=110,y=35)
        self.playlist_entry.insert(0, self.playlist_id)
        self.set_btn = tk.Button(self, text="SET", command=lambda:self.set(), width=7)
        self.set_btn.place(x=290,y=30)
        
        tk.Label(self, text="Search Spotify:").place(x=0,y=65)
        self.search_entry = tk.Entry(self)
        self.search_entry.place(x=110, y=65)
        self.submit_btn = tk.Button(self, text="SEARCH", command=lambda:self.search(), width=7)
        self.submit_btn.place(x=290,y=60)
        
        tk.Label(self, text="SEARCH RESULTS:").place(x=0,y=106)
        self.tkvar = tk.StringVar(self)
        self.tkvar.set("")
        self.options = [""]
        self.option_menu = tk.OptionMenu(self, self.tkvar, *self.options)
        self.option_menu.place(x=129, y=100, width=150)
        self.option_menu.config(state="disabled")
        self.tkvar.trace('w', self.option_select)

        tk.Label(self, text="Playlist Info:").place(x=0, y=150)
        self.playlist_text = tkscrolled.ScrolledText(self, wrap="none")
        self.playlist_text.place(x=0,y=170,height=160,width=370)
        self.playlist_text.config(state="disabled")
        
        self.playlist_entry.bind("<Return>", lambda:self.set())
        
    def search(self):
        #check length
        self.select_btn = tk.Button(self, text="SELECT", command=lambda:self.select_playlist(), width=7)
        self.select_btn.place(x=290,y=100)
        
        search = self.search_entry.get()
        self.search_results = self.sp.search(q=search, type="playlist", limit=10)['playlists']['items']

        self.options = []
        for s in self.search_results:
            self.options.append(s['name'].encode('ascii', errors='ignore').decode())
        self.option_menu.config(state="normal")
        menu = self.option_menu["menu"]
        menu.delete(0, "end")
        for string in self.options:
            menu.add_command(label=string, command=lambda value=string: self.tkvar.set(value))
            
    def set(self):
        self.destroy()
        
    def show(self):
        self.wm_deiconify()
        self.focus_force()
        self.wait_window()
        return self.return_var.get()
            
    def select_playlist(self):
        selected_id = self.playlist_json['id']
        if (len(self.playlist_entry.get()) != 0):
            self.playlist_entry.delete(0, "end")
        self.playlist_entry.insert(0, selected_id)

    def option_select(self, *args):
        self.playlist_json = self.get_playlist_json_from_option_menu(self.tkvar.get())
        json_obj = {}
        json_obj['id']= self.playlist_json['id']
        json_obj['name']= self.playlist_json['name']
        json_obj['tracks'] = {'total':self.playlist_json['tracks']['total']}
        json_obj['owner'] = dict((k, self.playlist_json['owner'][k]) for k in ('display_name', 'id'))
        
        self.playlist_text.config(state="normal")
        if (len(self.playlist_text.get("1.0", "end-1c")) != 0):
            self.playlist_text.delete('1.0', tk.END)
        self.playlist_text.insert(tk.END, json.dumps(json_obj,indent=2))
        self.playlist_text.config(state="disabled")

    def get_playlist_json_from_option_menu(self, value):
        for s in self.search_results:
            if (s['name'].encode('ascii', errors='ignore').decode() == value):
                return s
   
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(master=root)
    app.mainloop()
