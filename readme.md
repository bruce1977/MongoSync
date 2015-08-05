## OverView

This is simply python script to backup/restore mongodb with json config

## Usage

To backuo database we can use following syntax 
> python mongo_sync.py -config config.json

or restore a database
> python mongo_sync.py -r -config config.json


Arguments

- -config configfile
It use named configuration file that include server and mongo program info

- -restore or -r
This flag used for restore mode, default is backup mode

JSON format
``` javascript
{
	"servers":{
		//Used server arguments in command line
		"arguments":["host", "port", "username", "password"],	
		//The source mongodb server used for backup
		"source":{												
			"host": "xxx.xxx.xxx.xxx",
			"port": "27017",
			"username": "",
			"password":"",
			"databases":["db1", "db2"]
		},
		//The target mongodb server used for restore.
		//It will use source server item for restore if it doesn't exist.
		"target":{												
			"host": "xxx.xxx.xxx.xxx",							
			"port": "27017",
			"username": "",
			"password":"",
			"databases":"db1"
		}
	},
	//This script use mongodump and mongorestore to backup/restore, We must set the program path of them
	"programs":{										
		"dump":"...\\mongodb\\mongodump.exe",
		"restore":"...\\mongodb\\mongorestore.exe"
	},
	//Output folder backup/restore, it support date flag
	"output":"..\\backup\\{$today:%Y%m%d}\\"
}
```
