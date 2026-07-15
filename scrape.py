# Built-in libs
from typing import Dict, List
from urllib.parse import urljoin

#External libs
import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_html(url: str) -> str:
    """
    Return the fetched raw HTML

    Parameters:
        url (str): the url from the site to be fetched (https://books.toscrape.com)
    
    Returns:
        res.text (str): the raw HTML if the request sucessed
    """
    session = requests.Session()    # for optimization


    res = session.get(url, timeout=10)
    res.encoding = 'utf-8'        # right encoding
    return res.text

