#!/usr/bin/env python3

import urllib.request
import re
from config import TODO_URL

def fetch_todo_items():
    req = urllib.request.urlopen(TODO_URL)
    st = str(req.read(), encoding='UTF-8')
    raw_todo = st.split('\n')
    return filter_by_regex(r'^\d{4}-\d{2}-\d{2}', raw_todo)

def filter_by_regex(regex, ls):
    return list(filter( lambda line: re.match(regex,line), ls))

def fetch_specific_items(tag):
    return filter_by_regex(r'.*%s.*' % tag, fetch_todo_items())

if __name__ == '__main__':
    print(fetch_todo_items())
