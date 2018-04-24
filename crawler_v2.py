from bs4 import BeautifulSoup
import requests
import json

'''
La documentacion puede ser encontrada en
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''

'''
LA MISION:
Rescatar los metadatos basicos de todas las tesis
doctorales de la Univerdad de Huelva
'''

def ncd(str):
    return str.encode('utf-8')

def parse_thesis_simplified(element, thesis):
    thesis['title'] = ncd(element.select_one('h4 a').text)
    info = element.find('div', class_='artifact-info')
    thesis['autor'] = info.select_one('span.author small span a').text
    thesis['publisher'] = info.select_one('span.publisher').getText()
    thesis['date'] = info.select_one('span.date').getText()



host_url = "http://rabida.uhu.es"
thesis_url = "/dspace/handle/10272/3/recent-submissions"
jump = 20

req  = requests.get("{}{}".format(host_url, thesis_url))
data = req.text
soup = BeautifulSoup(data, "html.parser")
thesis_collection = []

try:
    total_thesis = soup.select_one("p.pagination-info").text.split('de')[1].strip()
except:
    exit

for offset in xrange(0, int(20), jump):
    req  = requests.get("{}{}?offset={}".format(host_url, thesis_url, offset))
    data = req.text
    soup = BeautifulSoup(data, "html.parser")
    repository = soup.select_one("div#repository-content")
    for element in repository.find_all('li', class_='ds-artifact-item'):
        thesis = {}
        try:
            parse_thesis_simplified(element, thesis)
        except Exception, e:
            pass
        thesis_collection.append(thesis)

print json.dumps(thesis_collection, indent=4)
