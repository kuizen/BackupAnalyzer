#!/usr/bin/env python3

from stat import S_ISREG, ST_CTIME, ST_MODE
import os,sys,time,re,datetime
import backuplog
import json

def GetTime(seconds):
        sec = datetime.timedelta(seconds=int(seconds))
        d = datetime.datetime(1,1,1,1)+sec
        result = str("%dm %dd %dh %dmin %ds" %(d.month-1, d.day, d.hour, d.minute, d.second))
        return result

#####
#we had duplicates backups, which where made for test purposes. As its not needed to be analyzed, here is black list
ignorelist =  open('ignoredirs.cfg','r').read().splitlines()
def FolderIsInIgnoreList(path):
	for line in ignorelist:
		if re.search(line, path):
			print(path + " is in ignore list " + line)
			return True
	return False
#####

#recursively get dir tree starting from dir_path
def fast_scandir(dir_path):
	subfolders = [f.path for f in os.scandir(dir_path) if f.is_dir()]
	for directory in list(subfolders):
		if not FolderIsInIgnoreList(directory):
			subfolders.extend(fast_scandir(directory))
	return subfolders



def scan_backup(path):
	
	#match for bss naming convention
	list_servers =[]
	for line in fast_scandir(path):
		match = re.search('(kie|lvi)(t|l)\d{1,3}-\w{2,3}-\w{2,3}\d{1,3}.?$',line,re.IGNORECASE)
		if match:
			list_servers.append(line)

	messages = {}
	for dirs in list_servers:
		server_name= os.path.basename(dirs)	
		subfolders = [(os.stat(f.path).st_mtime,f.path) for f in os.scandir(dirs) if f.is_dir() and re.search('.*\/\d{8}_\d{6}\.\d{1,3}',f.path)]
		subfolders.sort(key =lambda x: x[0], reverse = True) #now we sort subfolders for creation datetime parameter or name(should be same) and try get most recent

		if len(subfolders) == 0:
			#some error report that folder is empty
			messages[server_name] = {'level':'ERROR','message':'is empty, no backup found'}
		else:
			if len(subfolders) >= 2:
				backup_interval = subfolders[0][0] - subfolders[1][0]
			else:
				backup_interval = 86400; 		#if there is only 1 backup directory we compare with const value, now its 24h
		
			last_bkp = time.time() - subfolders[0][0]
			if last_bkp > backup_interval:	
                                temp_msg = "backup is too old. Time from last bkp: "+GetTime(last_bkp)+" . Backup interval: "+ GetTime(backup_interval)
				messages[server_name] = {'level':'ERROR', 'message':temp_msg}
			else:
				bac = backuplog.parse_backuplog(subfolders[0][1]+'/backup.log')
				level = ""
				if bac['err_count'] != 0:
					level = 'ERROR'
				elif bac['warn_count'] !=0:
					level = 'WARNING'
				else:
					level = 'INFO'
				messages[server_name] = {'level':level, 'message':'backup folder is up to date, analyzing backup.log: '+json.dumps(bac)}
	return messages	

if __name__ == '__main__':
	path ='/backup'
	for it in scan_backup(path).items():
		source_host = it[0]
		level = it[1].get('level')
		message = it[1].get('message')
		print(level, source_host, message)



