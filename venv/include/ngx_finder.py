from include.logger import sendToLogger
from nginxparser import load


class NginxDomainFinder():

    def __init__(self, nginx_confpath):
        self.nginx_confpath = nginx_confpath

    def getDomains(self):
        conf = self.__readConfFile()
        print(self.__parseDomains(conf))

    def __readConfFile(self):
        return open(self.nginx_confpath)

    def __parseNginx(self):
        load(self.__readConfFile())

    def __parseDomains(self, conf):
        result = ""
        for line in conf:
            if ('server_name' in line) and ('#' not in line):
                line = line.replace(';', '')
                words = line.split()
                for word in words:
                    if ('server_name' not in word) and ('tmp' not in word) and ('www' not in word):
                        result = word + "\n" + result
                        break
        return conf





