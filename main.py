import logging
from src import config
from src.web_scraper.fetch_urls import get_sitemap_urls
from src.web_scraper.extract_text import retrieve_poem_text


def main():

    # Ensure that config is imported and initialized
    config.initialize()
    
    # List of sitemaps
    sitemaps = [
        'https://poetryarchive.org/poems-sitemap.xml',
        'https://poetryarchive.org/poems-sitemap2.xml',
        'https://poetryarchive.org/poems-sitemap3.xml',
    ]

    # Search each sitemap for URLs and compile as list
    poem_urls = []
    for link in sitemaps:
        try:
            urls = get_sitemap_urls(link)
            poem_urls.extend(urls)
    
        except Exception as e:
            logging.error(f"Failed to get sitemap URLs from {link}: {e}")

    logging.info(f"{len(poem_urls)} poem URLs extracted from sitemaps.")

    # Extract text from each url and store as plain text file
    poem_urls = poem_urls[:1] # filtered dataset for debugging..........
    for poem in poem_urls:
        retrieve_poem_text(poem)


if __name__== '__main__':
    main()