from bs4 import BeautifulSoup
import requests
import json

'''
La documentacion puede ser encontrada en
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''

'''
LA MISION:
Rescatar los metadatos basicos de las ultimas tesis
doctorales de la Univerdad de Huelva
'''

def ncd(str):
    return str.encode('utf-8')

req  = requests.get("http://rabida.uhu.es/dspace/handle/10272/3")
data = req.text
soup = BeautifulSoup(data, "html.parser")
tesis_collection = []
for element in soup.find_all('li', class_='ds-artifact-item'):
    tesis = {}
    tesis['title'] = ncd(element.select_one('h4 a').getText())
    info = element.find('div', class_='artifact-info')
    tesis['autor'] = info.select_one('span.author small span a').getText()
    tesis['publisher'] = info.select_one('span.publisher').getText()
    tesis['date'] = info.select_one('span.date').getText()
    tesis_collection.append(tesis)

print json.dumps(tesis_collection, indent=4)
