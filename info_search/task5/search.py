import streamlit as st
import sys
import random
import pandas as pd
sys.path.append('../..')
from info_search.task3.bool_search import BooleanSearcher


def parse_sites(filename):
    _sites = dict()
    with open(filename, "r", encoding="UTF-8") as f:
        for line in f:
            sites_array = line.split(' - ')
            _sites[sites_array[0]] = sites_array[1].rstrip()
    return _sites


def get_urls(_set, _sites) -> list:
    _urls = list()
    for item in _set:
        _urls.append(_sites[str(item)])
    return _urls


st.write("Bool Srch")
token_map = BooleanSearcher.read_token_map('../task3/token_map.txt')
st.write(f"Например: {random.choice(['', 'not '])}{random.choice(list(token_map.keys()))}{random.choice([' and ', ' or '])}{random.choice(['', 'not '])}{random.choice(list(token_map.keys()))}")
search = st.text_input("Введите запрос для поиска")

if st.button("Искать"):
    sites = parse_sites("../task1/data/index.txt")
    indices = BooleanSearcher.run_query(search, token_map)
    urls_list = get_urls(indices, sites)
    urls_df = pd.DataFrame(urls_list, columns=["Сайты"])
    if not urls_list:
        st.write("Ничего не найдено")
    else:
        st.table(urls_df)