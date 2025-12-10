# 🔧 Scripts de Controle - FlashNews AI

Guia completo dos scripts `.bat` para gerenciar os serviços.

---

## 📋 Scripts Disponíveis

### 1. **iniciar_flashnews.bat** ▶️
**O que faz:**
- Verifica se Ollama está rodando (senão, inicia)
- Inicia servidor backend FastAPI (porta 8000)
- Abre interface no navegador
- Deixa servidor rodando em background

**Quando usar:**
- Primeira vez do dia
- Após reiniciar o computador
- Quando quiser gerar flashcards

**Como usar:**
```batch
.\iniciar_flashnews.bat
```

**Resultado:**
- ✅ Ollama rodando
- ✅ Backend em http://localhost:8000
- ✅ Interface aberta no navegador

---

### 2. **parar_flashnews.bat** ⏹️
**O que faz:**
- Para servidor backend (FastAPI)
- Para Ollama (LLM local)

**Quando usar:**
- Quando terminar de usar
- Para economizar recursos
- Antes de reiniciar o sistema

**Como usar:**
```batch
.\parar_flashnews.bat
```

**Resultado:**
- ✅ Backend parado
- ✅ Ollama parado

---

### 3. **iniciar_viewer.bat** 👁️
**O que faz:**
- Inicia servidor HTTP simples (porta 8001)
- Serve arquivos estáticos (viewer)

**Quando usar:**
- Para visualizar posts salvos
- Testar o viewer localmente
- ✅ Pode rodar junto com backend!

**Como usar:**
```batch
.\iniciar_viewer.bat
```

**Acesso:**
- http://localhost:8001/viewer/

**Resultado:**
- ✅ Viewer disponível

---

### 4. **parar_viewer.bat** ⏹️ ✨ NOVO
**O que faz:**
- Para servidor HTTP do viewer
- Libera porta 8001

**Quando usar:**
- Quando terminar de visualizar
- Para economizar recursos

**Como usar:**
```batch
.\parar_viewer.bat
```

**Resultado:**
- ✅ Viewer parado
- ✅ Porta 8001 liberada

---

### 5. **parar_tudo.bat** ⏹️⏹️⏹️ ✨ NOVO
**O que faz:**
- Para TUDO de uma vez:
  * Backend (FastAPI)
  * Viewer (HTTP server)
  * Ollama (LLM)
  * Processos Python pendentes

**Quando usar:**
- No final do dia
- Quando algo travou
- Reset completo do sistema

**Como usar:**
```batch
.\parar_tudo.bat
```

**Resultado:**
- ✅ Todos os serviços parados
- ✅ Memória liberada
- ✅ Processos limpos

---

### 6. **enviar_cards_github.bat** 📤
**O que faz:**
- Faz commit dos posts gerados
- Push para GitHub
- Atualiza GitHub Pages

**Quando usar:**
- Após gerar vários posts
- Publicar manualmente
- Quando auto-push falhar

**Como usar:**
```batch
.\enviar_cards_github.bat
```

**Resultado:**
- ✅ Commit criado
- ✅ Push para GitHub
- ✅ Pages atualizado

---

## 🔄 Workflows Comuns

### Workflow 1: Gerar Flashcards

```batch
# 1. Iniciar sistema
.\iniciar_flashnews.bat

# 2. Usar interface web (geração automática)

# 3. Ao terminar
.\parar_flashnews.bat
```

---

### Workflow 2: Visualizar Posts

```batch
# 1. Iniciar viewer (pode estar junto com backend)
.\iniciar_viewer.bat

# 2. Acessar http://localhost:8001/viewer/

# 3. Ao terminar
.\parar_viewer.bat
```

---

### Workflow 3: Desenvolvimento/Debug

```batch
# 1. Parar tudo primeiro
.\parar_tudo.bat

# 2. Startar com código atualizado
.\iniciar_flashnews.bat

# 3. Testar

# 4. Se travar, parar tudo de novo
.\parar_tudo.bat
```

---

### Workflow 4: Publicação Manual

```batch
# 1. Gerar posts normalmente

# 2. Publicar manualmente
.\enviar_cards_github.bat

# 3. Aguardar 1-2 minutos

# 4. Verificar GitHub Pages
```

---

## ⚙️ Portas Utilizadas

| Serviço | Porta | Script |
|---------|-------|--------|
| Backend (FastAPI) | 8000 | iniciar_flashnews.bat |
| Viewer (HTTP) | 8001 | iniciar_viewer.bat |
| Ollama | 11434 | (automático) |

**✅ PORTAS SEPARADAS:** Backend e Viewer podem rodar simultaneamente!

---

## 🐛 Troubleshooting

### Problema: "Porta 8000 em uso"

**Solução:**
```batch
.\parar_tudo.bat
# Aguardar 5 segundos
.\iniciar_flashnews.bat
```

---

### Problema: "Ollama não responde"

**Solução:**
```batch
# 1. Parar tudo
.\parar_tudo.bat

# 2. Iniciar Ollama manualmente
ollama serve

# 3. Em outra janela
.\iniciar_flashnews.bat
```

---

### Problema: "Processo travado"

**Solução:**
```batch
# Força parar TUDO
.\parar_tudo.bat

# Aguardar 10 segundos

# Iniciar limpo
.\iniciar_flashnews.bat
```

---

### Problema: "Backend não inicia"

**Checklist:**
1. ✅ Python instalado? `python --version`
2. ✅ Dependências? `pip install -r requirements.txt`
3. ✅ Porta livre? `netstat -ano | findstr :8000`
4. ✅ Ollama rodando? `ollama list`

---

## 📊 Gestão de Recursos

### Uso de Memória (Aproximado)

| Serviço | RAM | CPU |
|---------|-----|-----|
| Ollama (idle) | ~1 GB | 0-5% |
| Ollama (gerando) | ~4 GB | 80-100% |
| Backend | ~200 MB | 5-10% |
| Viewer | ~50 MB | 1-2% |

**Total quando tudo rodando:** ~5 GB RAM

### Quando Parar Serviços

**Parar tudo se:**
- Computador lento
- Bateria baixa (laptop)
- Não vai usar por +30min
- Fazer backup/update

**Deixar rodando se:**
- Vai gerar vários posts seguidos
- Testando funcionalidades
- Desenvolvimento ativo

---

## 🎯 Resumo Rápido

| Quero... | Script |
|----------|--------|
| Gerar flashcards | `iniciar_flashnews.bat` |
| Ver posts salvos | `iniciar_viewer.bat` |
| Parar backend | `parar_flashnews.bat` |
| Parar viewer | `parar_viewer.bat` |
| Parar TUDO | `parar_tudo.bat` |
| Publicar posts | `enviar_cards_github.bat` |

---

## 🆘 Comandos Manuais (Se Scripts Falharem)

### Iniciar Ollama
```cmd
ollama serve
```

### Iniciar Backend
```cmd
cd backend
python server.py
```

### Parar Processo por Porta
```cmd
# Ver qual processo usa a porta
netstat -ano | findstr :8000

# Parar por PID
taskkill /F /PID [número_do_pid]
```

### Parar Ollama
```cmd
taskkill /F /IM ollama.exe
```

---

_Última atualização: 10/12/2025_  
_Scripts criados: 6_  
_Status: Todos funcionais_ ✅
