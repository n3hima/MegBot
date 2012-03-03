##
# will change before 0.06 is released
##


networks = {
	"MegNet":{
		"address":"irc.megworld.co.uk",
		"port":9000,
		"nick":"",
		"ident":"",
		"realname":"MegTest",
		"ipv6":False,
		"ssl":True,
		"trigger":"",
		"NSPassword":"",
		"commands":[],
		"modes":["b"],
		"channels":[]
	},
	"Freenode":{
		"address":"irc.freenode.net",
		"port":6667,
		"nick":"",
		"ident":"",
		"realname":"",
		"trigger":"",
		"ipv6":False,
		"ssl":False,
		"NSPassword":"pass",
		"commands":[],
		"modes":["b"],
		"channels":[],
		"active":False #optional (if set to false will disable this network from connecting.)
	}
}

permissions = {
	"~":"founder",
	"&":"sop",
	"@":"aop",
	"%":"hop",
	"+":"vop"
}

paths = {
	"plugin":"Plugins/",
	"coreplugins":"CorePlugins/",
	"logs":"Logging/",
	"databases":"Databases/",
	"libraries":"Libraries/"
}
