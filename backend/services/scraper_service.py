"""
Web scraping service to extract article content from URLs
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ArticleScraperService:
    """
    Service to scrape news article content from URLs
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.timeout = 10
    
    def _decode_google_news_url(self, url: str) -> str:
        """
        Decode Google News URL to get real article URL
        Google News URLs are base64 encoded
        """
        try:
            import base64
            import urllib.parse
            
            # Extract the article ID from Google News URL
            if '/articles/' in url:
                # Get everything after /articles/
                article_id = url.split('/articles/')[-1].split('?')[0]
                
                # Try to decode base64
                try:
                    # Remove URL-safe characters
                    decoded = base64.urlsafe_b64decode(article_id + '==')
                    decoded_str = decoded.decode('utf-8', errors='ignore')
                    
                    # Look for URLs in the decoded string
                    import re
                    urls = re.findall(r'https?://[^\s<>"]+', decoded_str)
                    if urls:
                        # Return first URL that's not Google
                        for found_url in urls:
                            if 'google.com' not in found_url:
                                logger.info(f"Decoded URL: {found_url}")
                                return found_url
                except Exception as e:
                    logger.debug(f"Base64 decode failed: {e}")
            
            # Fallback: try to follow redirect with extended timeout
            logger.info("Trying HTTP redirect...")
            response = self.session.get(url, allow_redirects=True, timeout=10)
            if response.url != url and 'google.com' not in response.url:
                logger.info(f"Redirect found: {response.url}")
                return response.url
            
        except Exception as e:
            logger.warning(f"Could not decode Google News URL: {e}")
        
        return url  # Return original if all else fails
    
    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape article content from URL
        Supports Google News redirects!
        
        Returns:
            Dict with 'title', 'content', 'author', 'publish_date' or None if failed
        """
        try:
            logger.info(f"Scraping article from: {url}")
            
            # Handle Google News URLs
            if 'news.google.com' in url:
                logger.info("Detected Google News URL, decoding...")
                url = self._decode_google_news_url(url)
            
            # Fetch the page
            response = self.session.get(url, timeout=self.timeout, headers=self.session.headers)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content using common patterns
            article_data = self._extract_article_data(soup, url)
            
            if article_data and article_data.get('content'):
                logger.info(f"Successfully scraped {len(article_data['content'])} characters from {url}")
                return article_data
            else:
                logger.warning(f"Could not extract content from {url}")
                return None
                
        except requests.Timeout:
            logger.error(f"Timeout scraping {url}")
            return None
        except requests.RequestException as e:
            logger.error(f"Request error scraping {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return None
    
    def _extract_article_data(self, soup: BeautifulSoup, url: str) -> Dict[str, str]:
        """
        Extract article data from BeautifulSoup object
        """
        article_data = {
            'title': '',
            'content': '',
            'author': '',
            'publish_date': ''
        }
        
        # Extract title
        title = None
        # Try different title selectors
        title_selectors = [
            ('meta', {'property': 'og:title'}),
            ('meta', {'name': 'twitter:title'}),
            ('h1', {}),
            ('title', {})
        ]
        
        for tag, attrs in title_selectors:
            element = soup.find(tag, attrs)
            if element:
                if tag == 'meta':
                    title = element.get('content', '')
                else:
                    title = element.get_text(strip=True)
                if title:
                    break
        
        article_data['title'] = title or ''
        
        # Extract main content
        content_parts = []
        
        # Try schema.org ArticleBody
        article_body = soup.find('div', {'itemprop': 'articleBody'})
        if article_body:
            paragraphs = article_body.find_all('p')
            content_parts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        
        # Try common article containers
        if not content_parts:
            article_containers = [
                soup.find('article'),
                soup.find('div', {'class': lambda x: x and 'article' in x.lower()}),
                soup.find('div', {'class': lambda x: x and 'content' in x.lower()}),
                soup.find('div', {'id': lambda x: x and 'article' in x.lower()}),
            ]
            
            for container in article_containers:
                if container:
                    paragraphs = container.find_all('p')
                    content_parts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
                    if len(content_parts) >= 3:  # At least 3 paragraphs
                        break
        
        # Fallback: get all paragraphs from body
        if not content_parts:
            paragraphs = soup.find_all('p')
            content_parts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50]
        
        # Join paragraphs
        article_data['content'] = '\n\n'.join(content_parts[:15])  # Limit to first 15 paragraphs
        
        # Extract author
        author_selectors = [
            ('meta', {'name': 'author'}),
            ('meta', {'property': 'article:author'}),
            ('span', {'class': lambda x: x and 'author' in x.lower()}),
            ('a', {'rel': 'author'})
        ]
        
        for tag, attrs in author_selectors:
            element = soup.find(tag, attrs)
            if element:
                if tag == 'meta':
                    article_data['author'] = element.get('content', '')
                else:
                    article_data['author'] = element.get_text(strip=True)
                if article_data['author']:
                    break
        
        # Extract publish date
        date_selectors = [
            ('meta', {'property': 'article:published_time'}),
            ('meta', {'name': 'publish_date'}),
            ('time', {}),
        ]
        
        for tag, attrs in date_selectors:
            element = soup.find(tag, attrs)
            if element:
                if tag == 'meta':
                    article_data['publish_date'] = element.get('content', '')
                elif tag == 'time':
                    article_data['publish_date'] = element.get('datetime', '') or element.get_text(strip=True)
                if article_data['publish_date']:
                    break
        
        return article_data

# Global instance
article_scraper = ArticleScraperService()
