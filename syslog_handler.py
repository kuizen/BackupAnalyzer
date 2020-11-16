#!/usr/bin/env python3

import logging, logging.handlers, platform

import sys
import io
import os


#host = '192.168.224.74'
#port = 514
#hname = 'kiet-test1-k2'

def send_syslog(syslogserver,port,level, source_host, message):
	logger = logging.getLogger()
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
	hname = 'testing-messages'
	send_syslog(h,port,'WARNING',hname,'lets test that all works fine')
