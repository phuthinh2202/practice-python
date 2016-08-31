#!/usr/bin/python
# author: Lis
# description: For practice python
import paramiko, argparse, sys, os
import requests
import datetime

parser = argparse.ArgumentParser(description='For monitor service on remote server')
parser.add_argument('-u', '--username', help='Username', required=True)
parser.add_argument('-p', '--password', help='Password', required=False)
parser.add_argument('-sm', '--service_monitor', help='Server monitor', required=True)
parser.add_argument('-ipsv', '--ipserver', help='IP remote server', required=True)
parser.add_argument('-po', '--port', help='Port SSH server', required=False)
parser.add_argument('-key', '--key_filename', help='Private key for authen', required=False)
parser.add_argument('-w', '--warning', help='Process warning', required=True)
parser.add_argument('-c', '--critical', help='Process critical', required=True)
args = parser.parse_args()

#print ("Username: %s" % args.username)
#print ("Password: %s" % args.password)
#print ("Server monitor: %s" % args.service_monitor)
#print ("Port SSH: %s" % args.port)
#print ("Path private key: %s" % args.key_filename)
#print ("Remote server: %s" % args.ipserver)
#print ("Warning: %s" % args.warning)
#print ("Critical: %s" % args.critical)

# Init SSHClient
#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Init params
if args.port is None:
    port = 22
else:
    port = int(args.port)
server = args.ipserver
username = args.username
service = args.service_monitor
proc_warning = int(args.warning)
proc_critical = int(args.critical)

# Using Paramiko library SSH to remote server 
#if args.password is None:
#    prikey = paramiko.RSAKey.from_private_key_file(args.key_filename)
#    ssh.connect(server, port=port, username=username, pkey=prikey)
#else:
#    password = args.password
#    ssh.connect(server, port=port, username=username, password=password)
#command = "pgrep " + service + "|wc -l"
#stdin, stdout, stderr = ssh.exec_command(command)
#proc_running =  int(stdout.read())

#if proc_running < proc_warning:
#    status = 'OK'
#elif proc_running > proc_warning and proc_running < proc_critical:
#    status = 'WARNING'
#else:
#    status = 'CRITICAL'

#print ("%s %s - process running: %d" % (service, status, proc_running))
#print stdout.read()
#print ("Process running of %s: %s" % (service, proc))

#ssh.close()

# Request URL to GET service status
url = 'http://' + server + '/status?json'
r = requests.get(url)
data = r.json()

def nagios_exit(nick_name, status, messages, infoData, perfData):
    print ("%s %s %s - %s | %s" % (nick_name, status, messages, infoData, perfData))

infoData = "Pool: %s, Start time: %s, Busy/Idle: %s/%s" % (data['pool'], datetime.datetime.fromtimestamp(data['start time']).strftime('%d-%m-%Y %H:%M:%S'), data['active processes'], data['idle processes'])
perfData = "Idle: %s, Active: %s, Accepted conn: %s" % (data['idle processes'], data['active processes'], data['accepted conn'])
if r.status_code == 200:
    if data['total processes'] < args.warning:
        nagios_exit(service, "OK", "", infoData, perfData)
    elif data['total processes'] > args.warning and data['total processes'] < args.critical:
        nagios_exit(service, "WARNING", "Process running is WARNING", infoData, perfData)
    elif data['total processes'] > args.critical:
        nagios_exit(service, "CRITICAL", "Process running is CRITICAL", infoData, perfData)
else:
    print "NOT FOUND DATA"
