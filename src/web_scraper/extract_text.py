import logging
import requests
from bs4 import BeautifulSoup
from src import config
from src.web_scraper import process_text


def retrieve_poem_text(url):
    """
    Retrieves poem text from a single poetryarchive url. 

    Args:
        url (str): The poem URL.

    Returns:
        .....

    Raises:
        Exception: If poem text cannot be extracted from specified URL.
    """

    try:
        response = requests.get(url, headers=config.headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')
        content = soup.get_text()

        author_name = process_text.get_author(content)
        poem_title = process_text.get_title(content)
        poem_text = process_text.get_poem()


        # write poem text to file (for initial testing)
        with open('./output/test_file.txt', 'w') as file:
            file.write(content)
        
    
    except requests.RequestException as e:
        logging.error(f"Failed to extract poem text from URL {url}: {e}")