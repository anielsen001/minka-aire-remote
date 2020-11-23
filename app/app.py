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

# create a list of fan controller threads, should be a global
fan_threads=list()

from mar import MinkaAireRemote
mr = MinkaAireRemote()

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

class FanThread(threading.Thread):
    """
    create a fan thread
    """
    def __init__(self, filename):

        time_on, time_off, fan_speed = minka_remote.parse_file(filename)
        
        self.time_on = time_on
        self.time_off = time_off
        self.fan_speed = fan_speed

        self.stop = False

    def run(self):

        time_on = self.time_on
        time_off = self.time_off
        fan_speed = self.fan_speed

        print('{0} on for {1} seconds, off for {2} seconds'.format(fan_speed,time_on,time_off))

        while True:
            # set fan on low for 10 minutes
            print( str(datetime.datetime.now()) + ' : Setting fan to {0}'.format(fan_speed) )
            mr.fan(fan_speed)
            time.sleep( time_on )

            # after sleep, check if stop set, if so, return
            if self.stop:
                return
           
            # set fan off for 50 minutes
            print( str(datetime.datetime.now()) + ' : Setting fan to off' )
            mr.fan_off()
            time.sleep( time_off )        

            # after sleep, check if stop set, if so, return
            if self.stop:
                return


@app.route("/", methods=['POST'])
def main_button():
    #Moving forward code
    #print(request.form) 
    button = request.form.to_dict(flat=False)
    fan_status = button
    savedata(button)
    print(button)

    # stop existing threads, by setting stop flag
    for et in fan_threads:
        et.stop = True
    
    if  'on_forBtn' in button:
        #fan_status = mfam.get_sensor_status()
        a = 5
    elif 'off_forBtn' in button:
        #mfam_status = mfam.get_mfam_status()
        message = "Please send data"
        print(message)
        
    # Fan Threading
    ft = FanThread('fan_status.txt')
    #at = threading.Thread(target=minka_remote.main_file, args=('fan_status.txt',))

    # add the thread to the the fan_threads list
    fan_threads.append(ft)

    # start the thread
    ft.start()

    # return
    return render_template('main.html', fan_status=fan_status)


if __name__ == "__main__":
    app.run(host=get_ip(), port=5342)



'''



{% if data %}
<p>{{data}}</p>
{% endif %}

'''
