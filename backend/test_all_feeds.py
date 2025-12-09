#!/usr/bin/env python
"""
Quick test for new RSS feeds (G1 + UOL mix)
"""
import sys
sys.path.insert(0, '.')

from services.rss_service import RSSService

rss_service = RSSService()

categories = ["Brasil", "Mundo", "Política", "Esportes", "Tecnologia", "Economia"]

print("\n" + "="*80)
print("TESTE: RSS Feeds de G1 + UOL")
print("="*80 + "\n")

for cat in categories:
    print(f"📰 Testando {cat}...")
    headlines = rss_service.fetch_headlines(cat)
    if headlines:
        print(f"✅ {len(headlines)} headlines encontradas")
        print(f"   Exemplo: {headlines[0]['title'][:80]}...")
        print(f"   Fonte: {headlines[0]['source']}")
    else:
        print(f"❌ FALHA ao buscar headlines de {cat}")
    print()

print("="*80)
print("✅ Teste concluído!")
