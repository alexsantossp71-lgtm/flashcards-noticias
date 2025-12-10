# 📋 PLANEJAMENTO - Diagnóstico: Imagens não refletem Legendas

**Data:** 10/12/2025 08:45  
**Objetivo:** Identificar por que imagens geradas não correspondem às legendas dos flashcards

---

## 🔍 DIAGNÓSTICO COMPLETO

### 1. Testes Realizados

✅ **Sistema iniciado com sucesso**
- Ollama rodando
- Backend rodando (http://localhost:8000)
- Interface aberta no navegador

✅ **Geração de flashcards testada**
- Fonte: UOL - "EUA apoiam Japão em disputa com China..."
- Geração completou em ~2 minutos
- ✅ 5 flashcards gerados
- ✅ Resumo TikTok com 5 hashtags
- ✅ Link original incluído

### 2. Análise de Posts Salvos

#### Notícia 1: "Mundo pode registrar primeira alta em mortes infantis"
- ✅ Título TikTok: Gerado
- ✅ Resumo TikTok: Gerado com hashtags
- ✅ 7 cards com campo `text` preenchido
- 🔴 **Campo `imagePrompt`: VAZIO** (0 caracteres)

#### Notícia 2: "Invasão dos EUA à Venezuela"
- ✅ Título TikTok: Gerado
- ✅ Resumo TikTok: Com hashtags e link
- ✅ 7 cards com campo `text`
- 🔴 **Campo `imagePrompt`: VAZIO** (0 caracteres)

#### Notícia 3: "Polícia Legislativa expulsa jornalistas"
- ✅ Título: Gerado
- ✅ Resumo: Gerado
- ✅ 6 cards com `text`
- 🔴 **Campo `imagePrompt`: VAZIO**

#### Métricas
- **Posts analisados:** 3
- **Total de cards:** 20
- **Overlap médio:** 0.0%
- **Cards com `imagePrompt` vazio:** 20 (100%)

---

## ❗ PROBLEMA IDENTIFICADO

### Causa Raiz

Os **prompts de imagem NÃO estão sendo salvos** no `metadata.json`, resultando em 0% de overlap entre legendas e prompts.

### Estrutura Atual (INCORRETA)

```json
{
  "text": "Legenda do card aqui",
  "imagePrompt": "",  // ← VAZIO!
  "imageSource": "local",
  "imagePath": "card_2.png"
}
```

### Estrutura Esperada (CORRETA)

```json
{
  "text": "EUA apoiam Japão em disputa...",
  "imagePrompt": "Map of Asia showing Japan and China territorial dispute, military radar, ships, realistic photographic style",
  "imageSource": "local",
  "imagePath": "card_2.png"
}
```

---

## ✅ CÓDIGO VERIFICADO

### Backend - Ollama Service ✅

**Arquivo:** `backend/services/ollama_service.py`  
**Status:** **CORRETO** ✅

```python
# O prompt do Ollama INCLUI imagePrompt:
{
  "flashcards": [
    {"text": "...", "imagePrompt": "visual in English, {style_prompt}"},
    ...
  ]
}
```

✅ Confirmado: Backend **GERA** os prompts corretamente

### Backend - Storage Service ✅

**Arquivo:** `backend/services/storage_service.py`  
**Status:** **CORRETO** ✅

```python
def save_post(..., cards: List[Dict], ...):
    # Salva cards como recebidos
    metadata = {
        ...
        "cards": cards,  # ← Salva exatamente o que recebe  
        ...
    }
```

✅ Confirmado: Backend **SALVA** o que recebe do frontend

### Frontend - Uso de imagePrompt ✅

**Arquivos verificados:**
- `static/index.html` (linha 370, 419)
- `static/js/app-bundle.js` (linha 220, 235)
- `static/js/pages.js` (linha 395, 412, 441)

✅ Confirmado: Frontend **USA** `imagePrompt` no código

---

## 🎯 HIPÓTESES

### Hipótese 1: API Response não inclui `imagePrompt` 🔍
**Verificar:** Response de `/api/generate-content`

**Como testar:**
```bash
# Interceptar response da API durante geração
# OU verificar logs do backend
```

### Hipótese 2: Frontend não salva `imagePrompt` ⚠️
**Verificar:** Payload enviado para `/api/save-post`

**Possível problema:**
```javascript
// Possível código problemático no frontend:
cards.push({
  text: card.text,      // ✅ Inclui
  imageBase64: img,     // ✅ Inclui
  imageSource: 'local'  // ✅ Inclui
  // imagePrompt: ???   // ❌ Faltando?
});
```

### Hipótese 3: Dados perdidos durante transformação 🔄
**Verificar:** Fluxo completo de dados

```
Ollama → Server → Frontend → Save Request → Storage
         ↓         ↓          ↓             ↓
     [ ] OK    [ ] OK     [ ] OK        [ ] OK
```

---

## 🔧 PRÓXI MAS AÇÕES

### 1. ✅ Verificar Response da API

```javascript
// Em index.html ou pages.js, procurar por:
const response = await fetch('/api/generate-content', {...});
const data = await response.json();

// Adicionar log:
console.log('API Response flashcards:', data.flashcards);
// Verificar se cada card tem imagePrompt
```

### 2. ⚠️ Verificar Payload de Save

```javascript
// Procurar por fetch('/api/save-post'...)
// Adicionar log antes do fetch:
console.log('Saving cards:', cards);
// Verificar se imagePrompt está presente
```

### 3. 🔍 Inspecionar um card completo

```javascript
// Durante a geração, após receber flashcards:
state.flashcards.forEach((card, i) => {
  console.log(`Card ${i+1}:`, {
    text: card.text,
    imagePrompt: card.imagePrompt,
    hasPrompt: !!card.imagePrompt
  });
});
```

---

## 📊 EXEMPLO DO PROBLEMA

###  Caso Real Analisado

**Notícia:** "EUA apoiam Japão em disputa com China..."

**Card 2 - Esperado:**

```json
{
  "text": "EUA reafirmam apoio ao Japão após incidente com radar militar chinês ",
  "imagePrompt": "US and Japan flags together, military radar equipment, China in background, geopolitical tension, news photography style, realistic"
}
```

**Overlap esperado:** ~40% (palavras: EUA, Japão, radar, militar, China)

**Card 2 - Atual (SALVO):**

```json
{
  "text": "...",
  "imagePrompt": ""  // ← VAZIO!
}
```

**Overlap atual:** 0% ❌

---

## 🎯 RESULTADO ESPERADO

Após correção:

✅ `image Prompt` preenchido em TODOS os cards  
✅ Overlap mínimo de 30-40% entre legenda e prompt  
✅ Imagens que realmente ilustram o conteúdo textual  
✅ Correlação visual clara entre texto e imagem  

---

## 📝 SCRIPTS CRIADOS

1. ✅ `diagnostico_prompts.py` - Busca notícias e gera conteúdo  
2. ✅ `analisar_posts.py` - Analisa posts salvos e calcula overlap  
3. ✅ `ANALISE_POSTS.md` - Relatório detalhado em Markdown  
4. ✅ `ANALISE_GERADA.md` - Documento de diagnóstico  
5. ✅ `PLANEJAMENTO.md` - Este documento

---

_Documento criado durante sessão de debugging - 10/12/2025_
