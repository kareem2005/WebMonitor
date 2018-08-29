from include.site_checker import SiteChecker
from include.zbx_controller import ZabbixController
from include.ngx_finder import NginxDomainFinder


# http status code - ex.: 200, 404
allowable_http_status = 200
# special word for identifying site
site_keyword = "cit"
# http or https
site_protocol = "http"
# domain - ex.: example.com
site = "cit-sk.ru"
# warn, debug, none
log_level = "debug"

# _________ ZABBIX ___________
# zabbix url
zbx_url = "http://192.168.0.111/zabbix"
# zabbix_user
zbx_user = "Admin"
# zabbix password
zbx_pass = "zabbix"
# zabbix host for web monitor
zbx_wmhost = "Web Monitor"
# zbx_wmhost = "Zabbix server"
zbx_wmgroup = "Hosting"

# __________ NGINX ____________
# path to nginx configuration file
nginx_confpath = "F:\\Projects\\Files for Projects\\nginx.conf"
domain_list = "cit-sk.ru\n" \
              "velomap.ru\n" \
              "ya.ru"


def main():
#    check = SiteChecker(site, site_keyword, site_protocol, allowable_http_status)
#    check.doCheck()
    zbxUpdater = ZabbixController(zbx_url, zbx_user, zbx_pass, zbx_wmhost, zbx_wmgroup)
    zbxUpdater.addToMonitor(domain_list)
#    ngxDomains = NginxDomainFinder(nginx_confpath)
#    ngxDomains.getDomains()


if __name__== "__main__":
  main()


