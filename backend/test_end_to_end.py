"""
Teste Abrangente End-to-End do FlashNews
Testa: RSS → Scraping → Ollama → Geração de 5 Cards

Valida todas as 14 fontes RSS
"""

import sys
import os
from datetime import datetime
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.rss_service import RSSService, RSS_FEEDS
from services.scraper_service import ArticleScraperService
from services.ollama_service import OllamaService

def test_end_to_end():
    print("="*80)
    print("🧪 TESTE ABRANGENTE END-TO-END - FLASHNEWS AI")
    print("="*80)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total de fontes RSS: {len(RSS_FEEDS)}")
    print("="*80)
    
    rss_service = RSSService()
    scraper_service = ArticleScraperService()
    ollama_service = OllamaService()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "total_sources": len(RSS_FEEDS),
        "tests": []
    }
    
    # Verificar Ollama
    print("\n📡 Verificando Ollama...")
    ollama_ok = ollama_service.check_health()
    if not ollama_ok:
        print("❌ ERRO: Ollama não está rodando!")
        print("   Execute 'ollama serve' em outro terminal")
        return
    print("✅ Ollama está rodando")
    
    # Testar cada fonte RSS
    for category, url in RSS_FEEDS.items():
        test_result = {
            "category": category,
            "url": url,
            "rss_ok": False,
            "scraping_ok": False,
            "ollama_ok": False,
            "cards_ok": False,
            "errors": []
        }
        
        print(f"\n{'='*80}")
        print(f"📰 Testando: {category}")
        print(f"URL: {url}")
        print("-"*80)
        
        # 1. Teste RSS
        try:
            print(f"1️⃣ Buscando headlines...")
            headlines = rss_service.fetch_headlines(category)
            if headlines and len(headlines) > 0:
                test_result["rss_ok"] = True
                test_result["headlines_count"] = len(headlines)
                print(f"   ✅ {len(headlines)} headlines encontrados (últimas 48h)")
                
                # Pegar primeiro headline para testar
                headline = headlines[0]
                print(f"   📌 Testando: {headline['title'][:60]}...")
                test_result["test_headline"] = headline['title']
                test_result["test_url"] = headline['link']
                
                # 2. Teste Scraping
                try:
                    print(f"2️⃣ Fazendo scraping do artigo...")
                    article = scraper_service.scrape_article(headline['link'])
                    if article and len(article.get('content', '')) > 100:
                        test_result["scraping_ok"] = True
                        test_result["article_length"] = len(article['content'])
                        print(f"   ✅ Artigo extraído: {len(article['content'])} caracteres")
                        
                        # 3. Teste Ollama
                        try:
                            print(f"3️⃣ Gerando conteúdo com Ollama...")
                            content = ollama_service.generate_flashcard_content(
                                headline=headline['title'],
                                url=headline['link'],
                                style_prompt="photorealistic",
                                source=headline['source'],
                                article_text=article['content']
                            )
                            
                            test_result["ollama_ok"] = True
                            print(f"   ✅ Conteúdo gerado")
                            
                            # 4. Validar Cards
                            if 'flashcards' in content:
                                num_cards = len(content['flashcards'])
                                test_result["num_cards"] = num_cards
                                
                                if num_cards == 5:
                                    test_result["cards_ok"] = True
                                    print(f"   ✅ {num_cards} cards gerados (correto!)")
                                else:
                                    print(f"   ⚠️  {num_cards} cards (esperado: 5)")
                                    test_result["errors"].append(f"Wrong card count: {num_cards}")
                                
                                # Validar hashtags e link
                                summary = content.get('tiktokSummary', '')
                                has_hashtags = summary.count('#') >= 5
                                has_link = '🔗' in summary or 'Leia mais' in summary
                                
                                test_result["has_hashtags"] = has_hashtags
                                test_result["has_link"] = has_link
                                
                                if not has_hashtags:
                                    print(f"   ⚠️  Faltam hashtags")
                                    test_result["errors"].append("Missing hashtags")
                                
                                if not has_link:
                                    print(f"   ⚠️  Falta link")
                                    test_result["errors"].append("Missing link")
                                
                            else:
                                print(f"   ❌ 'flashcards' não encontrado no JSON")
                                if 'keys' in content:
                                    print(f"      Keys: {content.keys()}")
                                test_result["errors"].append("Missing flashcards key")
                                
                        except Exception as e:
                            print(f"   ❌ Erro Ollama: {e}")
                            test_result["errors"].append(f"Ollama error: {str(e)}")
                    else:
                        print(f"   ❌ Artigo muito curto ou vazio")
                        test_result["errors"].append("Article too short")
                        
                except Exception as e:
                    print(f"   ❌ Erro Scraping: {e}")
                    test_result["errors"].append(f"Scraping error: {str(e)}")
            else:
                print(f"   ❌ Nenhum headline nas últimas 48h")
                test_result["errors"].append("No recent headlines")
                
        except Exception as e:
            print(f"   ❌ Erro RSS: {e}")
            test_result["errors"].append(f"RSS error: {str(e)}")
        
        # Adicionar resultado
        results["tests"].append(test_result)
        
        # Summary do teste
        if test_result["cards_ok"]:
            print(f"✅ SUCESSO COMPLETO")
        elif test_result["ollama_ok"]:
            print(f"⚠️  PARCIAL (Ollama OK, mas problemas nos cards)")
        elif test_result["scraping_ok"]:
            print(f"⚠️  PARCIAL (Scraping OK, Ollama falhou)")
        elif test_result["rss_ok"]:
            print(f"⚠️  PARCIAL (RSS OK, Scraping falhou)")
        else:
            print(f"❌ FALHA TOTAL")
    
    # Estatísticas finais
    print(f"\n{'='*80}")
    print("📊 ESTATÍSTICAS FINAIS")
    print("="*80)
    
    total = len(results["tests"])
    rss_success = sum(1 for t in results["tests"] if t["rss_ok"])
    scraping_success = sum(1 for t in results["tests"] if t["scraping_ok"])
    ollama_success = sum(1 for t in results["tests"] if t["ollama_ok"])
    cards_success = sum(1 for t in results["tests"] if t["cards_ok"])
    
    print(f"RSS Funcional:      {rss_success}/{total} ({rss_success/total*100:.0f}%)")
    print(f"Scraping OK:        {scraping_success}/{total} ({scraping_success/total*100:.0f}%)")
    print(f"Ollama OK:          {ollama_success}/{total} ({ollama_success/total*100:.0f}%)")
    print(f"5 Cards Corretos:   {cards_success}/{total} ({cards_success/total*100:.0f}%)")
    
    # Salvar resultado
    output_file = "teste_end_to_end_resultado.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultado completo salvo em: {output_file}")
    print("="*80)
    
    return results

if __name__ == "__main__":
    test_end_to_end()
