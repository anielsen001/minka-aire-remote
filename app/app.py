from flask import Flask, render_template, Response, request, session
import sys
import os
import threading
import time
import logging
import socket
import pickle
import minka_remote

app = Flask(__name__)

fan_status_file = "/home/pi/proj/minka-aire-remote/fan_status.pickle"
stop_thread = True
PERMANENT_SESSION_LIFETIME = 180


@app.route('/popsession')
def popsession():
    session.pop('Username', None)
    return "Session Deleted"


def test(h, stop):
    while True:
        time.sleep(.5)
        print("Now on ", h)
        if stop():
            break


def get_ip():
    """
    find the primary IP address of the machine we are running on and 
    return as a string

    will return 127.0.0.1 (locahost) if none is found
    """
    # from here:
    # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


@app.route("/")
def main():
    fan_status = opendata()
    return render_template('main.html', fan_status=fan_status)


def savedata(fan_status={}, outdata=fan_status_file):
    keys = ['Mode', 'on_for', 'off_for', 'change_fan', 'change_light', 'light']
    with open(outdata, 'wb') as f_pickle:
        pickle.dump(fan_status, f_pickle, protocol=pickle.HIGHEST_PROTOCOL)


def opendata(fan_status={}, outdata=fan_status_file):
    try:
        with open(outdata, 'rb') as f_pickle:
            fan_status = pickle.load(f_pickle)
    except FileNotFoundError:
        fan_status = {'on_for': "0", 'off_for': "30", "fan_mode": "OFF"}
        savedata(fan_status)
    return fan_status


@app.route("/", methods=['POST'])
def main_button():
    global at
    global stop_thread
    #print(request.form)
    button = request.form.to_dict(flat=False)
    fan_status = opendata()
    fan_status["change_fan"] = False
    fan_status['change_light'] = False
    print(button)
    if 'light_on' in button:
        fan_status['change_light'] = True
        fan_status["light"] = True
    elif 'light_off' in button:
        fan_status['change_light'] = True
        fan_status["light"] = False
    elif "fan_modebtn" in button:
        fan_status['change_fan'] = True
        fan_status['on_for'] = button['on_for'][0]
        fan_status['off_for'] = button['off_for'][0]
        fan_status['fan_mode'] = button['fan_mode'][0]
    savedata(fan_status)
    try:
        stop_thread = True
        at.join()
    except:
        print("No thread")
    # Fan Threading
    stop_thread = False
    at = threading.Thread(target=minka_remote.main_file, args=(fan_status_file, lambda : stop_thread))
    at.start()
    return render_template('main.html', fan_status=fan_status)


if __name__ == "__main__":
    app.run(host=get_ip(), port=5342)



'''



{% if data %}
<p>{{data}}</p>
{% endif %}

'''
