#shell to backup/restone mongo database with json file
import datetime
import json
import os
import sys

def get_arguments():

	args = {}
	for i in range(len(sys.argv)):
		print(sys.argv[i])
		if sys.argv[i].startswith('-'):
			args[sys.argv[i]] = sys.argv[i + 1] if (((i + 1) < len(sys.argv)) and not sys.argv[i + 1].startswith('-')) else sys.argv[i]
		else:
			pass

	return args

def get_databases(serverConfig):
	databases = serverConfig['databases'] if 'databases' in serverConfig else []	
	if type(databases) == type(''):
		return [databases]
	else:
		return databases

def append_arguments(serverArgs, serverConfig):
	#init
	args = ''

	#append server arguments to command
	for arg in serverArgs:
		if arg in serverConfig and serverConfig[arg]:
			format = str.format(' --{} {{', arg) + arg + '}'
			args += str.format(format, **serverConfig)

	return args

args = get_arguments()

# get backup or restore flag, 1 is backup and 0 is restore mode
backup_or_restore = 1 if len(({'-r', '-restore'} & args.keys())) == 0 else 0

#get the path of configuration, default is config.json
configFile = args['-config'] if '-config' in args else 'config.json'

#read json configuration file
f = open(configFile, 'r')
config = json.load(f);

#get server item and prase server arguments.
serversConfig = config['servers'] if 'servers' in config else {}
serverArgs = serversConfig['arguments'] if 'arguments' in serversConfig else ['host', 'port']


#if server target item doesn't exist, it see use one server to backup and restore
serverSource = serversConfig['source'] if 'source' in serversConfig else [];
serverTarget = serversConfig['target'] if 'target' in serversConfig else serverSource;

#create backup/restore command
command = ''
programs = config['programs']
if backup_or_restore == 1:	# 1 is backup
	command = programs['dump']
	command += append_arguments(serverArgs, serverSource)
else:						# 0 is restore
	command = programs['restore']
	command += append_arguments(serverArgs, serverTarget)

out_dict = {'$today': datetime.datetime.now()}
databaseSource = get_databases(serverSource)
databaseTarget = get_databases(serverTarget)

for i in range(len(databaseSource) if backup_or_restore == 1 else len(databaseTarget)):

	shell = ''
	if backup_or_restore == 1:
		if len(databaseSource) > i:
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

