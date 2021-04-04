import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import math
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
from lxml import etree
import re
import string
from nltk.stem import PorterStemmer


def compute_tfidf(corpus):
    def compute_tf(text):
        tf_text = Counter(text)
        for i in tf_text:
            tf_text[i] = tf_text[i] / float(len(text))
        return tf_text

    def compute_idf(word, corpus):
        return math.log10(len(corpus) / sum([1.0 for i in corpus if word in i]))

    documents_list = []
    for text in corpus:
        tf_idf_dictionary = {}
        computed_tf = compute_tf(text)
        for word in computed_tf:
            computed_idf = compute_idf(word, corpus)
            tf_idf_dictionary[word] = [computed_idf, computed_tf[word] * computed_idf]
        documents_list.append(tf_idf_dictionary)
    return documents_list


def get_files(path):
    files = os.listdir(path)
    files.remove('index.txt')
    files.sort(key=lambda x: int(x.split('.')[0]))
    return files


def get_content(file) -> 'str':
    htmlparser = etree.HTMLParser()
    with open(file, 'r', encoding="UTF-8") as html:
        tree = etree.parse(html, htmlparser)
        texts_from_html = tree.xpath("//p//text()")
        return str.join('', texts_from_html).lower()


def tokenize(content):
    # remove links
    result = re.sub(r'http\S+', '', content)

    # remove words with number in it
    result = ' '.join(s for s in result.split() if not any(c.isdigit() for c in s))

    # remove punctuation
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    result = result.translate(translator)
    # bad_symbols = ['`', '●', '·', '•', '—', '”', '•', '•']
    # [result.replace(symbol, ' ') for symbol in bad_symbols]

    # tokenize string
    result = word_tokenize(result)

    # remove stop words
    result = [w for w in result if w not in set(stopwords.words('english'))]

    # create Stemmer
    stemmer = PorterStemmer()

    # stem tokens
    result = [stemmer.stem(''.join(filter(str.isalpha, w))) for w in result]

    return result


if __name__ == "__main__":
    PATH = '../task1/data'  # directory with files
    files = get_files(PATH)  # get files
    gallery = []  # space with all tokens
    indices = set()  # contains unique indices

    arr_tokens = []
    for i, f in enumerate(files):
        arr_tokens.append(tokenize(get_content(os.path.join(PATH, f))))

    tfidf = compute_tfidf(arr_tokens)
    with open("out.txt", "w", encoding="UTF-8") as out:
        for dictionary in tfidf:
            print(dictionary, file=out)
