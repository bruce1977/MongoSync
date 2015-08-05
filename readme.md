## OverView

This is simply python script to backup/restore mongodb with json config

## Usage

To backuo database we can use following syntax 
> python mongo_sync.py -config config.json

or restore a database
> python mongo_sync.py -r -config config.json


Arguments
-config configfile


-restore or -r
run 

JSON format
``` javascript
{
	"servers":{
		"arguments":["host", "port", "username", "password"],	//Used server arguments in command line
		"source":{												//The source mongodb server used for backup
			"host": "xxx.xxx.xxx.xxx",
			"port": "27017",
			"username": "",
			"password":"",
			"databases":["db1", "db2"]
		},
		"target":{												//The target mongodb server used for restore.
			"host": "xxx.xxx.xxx.xxx",							//It will use source server item for restore if it doesn't exist.
			"port": "27017",
			"username": "",
			"password":"",
			"databases":"db1"
		}
	},
	"programs":{											//This script use mongodump and mongorestore to backup/restore
		"dump":"...\\mongodb\\mongodump.exe",				//We must set the program path of them
		"restore":"...\\mongodb\\mongorestore.exe"
	},
	"output":"..\\backup\\{$today:%Y%m%d}\\"				//Output folder backup/restore, it support date flag
}
```