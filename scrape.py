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
    

def build_df(books: List[Dict]) -> pd.DataFrame:
    """
    Return a DataFrame with all books info normalized

    Parameters:
        books(List[Dict]): the list with dicts about the books
    
    Returns:
        df_all_books(pd.DataFrame): a DataFrame with the columns (name, price, url)
  
    """

    df_all_books = pd.DataFrame(books).reset_index(drop=True)
    df_all_books["price"] = df_all_books["price"].str.replace('.',',', regex=False)

    df_all_books = df_all_books.rename(columns={
        "name": "nome",
        "price": "preco",
        "book_url": "url"
    })


    return df_all_books


def export_excel(df: pd.DataFrame, filename: str = "itens.xlsx") -> None:
    """
    Export the data to excel

    Parameters:
        df(pd.DataFrame): the DataFrame from the build_df function, with the books info
    
        filename(str): the choosen name of the file

    """

    df.to_excel(filename, index = False)



def scrape_all_books(initial_url: str ='https://books.toscrape.com') -> pd.DataFrame:
    """
    Commands the entire pipeline: fetches all the raw html pages from the site with, get the data from the raw html
    and turns into a list with dicts that are turn into a DataFrame with the normalized data, and finally Extract to a Excel
    file.

    Parameters:
        initial_url(str): the root page from the site, will be the first to be scrapped and will be used initialize the loop
    
    Returns:
        df_all_books(pd.DataFrame): the DataFrame that will be Extracted to the Excel File
        
    """

    url = initial_url
    all_books = []

    while url:
        html = fetch_html(url=url)
        data, next_url = get_data(html=html, url=url)
        all_books.extend(data)
        print(f"collecting data from: {next_url} . . .")                     #print page checked
        url = urljoin(url, next_url) if next_url else None                  #handles the url concatenation


    df_all_books = build_df(all_books)

    #export DF to a Excel File
    export_excel(df_all_books)

    return df_all_books


if __name__ == "__main__":
    scrape_all_books()
