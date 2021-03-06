from flask import Flask, render_template, Response, request
import sys
import os
import threading
import time
import logging
import socket

import minka_remote

app = Flask(__name__)
keys = ['Mode','on_for','off_for']

def test(h, stop):
    while True:
        time.sleep(.5)
        print("Now on ",h)
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
    try:
        fan_status = opendata()
    except:
        fan_status={'on_for':"",'off_for':"","Mode":["TBD"]}
    return render_template('main.html', fan_status=fan_status)


def savedata(fan_status={}, outdata='fan_status.txt'):
    with open(outdata,'w') as f:
        for key in keys:
            try:
                value = fan_status[key][0]
            except:
                value = ""
            f.write(str(value)+"\n")
    #Done with writing


def opendata(fan_status={}, outdata='fan_status.txt'):
    with open(outdata, 'r') as f:
        for k in keys:
            fan_status[k]=[f.readline()]
    return fan_status


stop_thread=True
#at = threading.Thread(target=test, args=("Test",lambda : stop_thread) )

@app.route("/", methods=['POST'])
def main_button():
    global at
    global stop_thread
    #print(request.form)
    button = request.form.to_dict(flat=False)
    fan_status = button
    savedata(button)
    print(button)
    if  'on_forBtn' in button:
        #fan_status = mfam.get_sensor_status()

        a = 5
    elif 'off_forBtn' in button:
        #mfam_status = mfam.get_mfam_status()

        message = "Please send data"
        print(message)
    try:
        stop_thread = True
        at.join()
    except:
        print("No thread")
    stop_thread = False
    # Fan Threading
    at = threading.Thread(target=minka_remote.main_file, args=('fan_status.txt',lambda : stop_thread))
    at.start()
    return render_template('main.html', fan_status=fan_status)


if __name__ == "__main__":
    app.run(host=get_ip(), port=5342)



'''



{% if data %}
<p>{{data}}</p>
{% endif %}

'''
