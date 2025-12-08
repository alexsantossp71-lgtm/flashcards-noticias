<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# FlashNews Viewer 📱

Visualizador de cards/stories de notícias gerados por IA para TikTok/Instagram.

## 📖 Sobre

Este repositório contém a interface web para visualizar cards de notícias já gerados. Os cards são criados automaticamente a partir de headlines de notícias e incluem:

- 📰 Conteúdo adaptado para social media
- 🎨 Imagens geradas por IA
- 💾 Organização por data
- 🔄 Histórico completo de posts salvos

## 🚀 Como Usar

### Visualização Local

Basta abrir o arquivo no seu navegador:

```bash
# Navegar até a pasta
cd static

# Abrir index.html no navegador
start index.html  # Windows
# ou
open index.html   # Mac
# ou  
xdg-open index.html  # Linux
```

Ou usar um servidor local simples:

```bash
# Python
python -m http.server 8000

# Node.js
npx http-server static

# Depois acesse: http://localhost:8000
```

## 📁 Estrutura

```
├── static/              # Interface web
│   ├── index.html      # Página principal
│   ├── css/            # Estilos
│   ├── js/             # Scripts
│   └── assets/         # Recursos visuais
│
└── generated_posts/     # Cards gerados
    ├── index.json      # Índice de posts
    └── YYYY-MM-DD/     # Posts organizados por data
```

## 🎯 Funcionalidades

- 📱 Visualização de cards estilo Instagram/TikTok
- 🗓️ Navegação por data
- 💾 Posts salvos persistentes
- 📊 Estatísticas de posts
- 🎨 Interface moderna e responsiva

---

**Nota:** Este é apenas o visualizador. Para gerar novos cards, você precisará do sistema completo com backend Python + Ollama/Gemini.
