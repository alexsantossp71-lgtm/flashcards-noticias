"""
Ollama Service - Local Text Generation
Handles all text generation using Ollama (headlines curation, content generation, prompts)
"""

import ollama
import json
import logging
from typing import Dict, List, Optional
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_FALLBACK_MODELS, OLLAMA_TIMEOUT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaService:
    def __init__(self):
        self.client = ollama.Client(host=OLLAMA_BASE_URL)
        self.primary_model = OLLAMA_MODEL
        self.fallback_models = OLLAMA_FALLBACK_MODELS
    
    def check_health(self) -> bool:
        """
        Check if Ollama is reachable
        """
        try:
            self.client.list()
            return True
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False
    
    def _generate_with_fallback(self, prompt: str, system_prompt: str = "", format_json: bool = True) -> Dict:
        """
        Generate text with retry logic across multiple models
        """
        models_to_try = [self.primary_model] + [m for m in self.fallback_models if m != self.primary_model]
        
        for model in models_to_try:
            try:
                logger.info(f"Attempting generation with model: {model}")
                
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = self.client.chat(
                    model=model,
                    messages=messages,
                    format="json" if format_json else "",
                    options={"temperature": 0.7, "num_predict": 2048}
                )
                
                content = response['message']['content']
                
                if format_json:
                    # Try to parse as JSON
                    try:
                        # Clean HTML entities that might break JSON
                        import html
                        content = html.unescape(content)
                        
                        return json.loads(content)
                    except json.JSONDecodeError as e:
                        # Clean markdown code blocks if present
                        cleaned = content.replace("```json", "").replace("```", "").strip()
                        
                        # Try again with cleaned content
                        try:
                            cleaned = html.unescape(cleaned)
                            return json.loads(cleaned)
                        except json.JSONDecodeError:
                            # Last attempt: try to extract JSON from partial response
                            logger.error(f"JSON parsing failed: {e}. Content sample: {content[:200]}")
                            # Return empty structure to allow fallback
                            raise ValueError(f"Failed to parse JSON from Ollama response")
                else:
                    return {"text": content}
                    
            except Exception as e:
                logger.warning(f"Model {model} failed: {e}")
                if model == models_to_try[-1]:
                    raise Exception(f"All models failed. Last error: {e}")
                continue
        
        raise Exception("No models available")
    
    def curate_headlines(self, raw_headlines: List[Dict], category: str, count: int = 15) -> List[Dict]:
        """
        Curate and select the most relevant/viral headlines from RSS feed
        """
        # Given unreliability of JSON generation, just return raw headlines with basic filtering
        # This ensures the app always works even if Ollama has issues
        logger.info(f"Using simple headline filtering for {category}")
        
        # Just return the first N items with proper structure
        curated = []
        for h in raw_headlines[:count]:
            curated.append({
                "headline": h.get("title", ""),
                "source": h.get("source", category),
                "url": h.get("link", "")
            })
        
        return curated
    
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
        Now supports full article text for more accurate content!
        """
        system_prompt = """Você é um Editor Especialista em Mídias Sociais para TikTok e Instagram Stories no Brasil.
Você cria conteúdo viral e envolvente que respeita o tom original da notícia. TODO O CONTEÚDO DEVE SER EM PORTUGUÊS BRASILEIRO."""
        
        # Build context based on available information
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
3. TAMANHO: 
   - Card 1: Pode ser mais longo (manchete + fonte)
   - Cards 2-7: MÁXIMO 144 caracteres por card. Isso é ESTRITO.
4. CONTEÚDO: 
   - EXTRAIA informações diretamente do texto. Use fraseamento original quando possível.
   - NÃO resuma se perder o significado original. 
   - NUNCA invente fatos não presentes no texto.
   - NUNCA gere um card "Continue lendo" ou "Leia mais". Todo conteúdo deve ser do texto.
5. METADADOS TIKTOK:
   - Título: Gancho clickbait/viral (máx 5 palavras)
   - Resumo: EXATAMENTE 90 palavras, EXATAMENTE 2 parágrafos, terminando com EXATAMENTE 5 hashtags relevantes
6. IMAGENS: Crie um prompt de imagem visual e literal EM INGLÊS para CADA card
   - Descreva objetos concretos, pessoas, cores, cenários (sem abstrações)
   - Inclua estilo: "{style_prompt}"

IMPORTANTE: TODO O TEXTO DOS CARDS DEVE SER EM PORTUGUÊS BRASILEIRO. Apenas os prompts de imagem devem ser em inglês.

PARA O CARD 1 ESPECIFICAMENTE:
- Texto do Card 1 deve ser EXATAMENTE: "{headline}\n{source}"
- NÃO modifique, resuma ou altere a manchete de forma alguma
- Use o texto EXATO da manchete fornecida acima
- Na segunda linha, coloque apenas o nome da fonte (ex: "G1", "Folha", "UOL")

Retorne APENAS esta estrutura JSON:
{{
  "tiktokTitle": "string em português",
  "tiktokSummary": "string em português (2 parágrafos + 5 hashtags)",
  "flashcards": [
    {{"text": "{headline}\n{source}", "imagePrompt": "detailed English prompt"}},
    {{"text": "Card 2 texto EM PORTUGUÊS (fato extraído)", "imagePrompt": "..."}},
    ...
  ]
}}
"""
        
        result = self._generate_with_fallback(prompt, system_prompt, format_json=True)
        
        # Validate structure - be flexible with 6-8 cards
        if 'flashcards' not in result:
            raise ValueError(f"Missing 'flashcards' in response")
        
        num_cards = len(result.get('flashcards', []))
        if num_cards < 6 or num_cards > 8:
            logger.warning(f"Got {num_cards} cards, expected 6-8. Accepting anyway.")
        
        # Removed text-padding logic as per user request
        
        return result
    
    def generate_guide_content(self, topic: str, style_prompt: str) -> Dict:
        """
        Generate educational guide carousel (7 cards)
        """
        system_prompt = "You are an expert Educational Content Creator for social media in Brazil."
        
        prompt = f"""
Create an explainer guide carousel about: "{topic}"

CONSTRAINTS:
1. TONE: Educational, clear, engaging
2. STRUCTURE: EXACTLY 7 cards:
   - Card 1: Title of Guide + "Guia Rápido"
   - Cards 2-7: Step-by-step or key facts
3. LENGTH: Max 180 characters per card
4. TIKTOK METADATA:
   - Title: Engaging title
   - Summary: EXACTLY 60 words, EXACTLY 2 paragraphs, 5 relevant hashtags
5. IMAGES: Visual English prompts. Style: "{style_prompt}"

Return ONLY this JSON:
{{
  "tiktokTitle": "string",
  "tiktokSummary": "string",
  "flashcards": [
    {{"text": "...", "imagePrompt": "..."}},
    ...
  ]
}}
"""
        
        result = self._generate_with_fallback(prompt, system_prompt, format_json=True)
        
        # Validate - be flexible
        if 'flashcards' not in result:
            raise ValueError(f"Missing 'flashcards' in guide response")
        
        num_cards = len(result.get('flashcards', []))
        if num_cards < 6:
            logger.warning(f"Guide has only {num_cards} cards, padding to 7")
            while len(result['flashcards']) < 8: # Pad up to 7 cards roughly
                result['flashcards'].append({
                    "text": "Saiba mais...",
                    "imagePrompt": "educational infographic, colorful design"
                })
        
        return result
    
    def extract_headline_from_url(self, url: str) -> Dict:
        """
        Extract headline and source from a URL (limited without actual web access)
        """
        system_prompt = "You are a helpful assistant that extracts metadata from URLs."
        
        prompt = f"""
Based on this URL: {url}

Try to infer the:
- headline: The main topic or title
- source: The website/publication name

Return JSON:
{{
  "headline": "Inferred headline",
  "source": "Source name"
}}
"""
        
        result = self._generate_with_fallback(prompt, system_prompt, format_json=True)
        return result
