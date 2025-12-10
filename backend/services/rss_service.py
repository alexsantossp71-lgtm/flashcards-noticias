"""
RSS Service - Fetch headlines from RSS feeds
"""

import feedparser
import logging
import random
from typing import List, Dict
from datetime import datetime, timedelta
from config import RSS_TIMEOUT, RSS_MAX_ITEMS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# RSS feeds from major Brazilian and international news sites
# Organized by category with diverse sources
RSS_FEEDS = {
    # Notícias Gerais - Fontes Principais
    "Brasil": "https://g1.globo.com/rss/g1/brasil/",
    "Mundo": "https://feeds.bbci.co.uk/portuguese/rss.xml",  # BBC Brasil
    "Política": "https://www.cartacapital.com.br/feed/",  # Carta Capital
    
    # Categorias Tradicionais
    "Esportes": "https://rss.uol.com.br/feed/esporte.xml",  # UOL
    "Tecnologia": "https://g1.globo.com/rss/g1/tecnologia/",  # G1
    "Economia": "https://rss.uol.com.br/feed/economia.xml",  # UOL
    
    # Fontes Diversificadas por Veículo
    "UOL": "https://rss.uol.com.br/feed/noticias.xml",  # Feed de notícias UOL
    "Terra": "https://www.terra.com.br/noticias/rss.xml",  # Feed principal Terra
    "Estadão": "https://www.estadao.com.br/arc/outboundfeeds/feeds/rss/sections/brasil/",
    "Veja": "https://veja.abril.com.br/rss/",
    "G1": "https://g1.globo.com/dynamo/rss2.xml",  # Feed geral G1
    "BBC Brasil": "https://feeds.bbci.co.uk/portuguese/rss.xml",
    "DW Brasil": "https://follow.it/dw-brasil/rss",  # Deutsche Welle
    "Carta Capital": "https://www.cartacapital.com.br/feed/",
}

# Categorias que agregam múltiplas fontes para diversidade
CATEGORY_AGGREGATION = {
    "Brasil": ["Brasil", "G1", "UOL", "Estadão", "Veja"],
    "Mundo": ["Mundo", "BBC Brasil", "DW Brasil"],
    "Política": ["Política", "Carta Capital", "Estadão"],
    "Esportes": ["Esportes", "UOL", "Terra"],
    "Tecnologia": ["Tecnologia", "G1", "UOL"],
    "Economia": ["Economia", "UOL", "Estadão", "Veja"],
}


class RSSService:
    @staticmethod
    def _extract_source_from_url(url: str, category: str) -> str:
        """
        Extract the news site name from the RSS feed URL or article link
        """
        if not url:
            return category
        
        url_lower = url.lower()
        
        # Map domains to news site names
        if 'g1.globo.com' in url_lower:
            return 'G1'
        elif 'uol.com.br' in url_lower:
            return 'UOL'
        elif 'folha.uol.com.br' in url_lower or 'folha.com.br' in url_lower:
            return 'Folha de S.Paulo'
        elif 'estadao.com.br' in url_lower:
            return 'Estadão'
        elif 'terra.com' in url_lower:
            return 'Terra'
        elif 'veja.abril.com.br' in url_lower or 'veja.com' in url_lower:
            return 'Veja'
        elif 'cartacapital.com.br' in url_lower:
            return 'Carta Capital'
        elif 'dw.com' in url_lower or 'follow.it/dw-brasil' in url_lower:
            return 'DW Brasil'
        elif 'globo.com' in url_lower:
            return 'Globo'
        elif 'cnn.com.br' in url_lower:
            return 'CNN Brasil'
        elif 'bbcbrasil' in url_lower or 'bbc.com' in url_lower or 'bbci.co.uk' in url_lower:
            return 'BBC Brasil'
        else:
            return category
    
    @staticmethod
    def fetch_headlines(category: str) -> List[Dict]:
        """
        Fetch raw headlines from RSS feed for given category
        For thematic categories, aggregates from multiple sources
        Only returns headlines from the last 48 hours
        """
        # Check if this category should aggregate multiple sources
        sources_to_fetch = CATEGORY_AGGREGATION.get(category, [category])
        
        try:
            logger.info(f"Fetching RSS feeds for category: {category} from {len(sources_to_fetch)} sources")
            
            # Calculate cutoff time (48 hours ago)
            cutoff_time = datetime.now() - timedelta(hours=48)
            
            all_headlines = []
            
            # Fetch from each source
            for source_category in sources_to_fetch:
                rss_url = RSS_FEEDS.get(source_category)
                if not rss_url:
                    continue
                    
                try:
                    feed = feedparser.parse(rss_url)
                    
                    if feed.bozo:
                        logger.warning(f"RSS feed parsing warning for {source_category}: {feed.bozo_exception}")
                    
                    for entry in feed.entries:
                        # Check if entry has published date
                        published_parsed = entry.get("published_parsed")
                        
                        # Filter by date - only include entries from last 48 hours
                        if published_parsed:
                            entry_date = datetime(*published_parsed[:6])
                            if entry_date < cutoff_time:
                                continue  # Skip entries older than 48 hours
                        
                        # Extract source from entry source, article link, or feed URL
                        entry_source = entry.get("source", {}).get("title", "")
                        article_link = entry.get("link", "")
                        
                        # Try to get real source name
                        if entry_source and entry_source != source_category:
                            source = entry_source
                        else:
                            # Extract from article link or fall back to feed URL
                            source = RSSService._extract_source_from_url(article_link, source_category)
                            if source == source_category:
                                source = RSSService._extract_source_from_url(rss_url, source_category)
                        
                        all_headlines.append({
                            "title": entry.get("title", ""),
                            "link": article_link,
                            "source": source
                        })
                
                except Exception as e:
                    logger.error(f"Error fetching from {source_category}: {e}")
                    continue
            
            # Remove duplicates based on title (case insensitive)
            seen_titles = set()
            unique_headlines = []
            for headline in all_headlines:
                title_lower = headline["title"].lower()
                if title_lower not in seen_titles:
                    seen_titles.add(title_lower)
                    unique_headlines.append(headline)
            
            # Shuffle to mix sources and limit to 20
            random.shuffle(unique_headlines)
            final_headlines = unique_headlines[:20]
            
            logger.info(f"Fetched {len(final_headlines)} unique headlines from {category} (last 48 hours)")
            return final_headlines
            
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed for {category}: {e}")
            return []
