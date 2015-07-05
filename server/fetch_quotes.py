#!/usr/bin/env python3

import urllib.request
import random
import json
import re

def fetch_json_quote(api_url):
    try:
        req = urllib.request.urlopen(api_url)
    except urllib.error.HTTPError as e:
        raise FetchQuoteException(str(api_url))

    json_obj = json.loads(str(req.read(), encoding='UTF-8'))

    if not json_obj:
        raise  FetchQuoteException('Object at %s' % str(api_url))

    return json_obj

def clean_quote(s):
    st = re.sub(r'\s+', ' ', s)
    st = st.strip()
    return st

#TODO: Fix
def i_heart_quotes():
    api_url = 'http://www.iheartquotes.com/api/v1/random'
    sources = [
        'computers',
        'woody_allen',
        'winston_churchill',
        'steven_wright',
        'oscar_wilde',
        'oneliners',
        'esr',
        'hitchiker',
        'paul_graham',
        'prog_style',
    ]

    source = random.choice(sources)
    query_str = '?format=json&source=' + source
    json_obj = fetch_json_quote(api_url + query_str)
    return clean_quote(json_obj['quote'])

#TODO: Fix
def they_said_so():
    json_obj = fetch_json_quote('http://api.theysaidso.com/qod.json')
    contents = json_obj['contents']
    quote = contents['quote'] + ' - ' + contents['author']
    return clean_quote(quote)

def quotes_on_design():
    json_obj = fetch_json_quote('http://quotesondesign.com/api/3.0/api-3.0.json')
    quote = json_obj['quote'] + ' - ' + json_obj['author']
    return clean_quote(quote)

def quotedb():
    api_url = 'http://www.quotedb.com/quote/quote.php?action=random_quote'
    try:
        req = urllib.request.Request(api_url,
                data=None,
                headers={'User-Agent' :
                'Mozilla/5.0 (X11; U; Linux i686)'},
            )
        raw_str = urllib.request.urlopen(req).read()
        st = raw_str.decode('utf-8')

        st = re.sub(r'document.write\(', '', st)
        st = re.sub(r'</a></i>\'\);', '', st)
        st = re.sub(r'<br>\'\);\n', '', st)
        st = re.sub(
            r'<i>More quotes from <a href="http://www.quotedb.com/authors/.*">',
            ' - ', st)
        st = clean_quote(st)
        return st

    except urllib.error.HTTPError as e:
        raise FetchQuoteException(api_url)

def fetch_random_quote():
    quote_gens = [
        # i_heart_quotes,
        # i_heart_quotes,
        # i_heart_quotes,
        # i_heart_quotes,
        # i_heart_quotes,
        # i_heart_quotes,
        # i_heart_quotes,
        quotedb,
        quotedb,
        quotedb,
        quotedb,
        quotedb,
        quotedb,
        quotes_on_design,
        quotes_on_design,
        # they_said_so,
    ]
    tries = 10
    while(tries):
        try:
            fn = random.choice(quote_gens)
            return fn()
        except FetchQuoteException as e:
            tries -= 1
            print('Failed fetching quote at %s' % str(e))
            print('Trying again. Tries left %s' % tries)

    print('Failed all attempts')
    return None

class FetchQuoteException(Exception):
    pass

if __name__ == '__main__':
    print(fetch_random_quote())

