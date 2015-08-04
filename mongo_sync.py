#shell to backup/restone mongo database with json file
import datetime
import json
import os
import sys

def get_databases(serverConfig):
	databases = serverConfig['databases'] if 'databases' in serverConfig else []	
	if type(databases) == type(''):
		return [databases]
	else:
		return databases

def append_arguments(serverConfig):
	args = ''
	serverArgs = ['host', 'port', 'username', 'password']
	#append server arguments
	for arg in serverArgs:
		if arg in serverConfig and serverConfig[arg]:
			format = str.format(' --{} {{', arg) + arg + '}'
			args += str.format(format, **serverConfig)

	return args

f = open('mongo-test.json', 'r')
config = json.load(f);

# 1 is backup and 0 is restore mode
backup_or_restore = 1

serverSource = config['servers']['source']
serverTarget = config['servers']['target']

#create backup/restore command
command = ''
programs = config['programs']
if backup_or_restore == 1:	# 1 is backup
	command = programs['dump']
	command += append_arguments(serverSource)
else:						# 0 is restore
	command = programs['restore']
	command += append_arguments(serverTarget)

out_dict = {'$today':datetime.datetime.now()}
databaseSource = get_databases(serverSource)
databaseTarget = get_databases(serverTarget)

for i in range(len(databaseSource)):

	shell = ''
	if backup_or_restore == 1:
		shell = command + str.format(' --db {}', databaseSource[i])
		shell += str.format(' --out {}', str.format(config['output'], **out_dict))
	else:
		if len(databaseTarget) > i:
			shell = command + str.format(' --db {}', databaseTarget[i])
			shell += str.format(' {}\{}\\', str.format(config['output'], **out_dict), databaseSource[i])

	try:
		if shell: print(shell)
		stream = os.popen(shell)
	except err:
		print(format(err))

