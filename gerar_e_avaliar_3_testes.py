# -*- coding: utf-8 -*-
"""
Gera 3 conjuntos de flashcards e AVALIA a qualidade
"""

import requests
import time
import json
from datetime import datetime
from pathlib import Path

API_URL = "http://127.0.0.1:8000"

# 3 Notícias com temas diferentes para testar contextos
TESTES = [
    {
        "nome": "Teste 1 - CIÊNCIA",
        "headline": "Pesquisadores brasileiros descobrem nova espécie de ave na Mata Atlântica",
        "source": "Ciência",
        "url": "https://exemplo.com/ciencia",
        "estilo": "documentary style, natural photography, wildlife"
    },
    {
        "nome": "Teste 2 - POLÍTICA",
        "headline": "Congresso vota reforma tributária nesta semana",
        "source": "Política",
        "url": "https://exemplo.com/politica",
        "estilo": "photorealistic, professional news photography"
    },
    {
        "nome": "Teste 3 - TECNOLOGIA",
        "headline": "IA revoluciona diagnóstico médico no Brasil",
        "source": "Tecnologia",
        "url": "https://exemplo.com/tech",
        "estilo": "futuristic, high-tech, modern, clean"
    }
]

def avaliar_prompt(prompt, caption):
    """Avalia qualidade de um imagePrompt"""
    issues = []
    score = 100
    
    # 1. Verificar se não está vazio
    if not prompt or len(prompt) < 20:
        issues.append("❌ Prompt muito curto ou vazio")
        score -= 50
        return score, issues
    
    # 2. Verificar weighting
    if ':1.5' not in prompt and ':1.3' not in prompt:
        issues.append("⚠️ Sem weighting aplicado")
        score -= 20
    
    # 3. Verificar se é genérico
    generic_signs = ['visual in english', 'visual,', 'image of']
    if any(sign in prompt.lower() for sign in generic_signs):
        issues.append("❌ Prompt genérico detectado")
        score -= 30
    
    # 4. Calcular overlap aproximado
    caption_words = set(caption.lower().split())
    prompt_words = set(prompt.lower().split())
    
    # Remover stopwords
    stopwords = {'a', 'o', 'de', 'da', 'do', 'em', 'na', 'no', 'para', 'com', 'que', 'e'}
    caption_words = {w for w in caption_words if len(w) > 3 and w not in stopwords}
    prompt_words = {w for w in prompt_words if len(w) > 3 and w not in stopwords}
    
    if caption_words:
        overlap = len(caption_words & prompt_words) / len(caption_words) * 100
        
        if overlap < 20:
            issues.append(f"❌ Overlap baixo ({overlap:.0f}%)")
            score -= 25
        elif overlap < 40:
            issues.append(f"⚠️ Overlap médio ({overlap:.0f}%)")
            score -= 10
        else:
            issues.append(f"✅ Overlap bom ({overlap:.0f}%)")
    
    # 5. Verificar se tem atmosfera/contexto
    context_words = ['atmosphere', 'lighting', 'style', 'feel', 'environment']
    if not any(word in prompt.lower() for word in context_words):
        issues.append("⚠️ Falta contexto/atmosfera")
        score -= 15
    
    return max(score, 0), issues

def avaliar_conjunto(metadata):
    """Avalia um conjunto completo de flashcards"""
    print(f"\n{'='*80}")
    print(f"AVALIAÇÃO DO CONJUNTO")
    print(f"{'='*80}")
    
    headline = metadata.get('headline', '')
    cards = metadata.get('cards', [])
    
    print(f"\n📰 Headline: {headline}")
    print(f"📊 Total de cards: {len(cards)}")
    
    if len(cards) != 5:
        print(f"❌ ERRO: Esperado 5 cards, encontrado {len(cards)}")
        return
    
    total_score = 0
    all_issues = []
    
    for i, card in enumerate(cards, 1):
        text = card.get('text', '')
        prompt = card.get('imagePrompt', '')
        
        print(f"\n{'─'*80}")
        print(f"CARD {i}")
        print(f"{'─'*80}")
        print(f"Legenda: {text[:70]}...")
        print(f"Prompt:  {prompt[:70]}...")
        
        score, issues = avaliar_prompt(prompt, text)
        total_score += score
        all_issues.extend(issues)
        
        print(f"\n📊 Score: {score}/100")
        for issue in issues:
            print(f"   {issue}")
    
    avg_score = total_score / len(cards)
    
    print(f"\n{'='*80}")
    print(f"RESULTADO FINAL")
    print(f"{'='*80}")
    print(f"📊 Score Médio: {avg_score:.1f}/100")
    
    if avg_score >= 80:
        print(f"✅ EXCELENTE - Sistema funcionando perfeitamente!")
    elif avg_score >= 60:
        print(f"🟡 BOM - Algumas melhorias possíveis")
    elif avg_score >= 40:
        print(f"⚠️ REGULAR - Precisa ajustes")
    else:
        print(f"❌ RUIM - Correções urgentes necessárias")
    
    return avg_score

print(f"\n{'='*80}")
print(f"TESTE COMPLETO - GERAÇÃO + AVALIAÇÃO DE 3 CONJUNTOS")
print(f"{'='*80}")
print(f"Início: {datetime.now().strftime('%H:%M:%S')}\n")

resultados = []

for idx, config in enumerate(TESTES, 1):
    print(f"\n{'#'*80}")
    print(f"# {config['nome']}")
    print(f"{'#'*80}")
    
    start_time = time.time()
    
    try:
        # 1. Gerar conteúdo
        print("🤖 Gerando conteúdo...")
        response = requests.post(
            f"{API_URL}/api/generate-content",
            json={
                "headline": config["headline"],
                "url": config["url"],
                "stylePrompt": config["estilo"],
                "source": config["source"]
            },
            timeout=180
        )
        
        if not response.ok:
            print(f"❌ Erro {response.status_code}")
            continue
            
        content = response.json()
        flashcards = content.get("flashcards", [])
        prompts_enhanced = content.get("promptsEnhanced", False)
        
        print(f"✅ {len(flashcards)} flashcards gerados")
        print(f"{'✅' if prompts_enhanced else '❌'} Prompts enhanced: {prompts_enhanced}")
        
        # 2. Gerar apenas 1 imagem (para teste rápido)
        print("🎨 Gerando imagem de teste (card 1)...")
        
        img_resp = requests.post(
            f"{API_URL}/api/generate-image",
            json={
                "prompt": flashcards[0].get("imagePrompt", ""),
                "stylePrompt": config["estilo"],
                "text": flashcards[0].get("text", ""),
                "cardNumber": 1
            },
            timeout=120
        )
        
        if img_resp.ok:
            print("✅ Imagem gerada com sucesso")
        
        # 3. Preparar metadata para avaliação
        metadata = {
            "headline": config["headline"],
            "cards": flashcards
        }
        
        # 4. AVALIAR
        score = avaliar_conjunto(metadata)
        resultados.append({
            "teste": config["nome"],
            "score": score,
            "tempo": time.time() - start_time
        })
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        resultados.append({
            "teste": config["nome"],
            "score": 0,
            "erro": str(e)
        })

# RESUMO FINAL
print(f"\n{'='*80}")
print(f"RESUMO FINAL DOS 3 TESTES")
print(f"{'='*80}\n")

for resultado in resultados:
    nome = resultado['teste']
    score = resultado.get('score', 0)
    tempo = resultado.get('tempo', 0)
    
    status = "✅" if score >= 80 else "🟡" if score >= 60 else "❌"
    print(f"{status} {nome}")
    print(f"   Score: {score:.1f}/100")
    if tempo > 0:
        print(f"   Tempo: {tempo:.1f}s\n")
    else:
        print(f"   Erro: {resultado.get('erro', 'Desconhecido')}\n")

# Score médio geral
if resultados:
    avg_all = sum(r.get('score', 0) for r in resultados) / len(resultados)
    print(f"{'='*80}")
    print(f"SCORE MÉDIO GERAL: {avg_all:.1f}/100")
    
    if avg_all >= 80:
        print(f"🎉 SISTEMA APROVADO - Pronto para produção!")
    elif avg_all >= 60:
        print(f"✅ SISTEMA BOM - Funcional com pequenas melhorias")
    else:
        print(f"⚠️ SISTEMA PRECISA MELHORIAS")
    
    print(f"{'='*80}\n")

print(f"Término: {datetime.now().strftime('%H:%M:%S')}")
