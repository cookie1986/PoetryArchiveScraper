import requests
from http import HTTPStatus
from bs4 import BeautifulSoup
import logging
from requests.exceptions import RequestException, Timeout

# configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_sitemap_urls(sitemap_url, max_retries=3, timeout=10):
    """
    Fetches URLs from a sitemap XML file, with retries for specific HTTP error codes.

    Args:
        sitemap_url (str): The URL of the sitemap XML file.
        max_retries (int): The maximum number of retry attempts for specified HTTP error codes. Default is 3.
        timeout (int): The timeout in seconds for the HTTP request. Default is 10.

    Returns:
        list: A list of URLs extracted from the sitemap.

    Raises:
        Exception: If all retry attempts fail or a non-retryable HTTP error occurs.
    """

    # headers to simulate web browser (prevents 403 error)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    # eligible retry codes
    http_retry_codes = {
        HTTPStatus.TOO_MANY_REQUESTS,  # 429
        HTTPStatus.INTERNAL_SERVER_ERROR,  # 500
        HTTPStatus.BAD_GATEWAY,  # 502
        HTTPStatus.SERVICE_UNAVAILABLE,  # 503
        HTTPStatus.GATEWAY_TIMEOUT  # 504
    }

    for attempt in range(max_retries):
        try:
            # fetch response from sitemap
            response = requests.get(sitemap_url, headers=headers, timeout=timeout)
            logging.info(f"HTTP: {response.status_code}")

            # check for non-retryable HTTP errors
            if response.status_code not in http_retry_codes:
                response.raise_for_status()

            # access the raw text
            content = response.text
            
            # parse the xml
            soup = BeautifulSoup(content, 'xml')

            # extract urls
            urls = [loc.text for loc in soup.find_all('loc')]
            logging.info(f"Successfully extracted {len(urls)} URLs from the sitemap.")
            return urls

        except (RequestException, Timeout) as e:
            if response.status_code not in http_retry_codes:
                logging.error(f"Non-retryable error {response.status_code} encountered on attempt {attempt + 1}.")
                raise Exception(f"Non-retryable error {response.status_code} encountered: {e}")
            if attempt == max_retries - 1:
                logging.error(f"All retry attempts failed after {attempt + 1} attempts.")
                raise Exception(f"Failed to fetch sitemap after {attempt + 1} attempts: {e}")
            logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying...")


            

def main():
    try: 
        sitemap_url = 'https://poetryarchive.org/poems-sitemap.xml'
        
        urls = get_sitemap_urls(sitemap_url)
    
    except Exception as e:
        logging.error(f"Failed to get sitemap URLs from {sitemap_url}: {e}")

if __name__== '__main__':
    main()