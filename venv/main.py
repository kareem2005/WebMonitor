from include.site_checker import SiteChecker


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



def main():
    check = SiteChecker(site, site_keyword, site_protocol, allowable_http_status)
    check.doCheck()


if __name__== "__main__":
  main()


