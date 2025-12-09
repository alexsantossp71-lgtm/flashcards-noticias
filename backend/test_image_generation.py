#!/usr/bin/env python
"""
Test Image Generation for Trump/Putin news flashcards
"""
import sys
import time
sys.path.insert(0, '.')

from services.image_service import ImageService

image_service = ImageService()

# Prompts gerados pelo Ollama para a notícia Trump/Putin
image_prompts = [
    "Image of a news headline with a red 'X' symbol on it, set against a modern cityscape at sunset.",
    "A photo of the White House's Oval Office with a desk and two chairs, including one for Donald Trump.",
    "Image of a TV screen showing a soccer match with the American flag waving in the background.",
    "The photo of Vladimir Putin taken during Trump's statement.",
    "Image of a computer screen displaying the InVID tool with various frames and screenshots from the video.",
    "Photos of news articles and websites on a desk with a computer screen displaying them in the background.",
    "Image of the official White House website on a computer screen with a photo of Trump and Putin displayed on it."
]

print("\n" + "="*80)
print("TESTE DE GERAÇÃO DE IMAGENS - Notícia Trump/Putin")
print("="*80 + "\n")

print(f"📸 Backend de imagem configurado: {image_service.backend}")
print(f"📋 Total de prompts: {len(image_prompts)}")
print("\n" + "="*80 + "\n")

results = []
total_time = 0

for i, prompt in enumerate(image_prompts, 1):
    print(f"🎨 Gerando imagem {i}/7...")
    print(f"Prompt: {prompt[:70]}...")
    
    start = time.time()
    try:
        # Gerar imagem
        image_base64, source = image_service.generate_image(
            prompt=prompt,
            style_prompt="modern, clean, vibrant colors"
        )
        
        elapsed = time.time() - start
        total_time += elapsed
        
        if image_base64:
            size_kb = len(image_base64) / 1024
            print(f"✅ Sucesso! ({elapsed:.1f}s, {size_kb:.1f} KB)")
            results.append({"card": i, "success": True, "time": elapsed, "size": size_kb})
        else:
            print(f"❌ Falhou (retornou None)")
            results.append({"card": i, "success": False, "time": elapsed})
            
    except Exception as e:
        elapsed = time.time() - start
        total_time += elapsed
        print(f"❌ Erro: {str(e)[:100]}")
        results.append({"card": i, "success": False, "time": elapsed, "error": str(e)})
    
    print()

# Sumário
print("="*80)
print("RESUMO DOS RESULTADOS:")
print("="*80 + "\n")

successful = sum(1 for r in results if r["success"])
failed = len(results) - successful

print(f"✅ Bem-sucedidas: {successful}/7")
print(f"❌ Falhadas: {failed}/7")
print(f"⏱️  Tempo total: {total_time:.1f}s")
print(f"⏱️  Tempo médio: {total_time/len(results):.1f}s por imagem")

if successful > 0:
    avg_time = sum(r["time"] for r in results if r["success"]) / successful
    avg_size = sum(r.get("size", 0) for r in results if r["success"]) / successful
    print(f"\n📊 Imagens geradas:")
    print(f"   - Tempo médio: {avg_time:.1f}s")
    print(f"   - Tamanho médio: {avg_size:.1f} KB")

print("\n" + "="*80)

if failed > 0:
    print("\n⚠️  PROBLEMAS ENCONTRADOS:")
    for r in results:
        if not r["success"]:
            print(f"   - Card {r['card']}: {r.get('error', 'Falha desconhecida')[:80]}")
    
    print("\n💡 SUGESTÕES:")
    if "timeout" in str(results).lower():
        print("   - Pollinations timeout: Considere usar ComfyUI local")
        print("   - Ou aumente o timeout em backend/.env")
    print()
