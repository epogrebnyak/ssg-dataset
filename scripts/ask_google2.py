# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 18:26:23 2021

@author: Евгений
"""

import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
URL     = "https://www.google.com/search?q=programming"
result = requests.get(URL, headers=headers)    

def from_google(q: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
    url = f"https://www.google.com/search?q={q}"
    return requests.get(url, headers=headers)

def find_div(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False).replace(u'\xa0', u' ') # this will give you the outer text which is like 'About 1,410,000,000 results'  

def parse(text):            
    soup = BeautifulSoup(text, 'html.parser')
    total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False) # this will give you the outer text which is like 'About 1,410,000,000 results'
    results_num = ''.join([s for s in total_results_text if s.isdigit()]) # now will clean it up and remove all the characters that are not a number .
    return int(results_num)

def num(text):
    return ''.join([s for s in text if s.isdigit()])

def n_results(q: str):
    return num(find_div(from_google(q).content))

q = '"from+Wordpress"+"to+Gatsby"'
r = from_google(q)
s1 = find_div(r.content)
n1 = n_results(q)
print(s1,n1)