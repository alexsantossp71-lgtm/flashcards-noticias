"""
Ollama Service - Local Text Generation (VERSÃO CORRIGIDA)
Handles all text generation using Ollama (headlines curation, content generation, prompts)

CORREÇÕES APLICADAS:
1. num_predict: 2048 → 3500 tokens
2. Prompt simplificado: 108 → 35 linhas
3. Validação automática de hashtags e link
4. Retry logic para 5 cards
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
                    options={"temperature": 0.7, "num_predict": 3500}  # CORREÇÃO 1: Aumentado para 3500
                )
                
                content = response['message']['content']
                
                if format_json:
                    # Try to parse as JSON
                    try:
                        # Clean HTML entities that might break JSON
                        import html
                        import re
                        content = html.unescape(content)
                        
                        # Clean markdown code blocks if present
                        cleaned = content.replace("```json", "").replace("```", "").strip()
                        
                        # Fix common Ollama JSON issues
                        def fix_json_newlines(text):
                            text = re.sub(r':\s*"([^"]*)\n([^"]*)"', r': "\1\\n\2"', text, flags=re.MULTILINE)
                            return text
                        
                        cleaned = fix_json_newlines(cleaned)
                        cleaned = html.unescape(cleaned)
                        
                        result = json.loads(cleaned)
                        logger.info(f"Successfully parsed JSON. Keys: {result.keys()}")
                        return result
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON parsing failed: {e}")
                        logger.error(f"Content (first 500 chars): {content[:500]}")
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
        logger.info(f"Using simple headline filtering for {category}")
        
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
        Generate complete flashcard content (5 cards, TikTok metadata, image prompts)
        CORREÇÃO 2: Prompt simplificado
        """
        system_prompt = """Você é um Editor Especializado em criar conteúdo viral para TikTok e Instagram Stories no Brasil.
Crie flashcards informativos, concisos e virais."""

        # Build context
        if article_text and len(article_text) > 100:
            context = f"""ARTIGO COMPLETO:
{article_text[:2000]}

MANCHETE: "{headline}"
FONTE: {source}
URL: {url}
"""
        else:
            context = f"""MANCHETE: "{headline}" de {source}
(Nota: Texto completo do artigo não disponível, crie baseado na manchete)
"""
        
        # ✅ MODO JORNALÍSTICO: Factual, direto, sem criatividade
        # Legendas longas (até 144 chars) usando trechos da notícia
        prompt = f"""{context}

🎯 ROLE: Você é um JORNALISTA profissional que resume notícias para cards visuais.

📋 INSTRUÇÕES:
- Use trechos DIRETOS da notícia original (não invente)
- Legendas LONGAS e INFORMATIVAS (até 144 caracteres)
- Estrutura NARRATIVA que conta uma história
- FACTUAL e OBJETIVO (sem criatividade ou interpretação)
- Card 1: Manchete + Fonte + Data

ESTRUTURA JSON OBRIGATÓRIA:
{{
  "articleDate": "YYYY-MM-DD ou 'hoje' se não souber",
  "tiktokTitle": "Título resumido (5-7 palavras)",
  "tiktokSummary": "Parágrafo 1: Lei/contexto principal (~50 palavras).

Parágrafo 2: Impacto e detalhes (~50 palavras).

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5

🔗 Leia mais: {url}",
  "flashcards": [
    {{"text": "{headline}\\n{source}\\nData: [extrair do artigo]", "imagePrompt": "(government official announcement:1.5), (Brazilian flag:1.3), presidential palace, official meeting, serious atmosphere, {style_prompt}"}},
    {{"text": "Valor: Salário mínimo passa de R$ [valor atual] para R$ [novo valor] em [ano]", "imagePrompt": "(money symbol R$:1.5), (minimum wage increase:1.3), financial concept, official announcement, {style_prompt}"}},
    {{"text": "Percentual: Aumento de X% em relação ao ano anterior, considerando inflação de Y% e crescimento do PIB de Z%", "imagePrompt": "(percentage chart:1.5), (economic growth graph:1.3), statistics, professional business setting, {style_prompt}"}},
    {{"text": "Cálculo: Reajuste baseado em [fórmula/regra específica da notícia]", "imagePrompt": "(calculation formula:1.5), (economic indicators:1.3), government planning, official document, {style_prompt}"}},
    {{"text": "Impacto: [Consequência/beneficiários/detalhes específicos da mudança]", "imagePrompt": "(workers receiving salary:1.5), (positive impact:1.3), people benefiting, hopeful atmosphere, {style_prompt}"}}
  ]
}}

⚠️ REGRAS CRÍTICAS:

1. **CARD 1 (Título)**:
   - Linha 1: {headline}
   - Linha 2: {source}
   - Linha 3: Data: [extrair da notícia ou usar "10/12/2025"]
   - imagePrompt: Cena oficial, autoridade, bandeira

2. **CARDS 2-5 (Fatos)**:
   - FORMATO: "Aspecto: Informação específica extraída da notícia"
   - EXEMPLOS de aspectos:
     * "Valor:" / "Percentual:" / "Cálculo:" / "Impacto:" / "Regra:"
     * "Quando:" / "Onde:" / "Quem:" / "Por quê:" / "Como:"
   - Use dados REAIS do artigo (números, percentuais, datas)
   - Máximo 144 caracteres (pode usar quase todo o espaço!)
   - Conte uma HISTÓRIA progressiva

3. **ImagePrompts**:
   - SEMPRE use (elemento principal:1.5)
   - Adicione (elemento secundário:1.3)
   - Descreva cena ESPECÍFICA relacionada ao texto
   - Inclua: pessoas, objetos, setting, atmosfera
   - Termine com: {style_prompt}

4. **articleDate**:
   - Tente extrair do conteúdo do artigo
   - Formato: "YYYY-MM-DD" ou "DD/MM/YYYY"
   - Se não encontrar: use "2025-12-10"

5. **Estrutura Narrativa**:
   Card 1: O QUÊ (anúncio principal)
   Card 2: VALOR/NÚMERO (dados concretos)
   Card 3: CONTEXTO (comparação, cálculo)
   Card 4: METODOLOGIA (como foi definido)
   Card 5: IMPACTO (consequências, beneficiários)

✅ EXEMPLO DE RESULTADO ESPERADO:

Card 1: "Governo confirma salário mínimo de R$ 1.621 em 2026\\nMinistério da Economia\\nData: 09/12/2025"

Card 2: "Valor: Salário mínimo sobe de R$ 1.518 para R$ 1.621 em 2026, representando aumento de R$ 103"

Card 3: "Percentual: Reajuste de 6,78% considera inflação estimada de 4,5% e crescimento do PIB de 2,3% em 2025"

Card 4: "Cálculo: Aplicada regra de correção pela inflação + variação do PIB dos últimos 2 anos, conforme lei vigente"

Card 5: "Impacto: Cerca de 59 milhões de brasileiros serão beneficiados, incluindo trabalhadores CLT e aposentados"

🚫 NÃO FAÇA:
- Legendas curtas e vagas
- Frases criativas ou interpretativas
- Inventar informações
- Repetir o mesmo conteúdo
- imagePrompts genéricos

RESPONDA APENAS COM O JSON VÁLIDO.

COMPLETE TODOS OS 5 CARDS com imagePrompts ESPECÍFICOS e WEIGHTED. NÃO abrevie com "...".
"""
        
        result = self._generate_with_fallback(prompt, system_prompt, format_json=True)
        
        # Validate structure - RIGOROSO: EXATAMENTE 5 cards
        if 'flashcards' not in result:
            logger.error(f"Missing 'flashcards' in response. Keys found: {result.keys()}")
            logger.error(f"Full response: {result}")
            raise ValueError(f"Missing 'flashcards' in response. Got keys: {list(result.keys())}")
        
        num_cards = len(result.get('flashcards', []))
        if num_cards != 5:
            logger.error(f"ERRO: Gerou {num_cards} cards, esperado EXATAMENTE 5!")
            
            # CORREÇÃO 4: Retry com prompt mais simples
            if num_cards > 0 and num_cards < 5:
                logger.warning(f"Tentando novamente com prompt simplificado...")
                
                retry_prompt = f"""Complete este JSON com EXATAMENTE 5 flashcards sobre: {headline}

{{
  "flashcards": [
    {{"text": "{headline}\\n{source}", "imagePrompt": "related visual, {style_prompt}"}},
    {{"text": "Fato 1 (max 90 chars)", "imagePrompt": "visual, {style_prompt}"}},
    {{"text": "Fato 2 (max 90 chars)", "imagePrompt": "visual, {style_prompt}"}},
    {{"text": "Fato 3 (max 90 chars)", "imagePrompt": "visual, {style_prompt}"}},
    {{"text": "Fato 4 (max 90 chars)", "imagePrompt": "visual, {style_prompt}"}}
  ]
}}

Preencha com fatos da notícia. Retorne JSON completo."""
                
                try:
                    retry_result = self._generate_with_fallback(retry_prompt, "", format_json=True)
                    if 'flashcards' in retry_result and len(retry_result['flashcards']) == 5:
                        logger.info("✅ Retry bem-sucedido! 5 cards gerados.")
                        result['flashcards'] = retry_result['flashcards']
                        num_cards = 5
                    else:
                        logger.warning(f"Retry gerou {len(retry_result.get('flashcards', []))} cards")
                except Exception as retry_error:
                    logger.warning(f"Retry falhou: {retry_error}")
            
            # Se ainda não tem 5 cards, forçar ou rejeitar
            if num_cards > 5:
                logger.warning(f"Removendo {num_cards - 5} cards extras...")
                result['flashcards'] = result['flashcards'][:5]
            elif num_cards < 5:
                raise ValueError(f"Insufficient cards: got {num_cards}, need exactly 5")
        
        # CORREÇÃO 3: Validar e corrigir hashtags e link
        summary = result.get('tiktokSummary', '')
        
        # Contar hashtags
        hashtag_count = summary.count('#')
        if hashtag_count < 5:
            logger.warning(f"Only {hashtag_count} hashtags found, expected 5. Adding generic hashtags...")
            generic_tags = "#Notícias #Brasil #Urgente #Hoje #News"
            if '\n\n' in summary:
                parts = summary.split('\n\n')
                if len(parts) >= 2:
                    parts.insert(-1, generic_tags)
                else:
                    parts.append(generic_tags)
                summary = '\n\n'.join(parts)
            else:
                summary += f"\n\n{generic_tags}"
        
        # Verificar link
        if '🔗' not in summary and 'Leia mais' not in summary:
            logger.warning("Link missing from summary, adding...")
            summary += f"\n\n🔗 Leia mais: {url}"
        
        # Atualizar summary corrigido
        result['tiktokSummary'] = summary
        
        # ✅ NOVO: Garantir que articleDate existe
        if 'articleDate' not in result or not result['articleDate']:
            from datetime import datetime
            result['articleDate'] = datetime.now().strftime('%Y-%m-%d')
            logger.info(f"articleDate não encontrado, usando data atual: {result['articleDate']}")
        
        return result
    
    def generate_guide_content(self, topic: str, style_prompt: str) -> Dict:
        """
        Generate educational guide carousel
        """
        system_prompt = "Você é um educador que cria guias visuais didáticos para redes sociais."
        
        prompt = f"""Crie um guia educativo sobre: {topic}

Retorne JSON:
{{
  "title": "Título do guia",
  "cards": [
    {{"text": "Card 1 texto", "imagePrompt": "visual description, {style_prompt}"}},
    {{"text": "Card 2 texto", "imagePrompt": "visual description, {style_prompt}"}}
  ]
}}
"""
        
        result = self._generate_with_fallback(prompt, system_prompt, format_json=True)
        return result
    
    def infer_headline_from_url(self, url: str) -> Dict:
        """
        Try to infer headline and source from URL when RSS doesn't provide it
        """
        system_prompt = "Você é um especialista em análise de URLs e extração de metadados."
        
        prompt = f"""Based on this URL: {url}

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
