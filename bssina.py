
import urllib.request
from bs4 import BeautifulSoup


url = 'http://www.sina.com.cn/'
headers = {
    'Host': 'www.sina.com.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'GET': 'url'
}
request = urllib.request.Request(url,headers = headers)
html = urllib.request.urlopen(request)

print(html.read().decode('gbk','ignore'))

html.close()
#soup = BeautifulSoup(html)

#atag = soup.findall('a')

#print(soup)

