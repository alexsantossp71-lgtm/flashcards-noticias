# FlashNews Viewer 📱

Visualizador estático de cards de notícias gerados por IA.

## 🌐 Ver Online

Acesse: **[FlashNews Viewer](https://alexsantossp71-lgtm.github.io/flashcards-noticias/viewer/)**

## 💻 Ver Localmente

```bash
# Opção 1: Abrir direto no navegador
cd viewer
start index.html  # Windows

# Opção 2: Servidor local
python -m http.server 8000  # Depois acesse http://localhost:8000/viewer/
```

## 📁 Estrutura

```
flashcards-noticias/
├── viewer/          # Visualizador standalone (GitHub)
│   └── index.html
│
├── generated_posts/ # Posts salvos
│   ├── index.json
│   └── YYYY-MM-DD/
│
└── static/          # Sistema completo (local)
    └── ...
```

## 🎯 Dois Ambientes

### 1. **Ambiente Local** (Sistema Completo)
- Gera novos cards com IA
- Requer backend Python + Ollama/Gemini
- Use: `iniciar_flashnews.bat`
- Interface: `static/index.html`

### 2. **Ambiente GitHub** (Visualizador)
- Apenas visualiza cards já gerados
- Sem dependências de backend
- Lê diretamente dos JSONs
- Interface: `viewer/index.html`

## 🚀 Funcionalidades do Viewer

- ✅ Lista todos os posts salvos
- 📊 Estatísticas (total de posts/cards/categorias)
- 🎴 Visualização de cards em grid
- ⬇️ Download individual de cards
- 📱 Interface responsiva
- 🎨 Design moderno com Tailwind CSS

## 🔄 Workflow

1. **Localmente:** Gere cards usando `static/index.html` com backend
2. **Commit:** Os cards são salvos em `generated_posts/`
3. **Push:** Envie para GitHub
4. **GitHub:** Visualizador em `viewer/` exibe automaticamente

---

**Nota:** Este visualizador lê dados localmente via `fetch()`. Para funcionar localmente ou no GitHub Pages, os arquivos JSON e imagens em `generated_posts/` devem estar acessíveis.
