#-*- coding: utf-8 -*-

import  requests
import sys
from config import base_conf,host_add_temp
import json
reload(sys)

sys.setdefaultencoding('utf-8')
class send_tos():

    @classmethod
    def post_server(cls,data):
        try:
            result = requests.post(url=base_conf.url,data=json.dumps(data),headers=base_conf.header)
        except requests.ConnectionError as e:
            print "\033[041m 认证失败请检查url！\033[0m",e
        except requests.Timeout as e:
            print "\033[041m 连接超时请重试！\033[0m",e
        except KeyError as e:
            print "\033[041m 认证失败请检查密码！\033[0m",e
        else:
          response = result.json()['result']
          result.close()
        return response

class zabbix_api:
    def __init__(self):
        self.url= base_conf.url
        self.header = base_conf.header
        self.autho = base_conf.data

    def user_login(self):
        try:
            result = requests.post(url=self.url,data=json.dumps(self.autho),headers=self.header)
        except requests.ConnectionError as e:
            print "\033[041m 认证失败请检查url！\033[0m",e
        except requests.Timeout as e:
            print "\033[041m 连接超时请重试！\033[0m",e
        except KeyError as e:
            print "\033[041m 认证失败请检查密码！\033[0m",e
        else:
          response = result.json()
          result.close()
          self.authID = response['result']
          print self.authID
          return self.authID
    def get_host_list(self):
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid","name","host"],
                "fileter": {"host": ""}
            },
            "id": 1,
            "auth": self.user_login()
                }
        result = send_tos.post_server(data)
        print result
        print "主机列表如下："
        for host in result:
           #print  host
             print " visible name: {:20}\t host_ID: {:10},host: {} ".format( host['name'],host['hostid'],host["host"])
        return result
    def get_host(self,hostName=None):
        data = {
            "jsonrpc": "2.0",
             "method": "host.get",
             "params": {
              "output": ["hostid","name","host"],
             "filter": {
             "host": hostName.split(',')
                 }
             },
            "auth": self.user_login(),
            "id": 1
        }
        result = send_tos.post_server(data)
        print "主机列表{}".format(result)
        return  result

    def get_host_from_visiblename(self, name=None):
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid", "name","host"],
                "filter": {
                    "name": name.split(',')
                }
            },
            "auth": self.user_login(),
            "id": 1
        }
        result = send_tos.post_server(data)
        print "主机列表{}".format(result)
        return result
    def hostgroup_getall(self):
        data ={"jsonrpc": "2.0",
                "method": "hostgroup.get",
                "params": {
                "output": ["groupid","name"],
                 },
             "auth": self.user_login(),
                 "id": 1}
        result=send_tos.post_server(data)
        #print result
        for hostgroup in result:
            if type(hostgroup["name"]) == 'unicode':
                hostgroup["name"] =  hostgroup["name"].encode('utf-8')
            print "hostgourp_name: {:20} groupid: {}".format(hostgroup["name"],hostgroup["groupid"])
        return  result
    def hostgourp_get(self,groupName=''):
        data = {
            "jsonrpc": "2.0",
             "method": "hostgroup.get",
             "params": {
                "output":  ["groupid","name"],
                "filter": {
                 "name": groupName.split(',')
                         }
                         },
            "auth": self.user_login(),
            "id": 1
                }
        result = send_tos.post_server(data)
        for hostgroup in result:
            if type(hostgroup["name"]) == 'unicode':
                hostgroup["name"] = hostgroup["name"].encode('utf-8')
            print "hostgourp_name: {:20} groupid: {}".format(hostgroup["name"], hostgroup["groupid"])
        #print result
        if result == []:
            print  'have no data'
            return ["no data"]
        return result
    def hostgroup_create(self,groupname=None):
        data ={
            "jsonrpc": "2.0",
            "method": "hostgroup.create",
            "params": {
                "name": groupname
            },
            "auth":self.user_login(),
            "id": 1
                }
        result = send_tos.post_server(data)
        print result
        return result
    def hostgroup_add_host(self,groupname='',host=''):
        for hostgroup in self.hostgourp_get(groupName=groupname):
            if hostgroup == "no data":
                print "groupname  erro"
                return 222
            groupid =hostgroup["groupid"]
            print groupid
            if len(groupid) == 0:
                print "name erro"

        for host in self.get_host(hostName=host):
            hostid = host["hostid"]
            print hostid
        data = {
            "jsonrpc": "2.0",
            "method": "hostgroup.massadd",
            "params": {
                "groups": [
                    {
                        "groupid": groupid
                    }
                ],
                "hosts": [
                    {
                        "hostid": hostid
                    }
                ]
            },
            "auth": self.user_login(),
            "id": 1
            }
        result = send_tos.post_server(data)
        print result
        return result
    def temple_list(self):
        data = {
         "jsonrpc": "2.0",
         "method": "template.get",
         "params": {
             "output": ["name","templateid","host"],
                "filter": {
                    "host": [ ]
                         }
                  },
         "auth": self.user_login(),
         "id": 1
                }
        result = send_tos.post_server(data)
        for temple in result:
            if type(temple["name"]) == 'unicode':
                temple["name"] = temple["name"].encode('utf-8')
            print "visible_name: {:30} templeid: {:10} host:{:10}".format(temple["name"], temple["templateid"],temple["host"])
        return result
    #根据模板名称获取模板
    def temple_get(self,tmple_Name=''):
        data = {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": ["name", "templateid","host"],
                "filter": {
                    "host": tmple_Name.split(',')
                }
            },
            "auth": self.user_login(),
            "id": 1
            }
        result = send_tos.post_server(data)
        for temple in result:
            if type(temple["name"]) == 'unicode':
                temple["name"] = temple["name"].encode('utf-8')
            print "visible_name: {:30} templeid: {:10} host:{:5}".format(temple["name"], temple["templateid"],temple["host"])
        return result
    #根据模板可见名称获取模板
    def temple_visible_name_get(self, tmple_Name=''):
        data = {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": ["name", "templateid", "host"],
                "filter": {
                    "name": tmple_Name.split(',')
                }
            },
            "auth": self.user_login(),
            "id": 1
        }
        result = send_tos.post_server(data)
        for temple in result:
            if type(temple["name"]) == 'unicode':
                temple["name"] = temple["name"].encode('utf-8')
            print "visible_name: {:30} templeid: {:10} host:{:5}".format(temple["name"], temple["templateid"],
                                                                         temple["host"])
        print result
        return result

    def host_create(self,ip= '',host=None,visible_name = '',groupname='',templename=''):
        for hostgroup in self.hostgourp_get(groupName=groupname):
            if hostgroup == "no data":
                print "groupname  erro"
                return 222
            groupid =hostgroup["groupid"]
            print groupid
            if len(groupid) == 0:
                print "name erro"
        for temple in self.temple_visible_name_get(tmple_Name=templename):
            templateid = temple["templateid"]
        data = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": host,
                "name": visible_name + "ip:" + ip,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "dns": "",
                        "port": "10050"
                    }
                ],
                "groups": [
                    {
                        "groupid": groupid
                    }
                ],
                "templates": [
                    {
                        "templateid": 10108

                    }
                ],
                "inventory_mode": 0,
                "inventory": {
                    "macaddress_a": "01234",
                    "macaddress_b": "56768"
                }
            },
            "auth": self.user_login(),
            "id": 1
        }
        result = send_tos.post_server(data)
        print result

zabb = zabbix_api()
for host in host_add_temp.hostlist:
    ip, host, visible_name, groupname, templename = host
    print host
    zabb.host_create(ip,host,visible_name,groupname,templename)
