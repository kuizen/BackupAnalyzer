#!/usr/bin/env python3

import logging, logging.handlers, platform

import sys
import io
import os

def send_syslog(syslogserver,port,level, source_host, message):
        logger = logging.getLogger(source_host)
        syslog = logging.handlers.SysLogHandler(address=(syslogserver,port))
        logger.addHandler(syslog)
        #"$HOST||$FACILITY||$PRIORITY||$LEVEL||$TAG||$R_YEAR-$R_MONTH-$R_DAY $R_HOUR:$R_MIN:$R_SEC||$MSG||$PROGRAM"
        send_msg = source_host + " " + message
        if level == 'ERROR':
                logger.error(send_msg)
        elif level == 'WARNING':
                logger.warn(send_msg)
        else:
                logger.info(send_msg)

if __name__ == '__main__':
        h = '10.29.97.11'
        port = 48654
        hname = 'DEBUG_MESSAGE'
        message = 'backup folder is up to date, analyzing backup.log: {"version": 1, "error_count": 2, "warnings_count": 3}'
        send_syslog(h,port,'ERROR',hname,message)
