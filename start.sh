#!/bin/sh

export WRKDIR=/home/pi/proj/minka-aire-remote
. $WRKDIR/bin/activate
python3 $WRKDIR/app/app.py 
