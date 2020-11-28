import datetime
import itertools
import logging
import multiprocessing
from typing import List, Optional, Union

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.sec.gov/Archives/edgar/Feed'
DAILY_ARCHIVE_EXTENSION = 'nc.tar.gz'
FIRST_YEAR = 1995
CURRENT_YEAR = datetime.datetime.now().year


def _get_quarter_listing_urls(year: Union[int, List[str], List[int], range],
                              quarter: Union[int, List[str], List[int], range]) -> List[str]:
    """
    Obtains the SEC EDGAR daily archive feed listings for each (year, quarter)
    :param year: year(s) to retrieve
    :param quarter: quarter(s) to retrieve
    :return: quarter listings for each (year, quarter)
    """

    # If year or quarter are singleton, convert them to iterables
    if isinstance(year, int):
        year = [year]

    if isinstance(quarter, int):
        quarter = [quarter]

    # Generate quarter listings for each (year, quarter)
    quarter_listing_urls = []
    for _year in year:
        for _quarter in quarter:
            quarter_listing_url = f'{BASE_URL}/{_year}/QTR{_quarter}/'
            quarter_listing_urls.append(quarter_listing_url)

    return quarter_listing_urls


def _get_daily_archive_urls_from_quarter_listing(quarter_listing_url: str) -> List[str]:
    """
    Given a quarter listing URL, return the URLs of the daily archives
    :param quarter_listing_url: URL of the SEC feed for a particular (year, quarter)
    :return: URLs of the SEC daily archives linked to in the quarter listing
    """

    # Parse the directory listing
    page = requests.get(quarter_listing_url).text
    soup = BeautifulSoup(page, 'html.parser')

    # List all of the hyperlinks in the directory listing
    links = [link.get('href') for link in soup.find_all('a')]

    # Filter only the daily archives
    daily_archive_filepaths = filter(lambda link: link.endswith(DAILY_ARCHIVE_EXTENSION), links)

    # Return the absolute filepath of the daily archives
    absolute_filepaths = [quarter_listing_url + filepath for filepath in daily_archive_filepaths]

    return absolute_filepaths


def _get_daily_archive_urls_from_multiple_quarter_listings(quarter_listing_urls: List[str],
                                                           num_processes: int) -> List[str]:
    """
    Given multiple quarter listing URLs, return the URLs of the daily archives
    :param quarter_listing_urls: URL of the SEC feed for a particular (year, quarter)
    :param num_processes: number of quarter listings to scrape at once
    :return: URLs of the SEC daily archives linked to in the quarter listings
    """

    # Set up the multiprocessing pool
    multiprocessing_pool = multiprocessing.Pool(num_processes)

    # Obtain (in parallel) the daily archive URLs from the quarter listing URLs; this returns a list of lists
    daily_archive_urls = multiprocessing_pool.imap(_get_daily_archive_urls_from_quarter_listing, quarter_listing_urls)

    # Flatten the daily archive URLs into one list
    daily_archive_urls = list(itertools.chain.from_iterable(daily_archive_urls))

    # Close the multiprocessing pool
    multiprocessing_pool.close()
    multiprocessing_pool.join()

    return daily_archive_urls


def edgar_crawler(year: Optional[Union[int, List[str], List[int], range]] = range(FIRST_YEAR, CURRENT_YEAR + 1),
                  quarter: Optional[Union[int, List[str], List[int], range]] = range(1, 4 + 1),
                  num_processes: Optional[int] = 1) -> List[str]:
    """
    Obtain the SEC EDGAR daily archive URLs for each day in the year(s) and quarter(s) specified. Default is for every
    filing day between 1995 and the current year
    :param year: year(s) to retrieve
    :param quarter: quarter(s) to retrieve
    :param num_processes: number of parallel crawlers
    :return: URLs of the SEC daily archives for each day in the year(s) and quarter(s) specified
    """

    # Get the SEC EDGAR daily archive feed listings for each (year, quarter)
    quarter_listing_urls = _get_quarter_listing_urls(year, quarter)

    # Get the URLs of the SEC daily archives for each day in the year(s) and quarter(s) specified
    daily_archive_urls = _get_daily_archive_urls_from_multiple_quarter_listings(quarter_listing_urls, num_processes)

    # Log the number of identified archives
    logging.info(f'Identified {len(daily_archive_urls)} daily archives to be downloaded')

    return daily_archive_urls
