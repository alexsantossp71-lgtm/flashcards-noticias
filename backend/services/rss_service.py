"""
RSS Service - Fetch headlines from RSS feeds
"""

import feedparser
import logging
from typing import List, Dict
from config import RSS_TIMEOUT, RSS_MAX_ITEMS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Direct RSS feeds from major Brazilian news sites
# Mix of G1 and UOL - only using working/reliable feeds
RSS_FEEDS = {
    "Brasil": "https://g1.globo.com/rss/g1/brasil/",
    "Mundo": "https://g1.globo.com/rss/g1/mundo/",
    "Política": "https://g1.globo.com/rss/g1/politica/",
    "Esportes": "https://rss.uol.com.br/feed/esporte.xml",  # UOL
    "Tecnologia": "https://g1.globo.com/rss/g1/tecnologia/",
    "Economia": "https://rss.uol.com.br/feed/economia.xml"  # UOL
}


class RSSService:
    @staticmethod
    def fetch_headlines(category: str) -> List[Dict]:
        """
        Fetch raw headlines from RSS feed for given category
        """
        rss_url = RSS_FEEDS.get(category, RSS_FEEDS["Brasil"])
        
        try:
            logger.info(f"Fetching RSS feed for category: {category}")
            feed = feedparser.parse(rss_url)
            
            if feed.bozo:
                logger.warning(f"RSS feed parsing warning: {feed.bozo_exception}")
            
            headlines = []
            for entry in feed.entries[:RSS_MAX_ITEMS]:
                headlines.append({
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "source": entry.get("source", {}).get("title", category)
                })
            
            logger.info(f"Fetched {len(headlines)} headlines from {category}")
            return headlines
            
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed for {category}: {e}")
            return []
