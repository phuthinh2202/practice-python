#!/usr/bin/env python
import os
import zipfile
import datetime
from mediafire import (MediaFireApi, MediaFireUploader)

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':

    api = MediaFireApi()
    session = api.user_get_session_token(
        email='your.email@example.net',
        password='password',
        #app_id='42511'
        )

    now = datetime.datetime.now()
    backup_file = now.year + now.month + now.day + '_' + '.zip'
    zipf = zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED)
    zipdir('/home/centos', zipf)
    zipf.close()

    uploader = MediaFireUploader(api)
    # ... authenticate ...
    fd = open(backup_file, 'rb')
    result = uploader.upload(fd, backup_file,
                         folder_key='backup')
