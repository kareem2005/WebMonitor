import urllib3

url = "http://cit-sk.ru"

print(url)
http = urllib3.PoolManager()
request = http.request('GET', url)

print(request.data)




