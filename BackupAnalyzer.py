#!/usr/bin/env python3

import syslog_handler
import get_subdirs
import time
import rmc
from datetime import datetime

##NFS scan config
path ='/mnt/auto/StoreOnce-NFS/'


##Remote syslog server
syslog = '10.29.101.11'

## RMC config section
rmc_servers = [ "###-rmc1", "###-rmc2" ]
login = "libre"
password = "####"
##

def send_messages(messages):
    for item in messages:
        source_host, level ,message = item
        print(level, source_host, message)
        syslog_handler.send_syslog(syslog,48654,level, source_host,message) #48654 - port on which librenms_syslog listens

def main():
    nfs_messages = get_subdirs.scan_backup(path)
    send_messages(nfs_messages)
    print("NFS Done ---------------------------------------------------------------")

    for source_host in rmc_servers:
        rmc_errors = rmc.get_failed_tasks(source_host, login, password)
        send_messages(rmc_errors)
    print("RMC done ---------------------------------------------------------------")

    dt = datetime.now.strftime("%d/%m/%Y %H:%M:%S")
    print("Backup Analyze ended at: " + dt)
    return True

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bye-Bye...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
