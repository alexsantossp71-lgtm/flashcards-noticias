# -*- coding: utf-8 -*-
"""
Teste do PromptEnhancer Service com notícia da Amazônia
"""

from backend.services.prompt_enhancer_service import PromptEnhancerService

service = PromptEnhancerService()

print("\n" + "="*80)
print("TESTE: Notícia sobre descoberta na Amazônia")
print("="*80 + "\n")

# Dados da notícia REAL
headline = "Cientistas descobrem nova espécie na Amazônia"
style = "anime style, manga, vibrant colors, detailed"

# Testar cada card
cards_texts = [
    "Cientistas descobrem nova espécie na Amazônia\nBBC",
    "Fato 1: A espécie foi descoberta em uma região remota da Amazônia, no Brasil.",
    "Fato 2: A nova espécie é um tipo de planta endêmica, ou seja, não é encontrada em nenhum outro lugar do mundo.",
    "Fato 3: Os cientistas acreditam que a espécie pode ter evoluído em isolamento durante milhões de anos.",
    "Fato 4: A descoberta é considerada uma das mais importantes da década para os científicos que estudam a biodiversidade da Amazônia."
]

for i, caption in enumerate(cards_texts, 1):
    print(f"{'='*80}")
    print(f"CARD {i}")
    print(f"{'='*80}")
    print(f"Legenda: {caption[:80]}...")
    
    prompt = service.enhance_prompt(
        caption=caption,
        headline=headline,
        article_text=None,  # Sem artigo
        style_prompt=style
    )
    
    print(f"\nPrompt Gerado:")
    print(f"{prompt}\n")

print("="*80)
print("ANÁLISE:")
print("="*80)
print("✅ Cada card deve ter prompt DIFERENTE")
print("✅ Prompts devem mencionar palavras-chave do caption")
print("✅ NÃO deve mencionar 'María Corina Machado'")
print("✅ Deve ter contexto 'science'")
print("="*80)
