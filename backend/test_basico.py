"""
Teste Básico do Sistema FlashNews
Verifica os componentes principais do sistema
"""

import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se os módulos principais podem ser importados"""
    print("🔍 Testando importações dos módulos...")
    
    try:
        from config import RSS_TIMEOUT, RSS_MAX_ITEMS, OLLAMA_MODEL, IMAGE_BACKEND, TEXT_BACKEND
        print("✅ Config importado com sucesso")
        print(f"   - RSS_MAX_ITEMS: {RSS_MAX_ITEMS}")
        print(f"   - RSS_TIMEOUT: {RSS_TIMEOUT}")
        print(f"   - OLLAMA_MODEL: {OLLAMA_MODEL}")
        print(f"   - TEXT_BACKEND: {TEXT_BACKEND}")
        print(f"   - IMAGE_BACKEND: {IMAGE_BACKEND}")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar config: {e}")
        return False

def test_rss_service():
    """Testa o serviço de RSS"""
    print("\n🔍 Testando RSS Service...")
    
    try:
        from services.rss_service import RSSService
        print("✅ RSSService importado com sucesso")
        
        # Testar fetch de headlines
        print("   Buscando headlines da categoria 'Brasil'...")
        headlines = RSSService.fetch_headlines("Brasil")
        
        if headlines:
            print(f"✅ {len(headlines)} headlines encontrados")
            print(f"   Exemplo: {headlines[0]['title'][:60]}...")
            print(f"   Fonte: {headlines[0]['source']}")
            return True
        else:
            print("⚠️  Nenhum headline encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro no RSS Service: {e}")
        return False

def test_scraper_service():
    """Testa o serviço de scraper"""
    print("\n🔍 Testando Scraper Service...")
    
    try:
        from services.scraper_service import ArticleScraperService
        print("✅ ArticleScraperService importado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar ArticleScraperService: {e}")
        return False

def test_ollama_service():
    """Testa o serviço Ollama"""
    print("\n🔍 Testando Ollama Service...")
    
    try:
        from services.ollama_service import OllamaService
        print("✅ OllamaService importado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar OllamaService: {e}")
        return False

def test_image_service():
    """Testa o serviço de imagens"""
    print("\n🔍 Testando Image Service...")
    
    try:
        from services.image_service import ImageService
        print("✅ ImageService importado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar ImageService: {e}")
        return False

def test_storage_service():
    """Testa o serviço de storage"""
    print("\n🔍 Testando Storage Service...")
    
    try:
        from services.storage_service import StorageService
        print("✅ StorageService importado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar StorageService: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🚀 TESTE BÁSICO DO SISTEMA FLASHNEWS")
    print("=" * 60)
    
    tests = [
        ("Importações de Config", test_imports),
        ("RSS Service", test_rss_service),
        ("Scraper Service", test_scraper_service),
        ("Ollama Service", test_ollama_service),
        ("Image Service", test_image_service),
        ("Storage Service", test_storage_service),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Erro inesperado em {name}: {e}")
            results.append((name, False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {name}")
    
    print("\n" + "=" * 60)
    print(f"Resultado: {passed}/{total} testes passaram ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! Sistema OK!")
        return 0
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    exit(main())
