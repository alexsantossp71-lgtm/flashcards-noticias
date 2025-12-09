#!/usr/bin/env python
"""
Quick test: Generate 1 image with ComfyUI
"""
import sys
import time
import os
sys.path.insert(0, '.')

os.environ['IMAGE_BACKEND'] = 'comfyui'

from services.image_service import ImageService

image_service = ImageService()

print("\n" + "="*80)
print("TESTE RÁPIDO - 1 Imagem com ComfyUI")
print("="*80 + "\n")

prompt = "A beautiful sunset over the ocean with vibrant orange and pink colors"

print(f"📸 Backend: {image_service.backend}")
print(f"🎨 Prompt: {prompt}")
print(f"\n🔄 Gerando...\n")

start = time.time()
try:
    image_base64, source = image_service.generate_image(
        prompt=prompt,
        style_prompt="photorealistic, 8k, uhd"
    )
    
    elapsed = time.time() - start
    
    if image_base64:
        size_kb = len(image_base64) / 1024
        print(f"✅ SUCESSO!")
        print(f"   Backend usado: {source}")
        print(f"   Tempo: {elapsed:.1f}s")
        print(f"   Tamanho: {size_kb:.1f} KB")
    else:
        print(f"❌ Falhou (retornou None)")
        
except Exception as e:
    elapsed = time.time() - start
    print(f"❌ ERRO ({elapsed:.1f}s):")
    print(f"   {str(e)[:200]}")

print("\n" + "="*80 + "\n")
