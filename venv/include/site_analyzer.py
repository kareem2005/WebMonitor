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
        text = self.__get_clean_html_footer(data)
        print(self.__select_keyword(text))

    def __select_keyword(self, text):
        for line in text.decode('utf-8'):
            print(line)
        return True

    def __get_clean_html_footer(self, html_text):
        return BeautifulSoup(html_text, "lxml").footer.text

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