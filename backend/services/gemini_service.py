"""
Gemini Service - Fast Text Generation with Google Gemini API
Handles all text generation (headlines, flashcard content, prompts)
10-20x faster than Ollama with better accuracy
"""

import google.generativeai as genai
import json
import logging
from typing import Dict, List, Optional
from config import GEMINI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiService:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in .env file")
        
        genai.configure(api_key=GEMINI_API_KEY)
        # Use experimental flash model with less restrictive filtering
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        logger.info("✅ Gemini 2.0 Flash Experimental initialized")
    
    def check_health(self) -> bool:
        """Check if Gemini API is accessible"""
        try:
            # Simple test generation
            response = self.model.generate_content("Say 'OK'")
            return response.text.strip().upper() == "OK"
        except Exception as e:
            logger.error(f"Gemini health check failed: {e}")
            return False
    
    def generate_flashcard_content(
        self, 
        headline: str, 
        url: str, 
        style_prompt: str,
        source: str = "Web",
        article_text: str = None
    ) -> Dict:
        """
        Generate complete flashcard content (7 cards, TikTok metadata, image prompts)
        Uses Gemini for fast and accurate generation
        """
        system_prompt = """Você é um Editor Especialista em Mídias Sociais para TikTok e Instagram Stories no Brasil.
Você cria conteúdo viral e envolvente que respeita o tom original da notícia. TODO O CONTEÚDO DEVE SER EM PORTUGUÊS BRASILEIRO."""
        
        # Build context
        if article_text and len(article_text) > 100:
            context = f"""MANCHETE: "{headline}" de {source}

CONTEÚDO COMPLETO DO ARTIGO:
{article_text[:3000]}
"""
        else:
            context = f"""MANCHETE: "{headline}" de {source}
(Nota: Texto completo do artigo não disponível, crie baseado na manchete)
"""
        
        fact_instruction = "- Use FATOS REAIS do artigo acima" if article_text else "- Infira progressão lógica da história a partir da manchete"
        
        prompt = f"""{context}
Crie um roteiro para um carrossel "Flash de Notícias" baseado nesta notícia.

RESTRIÇÕES:
1. TOM: Combine com o tom ORIGINAL (sério=formal, bizarro=irônico, político=crítico/jornalístico)
2. ESTRUTURA: Gere EXATAMENTE 7 cards:
   - Card 1: APENAS a Manchete + Nome da Fonte. SEM texto de resumo.
   - Cards 2-7: Conte a história em 6 cards progressivos usando APENAS FATOS REAIS do artigo
   {fact_instruction}

3. TAMANHO DOS CARDS 2-7:
   - MÁXIMO 90 caracteres por card (incluindo espaços e pontuação)
   - Isso garante NO MÁXIMO 4 linhas de texto quando renderizado
   - Conte cada caractere. Seja EXTREMAMENTE conciso.

4. CONTEÚDO DOS CARDS 2-7 (CRÍTICO):
   - Cada card deve ser um RESUMO CONCISO de um fato específico da notícia
   - Use o TOM ORIGINAL do artigo (sério=formal, bizarro=irônico, político=jornalístico)
   - EXTRAIA informações diretamente do texto. Use fraseamento fiel ao original.
   - Seja DIRETO e OBJETIVO. Vá direto ao ponto.
   - Máximo 4 linhas = 90 caracteres
   - NUNCA use frases genéricas como "Continue lendo", "Leia mais", "Saiba mais"
   - NUNCA invente fatos. Use APENAS informações do artigo.
   - Cada card deve adicionar uma nova informação relevante da história.

5. PROMPTS DE IMAGEM (CRÍTICO):
   - LEIA o texto do card antes de criar o prompt
   - O prompt da imagem DEVE REFLETIR o conteúdo ESPECÍFICO do card
   - Use informações do artigo completo para enriquecer o prompt visual
   - Descreva: pessoas, objetos, ações, cenários, cores, emoções
   - Seja LITERAL e VISUAL (evite conceitos abstratos)
   - LIMITE: MÁXIMO 200 caracteres (o estilo será adicionado depois)

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5

🔗 Leia mais: {url}

Retorne APENAS esta estrutura JSON:
{{
  "tiktokTitle": "string em português",
  "tiktokSummary": "2 parágrafos + 5 hashtags (formato: #Tag1 #Tag2 #Tag3 #Tag4 #Tag5) + link (🔗 Leia mais: URL)",
  "flashcards": [
    {{"text": "{headline}\\n{source}", "imagePrompt": "detailed English prompt"}},
    {{"text": "Card 2 texto EM PORTUGUÊS (fato extraído)", "imagePrompt": "..."}},
    ...
  ]
}}
"""
        
        try:
            logger.info("Generating flashcard content with Gemini...")
            
            # MAXIMALLY permissive safety settings (all valid categories)
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            response = self.model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                )
            )
            
            # Check if response was blocked
            if not response.parts:
                logger.error(f"Gemini blocked the response. Reason: {response.prompt_feedback}")
                raise ValueError(f"Response blocked by Gemini safety filters: {response.prompt_feedback}")
            
            # Parse JSON response
            content = response.text.strip()
            
            # Clean markdown code blocks if present
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()
            
            result = json.loads(content)
            
            # Validate structure
            if 'flashcards' not in result:
                raise ValueError("Missing 'flashcards' in response")
            
            num_cards = len(result.get('flashcards', []))
            if num_cards < 6 or num_cards > 8:
                logger.warning(f"Got {num_cards} cards, expected 6-8. Accepting anyway.")
            
            logger.info(f"✅ Gemini generated {num_cards} cards successfully")
            return result
            
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise
    
    def curate_headlines(self, raw_headlines: List[Dict], category: str, count: int = 15) -> List[Dict]:
        """
        Simple headline filtering - just return the raw headlines
        (Can be enhanced with Gemini if needed)
        """
        logger.info(f"Using simple headline filtering for {category}")
        
        curated = []
        for h in raw_headlines[:count]:
            curated.append({
                "headline": h.get("title", ""),
                "source": h.get("source", category),
                "url": h.get("link", "")
            })
        
        return curated
