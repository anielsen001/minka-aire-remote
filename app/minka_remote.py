"""
run the minka-aire ceiling fan with a configurable cycle

Usage:
  minka_remote.py [ON] [OFF]
  minka_remote.py --file=FILE

Arguments:
  ON   time on in secconds [600]
  OFF  time off in seconds [3000]

Options:
  --file=FILE  file with fan configuration settings

"""
from __future__ import print_function
import datetime
import time
from mar import MinkaAireRemote
from docopt import docopt

import pickle
import sys
USEGPIO = True

mr = MinkaAireRemote()


def sleep_check(sleep_time, check_interval, stop=lambda: False):
    """
    sleep for an overall period of time, waking up to check for a 
    stop semaphore to be set, at a given interval
     
    Inputs:
    ======
    sleep_time :: overall time to sleep in seconds
    check_interval :: period before semaphore checking, seconds
    stop :: semaphore function, returns True when time to exit

    Returns:
    =======
    None
    """

    # get initial time when starting
    start_time = time.time()

    while True:
        # check for stop, if present return
        if stop():
            return None

        # sleep for check interval
        time.sleep(check_interval)
        # get current time
        curr_time = time.time()
        # exit criteria is when current time i
        if curr_time - start_time >= sleep_time:
            return None
        
    
def main(time_on, time_off, fan_speed, stop = lambda: False):

    print('{0} on for {1} seconds, off for {2} seconds'.format(fan_speed, time_on, time_off))

    while True:
        # set fan on low for 10 minutes
        print( str(datetime.datetime.now()) + ' : Setting fan to {0}'.format(fan_speed) )
        mr.wakeup()
        mr.fan(fan_speed)
        sleep_check( time_on, 1, stop )

        # after waking from sleep, see if we should stop
        if stop():
            print('thread exiting')
            break

        # set fan off for 50 minutes
        print( str(datetime.datetime.now()) + ' : Setting fan to off' )
        mr.fan_off()
        mr.sleep()
        sleep_check( time_off, 1, stop )

        # after waking from sleep, see if we should stop
        if stop():
            print('thread exiting')
            break

        # repeat, etc.


def change_light(fan_status):
    mr.wakeup()
    mr.toggle_light()
    mr.sleep()
    time.sleep(2)




def main_file(filename, stop):
    """
    run the main with a filename argument
    """
    time_on, time_off, fan_speed, fan_status = parse_file(filename)
    if fan_status["change_light"]:
        change_light(fan_status)
    main(time_on, time_off, fan_speed, stop = stop)


def parse_file(filename):
    with open(filename, 'rb') as f_pickle:
        fan_status = pickle.load(f_pickle)
    fan_speed = fan_status["fan_mode"]
    time_on = int(fan_status["on_for"])*60
    time_off = int(fan_status["off_for"])*60
    if int(time_on) == 0 and int(time_off) == 0:
        # Adding a buffer so this loop does not speed out of control.
        time_off = 2 * 60
    return time_on, time_off, fan_speed, fan_status

    
if __name__ == '__main__':

    args = docopt(__doc__)

    time_on = args['ON']
    time_off = args['OFF']

    if time_on is None:
        time_on = 600
    else:
        time_on = int(time_on)
    if time_off is None:
        time_off = 3000
    else:
        time_off = int(time_off)

    if not args['--file'] is None:
        setfile = args['--file']
        print('using configfile {0}'.format(setfile))
        time_on, time_off, fan_speed = parse_file(setfile)

    print('on for {0} seconds, off for {1} seconds'.format(time_on,time_off))

    if not USEGPIO:
        sys.exit()

    main(time_on, time_off, fan_speed)
    
    


