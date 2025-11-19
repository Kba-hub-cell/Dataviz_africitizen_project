"""
Utility functions for web scraping with Selenium/Helium and BeautifulSoup.
"""

from helium import start_chrome, wait_until, get_driver, kill_browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.options import Options


def scrape_table_from_url(url, headless=True, timeout_secs=30, chrome_options=None):
    """
    Scrape a <table> element from a URL using Selenium/Helium and parse it into a pandas DataFrame.
    
    Parameters
    ----------
    url : str
        The target URL containing the table to scrape.
    headless : bool, optional
        Whether to run Chrome in headless mode (default: True).
    timeout_secs : int, optional
        Maximum time (in seconds) to wait for the table to appear (default: 30).
    chrome_options : selenium.webdriver.chrome.options.Options, optional
        Custom Chrome options. If None, default safe options are used.
    
    Returns
    -------
    pd.DataFrame
        A pandas DataFrame containing the scraped table data.
        Returns an empty DataFrame if no table is found.
    
    Examples
    --------
    >>> from scraper_utils import scrape_table_from_url
    >>> url = 'https://ourworldindata.org/grapher/electricity-generation?tab=table'
    >>> df = scrape_table_from_url(url)
    >>> print(df.head())
    """
    
    # Set default Chrome options if not provided
    if chrome_options is None:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
    
    # Ensure no leftover browser instances
    try:
        kill_browser()
    except Exception:
        pass
    
    # Start Chrome and navigate to the page
    driver = start_chrome(url, headless=headless, options=chrome_options)
    
    # Wait until a <table> element appears on the page
    try:
        wait_until(
            lambda: len(get_driver().find_elements('tag name', 'table')) > 0,
            timeout_secs=timeout_secs
        )
    except Exception as e:
        print(f'Table not found within {timeout_secs} seconds:', e)
        return pd.DataFrame()
    
    # Get rendered page source
    rendered = get_driver().page_source
    soup = BeautifulSoup(rendered, 'html.parser')
    tbl = soup.find('table')
    
    if tbl is None:
        print('No <table> found in page source. The table may be rendered differently or inside an iframe.')
        return pd.DataFrame()
    
    # Extract headers (if present) and rows
    thead = tbl.find('thead')
    if thead:
        headers = [th.get_text(strip=True) for th in thead.find_all('th')]
    else:
        # Fallback: try first row as header
        first_row = tbl.find('tr')
        headers = [th.get_text(strip=True) for th in first_row.find_all(['th', 'td'])] if first_row else []
    
    tbody = tbl.find('tbody') or tbl
    rows = []
    for tr in tbody.find_all('tr'):
        cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
        # Skip empty rows
        if any(c != '' for c in cells):
            rows.append(cells)
    
    # Normalize row length to headers (pad with None)
    if headers:
        max_cols = len(headers)
        normalized = [
            r + [None] * (max_cols - len(r)) if len(r) < max_cols else r[:max_cols]
            for r in rows
        ]
        df = pd.DataFrame(normalized, columns=headers)
    else:
        df = pd.DataFrame(rows)
    
    # Display basic info
    print(f'Extracted DataFrame shape: {df.shape}')
    
    return df


def close_browser():
    """
    Close any open browser instances to free resources.
    
    Examples
    --------
    >>> from scraper_utils import close_browser
    >>> close_browser()
    """
    try:
        kill_browser()
        print('Browser closed successfully.')
    except Exception as e:
        print('kill_browser() failed or browser already closed:', e)
