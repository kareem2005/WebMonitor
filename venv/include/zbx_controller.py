from pyzabbix import ZabbixAPI
from include.logger import sendToLogger


class ZabbixController():

    def __init__(self, zbx_url, zbx_user, zbx_pass, zbx_wmhostname, zbx_wmgroup):
        self.zbx_url = zbx_url
        self.zbx_user = zbx_user
        self.zbx_pass = zbx_pass
        self.zbx_wmhostname = zbx_wmhostname
        self.zbx_wmgroup = zbx_wmgroup
        self.wmhost_id = 0
        self.zapi = self.__createConnection()

    def addToMonitor(self, domain_list):
        if self.__checkWmHost():
            self.__checkDomainMonitor(domain_list)
        else:
            self.__createWmHost()
            self.__checkWmHost()
            self.__checkDomainMonitor(domain_list)

    def __checkDomainMonitor(self, domain_list):
        domain_list = domain_list.split()
        for domain in domain_list:
            print(self.__isDomainMonitorCreated(domain))
            print(domain)
     #       self.__createDomainMonitor(domain)

    def __isDomainMonitorCreated(self, domain):
        print(domain)
        return self.zapi.httptest.get(
            {
                "name": domain,
                "hostids": self.wmhost_id
            }
        )

    def __createDomainMonitor(self, domain, protocol, status_code, phrase):
        self.zapi.httptest.create(
            {
                "name": domain,
                "hostid": self.wmhost_id,
                "steps": [
                    {
                        "name": domain,
                        "url": protocol + "://" + domain,
                        "status_codes": status_code,
                        "no": 1,
                        "required": phrase
                    }
                ]
            }
        )
        print(self.wmhost_id)

    def __createConnection(self):
        sendToLogger('debug', 'Connecting to zabbix-server on ' + str(self.zbx_url))
        try:
            zapi = ZabbixAPI(self.zbx_url)
            zapi.login(self.zbx_user, self.zbx_pass)
            sendToLogger('debug', 'Connected to zabbix-server API Version ' + zapi.api_version())
            return zapi
        except:
            sendToLogger('error', 'Connection to zabbix-server on ' + str(self.zbx_url) + ' failed.')
            exit(2)

    def __checkWmHost(self):
        host_status = 0
        host = self.zapi.host.get(output=["status"], filter={"host": self.zbx_wmhostname}, limit=1)
        try:
            host_status = host[0]['status']
            self.wmhost_id = host[0]['hostid']
        except:
            sendToLogger('debug', 'Web Monitor host not created.')
            return False
        if (host_status == '1' or host_status == '0'):
            sendToLogger('debug', 'Web Monitor host \"' + self.zbx_wmhostname + '\" already created.')
            return True
        else:
            sendToLogger('debug', 'Web Monitor host not created.')
            return False


    def __createWmHost(self):
        group_id = 0
        group = self.zapi.hostgroup.get(filter={"name": self.zbx_wmgroup})
        try:
            group_id = group[0]['groupid']
        except:
            sendToLogger('debug', 'Web Monitor group \"' + self.zbx_wmgroup + '\" creation started.')
            group = self.zapi.hostgroup.create({"name": self.zbx_wmgroup})
            sendToLogger('debug', 'Web Monitor group created with group id = ' + group['groupids'][0])
            group_id = group['groupids'][0]
        if (group_id):
            try:
                sendToLogger('debug', 'Web Monitor host \"' + self.zbx_wmhostname + '\" creation started.')
                self.zapi.host.create({"host": self.zbx_wmhostname,
                                       "groups": [
                                           {
                                               "groupid": group_id
                                           }
                                        ],
                                       "interfaces": [
                                           {
                                               "type": "1",
                                               "main": "1",
                                               "useip": "1",
                                               "ip": "127.0.0.1",
                                               "dns": "",
                                               "port": "10050"
                                           }
                                       ]
                                       })
                sendToLogger('debug', 'Web Monitor host \"' + self.zbx_wmhostname + '\" creation successful.')
            except:
                sendToLogger('error', 'Web Monitor host \"' + self.zbx_wmhostname + '\" creation failed.')

