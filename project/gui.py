import guizero as gui
import sys
import json

import spotify


def authenticate():
    username = username_textbox.value
    sp = spotify.MySpotify(username)

    username_box.enabled = False
    user_details_box = gui.Box(app)
    gui.Text(user_details_box, text="Display Name: "+sp.get_user_display_name())
    gui.Text(user_details_box, text="ID: "+sp.get_user_id())
    
    mood_options = []
    for p in sp.get_mood_playlists():
        mood_options.append(p['name'])
    combo = gui.Combo(app, options=mood_options)
    


app = gui.App(title='IoT Project')
username_box = gui.Box(app)
gui.Text(username_box, align='left', text='Enter username:')
username_textbox=gui.TextBox(username_box, align='left', width=25)
gui.PushButton(username_box, align='left', padx=5, pady=5, text='Submit', command=authenticate)
app.display()
