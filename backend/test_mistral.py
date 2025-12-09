"""
Test script to verify Mistral speed and rule compliance for flashcard generation
"""
import requests
import json
import time

# Test headline
test_data = {
    "headline": "Aviões chineses apontaram radares de ataque potencial a caças do Japão, diz governo japonês",
    "url": "https://g1.globo.com/mundo/noticia/2025/12/07/avioes-chineses-apontaram-radares-de-ataque-potencial-a-cacas-do-japao-diz-governo-japones.ghtml",
    "stylePrompt": "3D Pixar style, colorful, vibrant",
    "source": "G1"
}

print("=" * 80)
print("TESTE DE VELOCIDADE E OBEDIÊNCIA ÀS REGRAS - MISTRAL")
print("=" * 80)
print(f"\nManchete: {test_data['headline']}")
print(f"Fonte: {test_data['source']}")
print("\n" + "=" * 80)

# Call API
print("\n⏱️  Iniciando geração de conteúdo...")
start_time = time.time()

try:
    response = requests.post(
        "http://127.0.0.1:8000/api/generate-content",
        json=test_data,
        timeout=120
    )
    
    end_time = time.time()
    elapsed = end_time - start_time
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n✅ Geração concluída em {elapsed:.2f} segundos")
        print("\n" + "=" * 80)
        print("VERIFICAÇÃO DE REGRAS")
        print("=" * 80)
        
        # Rule 1: Number of cards
        num_cards = len(result.get('flashcards', []))
        print(f"\n1. Número de cards: {num_cards}")
        if num_cards == 7:
            print("   ✅ CORRETO (esperado: 7)")
        else:
            print(f"   ❌ INCORRETO (esperado: 7, recebido: {num_cards})")
        
        # Rule 2: Card 1 structure
        card1 = result['flashcards'][0] if result.get('flashcards') else {}
        card1_text = card1.get('text', '')
        print(f"\n2. Card 1 (Título + Fonte):")
        print(f"   Texto: {card1_text[:100]}...")
        has_newline = '\n' in card1_text
        if has_newline:
            parts = card1_text.split('\n', 1)
            print(f"   ✅ Tem quebra de linha")
            print(f"   - Linha 1 (Título): {parts[0]}")
            if len(parts) > 1:
                print(f"   - Linha 2 (Fonte): {parts[1]}")
        else:
            print(f"   ⚠️  Sem quebra de linha (esperado: Título\\nFonte)")
        
        # Rule 3: Character limits for cards 2-7
        print(f"\n3. Limite de caracteres (Cards 2-7: máx 144 chars):")
        for i, card in enumerate(result['flashcards'][1:7], start=2):
            text = card.get('text', '')
            char_count = len(text)
            status = "✅" if char_count <= 144 else "❌"
            print(f"   Card {i}: {char_count} chars {status}")
            if char_count > 144:
                print(f"      Texto: {text[:80]}...")
        
        # Rule 4: Language check
        print(f"\n4. Idioma (deve ser português):")
        sample_texts = [card.get('text', '')[:50] for card in result['flashcards'][:3]]
        print(f"   Amostras:")
        for i, text in enumerate(sample_texts, 1):
            print(f"   - Card {i}: {text}...")
        
        # Check for English words
        english_indicators = ['the', 'and', 'is', 'are', 'was', 'were', 'in', 'on', 'at']
        all_text = ' '.join([card.get('text', '').lower() for card in result['flashcards']])
        found_english = [word for word in english_indicators if f' {word} ' in f' {all_text} ']
        if found_english:
            print(f"   ⚠️  Possíveis palavras em inglês encontradas: {found_english}")
        else:
            print(f"   ✅ Aparenta estar em português")
        
        # Rule 5: TikTok metadata
        print(f"\n5. Metadados TikTok:")
        title = result.get('tiktokTitle', '')
        summary = result.get('tiktokSummary', '')
        print(f"   Título: {title}")
        print(f"   Resumo: {len(summary)} caracteres")
        
        # Count hashtags
        hashtag_count = summary.count('#')
        print(f"   Hashtags: {hashtag_count} (esperado: 5)")
        if hashtag_count == 5:
            print(f"   ✅ CORRETO")
        else:
            print(f"   ⚠️  Diferente do esperado")
        
        # Full output
        print("\n" + "=" * 80)
        print("RESULTADO COMPLETO (JSON)")
        print("=" * 80)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    else:
        print(f"\n❌ Erro: Status {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ Erro na requisição: {e}")

print("\n" + "=" * 80)
print("FIM DO TESTE")
print("=" * 80)
