#!/usr/bin/python3
 
import MySQLdb
import os
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
 
user='xyz'
passwd='abc'
host='localhost'
 
#! Mail authentication for sending attachment to administrator
gmail_user = "admin@example.com"
gmail_pwd = "123456"
filestamp = time.strftime('%Y-%m-%d')
conn = MySQLdb.connect (host, user, passwd)
 
cursor = conn.cursor()
 
cursor.execute("SHOW DATABASES")
 
results = cursor.fetchall()
cursor.close()
conn.close()
 
for result in results:
    if result[0] == 'MAP':
            backupfile=result[0]+ "_"+ filestamp + ".sql.gz"
            cmd="echo 'Back up "+result[0]+" database to /Backup/"+backupfile+"'"
            os.system(cmd)
            cmd="mysqldump -u "+user+" -h "+host+" -p"+passwd+"  "+result[0]+" | gzip -9 --rsyncable > /Backup/"+backupfile
            os.system(cmd)
 
#! Send email method
 
def mail(to, subject, text, attach):
  msg = MIMEMultipart()
 
  msg['From'] = gmail_user
  msg['To'] = to
  msg['Subject'] = subject
 
  msg.attach(MIMEText(text))
 
  part = MIMEBase('application', 'octet-stream')
  part.set_payload(open(attach, 'rb').read())
  Encoders.encode_base64(part)
  part.add_header('Content-Disposition',
          'attachment; filename="%s"' % os.path.basename(attach))
  msg.attach(part)
 
  mailServer = smtplib.SMTP("mail.abc.com", 25)
  mailServer.ehlo()
  mailServer.starttls()
  mailServer.ehlo()
  mailServer.login(gmail_user, gmail_pwd)
  mailServer.sendmail(gmail_user, to, msg.as_string())
  # Should be mailServer.quit(), but that crashes...
  mailServer.close()
 
title = filestamp + " Backup File HAN MAP database!"
mail("destinationEmail@abc.com",
  title,
  "Hello. Please refer to attachment about database backup",
  backupfile)
