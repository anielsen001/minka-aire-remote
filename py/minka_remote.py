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

import sys
USEGPIO = False

def main(time_on, time_off, fan_speed):
    
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

def main_file(filename):
    """
    run the main with a filename argument
    """
    time_on, time_off, fan_speed = parse_file(filename)
    main(time_on, time_off, fan_speed)

def parse_file(filename):
    with open(filename) as f:
        fan_speed = f.readline().strip()
        time_on = int(f.readline().strip())
        time_off = int(f.readline().strip())
    return time_on, time_off, fan_speed

    
if __name__=='__main__':

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
    
    


