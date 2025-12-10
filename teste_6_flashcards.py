"""
Teste Automático Simplificado - 6 Flash cards com Estilos Diferentes
Usa URLs diretas de notícias ao invés de RSS
"""

import requests
import time
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

# 6 Notícias diretas com estilos diferentes
TESTES = [
    {
        "nome": "Teste 1",
        "url": "https://www1.folha.uol.com.br/cotidiano/2025/12/sp-tem-maior-numero-de-mortes-por-dengue.shtml",
        "headline": "SP tem maior número de mortes por dengue",
        "source": "Folha",
        "estilo": "3D Pixar style, colorful, vibrant, cartoon"
    },
    {
        "nome": "Teste 2",
        "url": "https://g1.globo.com/politica/noticia/2025/12/10/congresso-aprova-reforma-administrativa.ghtml",
        "headline": "Congresso aprova reforma administrativa",
        "source": "G1",
        "estilo": "photorealistic, high quality, detailed, professional photography"
    },
    {
        "nome": "Teste 3",
        "url": "https://www.terra.com.br/economia/bitcoin-atinge-novo-recorde-historico.html",
        "headline": "Bitcoin atinge novo recorde histórico",
        "source": "Terra",
        "estilo": "anime style, manga, vibrant colors, detailed"
    },
    {
        "nome": "Teste 4",
        "url": "https://veja.abril.com.br/saude/oms-alerta-para-nova-variante.html",
        "headline": "OMS alerta para nova variante",
        "source": "Veja",
        "estilo": "minimalist, clean, simple, modern design"
    },
    {
        "nome": "Teste 5",
        "url": "https://www.estadao.com.br/internacional/tensao-aumenta-no-oriente-medio.htm",
        "headline": "Tensão aumenta no Oriente Médio",
        "source": "Estadão",
        "estilo": "cyberpunk style, neon, futuristic, dark"
    },
    {
        "nome": "Teste 6",
        "url": "https://www.bbc.com/portuguese/articles/mudancas-climaticas-afetam-agricultura-brasil",
        "headline": "Mudanças climáticas afetam agricultura no Brasil",
        "source": "BBC Brasil",
        "estilo": "watercolor painting, artistic, soft colors"
    },
]

print("\n" + "="*80)
print("TESTE AUTOMÁTICO SIMPLIFICADO - 6 FLASHCARDS COM ESTILOS DIFERENTES")
print("="*80)
print(f"Início: {datetime.now().strftime('%H:%M:%S')}\n")

def gerar_flashcard_completo(config, numero):
    """Gera um flashcard completo"""
    print(f"{'='*80}")
    print(f"{config['nome'].upper()}: {config['headline']}")
    print(f"Estilo: {config['estilo'][:50]}...")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        # 1. Gerar conteúdo
        print("  🤖 Gerando conteúdo com Ollama...")
        content_response = requests.post(
            f"{API_URL}/api/generate-content",
            json={
                "headline": config["headline"],
                "url": config["url"],
                "stylePrompt": config["estilo"],
                "source": config["source"]
            },
            timeout=180
        )
        
        if not content_response.ok:
            print(f"  ❌ Erro no servidor: {content_response.status_code}")
            print(f"     {content_response.text[:200]}")
            return False
        
        content = content_response.json()
        flashcards = content.get("flashcards", [])
        print(f"  ✅ {len(flashcards)} flashcards gerados")
        
        # 2. Gerar imagens
        cards_completos = []
        for i, card in enumerate(flashcards, 1):
            print(f"  🎨 Gerando imagem {i}/{len(flashcards)}...")
            
            img_response = requests.post(
                f"{API_URL}/api/generate-image",
                json={
                    "prompt": card.get("imagePrompt", ""),
                    "stylePrompt": config["estilo"],
                    "text": card.get("text", ""),
                    "cardNumber": i
                },
                timeout=120
            )
            
            if img_response.ok:
                img_data = img_response.json()
                cards_completos.append({
                    "text": card.get("text", ""),
                    "imagePrompt": card.get("imagePrompt", ""),
                    "imageBase64": img_data["imageBase64"],
                    "imageSource": "local"
                })
                print(f"    ✅ Card {i} completo")
            else:
                print(f"    ❌ Erro na imagem {i}: {img_response.status_code}")
                return False
        
        # 3. Salvar post
        print("  💾 Salvando post...")
        save_response = requests.post(
            f"{API_URL}/api/save-post",
            json={
                "category": "Geral",
                "headline": config["headline"],
                "source": config["source"],
                "url": config["url"],
                "tiktokTitle": content.get("tiktokTitle", ""),
                "tiktokSummary": content.get("tiktokSummary", ""),
                "cards": cards_completos,
                "generationTime": 0,
                "modelUsed": {}
            },
            timeout=30
        )
        
        if save_response.ok:
            result = save_response.json()
            print(f"  ✅ Post salvo: {result['id']}")
        else:
            print(f"  ❌ Erro ao salvar: {save_response.status_code}")
            return False
        
        # 4. Push para GitHub
        print("  📤 Enviando para GitHub...")
        try:
            push_response = requests.post(f"{API_URL}/api/push-to-github", timeout=60)
            if push_response.ok:
                push_result = push_response.json()
                print(f"  ✅ {push_result.get('message', 'Push OK')}")
            else:
                print(f"  ⚠️ Push falhou (código {push_response.status_code}), mas post foi salvo")
        except:
            print(f"  ⚠️ Push não disponível, mas post foi salvo")
        
        elapsed = time.time() - start_time
        print(f"\n  ⏱️  Tempo: {elapsed/60:.1f} minutos")
        print(f"  ✅ {config['nome']} CONCLUÍDO!\n")
        
        return True
        
    except Exception as e:
        print(f"  ❌ ERRO: {e}\n")
        return False

# Executar testes
total_start = time.time()
sucessos = 0
falhas = 0

for i, config in enumerate(TESTES, 1):
    if gerar_flashcard_completo(config, i):
        sucessos += 1
    else:
        falhas += 1
    
    # Pausa entre testes
    if i < len(TESTES):
        print(f"⏸️  Pausa de 3 segundos antes do próximo teste...\n")
        time.sleep(3)

total_elapsed = time.time() - total_start

print("\n" + "="*80)
print("TESTE COMPLETO!")
print("="*80)
print(f"✅ Sucessos: {sucessos}/{len(TESTES)}")
print(f"❌ Falhas: {falhas}/{len(TESTES)}")
print(f"⏱️  Tempo total: {total_elapsed/60:.1f} minutos ({total_elapsed/3600:.2f} horas)")
print(f"Término: {datetime.now().strftime('%H:%M:%S')}")
print("="*80)
