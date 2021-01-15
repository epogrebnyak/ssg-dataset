# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 17:58:21 2021

@author: Евгений
"""
import requests
import bs4
import re
import requests_cache

#requests_cache.install_cache('google')

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
}

# "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"


def get_n_results_dumb(q):
    r = requests.get('http://www.google.com/search',
                     params={'q': q,
                             "tbs": "li:1"})
    r.raise_for_status()
    soup = bs4.BeautifulSoup(r.text)
    s = soup.find('div', {'id': 'resultStats'}).text
    if not s:
        return 0
    m = re.search(r'([0-9,]+)', s)
    return int(m.groups()[0].replace(',', ''))

s1 = "Migrate from Jekyll to Hugo"
r = requests.get('http://www.google.com/search',
                 headers=headers,
                     params={'q': s1,  
                             "tbs": "li:1"})

from pathlib import Path
p = Path("res.txt").write_text(r.text)
#n1 = get_n_results_dumb("Migrate from Jekyll to Hugo")
#n2 = get_n_results_dumb("Migrate from Hugo to Jekyll")