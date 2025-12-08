// All Page Rendering Logic
import { api } from './api.js';
import { state } from './state.js';
import { navigateTo } from './router.js';
import { icons, render, ProgressBar } from './components.js';

// Constants
const NEWS_CATEGORIES = ['Brasil', 'Mundo', 'Política', 'Esportes', 'Tecnologia', 'Economia'];

const IMAGE_STYLES = [
    { id: 'default', label: 'Vetorial Padrão', emoji: '🔷', prompt: 'o estilo deve ser vetorial, moderno, com cores extremamente vibrantes, contornos nítidos e um alto nível de detalhe. A estética deve ser limpa e gráfica.' },
    { id: 'cartoon', label: 'Cartoon 2D', emoji: '🎬', prompt: 'o estilo deve ser cartoon 2D vibrante, com linhas de contorno definidas, cores planas e saturadas, e personagens expressivos, lembrando animações modernas de TV.' },
    { id: '3d', label: '3D Pixar', emoji: '🧸', prompt: 'o estilo deve ser renderização 3D estilizada (tipo Pixar/Disney), com iluminação suave, texturas fofas (soft shading), formas arredondadas e cores agradáveis.' },
    { id: 'watercolor', label: 'Aquarela', emoji: '🖌️', prompt: 'o estilo deve ser aquarela artística, com pinceladas suaves, transições de cor fluidas, bordas levemente desfocadas e uma estética delicada e orgânica.' },
    { id: 'neon', label: 'Neon Cyberpunk', emoji: '🌃', prompt: 'o estilo deve ser cyberpunk neon, com cores vibrantes (rosa, ciano, roxo), iluminação neon intensa, alto contraste, atmosfera futurista e urbana noturna.' },
    { id: 'minimalist', label: 'Minimalista', emoji: '⚪', prompt: 'o estilo deve ser minimalista e clean, com formas geométricas simples, paleta de cores limitada (2-3 cores), muito espaço negativo e design ultra-simplificado.' }
];

// ========== HOME PAGE ==========
export function renderHomePage() {
    const useGoogle = state.get('useGoogleSearch');

    render(`
        <div class="min-h-screen bg-gray-900 flex flex-col p-4">
            <!-- Header -->
            <div class="flex justify-between items-center py-4 mb-2">
                <h1 class="text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-sky-400 to-purple-500">
                    FlashNews AI
                </h1>
                <div class="flex items-center gap-2">
                    <button id="btn-saved" class="px-3 py-1 bg-gray-800 text-xs font-bold text-gray-300 rounded-full border border-gray-700 hover:border-primary-500 hover:text-white transition-all">
                        Meus Posts
                    </button>
                    <button id="btn-about" class="p-2 text-gray-400 hover:text-white">
                        ${icons.info}
                    </button>
                </div>
            </div>

            <p class="text-gray-400 text-sm mb-6">Crie stories virais em segundos.</p>

            <!-- Tab Switcher -->
            <div class="flex bg-gray-800 p-1 rounded-xl mb-6">
                <button id="tab-categories" class="flex-1 py-2 text-sm font-medium rounded-lg transition-all bg-gray-700 text-white shadow">Categorias</button>
                <button id="tab-link" class="flex-1 py-2 text-sm font-medium rounded-lg transition-all text-gray-400">Link</button>
                <button id="tab-topic" class="flex-1 py-2 text-sm font-medium rounded-lg transition-all text-gray-400">Tópico</button>
            </div>

            <!-- Content -->
            <div id="tab-content" class="flex-1"></div>
        </div>
    `);

    // Event listeners
    document.getElementById('btn-saved').addEventListener('click', () => navigateTo('/saved'));
    document.getElementById('btn-about').addEventListener('click', () => navigateTo('/about'));

    // Tab switching
    const tabs = ['categories', 'link', 'topic'];
    tabs.forEach(tab => {
        document.getElementById(`tab-${tab}`).addEventListener('click', () => {
            tabs.forEach(t => {
                const btn = document.getElementById(`tab-${t}`);
                if (t === tab) {
                    btn.className = 'flex-1 py-2 text-sm font-medium rounded-lg transition-all bg-gray-700 text-white shadow';
                } else {
                    btn.className = 'flex-1 py-2 text-sm font-medium rounded-lg transition-all text-gray-400';
                }
            });
            renderTabContent(tab);
        });
    });

    renderTabContent('categories');
}

function renderTabContent(tab) {
    const container = document.getElementById('tab-content');
    const useGoogle = state.get('useGoogleSearch');

    if (tab === 'categories') {
        container.innerHTML = `
            <div class="animate-fade-in space-y-4">
                <!-- Quick URL Input -->
                <div class="bg-gray-800 p-4 rounded-xl border border-gray-700">
                    <h3 class="text-white font-semibold mb-3 flex items-center text-sm">${icons.externalLink} Cole uma URL diretamente</h3>
                    <div class="flex gap-2">
                        <input id="quick-url-input" type="text" placeholder="https://..." class="flex-1 bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-sky-500 outline-none text-white placeholder-gray-500" />
                        <button id="btn-quick-analyze" class="bg-sky-600 hover:bg-sky-500 text-white px-4 py-2 rounded-lg font-bold text-sm whitespace-nowrap">Gerar</button>
                    </div>
                </div>

                <!-- Categories -->
                <div class="flex justify-between items-center px-2">
                    <h2 class="text-white font-semibold flex items-center">${icons.fire} Em alta</h2>
                    <button id="toggle-source" class="flex items-center px-3 py-1 rounded-full text-xs font-bold transition-all ${useGoogle ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}">
                        ${useGoogle ? icons.globe + ' Web' : icons.rss + ' RSS'}
                    </button>
                </div>
                <div class="grid grid-cols-2 gap-3" id="categories-grid"></div>
            </div>
        `;

        const grid = document.getElementById('categories-grid');
        NEWS_CATEGORIES.forEach(cat => {
            const btn = document.createElement('button');
            btn.className = 'p-4 bg-gray-800 active:bg-sky-700 rounded-xl border border-gray-700 hover:border-sky-500 transition-all text-left font-medium text-white shadow-sm';
            btn.textContent = cat;
            btn.addEventListener('click', () => fetchHeadlines(cat));
            grid.appendChild(btn);
        });

        document.getElementById('toggle-source').addEventListener('click', () => {
            state.set('useGoogleSearch', !state.get('useGoogleSearch'));
            renderTabContent('categories');
        });

        // Quick URL handler
        const quickInput = document.getElementById('quick-url-input');
        const quickBtn = document.getElementById('btn-quick-analyze');
        quickBtn.addEventListener('click', () => handleUrlSubmit(quickInput.value));
        quickInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') handleUrlSubmit(quickInput.value);
        });

    } else if (tab === 'link') {
        container.innerHTML = `
            <div class="animate-fade-in bg-gray-800 p-5 rounded-2xl border border-gray-700">
                <h2 class="text-lg font-semibold text-white mb-4 flex items-center">${icons.externalLink} Via Link</h2>
                <input id="url-input" type="text" placeholder="Cole a URL da notícia..." class="w-full bg-gray-900 border border-gray-600 rounded-xl px-4 py-3 mb-4 focus:ring-2 focus:ring-sky-500 outline-none text-white placeholder-gray-500" />
                <button id="btn-analyze" class="w-full bg-sky-600 text-white p-3 rounded-xl font-bold disabled:opacity-50">Analisar</button>
            </div>
        `;

        const input = document.getElementById('url-input');
        const btn = document.getElementById('btn-analyze');
        btn.addEventListener('click', () => handleUrlSubmit(input.value));

    } else if (tab === 'topic') {
        container.innerHTML = `
            <div class="animate-fade-in bg-gray-800 p-5 rounded-2xl border border-gray-700">
                <h2 class="text-lg font-semibold text-white mb-4 flex items-center">${icons.sparkles} Criar Guia</h2>
                <input id="topic-input" type="text" placeholder="Ex: História do Bitcoin..." class="w-full bg-gray-900 border border-gray-600 rounded-xl px-4 py-3 mb-4 focus:ring-2 focus:ring-purple-500 outline-none text-white placeholder-gray-500" />
                <button id="btn-create" class="w-full bg-purple-600 text-white p-3 rounded-xl font-bold disabled:opacity-50">Criar</button>
            </div>
        `;

        const input = document.getElementById('topic-input');
        const btn = document.getElementById('btn-create');
        btn.addEventListener('click', () => handleGuideSubmit(input.value));
    }
}

async function fetchHeadlines(category) {
    try {
        state.showLoading(`Buscando ${category}...`);
        const data = await api.getHeadlines(category);
        state.set('headlines', data.headlines || []);
        state.set('headlineSourceTitle', category);
        state.hideLoading();
        navigateTo('/headlines');
    } catch (error) {
        state.hideLoading();
        state.showError('Erro ao buscar manchetes: ' + error.message);
    }
}

async function handleUrlSubmit(url) {
    if (!url) return;
    try {
        state.showLoading('Extraindo informações...');
        const data = await api.getHeadlineFromUrl(url);
        state.set('selectedHeadline', data);
        state.hideLoading();
        navigateTo('/style');
    } catch (error) {
        state.hideLoading();
        state.showError('Erro ao processar URL: ' + error.message);
    }
}

async function handleGuideSubmit(topic) {
    if (!topic) return;
    state.showError('Funcionalidade de guia ainda não implementada na versão vanilla JS');
}

// ========== HEADLINES PAGE ==========
export function renderHeadlinesPage() {
    const headlines = state.get('headlines');
    const title = state.get('headlineSourceTitle');
    const selectedIndices = state.get('selectedIndices');

    render(`
        <div class="min-h-screen bg-gray-900 flex flex-col p-4 pb-24">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center">
                    <button id="btn-back" class="p-2 -ml-2 text-gray-400">${icons.chevronLeft}</button>
                    <h2 class="text-xl font-bold text-white ml-2">${title}</h2>
                </div>
                <button id="btn-select-all" class="text-sm text-primary-400 font-medium px-3 py-1 rounded hover:bg-gray-800">
                    ${selectedIndices.size === headlines.length ? 'Desmarcar Todos' : 'Selecionar Todos'}
                </button>
            </div>

            <div class="space-y-3 pb-safe" id="headlines-list"></div>

            ${selectedIndices.size > 0 ? `
                <div class="fixed bottom-6 left-4 right-4 animate-in slide-in-from-bottom duration-300">
                    <button id="btn-batch" class="w-full bg-primary-600 hover:bg-primary-500 text-white font-bold py-4 px-6 rounded-xl shadow-lg flex items-center justify-center gap-2">
                        ${icons.sparkles}
                        <span>Gerar ${selectedIndices.size} Itens Selecionados</span>
                    </button>
                </div>
            ` : ''}
        </div>
    `);

    document.getElementById('btn-back').addEventListener('click', () => navigateTo('/'));
    document.getElementById('btn-select-all').addEventListener('click', toggleSelectAll);
    if (selectedIndices.size > 0) {
        document.getElementById('btn-batch').addEventListener('click', startBatchGeneration);
    }

    renderHeadlinesList();
}

function renderHeadlinesList() {
    const headlines = state.get('headlines');
    const selectedIndices = state.get('selectedIndices');
    const list = document.getElementById('headlines-list');

    list.innerHTML = headlines.map((item, idx) => {
        const isSelected = selectedIndices.has(idx);
        return `
            <div class="relative p-5 rounded-xl border shadow-sm transition-all ${isSelected ? 'bg-gray-800 border-primary-500 ring-1 ring-primary-500' : 'bg-gray-800/50 border-gray-700 hover:bg-gray-800'}">
                <div class="flex items-start gap-4">
                    <div class="pt-1">
                        <input type="checkbox" data-idx="${idx}" ${isSelected ? 'checked' : ''} class="w-5 h-5 rounded border-gray-600 bg-gray-700 text-primary-600 focus:ring-primary-500 cursor-pointer" />
                    </div>
                    <button data-single="${idx}" class="flex-1 text-left">
                        <h3 class="font-semibold text-white mb-2 leading-snug">${item.headline}</h3>
                        <span class="text-xs text-sky-400 uppercase font-bold">${item.source}</span>
                    </button>
                </div>
            </div>
        `;
    }).join('');

    // Add event listeners
    list.querySelectorAll('input[type="checkbox"]').forEach(cb => {
        cb.addEventListener('change', (e) => {
            const idx = parseInt(e.target.dataset.idx);
            toggleSelection(idx);
        });
    });

    list.querySelectorAll('[data-single]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const idx = parseInt(e.currentTarget.dataset.single);
            state.set('selectedHeadline', headlines[idx]);
            navigateTo('/style');
        });
    });
}

function toggleSelection(idx) {
    const selected = state.get('selectedIndices');
    if (selected.has(idx)) {
        selected.delete(idx);
    } else {
        selected.add(idx);
    }
    state.set('selectedIndices', new Set(selected));
    renderHeadlinesPage();
}

function toggleSelectAll() {
    const headlines = state.get('headlines');
    const selected = state.get('selectedIndices');

    if (selected.size === headlines.length) {
        state.set('selectedIndices', new Set());
    } else {
        state.set('selectedIndices', new Set(headlines.map((_, i) => i)));
    }
    renderHeadlinesPage();
}

async function startBatchGeneration() {
    const headlines = state.get('headlines');
    const selectedIndices = state.get('selectedIndices');
    const selectedHeadlines = headlines.filter((_, i) => selectedIndices.has(i));

    // For now, navigate to style page to select style first
    // In full implementation, would need to handle batch with selected style
    state.showError('Selecione um estilo primeiro. Funcionalidade de lote completa em desenvolvimento.');
}

// ========== STYLE PAGE ==========
export function renderStylePage() {
    render(`
        <div class="min-h-screen bg-gray-900 flex flex-col p-4">
            <div class="flex items-center mb-6">
                <button id="btn-back" class="p-2 -ml-2 text-gray-400">${icons.chevronLeft}</button>
                <h2 class="text-xl font-bold text-white ml-2">Escolha o Estilo</h2>
            </div>

            <div class="grid grid-cols-2 gap-4" id="styles-grid"></div>
        </div>
    `);

    document.getElementById('btn-back').addEventListener('click', () => window.history.back());

    const grid = document.getElementById('styles-grid');
    IMAGE_STYLES.forEach(style => {
        const card = document.createElement('button');
        card.className = 'p-6 bg-gray-800 rounded-xl border-2 border-gray-700 hover:border-primary-500 transition-all text-center';
        card.innerHTML = `
            <div class="text-4xl mb-2">${style.emoji}</div>
            <div class="text-white font-semibold">${style.label}</div>
        `;
        card.addEventListener('click', () => selectStyle(style));
        grid.appendChild(card);
    });
}

function selectStyle(style) {
    state.set('selectedStyle', style);
    navigateTo('/result');
    startGeneration();
}

// ========== RESULT PAGE ==========
export function renderResultPage() {
    const flashcards = state.get('flashcards');

    render(`
        <div class="min-h-screen bg-gray-900 flex flex-col p-4">
            <div class="flex items-center mb-6">
                <button id="btn-back" class="p-2 -ml-2 text-gray-400">${icons.chevronLeft}</button>
                <h2 class="text-xl font-bold text-white ml-2">Flashcards Gerados</h2>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2 pb-safe" id="cards-grid">
                ${flashcards.length === 0 ? '<p class="text-gray-400 col-span-full text-center">Gerando...</p>' : ''}
            </div>
        </div>
    `);

    document.getElementById('btn-back').addEventListener('click', () => navigateTo('/'));
    renderFlashcards();
}

function renderFlashcards() {
    const flashcards = state.get('flashcards');
    const grid = document.getElementById('cards-grid');

    if (!grid) return;

    grid.innerHTML = flashcards.map((card, idx) => `
        <div class="relative aspect-[9/16] bg-gray-800 rounded-lg overflow-hidden shadow-lg">
            ${card.imageBase64 ? `
                <img src="data:image/png;base64,${card.imageBase64}" alt="Card ${idx + 1}" class="w-full h-full object-cover" />
            ` : `
                <div class="w-full h-full flex items-center justify-center bg-gray-700">
                    <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-500"></div>
                </div>
            `}
        </div>
    `).join('');
}

async function startGeneration() {
    const headline = state.get('selectedHeadline');
    const style = state.get('selectedStyle');

    try {
        state.showLoading('Gerando conteúdo...');
        const content = await api.generateFlashcardContent(
            headline.headline,
            headline.url,
            style.prompt,
            headline.source
        );

        // Initialize cards with placeholders
        const initialCards = content.flashcards.map(fc => ({
            text: fc.text,
            imagePrompt: fc.imagePrompt,
            imageBase64: null
        }));

        state.set('flashcards', initialCards);
        state.hideLoading();
        renderFlashcards();

        // Generate images one by one
        for (let i = 0; i < initialCards.length; i++) {
            state.showLoading(`Gerando imagem ${i + 1}/${initialCards.length}...`);
            try {
                const imageData = await api.generateImage(
                    initialCards[i].imagePrompt,
                    style.prompt,
                    initialCards[i].text,
                    i + 1  // Card number (1-indexed)
                );
                const flashcards = state.get('flashcards');
                flashcards[i].imageBase64 = imageData.imageBase64;
                state.set('flashcards', [...flashcards]);
                renderFlashcards();
            } catch (err) {
                console.error(`Error generating image ${i}:`, err);
            }
        }
        state.hideLoading();

    } catch (error) {
        state.hideLoading();
        state.showError('Erro na geração: ' + error.message);
    }
}

// ========== SAVED POSTS PAGE ==========
export function renderSavedPostsPage() {
    render(`
        <div class="min-h-screen bg-gray-900 flex flex-col p-4 pb-24">
            <div class="flex items-center mb-6">
                <button id="btn-back" class="p-2 -ml-2 text-gray-400">${icons.chevronLeft}</button>
                <h2 class="text-xl font-bold text-white ml-2">Posts Salvos</h2>
            </div>
            <div id="posts-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
        </div>
    `);

    document.getElementById('btn-back').addEventListener('click', () => navigateTo('/'));
    loadSavedPosts();
}

async function loadSavedPosts() {
    try {
        const data = await api.getSavedPosts();
        const container = document.getElementById('posts-container');

        if (!data.posts || data.posts.length === 0) {
            container.innerHTML = '<p class="text-gray-500 text-center col-span-full">Nenhum post salvo encontrado.</p>';
            return;
        }

        container.innerHTML = data.posts.map(post => `
            <div data-post-id="${post.id}" class="bg-gray-800 rounded-xl overflow-hidden border border-gray-700 shadow-sm hover:border-primary-500 transition-all cursor-pointer">
                <div class="h-32 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center relative">
                    <span class="text-3xl opacity-20">🖼️</span>
                    <div class="absolute top-2 right-2">
                        <span class="bg-black/50 text-white text-xs px-2 py-1 rounded backdrop-blur-sm">${post.category}</span>
                    </div>
                </div>
                <div class="p-4">
                    <h3 class="font-bold text-white mb-2 line-clamp-2 leading-snug">${post.headline}</h3>
                    <div class="flex items-center justify-between text-xs text-gray-400 mt-3">
                        <span>${new Date(post.timestamp).toLocaleDateString()}</span>
                        <button data-delete="${post.id}" class="p-2 hover:bg-red-500/20 hover:text-red-400 rounded-full transition-colors">
                            ${icons.trash}
                        </button>
                    </div>
                </div>
            </div>
        `).join('');

        // Add click handlers
        container.querySelectorAll('[data-post-id]').forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.closest('[data-delete]')) {
                    navigateTo(`/saved/${card.dataset.postId}`);
                }
            });
        });

        container.querySelectorAll('[data-delete]').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.stopPropagation();
                if (confirm('Tem certeza que deseja apagar este post?')) {
                    try {
                        await api.deletePost(btn.dataset.delete);
                        loadSavedPosts();
                    } catch (err) {
                        state.showError('Erro ao deletar: ' + err.message);
                    }
                }
            });
        });

    } catch (error) {
        state.showError('Erro ao carregar posts: ' + error.message);
    }
}

// ========== POST DETAIL PAGE ==========
export function renderPostDetailPage(params) {
    render(`
        <div class="min-h-screen bg-gray-900 flex flex-col p-4">
            <div class="flex items-center mb-6">
                <button id="btn-back" class="p-2 -ml-2 text-gray-400">${icons.chevronLeft}</button>
                <h2 class="text-xl font-bold text-white ml-2">Detalhes do Post</h2>
            </div>
            <div id="post-content"></div>
        </div>
    `);

    document.getElementById('btn-back').addEventListener('click', () => navigateTo('/saved'));
    loadPostDetails(params.id);
}

async function loadPostDetails(postId) {
    try {
        const post = await api.getSavedPostDetails(postId);
        const container = document.getElementById('post-content');

        container.innerHTML = `
            <div class="mb-6">
                <h1 class="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-secondary-400">
                    ${post.tiktokTitle || post.headline}
                </h1>
                <p class="text-gray-400 text-sm mt-1">
                    Gerado em ${new Date(post.timestamp).toLocaleDateString()}
                </p>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2 pb-safe">
                ${post.cards.map((card, idx) => `
                    <div class="relative aspect-[9/16] bg-gray-800 rounded-lg overflow-hidden shadow-lg">
                        <img 
                            src="${api.getPostImageUrl(postId, idx)}" 
                            alt="Card ${idx + 1}" 
                            class="w-full h-full object-cover"
                            onerror="this.src='https://placehold.co/400x600/1f2937/white?text=Error'"
                        />
                        <div class="absolute inset-x-0 bottom-0 p-3 text-overlay-gradient pt-10">
                            <div class="text-white text-xs md:text-sm font-medium leading-relaxed drop-shadow-md">
                                ${card.text || 'Sem legenda'}
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    } catch (error) {
        state.showError('Erro ao carregar post: ' + error.message);
    }
}

// ========== ABOUT PAGE ==========
export function renderAboutPage() {
    render(`
        <div class="min-h-screen bg-gray-900 flex flex-col p-4">
            <div class="flex items-center mb-6">
                <button id="btn-back" class="p-2 -ml-2 text-gray-400">${icons.chevronLeft}</button>
                <h2 class="text-xl font-bold text-white ml-2">Sobre</h2>
            </div>
            <div class="prose prose-invert max-w-none">
                <h3 class="text-white">FlashNews AI</h3>
                <p class="text-gray-400">Gerador de flashcards virais para redes sociais, powered by IA local.</p>
                <h4 class="text-white mt-4">Tecnologias</h4>
                <ul class="text-gray-400">
                    <li>Frontend: HTML/CSS/JS Vanilla</li>
                    <li>Backend: Python + FastAPI</li>
                    <li>IA: Ollama (Mistral) + Diffusers</li>
                </ul>
            </div>
        </div>
    `);

    document.getElementById('btn-back').addEventListener('click', () => navigateTo('/'));
}
