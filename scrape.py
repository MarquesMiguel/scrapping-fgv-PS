# Built-in libs
from typing import Dict, List, Tuple, Optional
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




def get_data(html: str, url: str) -> Tuple[List[Dict], Optional[str]]:
    """
    Return a list with dicts with the books info inside + the next page url to be scrapped

    Parameters:
        html(str): the raw html str fetched by the fecth_html() file

        url(str): same as the fetch_html, used to create the books url
    
    Returns:
        data(List): a list with dicts wich have the (name, price, url) keys refering to the books scrapped

        next_url(str): refers to the next page to be scrapped from the site
    """


    soup = BeautifulSoup(html, "html.parser")
    next = soup.find('li', class_ = 'next')

    ol = soup.find('ol', class_ = 'row')
    li = ol.find_all('li')


    data = []

    for child in li:
        name  = child.h3.a["title"]
        price = child.find('p', class_ = 'price_color').text
        book_url = urljoin(url, child.h3.a['href'])
    
        book = {"name": name, "price": price, "book_url": book_url} 

        data.append(book)
  

    if next:
        next_url = next.a["href"]
        return data, next_url
    else:
        return data, None
    


def build_df(books: List) -> pd.DataFrame: 
  """
  Return 
  """


  df_all_books = pd.DataFrame(books).reset_index(drop=True)

  df_all_books["price"] = df_all_books["price"].str.replace('.',',', regex=False)

  return df_all_books

