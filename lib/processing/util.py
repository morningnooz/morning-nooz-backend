import feedparser
import re
import logging
from urllib.parse import urlparse

def extract_subdomain(url):
    parsed_url = urlparse(url)
    parts = parsed_url.netloc.split('.')
    if len(parts) > 2:
        return parts[1]
    else:
        return parts[0]

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def parse_rss_feed(feed_url):
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)

    feed_entries = dict(feed)["entries"]
    result = ""

    print(len(feed_entries))
    
    for article in feed_entries:
        # Extracting the feed title (name), link (URL), and description (DESC)
        feed_name = article.title if 'title' in feed.feed else 'No title'
        feed_url = article.link if 'link' in article else 'No link'
        feed_provider = extract_subdomain(article.link) if 'link' in article else article.get('publisher', article.get('author', 'No provider'))
        feed_desc = clean_html(article.get('summary', article.get('content', 'No provider')))
    
        # Format the output string
        result += f"NAME: {feed_name}, URL: {feed_url}, PROVIDER: {feed_provider}, DESC: {feed_desc}| "
    
    return result

# Example usage
rss_feed_url = 'https://101greatgoals.com/feed'
result_string = parse_rss_feed(rss_feed_url)
print(result_string)
