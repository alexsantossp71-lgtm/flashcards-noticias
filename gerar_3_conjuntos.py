"""
Gerar 3 conjuntos de flashcards rapidamente
Com PromptEnhancerService ativo
"""

import requests
import time
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

CONJUNTOS = [
    {"nome": "Conjunto 1", "headline": "Brasil anuncia novo programa social", "source": "G1", "url": "https://g1.globo.com", "estilo": "photorealistic, high quality, detailed, professional photography"},
    {"nome": "Conjunto 2", "headline": "Cientistas descobrem nova espécie na Amazônia", "source": "BBC", "url": "https://bbc.com", "estilo": "anime style, manga, vibrant colors, detailed"},
    {"nome": "Conjunto 3", "headline": "Tecnologia revoluciona mercado financeiro", "source": "Valor", "url": "https://valor.com.br", "estilo": "cyberpunk style, neon, futuristic, dark"},
]

print(f"\n{'='*80}")
print("GERANDO 3 CONJUNTOS DE FLASHCARDS (com PromptEnhancerService)")
print(f"{'='*80}")
print(f"Início: {datetime.now().strftime('%H:%M:%S')}\n")

for i, config in enumerate(CONJUNTOS, 1):
    print(f"{'='*80}")
    print(f"{config['nome'].upper()}: {config['headline']}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        # 1. Gerar conteúdo (com PromptEnhancer automático!)
        print("  🤖 Gerando conteúdo...")
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
            print(f"  ❌ Erro {response.status_code}")
            continue
            
        content = response.json()
        flashcards = content.get("flashcards", [])
        enhanced = content.get("promptsEnhanced", False)
        
        print(f"  ✅ {len(flashcards)} flashcards gerados")
        print(f"  {'✅' if enhanced else '⚠️ '} Prompts {'ENHANCED' if enhanced else 'não enhanced'}")
        
        # Mostrar primeiro imagePrompt como exemplo
        if flashcards:
            print(f"\n  📸 Exemplo de prompt (Card 1):")
            print(f"     {flashcards[0].get('imagePrompt', 'N/A')[:100]}...\n")
        
        # 2. Gerar images
        cards_completos = []
        for idx, card in enumerate(flashcards, 1):
            print(f"  🎨 Gerando imagem {idx}/{len(flashcards)}...")
            
            img_resp = requests.post(
                f"{API_URL}/api/generate-image",
                json={
                    "prompt": card.get("imagePrompt", ""),
                    "stylePrompt": config["estilo"],
                    "text": card.get("text", ""),
                    "cardNumber": idx
                },
                timeout=120
            )
            
            if img_resp.ok:
                img_data = img_resp.json()
                cards_completos.append({
                    "text": card.get("text", ""),
                    "imagePrompt": card.get("imagePrompt", ""),
                    "imageBase64": img_data["imageBase64"],
                    "imageSource": "local"
                })
                print(f"    ✅ Card {idx} completo")
            else:
                print(f"    ❌ Erro {img_resp.status_code}")
        
        # 3. Salvar
        print("  💾 Salvando post...")
        save_resp = requests.post(
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
        
        if save_resp.ok:
            result = save_resp.json()
            print(f"  ✅ Post salvo: {result['id']}")
        
        elapsed = time.time() - start_time
        print(f"\n  ⏱️  Tempo: {elapsed/60:.1f} minutos")
        print(f"  ✅ {config['nome']} CONCLUÍDO!\n")
        
    except Exception as e:
        print(f"  ❌ ERRO: {e}\n")

print(f"\n{'='*80}")
print("TODOS OS 3 CONJUNTOS GERADOS!")
print(f"Término: {datetime.now().strftime('%H:%M:%S')}")
print(f"{'='*80}\n")
