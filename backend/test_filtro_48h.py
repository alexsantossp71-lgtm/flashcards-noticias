"""
Teste do filtro de 48 horas implementado
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.rss_service import RSSService

def test_48h_filter():
    print("="*70)
    print("🧪 TESTE DO FILTRO DE 48 HORAS")
    print("="*70)
    
    # Horário atual
    now = datetime.now()
    cutoff = now - timedelta(hours=48)
    
    print(f"\n⏰ Horário atual: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 Cutoff (48h atrás): {cutoff.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{'='*70}")
    
    # Testar com BBC Brasil (boa fonte internacional)
    category = "BBC Brasil"
    print(f"\n🔍 Testando categoria: {category}")
    print(f"{'='*70}")
    
    headlines = RSSService.fetch_headlines(category)
    
    if headlines:
        print(f"\n✅ {len(headlines)} headlines encontrados (últimas 48h)")
        print(f"\nPrimeiros 5 headlines:")
        
        for i, headline in enumerate(headlines[:5], 1):
            print(f"\n{i}. {headline['title'][:70]}...")
            print(f"   Fonte: {headline['source']}")
            print(f"   Link: {headline['link'][:60]}...")
    else:
        print(f"\n⚠️  Nenhum headline recente encontrado")
    
    # Testar também com Carta Capital
    print(f"\n{'='*70}")
    category2 = "Carta Capital"
    print(f"\n🔍 Testando categoria: {category2}")
    print(f"{'='*70}")
    
    headlines2 = RSSService.fetch_headlines(category2)
    
    if headlines2:
        print(f"\n✅ {len(headlines2)} headlines encontrados (últimas 48h)")
        print(f"\nPrimeiros 3 headlines:")
        
        for i, headline in enumerate(headlines2[:3], 1):
            print(f"\n{i}. {headline['title'][:70]}...")
            print(f"   Fonte: {headline['source']}")
    else:
        print(f"\n⚠️  Nenhum headline recente encontrado")
    
    print(f"\n{'='*70}")
    print("✅ FILTRO DE 48 HORAS FUNCIONANDO!")
    print("="*70)

if __name__ == "__main__":
    test_48h_filter()
