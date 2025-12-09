#!/usr/bin/env python
"""
Test RSS + Scraper: Fetch 5th headline from Economia and scrape full content
"""
import sys
sys.path.insert(0, '.')

from services.rss_service import RSSService
from services.scraper_service import article_scraper

rss_service = RSSService()

print("\n" + "="*80)
print("TESTE: RSS Economia - 5ª Notícia + Scraping Completo")
print("="*80 + "\n")

# 1. Buscar headlines de Economia
print("📰 Buscando headlines de Economia...")
headlines = rss_service.fetch_headlines('Economia')

if len(headlines) < 5:
    print(f"❌ Apenas {len(headlines)} headlines encontradas (precisa de pelo menos 5)")
    sys.exit(1)

# 2. Pegar a 5ª notícia (índice 4)
fifth_headline = headlines[4]

print(f"✅ Encontradas {len(headlines)} headlines\n")
print("="*80)
print("5ª NOTÍCIA SELECIONADA:")
print("="*80)
print(f"Título: {fifth_headline['title']}")
print(f"Fonte: {fifth_headline['source']}")
print(f"URL: {fifth_headline['link']}")
print("="*80 + "\n")

# 3. Fazer scraping da notícia
print("🔍 Fazendo scraping do conteúdo completo...\n")
article_data = article_scraper.scrape_article(fifth_headline['link'])

if article_data and article_data.get('content'):
    print("✅ SCRAPING BEM-SUCEDIDO!\n")
    print("="*80)
    print("METADADOS EXTRAÍDOS:")
    print("="*80)
    print(f"Título Extraído: {article_data.get('title', 'N/A')}")
    print(f"Autor: {article_data.get('author', 'N/A')}")
    print(f"Data de Publicação: {article_data.get('publish_date', 'N/A')}")
    print(f"Tamanho do Conteúdo: {len(article_data.get('content', ''))} caracteres")
    print("="*80 + "\n")
    
    print("="*80)
    print("CONTEÚDO COMPLETO DA NOTÍCIA:")
    print("="*80 + "\n")
    print(article_data['content'])
    print("\n" + "="*80)
    
    # Mostrar preview que será enviado ao Ollama
    content_for_ollama = article_data['content'][:3000]
    print(f"\n📤 PREVIEW DO QUE SERÁ ENVIADO AO OLLAMA (primeiros 3000 chars):")
    print("="*80 + "\n")
    print(content_for_ollama)
    print("\n" + "="*80)
    print(f"✅ Total sendo enviado ao Ollama: {len(content_for_ollama)} caracteres")
    
else:
    print("❌ SCRAPING FALHOU!")
    print(f"URL pode estar protegida ou ser um redirect do Google News")
    print(f"Neste caso, o Ollama usará apenas o título da manchete")
