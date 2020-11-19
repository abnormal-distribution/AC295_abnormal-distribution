import pandas as pd

import requests
from ratelimit import limits, sleep_and_retry
from bs4 import BeautifulSoup

from tqdm import tqdm



class SecAPI:
    """
    Helper class that caches data from the SEC and avoids exceeding # of calls allowed per second to the website.
    """
    SEC_CALL_LIMIT = {'calls': 10, 'seconds': 1}

    @staticmethod
    @sleep_and_retry
    # Dividing the call limit by half to avoid coming close to the limit
    @limits(calls=SEC_CALL_LIMIT['calls'] / 2, period=SEC_CALL_LIMIT['seconds'])
    def _call_sec(url):
        return requests.get(url)

    def get(self, url):
        return self._call_sec(url).text


def get_sec_data(cik, doc_type, date='2020-12-31', start=0, count=60):
    """

    Parameters
    ----------
    cik: str
        CIK of SEC document. 10 character string
    doc_type: str
        Type of SEC document. ('10-K' or '10-Q')
    date: str
    start: int
    count: int

    Returns
    -------
    List of tuples containing ('filing-href', 'filing-type', 'filing-date')

    """

    # instantiate SecAPI object to help with call limits to SEC website
    sec_api = SecAPI()

    final_date = pd.to_datetime(date)
    rss_url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany' \
        '&CIK={}&type={}&start={}&count={}&owner=exclude&output=atom' \
        .format(cik, doc_type, start, count)
    # get data
    sec_data = sec_api.get(rss_url)
    # convert to BeautifulSoup object for parsing
    feed = BeautifulSoup(sec_data.encode('ascii'), 'xml').feed
    # list of tuples containing ('filing-href', 'filing-type', 'filing-date')
    entries = [
        (
            entry.content.find('filing-href').getText(),
            entry.content.find('filing-type').getText(),
            entry.content.find('filing-date').getText())
        # recursive = False will restrict the search to the first found element and its child only
        for entry in feed.find_all('entry', recursive=False)
        # restrict to files before supplied date
        if pd.to_datetime(entry.content.find('filing-date').getText()) <= final_date]

    return entries

def download_docs(ticker_index, ciks, doc_type):

    sec_api = SecAPI()
    sec_data = {}

    for ticker in ticker_index:
        sec_data[ticker] = get_sec_data(ciks.loc[ticker].values[0], doc_type)

    raw_fillings_by_ticker = {}

    for ticker, data in sec_data.items():
        raw_fillings_by_ticker[ticker] = {}
        for index_url, file_type, file_date in tqdm(data,
                                                    desc='Downloading {} {} Fillings'.format(ticker, doc_type),
                                                    unit='filling'):
            if file_type == doc_type:
                file_url = index_url.replace('-index.htm', '.txt').replace('.txtl', '.txt')

                raw_fillings_by_ticker[ticker][file_date] = sec_api.get(file_url)

    return raw_fillings_by_ticker
