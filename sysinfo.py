#!/usr/bin/python

import os
import sigar

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


sg = sigar.open()
mem = sg.mem()
swap = sg.swap()
fslist = sg.file_system_list()
cpu = sg.cpu()

print bcolors.HEADER + "\tTOTAL\tUser\tIdle"
print bcolors.FAIL + "CPU:\t%s\t%s\t%s" % (cpu.total(), cpu.user(), cpu.idle())
print bcolors.HEADER + "==========Memory Information=============="
print bcolors.OKBLUE + "\tTotal\tUsed\tFree"
print bcolors.OKGREEN + "Mem:\t%s\t%s\t%s" % ((mem.total() / (1024*1024)), (mem.used() / (1024*1024)), (mem.free() / (1024*1024)))
print bcolors.OKGREEN + "Swap:\t%s\t%s\t%s" % ((swap.total() / (1024*1024)), (swap.used() / (1024*1024)), (swap.free() / (1024*1024)))
print bcolors.WARNING + "RAM:\t%s" % mem.ram() + "MB"
print bcolors.HEADER + "==========File System Information==============="
def format_size(size):
    return sigar.format_size(size * 1024)
    print 'Filesystem\tSize\tUsed\tAvail\tUse%\tMounted on\tType\n'
for fs in fslist:
    dir_name = fs.dir_name()
    usage = sg.file_system_usage(dir_name)
    total = usage.total()
    used = total - usage.free()
    avail = usage.avail()
    pct = usage.use_percent() * 100
    if pct == 0.0:
    	pct = '-'
    	print fs.dev_name(), format_size(total), format_size(used), format_size(avail), pct, dir_name, fs.sys_type_name(), '/', fs.type_name()

