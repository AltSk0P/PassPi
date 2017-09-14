#!/usr/bin/python
import os, re
import sys
import smtplib
import base64

# from email.mime.image import MIMEImage
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

sender = 'supasspi@gmail.com'
with open('pw') as f:
   #password = "".join(map(chr, decode_base64(f.read())))
   password = f.read()

recipient = sys.argv[1]
subject = ''
message = sys.argv[3]


def main():
    msg = MIMEMultipart()
    msg['Subject'] = sys.argv[2]
    msg['To'] = recipient
    msg['From'] = sender

    part = MIMEText('text', "plain")
    part.set_payload(message)
    msg.attach(part)

    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)

    session.ehlo()
    session.starttls()
    session.ehlo

    session.login(sender, password)

    fp = open(sys.argv[4], 'rb')
    msgq = MIMEBase('audio', 'audio')
    msgq.set_payload(fp.read())
    fp.close()
    # Encode the payload using Base64
    encoders.encode_base64(msgq)
    # Set the filename parameter
    filename = sys.argv[4]
    msgq.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(msgq)
    # Now send or store the message
    qwertyuiop = msg.as_string()

    session.sendmail(sender, recipient, qwertyuiop)

    session.quit()
    print('notify-send "Email sent"')


if __name__ == '__main__':
    main()