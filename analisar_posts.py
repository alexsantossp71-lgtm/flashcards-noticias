"""
Script de Análise - Posts Salvos
Objetivo: Analisar títulos, resumos, legendas e prompts dos posts já gerados
"""

import json
from pathlib import Path
from datetime import datetime

def analisar_post(post_path):
    """Analisa um post individual"""
    metadata_file = post_path / "metadata.json"
    
    if not metadata_file.exists():
        return None
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        post = json.load(f)
    
    analise = {
        "post_id": post.get('id', ''),
        "categoria": post.get('category', ''),
        "headline": post.get('headline', ''),
        "url": post.get('url', ''),
        "tiktok_title": post.get('tiktokTitle', ''),
        "tiktok_summary": post.get('tiktokSummary', ''),
        "cards": []
    }
    
    for i, card in enumerate(post.get('cards', []), 1):
        caption = card.get('caption', '')
        image_prompt = card.get('imagePrompt', '')
        
        # Análise de correspondência
        palavras_legenda = set(caption.lower().split())
        palavras_prompt = set(image_prompt.lower().split())
        overlap = palavras_legenda.intersection(palavras_prompt)
        
        # Remover palavras comuns (stopwords)
        stopwords = {'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'é', 'mais', 'as', 'dos', 'como', 'mas', 'ao', 'ele', 'das', 'à', 'seu', 'sua', 'ou', 'quando', 'muito', 'nos', 'já', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'você', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'numa', 'pelos', 'elas', 'qual', 'nós', 'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas'}
        overlap_significativo = overlap - stopwords
        
        analise["cards"].append({
            "numero": i,
            "legenda": caption,
            "legenda_tamanho": len(caption),
            "image_prompt": image_prompt,
            "prompt_tamanho": len(image_prompt),
            "total_palavras_legenda": len(palavras_legenda),
            "total_palavras_prompt": len(palavras_prompt),
            "overlap_total": len(overlap),
            "overlap_significativo": len(overlap_significativo),
            "overlap_percentual": len(overlap)/len(palavras_legenda)*100 if palavras_legenda else 0,
            "overlap_significativo_percentual": len(overlap_significativo)/len(palavras_legenda)*100 if palavras_legenda else 0,
            "palavras_comuns": sorted(list(overlap_significativo))[:20]
        })
    
    return analise

def main():
    print("=" * 80)
    print("ANÁLISE DE POSTS SALVOS - Legendas vs Prompts de Imagem")
    print("=" * 80)
    
    posts_dir = Path(__file__).parent / "generated_posts"
    
    # Encontrar todos os posts
    post_dirs = []
    for date_dir in sorted(posts_dir.glob("2025-*"), reverse=True):
        if date_dir.is_dir():
            for post_dir in date_dir.iterdir():
                if post_dir.is_dir() and (post_dir / "metadata.json").exists():
                    post_dirs.append(post_dir)
    
    if not post_dirs:
        print("❌ Nenhum post encontrado!")
        return
    
    print(f"\n✅ Encontrados {len(post_dirs)} posts")
    print(f"\n📊 Analisando os 3 posts mais recentes...")
    
    analises = []
    for post_dir in post_dirs[:3]:
        print(f"\n{'─' * 80}")
        print(f"Analisando: {post_dir.name}")
        analise = analisar_post(post_dir)
        if analise:
            analises.append(analise)
    
    # Salvar análise
    resultado = {
        "timestamp": datetime.now().isoformat(),
        "total_posts_analisados": len(analises),
        "posts": analises
    }
    
    output_json = Path(__file__).parent / "ANALISE_POSTS.json"
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 80}")
    print(f"✅ Análise JSON salva em: {output_json}")
    
    # Gerar relatório markdown
    relatorio = gerar_relatorio(resultado)
    output_md = Path(__file__).parent / "ANALISE_POSTS.md"
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(f"✅ Relatório Markdown salvo em: {output_md}")
    print("=" * 80)
    
    # Mostrar resumo no terminal
    mostrar_resumo(resultado)

def gerar_relatorio(resultado):
    """Gera relatório detalhado em markdown"""
    md = f"""# 🔍 Análise: Legendas vs Prompts de Imagem

**Data:** {resultado['timestamp']}  
**Posts Analisados:** {resultado['total_posts_analisados']}

---

## 🎯 Objetivo

Identificar problemas na correlação entre:
- 📝 **Legendas dos cards** (texto que aparece no flashcard)
- 🎨 **Prompts de imagem** (instruções para gerar a imagem)

---

"""
    
    for i, post in enumerate(resultado['posts'], 1):
        md += f"""
## Notícia {i}: {post['categoria'].upper()}

### 📰 Informações Gerais

- **Headline:** {post['headline']}
- **URL:** {post['url']}
- **ID:** `{post['post_id']}`

### 📱 Conteúdo TikTok

**Título:**
```
{post['tiktok_title']}
```

**Resumo:**
```
{post['tiktok_summary']}
```

---

### 🎴 Análise dos Flashcards

"""
        
        for card in post['cards']:
            md += f"""
#### Card {card['numero']}

**📝 Legenda ({card['legenda_tamanho']} caracteres):**
```
{card['legenda']}
```

**🎨 Prompt de Imagem ({card['prompt_tamanho']} caracteres):**
```
{card['image_prompt']}
```

**📊 Métricas de Correspondência:**

| Métrica | Valor |
|---------|-------|
| Palavras na legenda | {card['total_palavras_legenda']} |
| Palavras no prompt | {card['total_palavras_prompt']} |
| Palavras em comum (todas) | {card['overlap_total']} ({card['overlap_percentual']:.1f}%) |
| **Palavras significativas em comum** | **{card['overlap_significativo']} ({card['overlap_significativo_percentual']:.1f}%)** |

**🔑 Palavras-chave compartilhadas:**
```
{', '.join(card['palavras_comuns']) if card['palavras_comuns'] else 'Nenhuma palavra significativa em comum!'}
```

**❗ Problema Identificado:**

"""
            
            # Diagnóstico automático
            if card['overlap_significativo_percentual'] < 20:
                md += "- 🔴 **CRÍTICO**: Menos de 20% de overlap significativo - Prompt NÃO reflete a legenda!\n"
            elif card['overlap_significativo_percentual'] < 40:
                md += "- 🟡 **ATENÇÃO**: Overlap baixo (20-40%) - Prompt parcialmente relacionado à legenda\n"
            else:
                md += "- 🟢 **OK**: Boa correlação (>40%) entre legenda e prompt\n"
            
            if card['prompt_tamanho'] > card['legenda_tamanho'] * 3:
                md += "- ⚠️ Prompt muito mais longo que legenda - Pode ter excesso de jargão técnico\n"
            
            md += "\n---\n\n"
        
        md += "\n---\n\n"
    
    # Resumo geral e recomendações
    md += gerar_recomendacoes(resultado)
    
    return md

def gerar_recomendacoes(resultado):
    """Gera seção de recomendações baseadas na análise"""
    
    # Calcular métricas agregadas
    todos_cards = []
    for post in resultado['posts']:
        todos_cards.extend(post['cards'])
    
    if not todos_cards:
        return ""
    
    overlap_medio = sum(c['overlap_significativo_percentual'] for c in todos_cards) / len(todos_cards)
    cards_criticos = sum(1 for c in todos_cards if c['overlap_significativo_percentual'] < 20)
    cards_ok = sum(1 for c in todos_cards if c['overlap_significativo_percentual'] >= 40)
    
    md = f"""
---

## 📊 Resumo Geral

- **Total de cards analisados:** {len(todos_cards)}
-**Overlap significativo médio:** {overlap_medio:.1f}%
- **Cards críticos (< 20%):** {cards_criticos} ({cards_criticos/len(todos_cards)*100:.1f}%)
- **Cards OK (≥ 40%):** {cards_ok} ({cards_ok/len(todos_cards)*100:.1f}%)

---

## 🔧 Diagnóstico e Recomendações

### ❌ Problemas Identificados:

"""
    
    if overlap_medio < 30:
        md += """
1. **🔴 PROBLEMA CRÍTICO: Baixa correlação entre legendas e prompts**
   - Prompts de imagem estão sendo gerados de forma muito genérica
   - Não incorporam elementos específicos mencionados nas legendas
   - Resultado: Imagens que não ilustram o conteúdo do texto

"""
    
    md += """
2. **⚠️ Excesso de jargão técnico de fotografia/arte**
   - Prompts cheios de termos como "cinematográfico", "realista", "8k", etc.
   - Isso dilui o conteúdo real que deveria ser gerado
   - Modelo de imagem prioriza estilo sobre conteúdo

3. **📉 Falta de contexto específico**
   - Prompts não usam informações-chave da legenda
   - Elementos importantes da notícia não aparecem no prompt
   - Imagens genéricas que poderiam servir para qualquer notícia similar

### ✅ Soluções Propostas:

#### 1. **Reformular geração de prompts no Ollama**

```python
# ANTES (problemático):
"Fotografia cinematográfica realista em alta qualidade, 8k, iluminação natural..."

# DEPOIS (focado no conteúdo):
"[ELEMENTOS DA LEGENDA] + estilo fotográfico realista"
```

#### 2. **Aumentar peso da legenda no prompt**

- Extrair substantivos e verbos principais da legenda
- Incluir TODOS os elementos-chave no prompt
- Adicionar contexto da notícia completa

#### 3. **Reduzir jargão técnico**

- Limitar instruções de estilo a 1-2 palavras
- Focar 80% do prompt no **conteúdo**
- Apenas 20% no estilo

#### 4. **Validação de qualidade**

- Verificar overlap mínimo de 40% entre legenda e prompt
- Re-gerar prompt se correlação for muito baixa
- Usar palavras-chave extraídas da legenda

---

## 🚀 Próximos Passos

1. ✅ **Modificar `ollama_service.py`** para melhorar geração de prompts
2. ✅ **Adicionar extração de palavras-chave** das legendas
3. ✅ **Implementar validação de overlap** antes de enviar para geração de imagem
4. ✅ **Testar com 3 notícias** e verificar melhoria
5. ✅ **Ajustar parâmetros** até atingir >40% de overlap consistente

---
"""
    
    return md

def mostrar_resumo(resultado):
    """Mostra resumo colorido no terminal"""
    print("\n" + "=" * 80)
    print("📊 RESUMO DA ANÁLISE")
    print("=" * 80)
    
    for i, post in enumerate(resultado['posts'], 1):
        print(f"\n{'─' * 80}")
        print(f"NOTÍCIA {i}: {post['categoria'].upper()}")
        print(f"{'─' * 80}")
        print(f"📰 {post['headline'][:70]}...")
        
        for card in post['cards']:
            simbolo = "🔴" if card['overlap_significativo_percentual'] < 20 else "🟡" if card['overlap_significativo_percentual'] < 40 else "🟢"
            print(f"\n  {simbolo} Card {card['numero']}: {card['overlap_significativo_percentual']:.1f}% overlap")
            print(f"     📝 Legenda: {card['legenda'][:60]}...")
            print(f"     🎨 Palavras-chave no prompt: {', '.join(card['palavras_comuns'][:5])}")
    
    # Cálculo geral
    todos_cards = []
    for post in resultado['posts']:
        todos_cards.extend(post['cards'])
    
    if todos_cards:
        overlap_medio = sum(c['overlap_significativo_percentual'] for c in todos_cards) / len(todos_cards)
        print(f"\n{'=' * 80}")
        print(f"📊 OVERLAP MÉDIO: {overlap_medio:.1f}%")
        if overlap_medio < 30:
            print("🔴 CRÍTICO: Prompts NÃO refletem as legendas!")
        elif overlap_medio < 40:
            print("🟡 ATENÇÃO: Correlação baixa entre prompts e legendas")
        else:
            print("🟢 OK: Boa correlação entre prompts e legendas")
        print("=" * 80)

if __name__ == "__main__":
    main()
