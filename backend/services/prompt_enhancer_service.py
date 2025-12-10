# -*- coding: utf-8 -*-
"""
Prompt Enhancer Service - Gera prompts otimizados para imagens
Converte legendas simples em prompts ricos e específicos
"""

import re
import logging
from typing import Dict, List, Set, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PromptEnhancerService:
    """
    Service dedicado a transformar legendas em prompts de imagem otimizados
    
    Responsabilidades:
    1. Extrair entidades (pessoas, lugares, organizações)
    2. Identificar ações e verbos principais
    3. Determinar contexto e atmosfera
    4. Aplicar weighting automático
    5. Gerar prompt estruturado
    """
    
    def __init__(self):
        # Palavras-chave para diferentes contextos
        self.political_keywords = {
            'político', 'política', 'governo', 'presidente', 'congresso',
            'senado', 'câmara', 'eleição', 'votação', 'reforma', 'lei'
        }
        
        self.health_keywords = {
            'saúde', 'hospital', 'médico', 'enfermeiro', 'doença', 'dengue',
            'covid', 'vacina', 'tratamento', 'paciente', 'sus', 'oms'
        }
        
        self.economy_keywords = {
            'economia', 'dinheiro', 'dólar', 'real', 'bolsa', 'mercado',
            'bitcoin', 'inflação', 'juros', 'banco', 'investimento', 'empresa'
        }
        
        self.violence_keywords = {
            'polícia', 'crime', 'violência', 'assassinato', 'roubo',
            'prisão', 'operação', 'investigação', 'suspeito'
        }
        
        # Ações dinâmicas
        self.action_verbs = {
            'anuncia', 'declara', 'afirma', 'confirma', 'retorna', 'chega',
            'sai', 'entra', 'aumenta', 'diminui', 'atinge', 'supera'
        }
        
        # Atmosferas por contexto
        self.atmospheres = {
            'political': 'serious political atmosphere, formal setting',
            'health': 'medical professional atmosphere, clinical setting',
            'economy': 'business professional atmosphere, modern office',
            'violence': 'tense dramatic atmosphere, urgent situation',
            'sports': 'energetic competitive atmosphere, stadium setting',
            'science': 'scientific discovery atmosphere, natural environment, documentary feel',
            'default': 'professional news atmosphere, clean setting'
        }
    
    def enhance_prompt(
        self,
        caption: str,
        headline: Optional[str] = None,
        article_text: Optional[str] = None,
        style_prompt: str = "photorealistic"
    ) -> str:
        """
        Gera um prompt de imagem otimizado a partir da legenda
        
        Args:
            caption: Legenda do card (FONTE PRINCIPAL)
            headline: Manchete original (contexto adicional)
            article_text: Texto do artigo (contexto rico)
            style_prompt: Estilo artístico desejado
            
        Returns:
            Prompt otimizado com weighting e contexto
        """
        logger.info(f"Enhancing prompt for: {caption[:50]}...")
        
        # 1. Focar APENAS na legenda (caption) para este card específico
        # NÃO usar artigo completo para evitar poluição de outras notícias
        context_type = self._identify_context(caption, headline)
        keywords = self._extract_keywords_from_caption(caption)
        
        # 2. Construir elementos do prompt baseado SOMENTE no caption
        main_keywords = keywords[:2] if keywords else []  # Top 2 palavras-chave
        atmosphere = self.atmospheres.get(context_type, self.atmospheres['default'])
        lighting = self._suggest_lighting(context_type)
        
        # 3. Montar prompt com weighting
        prompt_parts = []
        
        # Palavras-chave principais do caption
        for i, keyword in enumerate(main_keywords):
            weight = 1.5 if i == 0 else 1.3
            prompt_parts.append(f"({keyword}:{weight})")
        
        # Contexto e atmosfera
        prompt_parts.append(atmosphere)
        
        # Iluminação
        if lighting:
            prompt_parts.append(lighting)
        
        # Estilo artístico
        prompt_parts.append(style_prompt)
        
        # Juntar tudo
        enhanced_prompt = ", ".join(prompt_parts)
        
        logger.info(f"Enhanced prompt: {enhanced_prompt[:100]}...")
        return enhanced_prompt
    
    def _extract_keywords_from_caption(self, caption: str) -> List[str]:
        """
        Extrai palavras-chave RELEVANTES do caption específico
        Foca em substantivos e conceitos importantes
        """
        # Remover palavras comuns (stopwords simplificado)
        stopwords = {
            'fato', 'sobre', 'para', 'após', 'antes', 'com', 'sem', 'que',
            'uma', 'um', 'os', 'as', 'de', 'da', 'do', 'em', 'na', 'no',
            'é', 'são', 'foi', 'foram', 'está', 'estão', 'ser', 'estar',
            'ter', 'tem', 'teve', 'tiveram', 'sua', 'seu', 'seus', 'suas',
            'o', 'a', 'e', 'mas', 'ou', 'então', 'diz', 'disse'
        }
        
        # Extrair palavras significativas
        words = caption.lower().split()
        keywords = []
        
        for word in words:
            # Limpar pontuação
            clean_word = re.sub(r'[^\w\sáéíóúâêôãõç]', '', word)
            
            # Pular palavras muito curtas ou stopwords
            if len(clean_word) < 4 or clean_word in stopwords:
                continue
            
            # Pular números puros
            if clean_word.isdigit():
                continue
            
            keywords.append(clean_word)
        
        # Retornar top palavras-chave (máx 3)
        return keywords[:3]
    
    def _extract_entities(
        self,
        caption: str,
        headline: Optional[str],
        article: Optional[str]
    ) -> Dict[str, Set[str]]:
        """
        Extrai entidades nomeadas (pessoas, lugares, organizações)
        ✅ CORREÇÃO: Focar APENAS no caption e headline, NÃO no artigo completo
        """
        entities = {
            'people': set(),
            'places': set(),
            'organizations': set(),
            'objects': set()
        }
        
        # ✅ USAR APENAS caption e headline (não article)
        text = f"{caption} {headline or ''}"
        
        # Padrão simples: palavras que começam com maiúscula
        words = text.split()
        for i, word in enumerate(words):
            if not word or len(word) <= 2:
                continue
                
            if word[0].isupper():
                # Context check para classificar
                prev_word = words[i-1].lower() if i > 0 else ''
                
                if prev_word in ['dr', 'dra', 'sr', 'sra', 'presidente', 'ministro']:
                    entities['people'].add(word)
                elif prev_word in ['em', 'de', 'para', 'no', 'na', 'da', 'do']:
                    entities['places'].add(word)
                elif word.isupper() or (i < len(words)-1 and len(words[i+1]) > 0 and words[i+1][0].isupper()):
                    entities['organizations'].add(word)
        
        return entities
    
    def _extract_actions(self, text: str) -> List[str]:
        """Extrai verbos de ação do texto"""
        actions = []
        text_lower = text.lower()
        
        # Adicionar mais verbos relevantes
        all_verbs = {
            'anuncia', 'declara', 'afirma', 'confirma', 'retorna', 'chega',
            'sai', 'entra', 'aumenta', 'diminui', 'atinge', 'supera',
            'descobre', 'descobrem', 'encontra', 'registra', 'mata', 'morre'
        }
        
        for verb in all_verbs:
            if verb in text_lower:
                actions.append(verb)
        
        return actions
    
    def _identify_context(self, caption: str, headline: Optional[str]) -> str:
        """Identifica o contexto da notícia"""
        text = f"{caption} {headline or ''}".lower()
        
        # Adicionar keywords de ciência/natureza
        science_keywords = {
            'cientista', 'cientistas', 'espécie', 'descoberta', 'descobrem',
            'pesquisa', 'pesquisadores', 'amazônia', 'amazónia', 'floresta',
            'animal', 'planta', 'biodiversidade', 'natureza'
        }
        
        for word in science_keywords:
            if word in text:
                return 'science'
        
        for word in self.political_keywords:
            if word in text:
                return 'political'
        
        for word in self.health_keywords:
            if word in text:
                return 'health'
        
        for word in self.economy_keywords:
            if word in text:
                return 'economy'
        
        for word in self.violence_keywords:
            if word in text:
                return 'violence'
        
        return 'default'
    
    def _get_main_subject(self, entities: Dict, caption: str) -> str:
        """
        Determina o assunto principal
        ✅ CORREÇÃO: Usar palavras-chave do caption, não entidades aleatórias
        """
        # Usar extração de keywords ao invés de entidades genéricas
        keywords = self._extract_keywords_from_caption(caption)
        
        if keywords:
            return keywords[0]
        
        # Fallback: primeira palavra significativa
        words = caption.split()
        for word in words:
            clean_word = re.sub(r'[^\w\sáéíóúâêôãõç]', '', word.lower())
            if len(clean_word) > 4:
                return clean_word
        
        return "news scene"
    
    def _get_secondary_elements(
        self,
        entities: Dict,
        main_subject: str
    ) -> List[str]:
        """Elementos secundários para contexto"""
        elements = []
        
        # Adicionar outras entidades (não o assunto principal)
        for entity_type in ['places', 'organizations', 'objects']:
            for entity in entities[entity_type]:
                if entity.lower() != main_subject.lower():
                    elements.append(entity.lower())
        
        return elements
    
    def _describe_action(self, actions: List[str], caption: str) -> str:
        """Descreve a ação principal"""
        if not actions:
            return ""
        
        # Mapeamento de verbos para descrições visuais
        action_descriptions = {
            'anuncia': 'announcing at press conference',
            'declara': 'making declaration',
            'confirma': 'confirming officially',
            'retorna': 'returning',
            'aumenta': 'rising upward',
            'diminui': 'declining downward',
            'atinge': 'reaching milestone',
            'descobre': 'discovering',
            'descobrem': 'scientific discovery',
            'encontra': 'finding new',
            'registra': 'documenting',
        }
        
        for action in actions:
            if action in action_descriptions:
                return action_descriptions[action]
        
        return "in action"
    
    def _suggest_lighting(self, context: str) -> str:
        """Sugere iluminação apropriada"""
        lighting_map = {
            'political': 'dramatic spotlighting',
            'health': 'bright clinical lighting',
            'economy': 'professional office lighting',
            'violence': 'dramatic shadowy lighting',
            'science': 'natural daylight, documentary style',
            'default': 'natural professional lighting'
        }
        
        return lighting_map.get(context, lighting_map['default'])
    
    def batch_enhance(
        self,
        cards: List[Dict],
        headline: str,
        article_text: Optional[str],
        style_prompt: str
    ) -> List[Dict]:
        """
        Processa múltiplos cards de uma vez
        
        Args:
            cards: Lista de cards com 'text' e 'imagePrompt'
            headline: Manchete da notícia
            article_text: Artigo completo
            style_prompt: Estilo artístico
            
        Returns:
            Cards com imagePrompts aprimorados
        """
        enhanced_cards = []
        
        for i, card in enumerate(cards):
            caption = card.get('text', '')
            
            # Pular card 1 se for só manchete + fonte
            if i == 0 and '\n' in caption and len(caption.split('\n')) == 2:
                # Card 1 é especial: manchete + fonte
                enhanced_prompt = self.enhance_prompt(
                    headline,
                    headline=headline,
                    article_text=article_text,
                    style_prompt=style_prompt
                )
            else:
                enhanced_prompt = self.enhance_prompt(
                    caption,
                    headline=headline,
                    article_text=article_text,
                    style_prompt=style_prompt
                )
            
            enhanced_card = card.copy()
            enhanced_card['imagePrompt'] = enhanced_prompt
            enhanced_cards.append(enhanced_card)
        
        return enhanced_cards


# Exemplo de uso
if __name__ == "__main__":
    service = PromptEnhancerService()
    
    # Teste 1: Notícia política
    caption1 = "María Corina Machado retornará à Venezuela em breve"
    headline1 = "María Corina Machado retornará à Venezuela em breve, diz sua filha"
    
    prompt1 = service.enhance_prompt(
        caption1,
        headline=headline1,
        style_prompt="3D Pixar style, colorful, vibrant"
    )
    print(f"Teste 1:\nLegenda: {caption1}\nPrompt: {prompt1}\n")
    
    # Teste 2: Notícia de saúde
    caption2 = "SP registra maior número de mortes por dengue em 2025"
    prompt2 = service.enhance_prompt(
        caption2,
        style_prompt="photorealistic, professional photography"
    )
    print(f"Teste 2:\nLegenda: {caption2}\nPrompt: {prompt2}\n")
    
    # Teste 3: Notícia econômica
    caption3 = "Bitcoin atinge recorde histórico de US$ 100 mil"
    prompt3 = service.enhance_prompt(
        caption3,
        style_prompt="cyberpunk style, neon, futuristic"
    )
    print(f"Teste 3:\nLegenda: {caption3}\nPrompt: {prompt3}\n")
