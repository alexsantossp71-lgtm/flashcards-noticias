"""
Teste de URLs alternativas para Folha de S.Paulo
"""

import feedparser

urls = {
    "Folha Original": "https://www1.folha.uol.com.br/feed/",
    "Folha www": "https://www.folha.uol.com.br/feed/",
    "Folha Poder": "https://www1.folha.uol.com.br/poder/feed/",
    "Folha Cotidiano": "https://www1.folha.uol.com.br/cotidiano/feed/",
}

for name, url in urls.items():
    print(f"\n{'='*70}")
    print(f"Testando: {name}")
    print(f"URL: {url}")
    
    try:
        feed = feedparser.parse(url)
        print(f"Bozo: {feed.bozo}, Entries: {len(feed.entries)}")
        
        if feed.entries:
            print(f"✅ FUNCIONA! Título: {feed.entries[0].get('title', '')[:60]}")
        else:
            print(f"⚠️  Feed vazio")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
