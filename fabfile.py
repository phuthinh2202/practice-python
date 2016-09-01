#!/usr/bin/python
# Description: Fabric practice 
# Author: Lis
from fabric.api import *

env.hosts = ['web_server']
env.user = 'root'
env.port = 7878
#env.use_ssh_config = True
env.key_filename = ['/home/keys/prikey.pem']

def ls():
    run('ls -l')
