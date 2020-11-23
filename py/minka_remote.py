from __future__ import print_function
import datetime
import time
from mar import MinkaAireRemote

if __name__=='__main__':

    mr = MinkaAireRemote()

    while True:
        # set fan on low for 10 minutes
        print( str(datetime.datetime.now()) + ' : Setting fan to low' )
        mr.fan_low()
        time.sleep( 600 )

        # set fan off for 50 minutes
        print( str(datetime.datetime.now()) + ' : Setting fan to off' )
        mr.fan_off()
        time.sleep( 50*60 )

        # repeat, etc.
