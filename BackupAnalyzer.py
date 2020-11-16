#!/usr/bin/env python3

import syslog_handler
import get_subdirs
import time

path ='/backup'
syslog = '192.168.224.74'

messages = get_subdirs.scan_backup(path)
for item in messages.items():
	source_host = str(item[0])
	level = str(item[1].get('level'))
	message = str(item[1].get('message'))

	print(level, source_host, message)
	syslog_handler.send_syslog(syslog,514,level, source_host,message)
