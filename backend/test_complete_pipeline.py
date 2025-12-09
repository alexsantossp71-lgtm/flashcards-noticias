#!/usr/bin/env python
"""
Complete Pipeline Test: RSS → Scraping → Ollama → Flashcards
Shows full article content, summary, captions, and image prompts
"""
import sys
import random
sys.path.insert(0, '.')

from services.rss_service import RSSService
from services.scraper_service import article_scraper
from services.ollama_service import OllamaService

rss_service = RSSService()
ollama_service = OllamaService()

print("\n" + "="*80)
print("TESTE COMPLETO DO PIPELINE FLASHNEWS AI")
print("="*80 + "\n")

# 1. Sortear categoria e notícia
categories = ["Brasil", "Mundo", "Política", "Esportes", "Tecnologia", "Economia"]
random_category = random.choice(categories)

print(f"🎲 Categoria sorteada: {random_category}")
print("📰 Buscando headlines...\n")

headlines = rss_service.fetch_headlines(random_category)
if not headlines:
    print("❌ Nenhuma headline encontrada!")
    sys.exit(1)

random_headline = random.choice(headlines)

print("="*80)
print("NOTÍCIA SORTEADA:")
print("="*80)
print(f"Título: {random_headline['title']}")
print(f"Fonte: {random_headline['source']}")
print(f"URL: {random_headline['link']}")
print("="*80 + "\n")

# 2. Fazer scraping
print("🔍 Fazendo scraping do artigo completo...\n")
article_data = article_scraper.scrape_article(random_headline['link'])

if not article_data or not article_data.get('content'):
    print("⚠️  Scraping falhou, gerando apenas com o título\n")
    article_text = None
else:
    article_text = article_data['content']
    print(f"✅ Scraping bem-sucedido: {len(article_text)} caracteres\n")
    print("="*80)
    print("CONTEÚDO COMPLETO DO ARTIGO:")
    print("="*80)
    print(article_text)
    print("\n" + "="*80 + "\n")

# 3. Gerar flashcards com Ollama
print("🤖 Gerando flashcards com Ollama...\n")

try:
    result = ollama_service.generate_flashcard_content(
        headline=random_headline['title'],
        url=random_headline['link'],
        style_prompt="modern, clean, vibrant colors",
        source=random_headline['source'],
        article_text=article_text
    )
    
    print("✅ Geração concluída!\n")
    
    # 4. Mostrar resultados
    print("="*80)
    print("RESUMO TIKTOK:")
    print("="*80)
    print(f"Título: {result.get('tiktokTitle', 'N/A')}")
    print(f"\n{result.get('tiktokSummary', 'N/A')}")
    print("\n" + "="*80 + "\n")
    
    print("="*80)
    print(f"FLASHCARDS GERADOS ({len(result.get('flashcards', []))} cards):")
    print("="*80 + "\n")
    
    for i, card in enumerate(result.get('flashcards', []), 1):
        print(f"CARD {i}:")
        print(f"{'─'*78}")
        print(f"Legenda ({len(card.get('text', ''))} chars):")
        print(f"  {card.get('text', 'N/A')}")
        print(f"\nPrompt de Imagem:")
        print(f"  {card.get('imagePrompt', 'N/A')}")
        print()
    
    print("="*80)
    print("✅ TESTE COMPLETO FINALIZADO!")
    print("="*80)
    
    # Estatísticas
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"  - Tamanho do artigo original: {len(article_text) if article_text else 0} chars")
    print(f"  - Artigo enviado ao Ollama: {min(len(article_text), 3000) if article_text else 0} chars")
    print(f"  - Total de cards gerados: {len(result.get('flashcards', []))}")
    print(f"  - Modelo usado: {ollama_service.primary_model}")
    
    total_caption_chars = sum(len(card.get('text', '')) for card in result.get('flashcards', []))
    print(f"  - Total de caracteres nas legendas: {total_caption_chars}")
    
except Exception as e:
    print(f"❌ Erro na geração: {e}")
    import traceback
    traceback.print_exc()
