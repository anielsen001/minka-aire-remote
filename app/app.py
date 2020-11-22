from flask import Flask, render_template, Response, request
import sys
import os
import threading
import time
import logging

app = Flask(__name__)

keys = ['Mode','on_for','off_for']

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
            f.write(str(value))
    #Done with writing


def opendata(fan_status={}, outdata='fan_status.txt'):
    with open(outdata, 'r') as f:
        for k in keys:
            fan_status[k]=[f.readline()]
    return fan_status




@app.route("/", methods=['POST'])
def main_button():
    #Moving forward code
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
    # Fan Threading
    #at = threading.Thread(target=mfam.main, args=(float(h),))
    # at.start()
    return render_template('main.html', fan_status=fan_status)


if __name__ == "__main__":
    app.run()



'''



{% if data %}
<p>{{data}}</p>
{% endif %}

'''
