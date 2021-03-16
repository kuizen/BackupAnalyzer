#!/usr/bin/env python3
import io
import re
import os
import json
import sys

def parse_backuplog(logfile):
        version = 1
        warning = []
        error = []
        last_msg =""

        if not os.path.isfile(logfile):
                error.append(logfile +' not a file')
        elif os.stat(logfile).st_size == 0:
                error.append(logfile + ' is empty')
        else:

                with io.open(logfile,'r') as f:
                        for line in reversed(list(f)):
                                match = re.search('^(error|warning):(\w+):(.*)', line, re.IGNORECASE)
                                if match:
                                        if match.group(1).upper() == 'ERROR':
                                                error.append(match.group(3))
                                        if match.group(1).upper() == 'WARNING':
                                                warning.append(match.group(3))
        if len(error) != 0 :
                last_msg = error[0]
        elif len(error) == 0 and len(warning) != 0:
                last_msg = warning[0]
        else:
                last_msg = " check OK"
        output = {'err_count':len(error),'warn_count':len(warning),'last_msg': last_msg}
#       return json.dumps(output)
        return output

if __name__ == '__main__':
        if len(sys.argv) < 2:
                exit('file path is needed as argument')
        print(parse_backuplog(sys.argv[1]))
