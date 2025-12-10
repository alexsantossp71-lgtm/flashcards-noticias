# 📰 MODO JORNALÍSTICO - Implementado

**Data:** 10/12/2025 12:40  
**Objetivo:** Legendas factuais, longas, usando trechos da notícia original  
**Status:** ✅ IMPLEMENTADO

---

## 🎯 MUDANÇAS APLICADAS

### 1. **Prompt do Ollama Reformulado**

**ANTES (Modo Criativo):**
```
- Legendas curtas (~60 chars)
- Criativo e interpretativo
- Fatos genéricos
```

**DEPOIS (Modo Jornalístico):**
```
🎯 ROLE: Jornalista profissional

📋 INSTRUÇÕES:
- Use trechos DIRETOS da notícia
- Legendas LONGAS (até 144 chars)
- FACTUAL e OBJETIVO
- Estrutura NARRATIVA
- Card 1: Manchete + Fonte + Data
```

### 2. **Estrutura de Cards Reformulada**

**Card 1 - Título com Fonte e Data:**
```
Linha 1: {headline}
Linha 2: {source}
Linha 3: Data: DD/MM/YYYY
```

**Cards 2-5 - Formato "Aspecto: Informação":**
```
Card 2: "Valor: Salário mínimo passa de R$ 1.518 para R$ 1.621..."
Card 3: "Percentual: Aumento de 6,78% considerando inflação..."
Card 4: "Cálculo: Aplicada regra de correção pela inflação..."
Card 5: "Impacto: Cerca de 59 milhões de brasileiros..."
```

**Aspectos Disponíveis:**
- Valor, Percentual, Cálculo, Impacto, Regra
- Quando, Onde, Quem, Por quê, Como

### 3. **Estrutura Narrativa Definida**

```
Card 1: O QUÊ?     → Anúncio principal
Card 2: NÚMERO?    → Dados concretos, valores
Card 3: CONTEXTO?  → Comparação, cálculo, percentual
Card 4: COMO?      → Metodologia, regra, fórmula
Card 5: IMPACTO?   → Consequências, beneficiários
```

Esta estrutura **conta uma história completa**.

### 4. **Data da Notícia Adicionada**

**Campo novo: `articleDate`**

Fluxo:
1. Ollama extrai data do artigo → `"articleDate": "2025-12-09"`
2. Se não encontrar → usa data atual
3. Salvo em `metadata.json`
4. Card 1 mostra: `"Data: 09/12/2025"`

**Modelo atualizado:**
```python
class SavePostRequest(BaseModel):
    # ... campos existentes ...
    articleDate: Optional[str] = None  # ✅ NOVO
```

**Storage atualizado:**
```python
metadata = {
    "id": post_id,
    "timestamp": "2025-12-10T12:40:00",
    "articleDate": "2025-12-09",  # ✅ NOVO
    # ... outros campos ...
}
```

### 5. **Legendas Mais Longas**

**ANTES:**
- Limite: 90 caracteres
- Resultado: "Fato 1: Aumento de 6,78%"

**DEPOIS:**
- Limite: 144 caracteres
- Resultado: "Percentual: Reajuste de 6,78% considera inflação estimada de 4,5% e crescimento do PIB de 2,3% em 2025"

**Tamanho:**
- Mínimo recomendado: 80 chars
- Máximo permitido: 144 chars
- Ideal: 110-130 chars (usa bem o espaço)

### 6. **ImagePrompts Narrativos**

**Exemplos por card:**

**Card 1 (Anúncio):**
```
(government official announcement:1.5), 
(Brazilian flag:1.3), 
presidential palace, 
official meeting, 
serious atmosphere, 
{style}
```

**Card 2 (Valor/Número):**
```
(money symbol R$:1.5), 
(minimum wage increase:1.3), 
financial concept, 
official announcement, 
{style}
```

**Card 3 (Contexto/Cálculo):**
```
(percentage chart:1.5), 
(economic growth graph:1.3), 
statistics, 
professional business setting, 
{style}
```

**Card 4 (Metodologia):**
```
(calculation formula:1.5), 
(economic indicators:1.3), 
government planning, 
official document, 
{style}
```

**Card 5 (Impacto):**
```
(workers receiving salary:1.5), 
(positive impact:1.3), 
people benefiting, 
hopeful atmosphere, 
{style}
```

---

## 📋 EXEMPLO COMPLETO

### Notícia: "Governo confirma salário mínimo de R$ 1.621 em 2026"

**Card 1:**
```
Text: "Governo confirma salário mínimo de R$ 1.621 em 2026
Ministério da Economia
Data: 09/12/2025"

ImagePrompt: "(government official announcement:1.5), (Brazilian flag:1.3), presidential palace, official meeting, serious atmosphere, comic book style"
```

**Card 2:**
```
Text: "Valor: Salário mínimo sobe de R$ 1.518 para R$ 1.621 em 2026, representando aumento de R$ 103"

ImagePrompt: "(money symbol R$:1.5), (minimum wage increase:1.3), financial concept, official announcement, comic book style"
```

**Card 3:**
```
Text: "Percentual: Reajuste de 6,78% considera inflação estimada de 4,5% e crescimento do PIB de 2,3% em 2025"

ImagePrompt: "(percentage chart:1.5), (economic growth graph:1.3), statistics, professional business setting, comic book style"
```

**Card 4:**
```
Text: "Cálculo: Aplicada regra de correção pela inflação + variação do PIB dos últimos 2 anos, conforme lei vigente"

ImagePrompt: "(calculation formula:1.5), (economic indicators:1.3), government planning, official document, comic book style"
```

**Card 5:**
```
Text: "Impacto: Cerca de 59 milhões de brasileiros serão beneficiados, incluindo trabalhadores CLT e aposentados"

ImagePrompt: "(workers receiving salary:1.5), (positive impact:1.3), people benefiting, hopeful atmosphere, comic book style"
```

---

## 🚫 O QUE NÃO FAZER

❌ **Legendas vagas:**
```
"Aumento confirmado"  // SEM DADOS!
```

❌ **Legendas curtas:**
```
"Valor de R$ 1.621"  // APENAS 19 CHARS!
```

❌ **Criatividade/Interpretação:**
```
"Brasileiros comemoram aumento"  // INTERPRETATIVO!
```

❌ **Repetir conteúdo:**
```
Card 2: "Aumento de 6,78%"
Card 3: "Aumento de 6,78%"  // REPETIDO!
```

❌ **Inventar informação:**
```
"Beneficia 100 milhões"  // SE NÃO ESTÁ NA NOTÍCIA!
```

---

## ✅ O QUE FAZER

✅ **Usar dados REAIS:**
```
"Valor: Salário mínimo passa de R$ 1.518 para R$ 1.621..."
// Números da notícia original
```

✅ **Estrutura clara:**
```
"Aspecto: Informação completa e factual"
```

✅ **Máximo de espaço:**
```
"Percentual: Reajuste de 6,78% considera inflação estimada de 4,5% e crescimento do PIB de 2,3% em 2025"
// 104 caracteres - BOM USO DO ESPAÇO!
```

✅ **Progressão narrativa:**
```
Card 1: O QUÊ
Card 2: QUANTO
Card 3: POR QUÊ/COMO
Card 4: MÉTODO
Card 5: RESULTADO
```

---

## 📊 COMPARAÇÃO: Antes vs Depois

| Aspecto | Modo Criativo | Modo Jornalístico |
|---------|---------------|-------------------|
| **Tamanho** | 60 chars | 110-144 chars |
| **Estilo** | Criativo | Factual |
| **Fonte** | Interpretação | Trechos diretos |
| **Card 1** | Só manchete | Manchete + Fonte + Data |
| **Estrutura** | Livre | Narrativa 5W2H |
| **articleDate** | ❌ Não | ✅ Sim |
| **Formato** | Livre | "Aspecto: Info" |

---

## 🔄 PARA REINICIAR

```bash
# 1. Parar servidor atual (Ctrl+C)

# 2. Reiniciar com código atualizado
.\iniciar_flashnews.bat

# 3. Gerar novo teste
# - Selecionar a notícia do salário mínimo
# - Verificar legendas longas e informativas
# - Verificar data no Card 1
# - Verificar progressão narrativa
```

---

## 📝 ARQUIVOS MODIFICADOS

1. `backend/services/ollama_service.py` - Prompt jornalístico
2. `backend/services/storage_service.py` - Adicionar articleDate
3. `backend/server.py` - Modelo SavePostRequest + articleDate

**Total de mudanças:** ~150 linhas de código

---

_Implementação concluída: 10/12/2025 12:40_  
_Status: PRONTO PARA TESTE_ ✅
