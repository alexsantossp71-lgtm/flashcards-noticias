#!/usr/bin/env python
"""
Test Image Generation with ComfyUI for Trump/Putin news
"""
import sys
import time
import os
sys.path.insert(0, '.')

# Force ComfyUI backend
os.environ['IMAGE_BACKEND'] = 'comfyui'

from services.image_service import ImageService

image_service = ImageService()

# Prompts gerados pelo Ollama
image_prompts = [
    "Image of a news headline with a red 'X' symbol on it, set against a modern cityscape at sunset.",
    "A photo of the White House's Oval Office with a desk and two chairs, including one for Donald Trump.",
    "Image of a TV screen showing a soccer match with the American flag waving in the background.",
]

print("\n" + "="*80)
print("TESTE DE GERAÇÃO COM COMFYUI - Notícia Trump/Putin")
print("="*80 + "\n")

print(f"📸 Backend: {image_service.backend}")
print(f"🔧 ComfyUI URL: {image_service.comfyui_url if hasattr(image_service, 'comfyui_url') else 'N/A'}")
print(f"📋 Testando com {len(image_prompts)} prompts")
print("\n" + "="*80 + "\n")

results = []
total_time = 0

for i, prompt in enumerate(image_prompts, 1):
    print(f"🎨 Gerando imagem {i}/{len(image_prompts)}...")
    print(f"Prompt: {prompt[:70]}...")
    
    start = time.time()
    try:
        image_base64, source = image_service.generate_image(
            prompt=prompt,
            style_prompt="modern, clean, vibrant colors, photorealistic"
        )
        
        elapsed = time.time() - start
        total_time += elapsed
        
        if image_base64:
            size_kb = len(image_base64) / 1024
            print(f"✅ Sucesso com {source}! ({elapsed:.1f}s, {size_kb:.1f} KB)")
            results.append({
                "card": i, 
                "success": True, 
                "time": elapsed, 
                "size": size_kb,
                "source": source
            })
        else:
            print(f"❌ Falhou (retornou None)")
            results.append({"card": i, "success": False, "time": elapsed})
            
    except Exception as e:
        elapsed = time.time() - start
        total_time += elapsed
        print(f"❌ Erro: {str(e)[:150]}")
        results.append({"card": i, "success": False, "time": elapsed, "error": str(e)})
    
    print()

# Sumário
print("="*80)
print("RESUMO:")
print("="*80 + "\n")

successful = sum(1 for r in results if r["success"])
failed = len(results) - successful

print(f"✅ Sucesso: {successful}/{len(image_prompts)}")
print(f"❌ Falhas: {failed}/{len(image_prompts)}")
print(f"⏱️  Tempo total: {total_time:.1f}s")

if successful > 0:
    avg_time = sum(r["time"] for r in results if r["success"]) / successful
    avg_size = sum(r.get("size", 0) for r in results if r["success"]) / successful
    print(f"\n📊 Estatísticas (imagens geradas):")
    print(f"   - Tempo médio: {avg_time:.1f}s por imagem")
    print(f"   - Tamanho médio: {avg_size:.1f} KB")
    print(f"   - Backend usado: {results[0].get('source', 'N/A')}")

print("\n" + "="*80)
print("✅ Teste concluído!")
print("="*80 + "\n")
