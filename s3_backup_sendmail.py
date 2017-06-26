#!/usr/bin/env python3
## Author: ThinhLP || Email: phuthinh2202@gmail.com

import os
import zipfile
import datetime
import boto
import boto.s3
import sys
from boto.s3.key import Key
from boto.s3.bucket import Bucket
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':

    now = datetime.datetime.now()
    backup_file = "backup_%s%s%s.zip" % (now.year,now.month,now.day)
    print ('-------- Backup Processing -------')
    print ('Backup filename: %s' % backup_file)
    zipf = zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED)
    zipdir('/data', zipf)
    zipf.close()
    print ('-------- Backup finished -------')
    #print ('-------- Upload processing ------')

    AWS_ACCESS_KEY_ID = 'Your_AWS_ACCESS_KEY_ID'
    AWS_SECRET_ACCESS_KEY = 'Your_AWS_SECRET_ACCESS_KEY'

    bucket_name = 'YOUR_BUCKET_NAME'
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    bucket = conn.get_bucket(bucket_name, validate=True)

    k = Key(bucket)
    k.key = 'YOUR_BUCKET_KEY'

    # Delete old backup file
    print ("---------------- Delete old backup file ----------")
    b = Bucket(conn, bucket_name)
    b.delete_key(k)
    time.sleep(2)
    # Upload new backup file
    print ("--------------- Upload new backup file -----------")
    k.set_contents_from_filename(backup_file)
    print ('------- Upload finished ----------')
    
    # Send mail
    gmailUser = 'your_email@gmail.com'
    gmailPassword = 'your_password'
    recipient = 'recipient_email@gmail.com'
    title = 'Finish backup file to S3 AWS'
    message = 'Finish backup filename: %s to S3 AWS' % (backup_file)

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = title
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()
    print ("Mail sent")
