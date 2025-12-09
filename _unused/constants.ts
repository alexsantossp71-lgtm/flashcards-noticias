
import { ImageStyle } from './types';

// NÍVEL 2: Google News RSS (Frescor e Agregação)
export const rssFeeds: Record<string, string> = {
    "Brasil": "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "Mundo": "https://news.google.com/rss/search?q=internacional+mundo+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "Política": "https://news.google.com/rss/search?q=politica+brasil+governo+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "Esportes": "https://news.google.com/rss/search?q=esportes+futebol+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "Tecnologia": "https://news.google.com/rss/search?q=tecnologia+inovacao+ia+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "Economia": "https://news.google.com/rss/search?q=economia+mercado+financeiro+when:1d&hl=pt-BR&gl=BR&ceid=BR:pt-419"
};

// NÍVEL 3: G1/Globo Feeds (Fonte Confiável Específica)
export const g1Feeds: Record<string, string> = {
    "Brasil": "https://g1.globo.com/rss/g1/",
    "Mundo": "https://g1.globo.com/rss/g1/mundo/",
    "Política": "https://g1.globo.com/rss/g1/politica/blog/andreia-sadi/",
    "Esportes": "https://ge.globo.com/rss/ge/",
    "Tecnologia": "https://g1.globo.com/rss/g1/tecnologia/",
    "Economia": "https://g1.globo.com/rss/g1/economia/"
};

export const imageStyles: ImageStyle[] = [
    {
        id: 'default',
        label: 'Vetorial Padrão',
        previewColor: '#0ea5e9',
        previewEmoji: '🔷',
        prompt: 'o estilo deve ser vetorial, moderno, com cores extremamente vibrantes, contornos nítidos e um alto nível de detalhe. A estética deve ser limpa e gráfica.'
    },
    {
        id: 'cartoon',
        label: 'Cartoon 2D',
        previewColor: '#f59e0b',
        previewEmoji: '🎬',
        prompt: 'o estilo deve ser cartoon 2D vibrante, com linhas de contorno definidas, cores planas e saturadas, e personagens expressivos, lembrando animações modernas de TV.'
    },
    {
        id: '3d',
        label: '3D Pixar',
        previewColor: '#6366f1',
        previewEmoji: '🧸',
        prompt: 'o estilo deve ser renderização 3D estilizada (tipo Pixar/Disney), com iluminação suave, texturas fofas (soft shading), formas arredondadas e cores agradáveis.'
    },
    {
        id: 'watercolor',
        label: 'Aquarela',
        previewColor: '#38bdf8',
        previewEmoji: '🖌️',
        prompt: 'o estilo deve ser pintura em Aquarela suave e artística, com bordas difusas, texturas de papel visíveis, cores translúcidas misturadas e efeitos de gotejamento.'
    },
    {
        id: 'cyberpunk',
        label: 'Cyberpunk',
        previewColor: '#d946ef',
        previewEmoji: '🌆',
        prompt: 'o estilo deve ser Cyberpunk futurista, utilizando uma paleta de cores neon (ciano, magenta, roxo) sobre fundos escuros, com elementos de tecnologia e brilhos.'
    },
    {
        id: 'impressionism',
        label: 'Impressionismo',
        previewColor: '#fcd34d',
        previewEmoji: '🎨',
        prompt: 'o estilo deve ser Impressionista, semelhante às obras de Van Gogh ou Monet, com pinceladas visíveis e expressivas, cores vibrantes misturadas diretamente na tela e foco na luz e movimento.'
    },
    {
        id: 'cubism',
        label: 'Cubismo',
        previewColor: '#a855f7',
        previewEmoji: '🧊',
        prompt: 'o estilo deve ser Cubismo analítico ou sintético, inspirado em Picasso, com formas geométricas fragmentadas, múltiplas perspectivas simultâneas e abstração da realidade.'
    },
    {
        id: 'popart',
        label: 'Pop Art',
        previewColor: '#ef4444',
        previewEmoji: '🥫',
        prompt: 'o estilo deve ser Pop Art no estilo de Andy Warhol ou Roy Lichtenstein, com cores primárias saturadas, alto contraste, retículas (pontos) visíveis e contornos pretos grossos.'
    },
    {
        id: 'surrealism',
        label: 'Surrealismo',
        previewColor: '#14b8a6',
        previewEmoji: '🕰️',
        prompt: 'o estilo deve ser Surrealista, como Salvador Dalí, combinando elementos realistas em cenários oníricos e bizarros, com distorções lógicas e uma atmosfera misteriosa.'
    },
    {
        id: 'noir',
        label: 'Filme Noir',
        previewColor: '#171717',
        previewEmoji: '🕵️',
        prompt: 'o estilo deve ser Fotografia Film Noir ou Sin City, em preto e branco de alto contraste (ou com uma única cor de destaque), sombras dramáticas e atmosfera de mistério.'
    },
    {
        id: 'artnouveau',
        label: 'Art Nouveau',
        previewColor: '#d97706',
        previewEmoji: '⚜️',
        prompt: 'o estilo deve ser Art Nouveau, inspirado em Alphonse Mucha, com linhas orgânicas fluidas, ornamentos florais complexos, molduras decorativas e uma elegância clássica.'
    },
    {
        id: 'steampunk',
        label: 'Steampunk',
        previewColor: '#78350f',
        previewEmoji: '⚙️',
        prompt: 'o estilo deve ser Steampunk vitoriano, com engrenagens de latão, vapor, cobre, roupas de época e uma estética retro-futurista industrial detalhada.'
    },
    {
        id: 'ukiyo',
        label: 'Ukiyo-e (Japão)',
        previewColor: '#f87171',
        previewEmoji: '🌊',
        prompt: 'o estilo deve ser Ukiyo-e (gravura japonesa clássica), como "A Grande Onda", com linhas finas, cores chapadas, texturas de papel de arroz e composições assimétricas.'
    },
    {
        id: 'renaissance',
        label: 'Renascença',
        previewColor: '#92400e',
        previewEmoji: '🖼️',
        prompt: 'o estilo deve ser pintura a óleo Renascentista clássica, com iluminação chiaroscuro (luz e sombra dramáticas), composições equilibradas, realismo anatômico e tons terrosos ricos.'
    },
    {
        id: 'pixel',
        label: 'Pixel Art',
        previewColor: '#22c55e',
        previewEmoji: '👾',
        prompt: 'o estilo deve ser Pixel Art de alta definição, lembrando jogos clássicos de 16-bits, com cores vibrantes e estética retrô.'
    },
    {
        id: 'minimalist',
        label: 'Minimalista',
        previewColor: '#64748b',
        previewEmoji: '⚪',
        prompt: 'o estilo deve ser Flat Design Minimalista, utilizando formas geométricas simples, ícones simbólicos e muito espaço negativo.'
    },
    {
        id: 'clay',
        label: 'Massinha',
        previewColor: '#8b5cf6',
        previewEmoji: '🏺',
        prompt: 'o estilo deve ser Claymation (animação de massinha), com texturas táteis, aparência de plasticina e iluminação de estúdio.'
    }
];
