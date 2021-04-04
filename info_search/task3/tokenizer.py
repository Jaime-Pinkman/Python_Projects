from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
from lxml import etree
import re
import string
from nltk.stem import PorterStemmer


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
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
    result = result.translate(translator)
    #bad_symbols = ['`', '●', '·', '•', '—', '”', '•', '•']
    #[result.replace(symbol, ' ') for symbol in bad_symbols]

    # tokenize string
    result = word_tokenize(result)

    # remove stop words
    result = [w for w in result if w not in set(stopwords.words('english'))]

    # create Stemmer
    stemmer = PorterStemmer()

    # stem tokens
    result = [stemmer.stem(''.join(filter(str.isalpha, w))) for w in result]

    return result


def save_token_map(index_map):
    with open("token_map.txt", 'w', encoding='utf-8') as f:
        for key, value in index_map.items():
            f.write(key + ' ' + str(sorted(value)) + '\n')


if __name__ == "__main__":
    PATH = '../task1/data'  # directory with files
    files = get_files(PATH)  # get files
    print(files)
    gallery = []  # space with all tokens
    indices = set()  # contains unique indices

    # get indices and fill the space of tokens
    for i, f in enumerate(files):
        tokens = tokenize(get_content(os.path.join(PATH, f)))
        [indices.add(token) for token in set(tokens)]
        gallery.append(tokens)

    token_map = {index: [] for index in indices}  # maps token to a certain file

    # search for indices in token space
    for token in indices:
        for i, content in enumerate(gallery):
            if token in content:
                token_map[token].append(i)

    save_token_map(token_map)
