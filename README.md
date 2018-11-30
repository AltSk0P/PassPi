# [ARCHIVED] Sign-In App

**This repository is no longer maintained.**

This application was developed for Schreiner University STEM Department to use as a sign-in / sign-out system. It was intended to be installed on a Raspberry Pi device with a connected barcode scanner.

##App requirements:
- Students and faculty have to be able to scan their IDs when signing in or out. If they're signing in, allow them to choose a reason for sign-in from a list.
- The records have to be saved in a sqlite database, which would then need to be converted to a comma delimited format and sent to a STEM department email address for data analysis purposes.

##Files Breakdown:
[check_wlan.sh](check_wlan.sh) - Is called by crontab after a reboot to make sure that the wireless adapter is functioning (sometimes it doesn't work after startup, so this additional check is required). Pi then reboots if the wi-fi is malfunctioning.
[cpl.py](cpl.py) - Main Python file which acts as a front-end of the system. Is ran immediately after a Pi startup by crontab.
[db2csv.sh](db2csv.sh) - Helper script which converts the database into the csv file that can later be sent out.
[journal.csv](journal.csv) - database file in comma delimited format (Repository contains an example of what data it could contain)
[locale](locale) - Contains custom greeting and goodbye lines for the GUI to display.
[mail_run.sh](mail_run.sh) - contains calls to [send.py](send.py) with different email addresses as parameters. Called on schedule to send out the [journal.csv](journal.csv)
[send.py](send.py) - a python script to send a gmail
[pw](pw) - file which should contain a password for a gmail account of the Pi

November 2017