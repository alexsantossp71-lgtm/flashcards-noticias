"""
Script de Diagnóstico - Análise de Prompts de Imagem
Objetivo: Identificar por que as imagens não refletem bem o conteúdo das legendas
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from services.rss_service import RSSService
from services.ollama_service import OllamaService
from services.scraper_service import article_scraper
import json
from datetime import datetime

def main():
    print("=" * 80)
    print("DIAGNÓSTICO: Análise de Geração de Conteúdo e Prompts")
    print("=" * 80)
    
    rss = RSSService()
    ollama = OllamaService()
    
    # Buscar 3 notícias de diferentes fontes
    categorias = ["uol", "g1", "cnn"]
    analise = {
        "timestamp": datetime.now().isoformat(),
        "noticias": []
    }
    
    for categoria in categorias:
        print(f"\n{'=' * 80}")
        print(f"CATEGORIA: {categoria.upper()}")
        print("=" * 80)
        
        # Buscar headlines
        headlines = rss.fetch_headlines(categoria)
        if not headlines:
            print(f"❌ Nenhuma headline encontrada para {categoria}")
            continue
        
        # Pegar primeira notícia
        headline_data = headlines[0]
        headline = headline_data.get('title', '')
        url = headline_data.get('link', '')
        
        print(f"\n📰 HEADLINE: {headline}")
        print(f"🔗 URL: {url}")
        
        # Scrape do artigo
        article_text = None
        if url:
            article_data = article_scraper.scrape_article(url)
            if article_data and article_data.get('content'):
                article_text = article_data['content']
                print(f"✅ Artigo extraído: {len(article_text)} caracteres")
        
        # Gerar conteúdo completo
        print("\n🤖 Gerando conteúdo com Ollama...")
        try:
            content = ollama.generate_flashcard_content(
                headline=headline,
                url=url,
                style_prompt="Fotografia realista, cinematográfica",
                source=categoria,
                article_text=article_text
            )
            
            # Extrair dados
            noticia_analise = {
                "categoria": categoria,
                "headline": headline,
                "url": url,
                "tiktok_title": content.get('tiktokTitle', ''),
                "tiktok_summary": content.get('tiktokSummary', ''),
                "cards": []
            }
            
            print(f"\n📱 TÍTULO TIKTOK: {content.get('tiktokTitle', '')}")
            print(f"\n📝 RESUMO TIKTOK:\n{content.get('tiktokSummary', '')}")
            
            flashcards = content.get('flashcards', [])
            print(f"\n🎴 FLASHCARDS GERADOS: {len(flashcards)}")
            
            for i, card in enumerate(flashcards, 1):
                caption = card.get('caption', '')
                image_prompt = card.get('imagePrompt', '')
                
                print(f"\n{'─' * 80}")
                print(f"CARD {i}")
                print(f"{'─' * 80}")
                print(f"📝 LEGENDA ({len(caption)} chars):")
                print(f"   {caption}")
                print(f"\n🎨 PROMPT DE IMAGEM ({len(image_prompt)} chars):")
                print(f"   {image_prompt}")
                
                # Análise de correspondência
                palavras_legenda = set(caption.lower().split())
                palavras_prompt = set(image_prompt.lower().split())
                overlap = palavras_legenda.intersection(palavras_prompt)
                
                print(f"\n📊 ANÁLISE DE CORRESPONDÊNCIA:")
                print(f"   - Palavras na legenda: {len(palavras_legenda)}")
                print(f"   - Palavras no prompt: {len(palavras_prompt)}")
                print(f"   - Palavras em comum: {len(overlap)} ({len(overlap)/len(palavras_legenda)*100:.1f}%)")
                print(f"   - Palavras comuns: {', '.join(list(overlap)[:10])}")
                
                noticia_analise["cards"].append({
                    "numero": i,
                    "legenda": caption,
                    "legenda_tamanho": len(caption),
                    "image_prompt": image_prompt,
                    "prompt_tamanho": len(image_prompt),
                    "overlap_percentual": len(overlap)/len(palavras_legenda)*100 if palavras_legenda else 0,
                    "palavras_comuns": list(overlap)
                })
            
            analise["noticias"].append(noticia_analise)
            
        except Exception as e:
            print(f"❌ Erro ao gerar conteúdo: {e}")
            import traceback
            traceback.print_exc()
    
    # Salvar análise completa
    output_file = Path(__file__).parent / "ANALISE_PROMPTS.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analise, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 80}")
    print(f"✅ Análise salva em: {output_file}")
    print("=" * 80)
    
    # Gerar relatório markdown
    relatorio = gerar_relatorio_markdown(analise)
    relatorio_file = Path(__file__).parent / "ANALISE_PROMPTS.md"
    with open(relatorio_file, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(f"✅ Relatório markdown salvo em: {relatorio_file}")
    print("=" * 80)

def gerar_relatorio_markdown(analise):
    """Gera relatório em markdown para fácil visualização"""
    md = f"""# 🔍 Análise de Geração de Prompts de Imagem

**Data:** {analise['timestamp']}

## 🎯 Objetivo

Identificar por que as imagens geradas não refletem adequadamente o conteúdo das legendas dos flashcards.

## 📊 Resultados

"""
    
    for i, noticia in enumerate(analise['noticias'], 1):
        md += f"""
---

### Notícia {i}: {noticia['categoria'].upper()}

**Headline:** {noticia['headline']}

**📱 Título TikTok:** {noticia['tiktok_title']}

**📝 Resumo TikTok:**
```
{noticia['tiktok_summary']}
```

#### 🎴 Flashcards

"""
        
        for card in noticia['cards']:
            md += f"""
##### Card {card['numero']}

**📝 Legenda ({card['legenda_tamanho']} caracteres):**
```
{card['legenda']}
```

**🎨 Prompt de Imagem ({card['prompt_tamanho']} caracteres):**
```
{card['image_prompt']}
```

**📊 Análise de Correspondência:**
- **Overlap:** {card['overlap_percentual']:.1f}% de palavras em comum
- **Palavras comuns:** {', '.join(card['palavras_comuns'][:15])}

**❓ Problema Identificado:**
- [ ] Prompt muito genérico
- [ ] Prompt não reflete contexto específico da legenda
- [ ] Excesso de instruções técnicas de estilo
- [ ] Falta de elementos-chave mencionados na legenda

---
"""
    
    md += """
## 🔧 Recomendações

### Problemas Potenciais:

1. **Prompts muito genéricos** - Não incorporam detalhes específicos da legenda
2. **Excesso de jargão técnico** - Muitas instruções de estilo que diluem o conteúdo real
3. **Falta de contexto** - Prompts não usam informações do artigo completo
4. **Baixo overlap** - Poucas palavras-chave da legenda aparecem no prompt

### Soluções Propostas:

1. ✅ **Aumentar peso do conteúdo da legenda** no prompt
2. ✅ **Reduzir instruções de estilo genéricas**
3. ✅ **Incluir palavras-chave específicas** da legenda
4. ✅ **Usar contexto do artigo** para enriquecer o prompt
5. ✅ **Adicionar elementos visuais concretos** mencionados na legenda

"""
    
    return md

if __name__ == "__main__":
    main()
