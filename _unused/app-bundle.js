// FlashNews AI - Simplified Bundle with Direct Navigation
(function () {
    'use strict';

    const API_URL = 'http://localhost:8000';
    const CATEGORIES = ['Brasil', 'Mundo', 'Política', 'Esportes', 'Tecnologia', 'Economia'];
    const STYLES = [
        { id: 'default', label: 'Vetorial Padrão', emoji: '🔷', prompt: 'o estilo deve ser vetorial, moderno, com cores extremamente vibrantes' },
        { id: 'cartoon', label: 'Cartoon 2D', emoji: '🎬', prompt: 'o estilo deve ser cartoon 2D vibrante' },
        { id: '3d', label: '3D Pixar', emoji: '🧸', prompt: 'o estilo deve ser renderização 3D estilizada tipo Pixar' },
        { id: 'watercolor', label: 'Aquarela', emoji: '🖌️', prompt: 'o estilo deve ser aquarela artística' },
        { id: 'neon', label: 'Neon Cyberpunk', emoji: '🌃', prompt: 'o estilo deve ser cyberpunk neon' },
        { id: 'minimalist', label: 'Minimalista', emoji: '⚪', prompt: 'o estilo deve ser minimalista e clean' }
    ];

    const state = {
        headlines: [],
        headlineSourceTitle: '',
        selectedHeadline: null,
        selectedStyle: null,
        flashcards: []
    };

    const ICONS = {
        back: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5"/></svg>`,
        info: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z"/></svg>`
    };

    function showLoading(msg) {
        document.getElementById('loading-overlay').classList.remove('hidden');
        document.getElementById('loading-message').textContent = msg;
    }

    function hideLoading() {
        document.getElementById('loading-overlay').classList.add('hidden');
    }

    function render(html) {
        document.getElementById('app').innerHTML = html;
    }

    function esc(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async function apiCall(endpoint, options = {}) {
        const response = await fetch(`${API_URL}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    }

    // ===== PAGES =====

    function showHome() {
        render(`
            <div class="min-h-screen bg-gray-900 p-4">
                <div class="flex justify-between items-center py-4 mb-2">
                    <h1 class="text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-sky-400 to-purple-500">FlashNews AI</h1>
                    <button onclick="app.showAbout()" class="p-2 text-gray-400 hover:text-white">${ICONS.info}</button>
                </div>
                <p class="text-gray-400 text-sm mb-6">Crie stories virais em segundos.</p>
                <div class="grid grid-cols-2 gap-3">
                    ${CATEGORIES.map(cat => `
                        <button onclick="app.fetchHeadlines('${cat}')" 
                                class="p-4 bg-gray-800 rounded-xl border border-gray-700 hover:border-sky-500 transition-all text-white font-medium">
                            ${cat}
                        </button>
                    `).join('')}
                </div>
            </div>
        `);
    }

    function showHeadlines() {
        render(`
            <div class="min-h-screen bg-gray-900 p-4">
                <div class="flex items-center mb-6">
                    <button onclick="app.showHome()" class="p-2 -ml-2 text-gray-400">${ICONS.back}</button>
                    <h2 class="text-xl font-bold text-white ml-2">${state.headlineSourceTitle}</h2>
                </div>
                <div class="space-y-3">
                    ${state.headlines.map((item, idx) => `
                        <div class="p-5 rounded-xl bg-gray-800 border border-gray-700 hover:border-primary-500 transition-all">
                            <button onclick="app.selectHeadline(${idx})" class="w-full text-left">
                                <h3 class="font-semibold text-white mb-2">${esc(item.headline)}</h3>
                                <span class="text-xs text-sky-400 uppercase font-bold">${esc(item.source)}</span>
                            </button>
                        </div>
                    `).join('')}
                </div>
            </div>
        `);
    }

    function showStyles() {
        render(`
            <div class="min-h-screen bg-gray-900 p-4">
                <div class="flex items-center mb-6">
                    <button onclick="app.showHeadlines()" class="p-2 -ml-2 text-gray-400">${ICONS.back}</button>
                    <h2 class="text-xl font-bold text-white ml-2">Escolha o Estilo</h2>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    ${STYLES.map((style, idx) => `
                        <button onclick="app.selectStyle(${idx})" 
                                class="p-6 bg-gray-800 rounded-xl border-2 border-gray-700 hover:border-primary-500 transition-all text-center">
                            <div class="text-4xl mb-2">${style.emoji}</div>
                            <div class="text-white font-semibold">${style.label}</div>
                        </button>
                    `).join('')}
                </div>
            </div>
        `);
    }

    function showResult() {
        render(`
            <div class="min-h-screen bg-gray-900 p-4">
                <div class="flex items-center mb-6">
                    <button onclick="app.showHome()" class="p-2 -ml-2 text-gray-400">${ICONS.back}</button>
                    <h2 class="text-xl font-bold text-white ml-2">Flashcards Gerados</h2>
                </div>
                <div id="cards-grid" class="grid grid-cols-2 md:grid-cols-4 gap-2"></div>
            </div>
        `);
        updateCards();
    }

    function updateCards() {
        const grid = document.getElementById('cards-grid');
        if (!grid) return;
        grid.innerHTML = state.flashcards.map((card, idx) => `
            <div class="relative aspect-[9/16] bg-gray-800 rounded-lg overflow-hidden">
                ${card.imageBase64 ? `
                    <img src="data:image/png;base64,${card.imageBase64}" class="w-full h-full object-cover" />
                ` : `
                    <div class="w-full h-full flex items-center justify-center">
                        <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-primary-500"></div>
                    </div>
                `}
                <div class="absolute inset-x-0 bottom-0 p-3 bg-gradient-to-t from-black/90 to-transparent pt-10">
                    <div class="text-white text-xs font-medium">${esc(card.text || '')}</div>
                </div>
            </div>
        `).join('');
    }

    function showAbout() {
        render(`
            <div class="min-h-screen bg-gray-900 p-4">
                <div class="flex items-center mb-6">
                    <button onclick="app.showHome()" class="p-2 -ml-2 text-gray-400">${ICONS.back}</button>
                    <h2 class="text-xl font-bold text-white ml-2">Sobre</h2>
                </div>
                <div class="max-w-2xl">
                    <h3 class="text-white text-xl font-bold mb-2">FlashNews AI</h3>
                    <p class="text-gray-400 mb-4">Gerador de flashcards virais com IA local.</p>
                    <h4 class="text-white font-bold mt-4 mb-2">Tecnologias</h4>
                    <ul class="text-gray-400 space-y-1">
                        <li>• Frontend: HTML/CSS/JS Vanilla</li>
                        <li>• Backend: Python + FastAPI</li>
                        <li>• IA: Ollama + Diffusers</li>
                    </ul>
                </div>
            </div>
        `);
    }

    // ===== ACTIONS =====

    async function fetchHeadlines(category) {
        try {
            showLoading(`Buscando ${category}...`);
            const data = await apiCall('/api/headlines', {
                method: 'POST',
                body: JSON.stringify({ category, count: 15 })
            });
            state.headlines = data.headlines || [];
            state.headlineSourceTitle = category;
            hideLoading();
            showHeadlines();
        } catch (error) {
            hideLoading();
            alert('Erro: ' + error.message);
        }
    }

    function selectHeadline(idx) {
        state.selectedHeadline = state.headlines[idx];
        showStyles();
    }

    async function selectStyle(idx) {
        state.selectedStyle = STYLES[idx];
        await startGeneration();
    }

    async function startGeneration() {
        const headline = state.selectedHeadline;
        const style = state.selectedStyle;

        try {
            showLoading('Gerando conteúdo...');
            const content = await apiCall('/api/generate-content', {
                method: 'POST',
                body: JSON.stringify({
                    headline: headline.headline,
                    url: headline.url,
                    stylePrompt: style.prompt,
                    source: headline.source
                })
            });

            state.flashcards = content.flashcards.map(fc => ({
                text: fc.text,
                imagePrompt: fc.imagePrompt,
                imageBase64: null
            }));

            hideLoading();
            showResult();

            // Generate images
            for (let i = 0; i < state.flashcards.length; i++) {
                showLoading(`Gerando imagem ${i + 1}/${state.flashcards.length}...`);
                try {
                    await new Promise(r => setTimeout(r, 2000));
                    const imgData = await apiCall('/api/generate-image', {
                        method: 'POST',
                        body: JSON.stringify({
                            prompt: state.flashcards[i].imagePrompt,
                            stylePrompt: style.prompt
                        })
                    });
                    state.flashcards[i].imageBase64 = imgData.imageBase64;
                    updateCards();
                } catch (err) {
                    console.error('Image error:', err);
                }
            }
            hideLoading();
        } catch (error) {
            hideLoading();
            alert('Erro: ' + error.message);
        }
    }

    // ===== PUBLIC API =====
    window.app = {
        showHome,
        showHeadlines,
        showStyles,
        showResult,
        showAbout,
        fetchHeadlines,
        selectHeadline,
        selectStyle
    };

    // ===== INIT =====
    showHome();
    console.log('FlashNews AI loaded');
})();
