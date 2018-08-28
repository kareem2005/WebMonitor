import urllib3
import re
from include.logger import *


class SiteChecker():

    def __init__(self, site, site_keyword, site_protocol, allowable_http_status):
        self.allowable_http_status = allowable_http_status
        self.site_protocol = site_protocol
        self.site_keyword = site_keyword
        self.site = site

    def doCheck(self):
        request = self.__getSite(self.site, self.site_protocol)

        if (self.__checkSiteStatus(request.status, self.allowable_http_status)):
            sendToLogger('debug', 'Checking site data ' + str(self.site))
            if (self.__checkSiteData(request.data, self.site_keyword)):
                sendToLogger('ok', 'Site data checking ' + str(self.site) + ' OK')
            else:
                sendToLogger('warn', 'Site data checking ' + str(self.site) + ' FAIL')
        else:
            sendToLogger('warn', 'Site status checking ' + str(self.site) + ' FAIL')

    def __getSite(self, domain, protocol):
        url = protocol + '://' + domain
        try:
            http = urllib3.PoolManager()
            request = http.request('GET', url)
            return request
        except urllib3.exceptions.NewConnectionError:
            sendToLogger('error', 'Connection failed  for ' + str(domain))
            exit(2)
        except urllib3.exceptions.MaxRetryError:
            sendToLogger('error', 'Max retries exceeded for ' + str(domain))
            exit(2)

    def __checkSiteStatus(self, request_status, allowable_status):
        if (request_status == allowable_status):
            return True
        else:
            sendToLogger('warn', 'HTTP status ' + str(request_status) + ' not allowable.')
            return False

    def __checkSiteData(self, request_data, keyword):
        if re.search(str(keyword), str(request_data)):
            return True
        else:
            sendToLogger('warn', 'Keyword ' + str(keyword) + ' not found.')
            return False