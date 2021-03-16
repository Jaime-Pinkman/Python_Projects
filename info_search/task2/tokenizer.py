import os
import re
from lxml import etree
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
#%%
PATH = '../task1/data/'
files = os.listdir(PATH)


#%%
htmlparser = etree.HTMLParser()
input_str = ''
for f in files:
    if f.endswith('.html'):
        with open(PATH+f, 'r', encoding="UTF-8") as html:
            tree = etree.parse(html, htmlparser)
            texts_from_html = tree.xpath("//p//text()")
            texts = []
            text = str.join('', texts_from_html)
            result = re.sub(r'\d +', '', text)
            result = ''.join([i for i in result if not i.isdigit()])
            result = result.translate(str.maketrans(' ', ' ', string.punctuation))
            result = result.strip()
            stemmer = PorterStemmer()
            input_str = word_tokenize(result)
            for word in input_str:
                texts.append(' '.join([word, ' - ', stemmer.stem(word), '\n']))

with open("lemms1.txt", 'w', encoding='utf-8') as f:
    for text in texts:
        f.write(text)

with open("words.txt", 'w', encoding='utf-8') as f:
    for word in input_str:
        f.write(word + '\n')


