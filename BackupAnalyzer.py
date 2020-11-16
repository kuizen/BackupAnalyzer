#!/usr/bin/env python3

import syslog_handler
import get_subdirs
import time

path ='/backup'
syslog = '192.168.224.74'

messages = get_subdirs.scan_backup(path)
for it in messages.items():
	source_host = str(it[0])
	level = str(it[1].get('level'))
	message = str(it[1].get('message'))

	print(level, source_host, message)
	syslog_handler.send_syslog(syslog,514,level, source_host,message)
	time.sleep(2)
