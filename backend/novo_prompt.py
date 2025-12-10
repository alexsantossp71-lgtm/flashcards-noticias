"""
NOVO PROMPT SIMPLIFICADO para Ollama
Reduzido de 108 linhas para ~35 linhas
"""

# Este é o novo prompt que será usado
new_prompt_template = """
{context}

Crie EXAT AMENTE 5 flashcards sobre esta notícia em formato JSON.

ESTRUTURA JSON OBRIGATÓRIA:
{{
  "tiktokTitle": "Título viral (máx 5 palavras em português)",
  "tiktokSummary": "Parágrafo 1 contextofalo (~40 palavras).

Parágrafo 2 detalhes (~40 palavras).

#Tag1 #Tag2 #Tag3 #Tag4 #Tag5

🔗 Leia mais: {url}",
  "flashcards": [
    {{"text": "{headline}\\n{source}", "imagePrompt": "visual description in English, {style_prompt}"}},
    {{"text": "Fato 1 em português (máx 90 chars)", "imagePrompt": "visual description in English, {style_prompt}"}},
    {{"text": "Fato 2 em português (máx 90 chars)", "imagePrompt": "visual description in English, {style_prompt}"}},
    {{"text": "Fato 3 em português (máx 90 chars)", "imagePrompt": "visual description in English, {style_prompt}"}},
    {{"text": "Fato 4 em português (máx 90 chars)", "imagePrompt": "visual description in English, {style_prompt}"}}
  ]
}}

REGRAS CRÍTICAS:
1. Card 1: Manchete exata + fonte (linha separada, não modifique a manchete)
2. Cards 2-5: Fatos extraídos do artigo, máximo 90 caracteres cada
3. tiktokSummary DEVE ter: 2 parágrafos + 5 hashtags + link com emoji 🔗
4. imagePrompt em inglês, visual, específico
5. Texto dos cards em português brasileiro

GERE O JSON COMPLETO ACIMA. NÃO abrevie, NÃO use "...". COMPLETE TODOS OS 5 CARDS.
"""
