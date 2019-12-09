from bs4 import BeautifulSoup
import requests
import simplejson as json

'''
La documentacion puede ser encontrada en
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''

'''
LA MISION:
Rescatar los metadatos basicos (+ abstract) de todas las tesis
doctorales de la Univerdad de Huelva
'''

def get_abstract_from_thesis(thesis):
    response = requests.get(thesis['url'])
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    thesis['abstract'] = soup.select_one("div.abstract-content").text


def parse_thesis(element, thesis):
    title = element.select_one('h4 a')
    thesis['title'] = title.text
    thesis['url'] = "{}{}".format(host_url, title['href'])
    get_abstract_from_thesis(thesis)
    info = element.find('div', class_='artifact-info')
    thesis['autor'] = info.select_one('span.author small span a').text
    thesis['publisher'] = info.select_one('span.publisher').getText()
    thesis['date'] = info.select_one('span.date').getText()



host_url = "http://rabida.uhu.es"
thesis_url = "/dspace/handle/10272/3/recent-submissions"
jump = 20

response  = requests.get("{}{}".format(host_url, thesis_url))
data = response.text
soup = BeautifulSoup(data, "html.parser")
thesis_collection = []

try:
    total_thesis = soup.select_one("p.pagination-info").text.split('de')[1].strip()
except:
    exit

for offset in range(0, int(total_thesis), jump):
    response  = requests.get("{}{}?offset={}".format(host_url, thesis_url, offset))
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    repository = soup.select_one("div#repository-content")
    for element in repository.find_all('li', class_='ds-artifact-item'):
        thesis = {}
        try:
            parse_thesis(element, thesis)
        except Exception:
            pass
        thesis_collection.append(thesis)

print(json.dumps(thesis_collection, indent=4, ensure_ascii=False, encoding="utf-8"))
