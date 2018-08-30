from include.logger import sendToLogger


class NginxDomainFinder():

    def __init__(self, nginx_confpath):
        self.nginx_confpath = nginx_confpath

    def getDomainsList(self):
        try:
            conf = self.__readConfFile()
        except:
            sendToLogger('error', 'Config file not found on ' + str(self.nginx_confpath))
        domain_list = self.__parseDomains(conf)
        return domain_list

    def __readConfFile(self):
        return open(self.nginx_confpath).read()

    def __parseDomains(self, conf):
        domains_list = list()
        for conf_part in conf.split('server {'):
            domain = self.__nginxGetDomain(conf_part)
            if (domain):
                protocol = self.__nginxGetListenProtocol(conf_part)
                domains_list.append(domain + ' ' + protocol)
        return domains_list

    def __nginxGetDomain(self, server_conf):
        server_conf = server_conf.splitlines()
        for line in server_conf:
            if ('server_name' in line) and ('#' not in line):
                line = line.replace(';', '')
                words = line.split()
                for word in words:
                    if ('server_name' not in word) and ('tmp' not in word) and ('www' not in word):
                        return word
        return ""

    def __nginxGetListenProtocol(self, server_conf):
        result = ""
        server_conf = server_conf.splitlines()
        for line in server_conf:
            if ('listen' in line) and ('#' not in line):
                line = line.replace(';', '')
                words = line.split()
                for word in words:
                    if ('80' in word):
                        return "http"
                    elif ('443' in word):
                        return "https"
        return ""

