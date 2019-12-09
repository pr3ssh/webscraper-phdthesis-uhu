from bs4 import BeautifulSoup
import requests
import simplejson as json

'''
La documentacion puede ser encontrada en
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''

'''
LA MISION:
Rescatar los metadatos basicos de las ultimas 20 tesis
doctorales de la Univerdad de Huelva
'''

response  = requests.get("http://rabida.uhu.es/dspace/handle/10272/3/recent-submissions")
data = response.text
soup = BeautifulSoup(data, "html.parser")
thesis_collection = []
for element in soup.find_all('li', class_='ds-artifact-item'):
    try:
        thesis = {}
        thesis['title'] = element.select_one('h4 a').getText()
        info = element.find('div', class_='artifact-info')
        thesis['author'] = info.select_one('span.author small span a').getText()
        thesis['publisher'] = info.select_one('span.publisher').getText()
        thesis['date'] = info.select_one('span.date').getText()
    except:
        pass
    thesis_collection.append(thesis)

print(json.dumps(thesis_collection, indent=4, ensure_ascii=False, encoding="utf-8"))
