import urllib3
import re
from bs4 import BeautifulSoup
from include.logger import *


class SiteAnalyzer():

    def __init__(self, site, site_protocol):
        self.site_protocol = site_protocol
        self.site = site
        self.request = self.__get_site(self.site, self.site_protocol)

    def get_http_status(self):
        if (self.request.status == 200):
            return self.request.status
        else:
            return 'none'

    def get_key_phrase(self):
        phrase = self.__analyze_site()
        if (phrase):
            return phrase
        else:
            return 'none'

    def __analyze_site(self):
        data = self.request.data.decode('utf-8')
        #print(data)
        print(self.__clear_html(data))

    def __clear_htmlbs(self, html_text):
        return BeautifulSoup(html_text, "lxml").text

    def __clear_html(self, html_text):
        clean_text = re.sub(re.compile('<.*?>'), '', html_text)
        return clean_text

    def __get_site(self, domain, protocol):
        url = protocol + '://' + domain
        try:
            http = urllib3.PoolManager()
            request = http.request('GET', url)
            return request
        except urllib3.exceptions.NewConnectionError:
            sendToLogger('error', 'Connection failed for ' + str(domain))
            exit(2)
        except urllib3.exceptions.MaxRetryError:
            sendToLogger('error', 'Max retries exceeded for ' + str(domain))
            exit(2)