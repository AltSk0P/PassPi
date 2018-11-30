#!/bin/bash
FOUND=`grep "wlan0" /proc/net/dev`

if  [ -n "$FOUND" ] ; then
echo "Network available."
else
shutdown -r now

exit 0
fi
