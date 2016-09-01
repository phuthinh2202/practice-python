#!/usr/bin/python
# Description: Fabric practice 
# Author: Lis
from fabric.api import *

env.hosts = ['web_server', 'localhost']
env.user = 'root'
env.port = 7878
#env.use_ssh_config = True
env.key_filename = ['/home/keys/prikey.pem']

def update_os():
   run('yum update -y')

def setup_nginx():

    print "Uploading nginx.repo ..."
    # Add nginx.repo
    upload_repo = put('nginx.repo', '/etc/yum.repos.d/nginx.repo')
    if upload_repo.succeeded:
	print "Upload succeeded."
    
    # Update OS
    update_os()
  
    # Install Nginx 1.10
    run('yum install -y nginx')


def setup_php():
    run('rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm')
    run('yum --enablerepo=remi,remi-php56 install -y php-opcache php php-fpm php-mysql php-intl php-mcrypt php-gd')
