import json
url = 'http://192.168.249.130/zabbix/api_jsonrpc.php'
header= {"Content-Type": "application/json"}
data = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "Admin",
        "password": "zabbix"
    },
    "id": 1,
    "auth": None
}

