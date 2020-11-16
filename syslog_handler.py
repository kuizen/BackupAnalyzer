#!/usr/bin/env python3

import logging, logging.handlers, platform

import sys
import io
import os


#host = '192.168.224.74'
#port = 514
#hname = 'kiet-test1-k2'

def send_syslog(syslogserver,port,level, source_host, message):
	logger = logging.getLogger(source_host)
	syslog = logging.handlers.SysLogHandler(address=(syslogserver,port))
	logger.addHandler(syslog)
	#"$HOST||$FACILITY||$PRIORITY||$LEVEL||$TAG||$R_YEAR-$R_MONTH-$R_DAY $R_HOUR:$R_MIN:$R_SEC||$MSG||$PROGRAM\n
	if level == 'ERROR':
		logger.error(source_host +" "+ message)
	elif level == 'WARNING':
		logger.warn(source_host +" "+ message)
	else:
		logger.info(source_host +" "+ message)

if __name__ == '__main__':
	h = '192.168.224.74'
	port = 514
	hname = 'kiet2-cs-sdp1a'
	message = 'backup folder is up to date, analyzing backup.log: {"version": 1, "error_count": 2, "warnings_count": 3}'
	send_syslog(h,514,'WARNING',hname,message)
