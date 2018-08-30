import urllib3
from include.logger import sendToLogger


class SiteAnalyzer():

    def __init__(self, site, site_protocol):
        self.site_protocol = site_protocol
        self.site = site

    def getHttpStatus(self):
        

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