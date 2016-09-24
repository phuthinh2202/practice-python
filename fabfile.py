#!/usr/bin/python
# Description: Fabric practice 
# Author: Lis
"""
Usage:
- fab -H [name_server] deploy:nginx=True,php=True,mariadb=True,galera=True,my_level='medium'
"""
from fabric.api import *

env.hosts = ['localhost']
env.user = 'root'
env.password = 'ABC@123'
env.port = 22
#env.use_ssh_config = True
env.key_filename = ['/home/keys/prikey.pem']

def update_os():
   run('yum update -y')

def setup_nginx():

    print "Uploading nginx.repo ..."
    # Add nginx.repo
    upload_repo = put('yum.repos.d/nginx.repo', '/etc/yum.repos.d/nginx.repo')
    if upload_repo.succeeded:
	print "Upload succeeded."
  
        # Install Nginx 1.10
        run('yum install -y nginx')
        run('rm -rf /etc/nginx/nginx.conf')
        run('mkdir -p /etc/nginx/{sites-available,sites-enabled}')

    
    # Upload nginx.conf and Vhost
    upload_nginx_conf = put('config/nginx.conf', '/etc/nginx/nginx.conf')
    upload_vhost_template = put('template/vhost_template.conf', '/etc/nginx/sites-available/vhost_template.conf')

    # Create symlink vhost
    if upload_nginx_conf.succeeded and upload_vhost_template.succeeded:
        print "Upload vhost and nginx.conf succeeded. Create symlinks vhost ..."
    	run('ln -s /etc/nginx/sites-available/vhost_template.conf /etc/nginx/sites-enabled/vhost_template.conf')

    run('service nginx restart')

def setup_php():
    #run('rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm')
    upload_remi_repo = put('yum.repos.d/remi.repo', '/etc/yum.repos.d/remi.repo')

    if upload_remi_repo.succeeded:
    	run('yum install -y php-opcache php php-fpm php-mysql php-intl php-mcrypt php-gd')

    	# Config pool www in php-fpm
    	run('rm -rf /etc/php-fpm.d/www.conf')
    	upload_www_conf = put('config/www.conf', '/etc/php-fpm.d/www.conf')
    	if upload_www_conf.succeeded:
		print "Upload www.conf successfully."
		run('service php-fpm restart')


def setup_mariadb(galera=False, my_level='medium'):
   
    print "Upload MariaDB repo ..."
    upload_mariadb_repo = put('yum.repos.d/MariaDB.repo', '/etc/yum.repos.d/MariaDB.repo')

    if upload_mariadb_repo.succeeded:
        print "Upload successfully ..."
        if galera:
            run('yum install -y MariaDB-server MariaDB-client galera')
        else:
            run('yum install -y MariaDB-Galera-server MariaDB-client')

	run('rm -rf /etc/my.cnf')
        if my_level == 'medium':
   	    run('cp /usr/share/mysql/my-medium.cnf /etc/my.cnf')
	elif my_level == 'large':
     	    run('cp /usr/share/mysql/my-large.cnf /etc/my.cnf')
	elif my_level == 'small':
	    run('cp /usr/share/mysql/my-small.cnf /etc/my.cnf')
	
	run('service mysql restart')

def deploy(nginx=True, php=True, mariadb=False, galera=False, my_level='medium'):

    if nginx:
    	setup_nginx()
	print "test"

    if php:
	setup_php()

    if mariadb:
	setup_mariadb(galera, my_level)

    print "TEST"
