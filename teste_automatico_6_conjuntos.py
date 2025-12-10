"""
Teste Automático - Gerar 6 Conjuntos de Flashcards
Cada conjunto usa uma fonte e estilo diferente
"""

import requests
import time
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

# Configuração dos 6 conjuntos de teste
CONJUNTOS = [
    {"nome": "Conjunto 1", "categoria": "uol", "estilo": "3D Pixar style, colorful, vibrant, cartoon"},
    {"nome": "Conjunto 2", "categoria": "g1", "estilo": "photorealistic, high quality, detailed, professional photography"},
    {"nome": "Conjunto 3", "categoria": "cnn", "estilo": "anime style, manga, vibrant colors, detailed"},
    {"nome": "Conjunto 4", "categoria": "estadao", "estilo": "minimalist, clean, simple, modern design"},
    {"nome": "Conjunto 5", "categoria": "terra", "estilo": "cyberpunk style, neon, futuristic, dark"},
    {"nome": "Conjunto 6", "categoria": "veja", "estilo": "watercolor painting, artistic, soft colors"},
]

def buscar_headlines(categoria):
    """Busca headlines de uma categoria"""
    print(f"  📰 Buscando headlines de {categoria.upper()}...")
    response = requests.post(
        f"{API_URL}/api/headlines",
        json={"category": categoria, "count": 5},
        timeout=30
    )
    response.raise_for_status()
    data = response.json()
    return data["headlines"]

def gerar_conteudo(headline, estilo):
    """Gera conteúdo dos flashcards"""
    print(f"  🤖 Gerando conteúdo com IA...")
    response = requests.post(
        f"{API_URL}/api/generate-content",
        json={
            "headline": headline["headline"],
            "url": headline["url"],
            "stylePrompt": estilo,
            "source": headline["source"]
        },
        timeout=180  # 3 minutos
    )
    response.raise_for_status()
    return response.json()

def gerar_imagem(prompt, estilo, texto, card_number):
    """Gera uma única imagem"""
    print(f"    🎨 Gerando imagem {card_number}...")
    response = requests.post(
        f"{API_URL}/api/generate-image",
        json={
            "prompt": prompt,
            "stylePrompt": estilo,
            "text": texto,
            "cardNumber": card_number
        },
        timeout=120  # 2 minutos por imagem
    )
    response.raise_for_status()
    return response.json()

def salvar_post(headline, conteudo, cards_completos):
    """Salva o post completo"""
    print(f"  💾 Salvando post...")
    response = requests.post(
        f"{API_URL}/api/save-post",
        json={
            "category": "Geral",
            "headline": headline["headline"],
            "source": headline["source"],
            "url": headline["url"],
            "tiktokTitle": conteudo["tiktokTitle"],
            "tiktokSummary": conteudo["tiktokSummary"],
            "cards": cards_completos,
            "generationTime": 0,
            "modelUsed": {}
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()

def push_github():
    """Faz push para GitHub"""
    print(f"  📤 Enviando para GitHub...")
    try:
        response = requests.post(f"{API_URL}/api/push-to-github", timeout=60)
        if response.ok:
            result = response.json()
            print(f"  ✅ {result.get('message', 'Push realizado')}")
            return True
        else:
            print(f"  ⚠️ Push falhou, mas post foi salvo")
            return False
    except Exception as e:
        print(f"  ⚠️ Erro no push: {e}")
        return False

def gerar_conjunto(config, numero):
    """Gera um conjunto completo de flashcards"""
    print(f"\n{'='*80}")
    print(f"{config['nome'].upper()} - {config['categoria'].upper()} + {config['estilo'][:30]}...")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        # 1. Buscar headlines
        headlines = buscar_headlines(config["categoria"])
        if not headlines:
            print(f"  ❌ Nenhuma headline encontrada para {config['categoria']}")
            return False
        
        headline = headlines[0]  # Primeira headline
        print(f"  ✅ Headline selecionada: {headline['headline'][:60]}...")
        
        # 2. Gerar conteúdo
        conteudo = gerar_conteudo(headline, config["estilo"])
        flashcards = conteudo.get("flashcards", [])
        print(f"  ✅ Gerados {len(flashcards)} flashcards")
        
        # 3. Gerar imagens para cada card
        cards_completos = []
        for i, card in enumerate(flashcards, 1):
            imagem_data = gerar_imagem(
                card.get("imagePrompt", ""),
                config["estilo"],
                card.get("text", ""),
                i
            )
            
            cards_completos.append({
                "text": card.get("text", ""),
                "imagePrompt": card.get("imagePrompt", ""),
                "imageBase64": imagem_data["imageBase64"],
                "imageSource": "local"
            })
            print(f"    ✅ Card {i}/{len(flashcards)} completo")
        
        # 4. Salvar post
        save_result = salvar_post(headline, conteudo, cards_completos)
        print(f"  ✅ Post salvo: {save_result['id']}")
        
        # 5. Push para GitHub
        push_github()
        
        elapsed = time.time() - start_time
        print(f"\n  ⏱️  Tempo total: {elapsed/60:.1f} minutos")
        print(f"  ✅ {config['nome']} CONCLUÍDO!")
        
        return True
        
    except Exception as e:
        print(f"  ❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("\n" + "="*80)
    print("TESTE AUTOMÁTICO - 6 CONJUNTOS DE FLASHCARDS")
    print("="*80)
    print(f"Início: {datetime.now().strftime('%H:%M:%S')}")
    
    total_start = time.time()
    sucessos = 0
    falhas = 0
    
    for i, config in enumerate(CONJUNTOS, 1):
        sucesso = gerar_conjunto(config, i)
        if sucesso:
            sucessos += 1
        else:
            falhas += 1
        
        # Pequena pausa entre conjuntos
        if i < len(CONJUNTOS):
            print(f"\n⏸️  Aguardando 5 segundos antes do próximo conjunto...")
            time.sleep(5)
    
    total_elapsed = time.time() - total_start
    
    print("\n" + "="*80)
    print("TESTE COMPLETO!")
    print("="*80)
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    print(f"⏱️  Tempo total: {total_elapsed/60:.1f} minutos ({total_elapsed/3600:.2f} horas)")
    print(f"Término: {datetime.now().strftime('%H:%M:%S')}")
    print("="*80)

if __name__ == "__main__":
    main()
