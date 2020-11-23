"""
run the minka-aire ceiling fan with a configurable cycle

Usage:
  minka_remote.py [ON] [OFF]

Arguments:
  ON   time on in secconds [600]
  OFF  time off in seconds [3000]

"""
from __future__ import print_function

import datetime
import time

from mar import MinkaAireRemote

from docopt import docopt

if __name__=='__main__':

    args = docopt(__doc__)

    time_on = args['ON']
    time_off = args['OFF']

    if time_on is None: time_on = 600 else int(time_on)
    if time_off is None: time_off = 3000 else int(time_off)

    print('on for {0} seconds, off for {1} seconds'.format(time_on,time_off))
    
    mr = MinkaAireRemote()

    while True:
        # set fan on low for 10 minutes
        print( str(datetime.datetime.now()) + ' : Setting fan to low' )
        mr.fan_low()
        time.sleep( time_on )

        # set fan off for 50 minutes
        print( str(datetime.datetime.now()) + ' : Setting fan to off' )
        mr.fan_off()
        time.sleep( time_off )

        # repeat, etc.
