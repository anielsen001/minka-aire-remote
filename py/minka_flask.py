from flask import Flask, render_template, request

from minka_remote import MinkaAireRemote

import datetime

def getTimeStr():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    return timeString

# create the minka aire remote object
mr = MinkaAireRemote()

# create the app
app = Flask(__name__)

@app.route('/')
def main():
    timeString = getTimeStr()
    templateData = {
        'title' : 'MinkaAire Ceiling Fan',
        'time': timeString,
        'message' : 'Starting up'
    }

    # create a dictionary of remote control options
    # skip for now
    
    # initial version will just show the remote options
    return render_template( 'main.html', **templateData )

@app.route('/toggle_light')
def toggle_light():
    mr.toggle_light()
    templateData = {
        'title' : 'MinkaAire Ceiling Fan',
        'time': getTimeStr(),
        'message' : 'Toggled light'
    }
    # initial version will just show the remote options
    return render_template( 'main.html', **templateData )
    
@app.route('/fan_off')
def fan_off():
    mr.fan_off()
    templateData = {
        'title' : 'MinkaAire Ceiling Fan',
        'time': getTimeStr(),
        'message' : 'Set fan off'
    }
    # initial version will just show the remote options
    return render_template( 'main.html', **templateData )

@app.route('/fan_low')
def fan_low():
    mr.fan_low()
    templateData = {
        'title' : 'MinkaAire Ceiling Fan',
        'time': getTimeStr(),
        'message' : 'Set fan low'
    }
    # initial version will just show the remote options
    return render_template( 'main.html', **templateData )

@app.route('/fan_med')
def fan_med():
    mr.fan_med()
    templateData = {
        'title' : 'MinkaAire Ceiling Fan',
        'time': getTimeStr(),
        'message' : 'Set fan medium'
    }
    # initial version will just show the remote options
    return render_template( 'main.html', **templateData )

@app.route('/fan_high')
def fan_high():
    mr.fan_high()
    templateData = {
        'title' : 'MinkaAire Ceiling Fan',
        'time': getTimeStr(),
        'message' : 'Set fan high'
    }
    # initial version will just show the remote options
    return render_template( 'main.html', **templateData )

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
