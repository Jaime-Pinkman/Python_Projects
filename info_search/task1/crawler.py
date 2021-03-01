import requests
import os
from lxml import etree
from io import StringIO


def parse(url):
    resp = requests.get(url, headers={'Content-Type': 'text/html'})
    return resp.text

html = parse('https://eco-farm.org/jobs?items_per_page=100')
htmlparser = etree.HTMLParser()
tree = etree.parse(StringIO(html), htmlparser)
links = tree.xpath('//a[contains(@href, \'/job/\')]/@href')
links = list(set(links))

os.makedirs("data", exist_ok=True)
index = open("data/index.txt", "w+", encoding='utf-8')
for i, link in enumerate(links):
    html_source = parse('https://eco-farm.org/' + link)
    with open("data/" + str.format("{}.html".format(i)), 'w', encoding='utf-8') as f:
        f.write(html_source)
    index.write("{} - https://eco-farm.org/{}\n".format(i, link))

index.close()
