"""
Teste dos novos feeds RSS adicionados ao sistema
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.rss_service import RSSService, RSS_FEEDS

def test_feed(category, url):
    """Testa um feed RSS específico"""
    print(f"\n{'='*70}")
    print(f"Categoria: {category}")
    print(f"URL: {url}")
    print(f"{'='*70}")
    
    try:
        headlines = RSSService.fetch_headlines(category)
        
        if headlines:
            print(f"✅ {len(headlines)} headlines encontrados")
            print(f"\nPrimeiros 3 headlines:")
            for i, headline in enumerate(headlines[:3], 1):
                print(f"  {i}. {headline['title'][:70]}...")
                print(f"     Fonte: {headline['source']}")
            return True
        else:
            print(f"⚠️  Nenhum headline encontrado (feed pode estar vazio)")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao buscar feed: {e}")
        return False

def main():
    print("="*70)
    print("🧪 TESTE DOS NOVOS FEEDS RSS")
    print("="*70)
    
    print(f"\n📊 Total de feeds configurados: {len(RSS_FEEDS)}")
    
    # Testar alguns feeds selecionados
    feeds_to_test = [
        "Brasil",
        "Mundo", 
        "Política",
        "UOL",
        "Terra",
        "Estadão",
        "Folha",
        "Veja",
        "BBC Brasil",
        "Carta Capital"
    ]
    
    results = {}
    
    for category in feeds_to_test:
        if category in RSS_FEEDS:
            url = RSS_FEEDS[category]
            results[category] = test_feed(category, url)
        else:
            print(f"\n⚠️  Categoria '{category}' não encontrada")
            results[category] = False
    
    # Resumo
    print("\n" + "="*70)
    print("📊 RESUMO DOS TESTES")
    print("="*70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for category, result in results.items():
        status = "✅ OK" if result else "❌ FALHOU"
        print(f"{status:12} - {category}")
    
    print("\n" + "="*70)
    print(f"Resultado: {passed}/{total} feeds funcionando ({passed/total*100:.1f}%)")
    print("="*70)
    
    # Mostrar todas as categorias disponíveis
    print("\n📝 TODAS AS CATEGORIAS DISPONÍVEIS:")
    print("-" * 70)
    for i, category in enumerate(RSS_FEEDS.keys(), 1):
        print(f"{i:2}. {category}")
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())
