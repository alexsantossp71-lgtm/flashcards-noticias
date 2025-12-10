"""
Teste detalhado dos feeds que falharam
"""

import feedparser
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_url(name, url):
    print(f"\n{'='*70}")
    print(f"Testando: {name}")
    print(f"URL: {url}")
    print(f"{'='*70}")
    
    try:
        feed = feedparser.parse(url)
        
        print(f"Bozo (erro de parsing): {feed.bozo}")
        if feed.bozo:
            print(f"Bozo Exception: {feed.bozo_exception}")
        
        print(f"Total de entries: {len(feed.entries)}")
        
        if feed.entries:
            print("\nPrimeiro entry:")
            entry = feed.entries[0]
            print(f"  Título: {entry.get('title', 'N/A')[:80]}")
            print(f"  Link: {entry.get('link', 'N/A')[:80]}")
            print(f"  Chaves disponíveis: {list(entry.keys())[:10]}")
        
        # Info do feed
        if hasattr(feed, 'feed'):
            print(f"\nInfo do feed:")
            print(f"  Título: {feed.feed.get('title', 'N/A')}")
            print(f"  Link: {feed.feed.get('link', 'N/A')}")
            
    except Exception as e:
        print(f"❌ ERRO: {e}")

# Testar os feeds problemáticos
failed_feeds = {
    "UOL Original": "https://rss.uol.com.br/",
    "Terra Original": "https://www.terra.com.br/rss/",
    "Folha Original": "https://www1.folha.uol.com.br/feed/",
    
    # Alternativas
    "UOL Notícias": "https://rss.uol.com.br/feed/noticias.xml",
    "Terra Feed": "https://www.terra.com/rss/noticias.xml",
}

for name, url in failed_feeds.items():
    test_url(name, url)
