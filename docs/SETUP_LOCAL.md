# FlashNews AI - Setup Local (Geração Local)

Este guia mostra como configurar o FlashNews AI para geração 100% local usando Ollama e modelos de imagem locais.

## Pré-requisitos

### Hardware
- **CPU**: Qualquer processador moderno
- **RAM**: Mínimo 8GB (16GB recomendado)
- **GPU** (Opcional mas recomendado): NVIDIA com 6GB+ VRAM para geração rápida de imagens
- **Espaço em disco**: ~20GB para modelos

### Software
- **Node.js** 18+ e npm
- **Python** 3.10+
- **Git**

---

## Instalação Passo a Passo

### 1. Instalar Ollama (Geração de Texto)

#### Windows
1. Baixe o instalador: https://ollama.ai/download/windows
2. Execute o instalador
3. Abra o terminal e verifique:
   ```bash
   ollama --version
   ```

#### Linux/Mac
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Baixar Modelo de Linguagem
```bash
# Modelo recomendado (3B parâmetros - rápido e eficiente)
ollama pull llama3.2:3b

# Alternativa (7B - mais qualidade, mais lento)
ollama pull mistral:7b
```

Verifique se o serviço está rodando:
```bash
curl http://localhost:11434/api/tags
```

---

### 2. Configurar Geração de Imagens

Você tem 3 opções. Escolha uma:

#### Opção A: Pollinations (Nenhuma instalação - usar API externa)
✅ **Recomendado para começar rapidamente**

Nenhuma configuração necessária! O backend usará automaticamente a API do Pollinations como fallback.

#### Opção B: Automatic1111 (Mais popular)
1. Clone o repositório:
   ```bash
   git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
   cd stable-diffusion-webui
   ```

2. Execute o instalador:
   ```bash
   # Windows
   webui-user.bat --api

   # Linux
   ./webui.sh --api
   ```

3. Baixe um modelo (ex: SDXL Turbo) e coloque em `models/Stable-diffusion/`

4. Acesse http://localhost:7860

#### Opção C: ComfyUI (Mais flexível)
1. Clone: `git clone https://github.com/comfyanonymous/ComfyUI.git`
2. Instale dependências: `pip install -r requirements.txt`
3. Execute: `python main.py`
4. Acesse http://localhost:8188

---

### 3. Configurar Backend Python

```bash
# Na raiz do projeto
cd backend

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

#### Configurar `.env`
Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite `.env` conforme sua configuração:
```bash
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# Escolha o backend de imagem:
# pollinations, automatic1111, comfyui, ou fooocus
IMAGE_BACKEND=pollinations

# Se usar A1111 (descomentar e configurar)
# A1111_URL=http://localhost:7860
# A1111_TIMEOUT=45

# Se usar ComfyUI (descomentar e configurar)
# COMFYUI_URL=http://localhost:8188
# COMFYUI_TIMEOUT=45
```

#### Executar Backend
```bash
# Ainda no diretório backend/
python server.py
```

O servidor estará em http://localhost:8000

---

### 4. Configurar Frontend React

```bash
# Na raiz do projeto
npm install
```

O arquivo `.env.local` já está configurado para apontar para `http://localhost:8000`.

#### Executar Frontend
```bash
npm run dev
```

O app estará em http://localhost:5173

---

## Uso

1. **Acesse** http://localhost:5173
2. **Selecione uma categoria** (ex: Tecnologia)
3. **Escolha uma manchete** da lista
4. **Selecione um estilo visual** (ex: Cyberpunk, Pixar 3D)
5. **Aguarde a geração** (pode levar 3-5 minutos para 7 cards)
6. **Salve o post** clicando em "Salvar Post" na aba Detalhes
7. **Baixe as imagens** ou copie a legenda para publicar no TikTok

### Posts Salvos
Os posts ficam salvos em:
```
generated_posts/
├── 2025-12-06/
│   ├── tecnologia_20251206_205500/
│   │   ├── metadata.json
│   │   ├── card_1.png
│   │   └── ...
```

---

## Troubleshooting

### Ollama não está rodando
```bash
# Windows: reiniciar serviço Ollama
# Linux/Mac:
ollama serve
```

### Geração de imagem falha
- Verifique se o backend de imagem está rodando (A1111/ComfyUI)
- Se usar Pollinations, verifique conexão com internet
- Configure `IMAGE_BACKEND=pollinations` no `.env` para garantir fallback

### Backend retorna erro 500
- Verifique logs do terminal do backend
- Certifique-se de que todas as dependências Python estão instaladas
- Verifique se o Ollama tem o modelo baixado: `ollama list`

### Frontend não conecta ao backend
- Verifique se o backend está rodando em http://localhost:8000
- Confirme que `.env.local` tem `VITE_API_BASE_URL=http://localhost:8000`
- Tente acessar http://localhost:8000 no navegador diretamente

---

## Performance Esperada

Com `llama3.2:3b` + Pollinations:
- **Texto**: ~3-5 segundos por geração
- **Imagem**: ~8-15 segundos por card
- **Total**: ~2-3 minutos para um post completo (7 cards)

Com modelo de imagem local (A1111 + GPU):
- **Imagem**: ~5-10 segundos por card
- **Total**: ~1-2 minutos para um post completo

---

## Próximos Passos

- [ ] Implementar página Library para visualizar posts salvos
- [ ] Adicionar geração de áudio local com Coqui TTS
- [ ] Suporte para batch processing (múltiplas notícias de uma vez)
- [ ] Integração com TikTok API para upload automático

---

## Suporte

Para problemas ou dúvidas:
1. Verifique os logs do backend (`python server.py`)
2. Verifique os logs do frontend (console do navegador)
3. Consulte a documentação do Ollama: https://ollama.ai/docs
