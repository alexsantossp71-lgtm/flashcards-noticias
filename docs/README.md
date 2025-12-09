# FlashNews - GitHub Pages

Este diretório contém a publicação dos flashcards gerados pelo FlashNews.

## Estrutura

```
docs/
├── index.html          # Página de listagem de posts
├── post.html           # Visualizador de post individual
├── posts/
│   ├── index.json      # Índice de todos os posts
│   └── [post-id]/      # Pasta de cada post
│       ├── metadata.json
│       ├── card_1.png
│       ├── ...
│       └── card_7.png
```

## Como Usar

1. **Gerar flashcards** no FlashNews
2. **Salvar** o post
3. **Publicar** com o script:

```bash
python publicar_github.py <POST_ID>
```

4. **Testar localmente**:

```bash
python -m http.server 8080 -d docs
```

Abra: http://localhost:8080

5. **Publicar no GitHub**:

```bash
git add docs/
git commit -m "Publicar novo post"
git push
```

## GitHub Pages

1. Vá em **Settings** → **Pages**
2. Set **Source**: `/docs` folder
3. Clique em **Save**
4. Aguarde alguns minutos
5. Acesse: `https://[USUARIO].github.io/[REPO]/`

## Funcionalidades

- 📱 **Mobile-first**: Responsivo para celular
- 📋 **Clipboard**: Copiar título e resumo com um clique
- 📦 **ZIP Download**: Baixar todas as imagens em um arquivo
- 🖼️ **Galeria**: Ver todas as 7 imagens do flashcard
- 🔗 **Compartilhar**: URL direto para cada post
