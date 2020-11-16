#!/usr/bin/env python3
import io
import re
import os
import json
import sys

version = 1
warning = []
error = []

def parse_backuplog(logfile):
	if not os.path.isfile(logfile):
		exit(logfile +' not a file')
 
	with io.open(logfile,'r') as f:
		for line in reversed(list(f)):
			match = re.search('^(error|warning):(\w+):(.*)', line, re.IGNORECASE)
			if match:	
				if match.group(1).upper() == 'ERROR':
					error.append(match.group(3))
				if match.group(1).upper() == 'WARNING':
					warning.append(match.group(3))	
	output = {'version': version,
		  'error_count':len(error),
		'warnings_count':len(warning)}
#	return json.dumps(output)
	return output

if __name__ == '__main__':
	if len(sys.argv) < 2:
		exit('file path is needed as argument')
	print(parse_backuplog(sys.argv[1]))
