let allPosts = [];
let currentPostId = null;
let currentPostData = null;

window.addEventListener('DOMContentLoaded', loadPosts);

async function loadPosts() {
    showLoading();
    try {
        const response = await fetch('../generated_posts/index.json');
        if (!response.ok) throw new Error('Falha ao carregar index.json');
        const data = await response.json();
        allPosts = data.posts || [];
        if (allPosts.length === 0) {
            showEmptyState();
        } else {
            displayStats();
            displayPosts();
        }
        hideLoading();
    } catch (error) {
        console.error('Error loading posts:', error);
        showError(error.message);
        hideLoading();
    }
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2000);
}

async function copyToClipboard(text, label) {
    try {
        await navigator.clipboard.writeText(text);
        showToast(`✓ ${label} copiado!`);
    } catch (err) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showToast(`✓ ${label} copiado!`);
    }
}

async function downloadAllCardsAsZip(postId, postData) {
    showToast('📦 Gerando ZIP...');
    const zip = new JSZip();
    const parts = postId.split('_');
    const date = parts[1];
    const dateFormatted = `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`;
    for (let i = 0; i < postData.cards.length; i++) {
        const imgPath = `../generated_posts/${dateFormatted}/${postId}/card_${i + 1}.png`;
        try {
            const response = await fetch(imgPath);
            const blob = await response.blob();
            zip.file(`card_${i + 1}.png`, blob);
        } catch (err) {
            console.error(`Failed to add card ${i + 1}:`, err);
        }
    }
    const zipBlob = await zip.generateAsync({ type: 'blob' });
    const url = URL.createObjectURL(zipBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `flashnews_${postId}.zip`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('✓ ZIP baixado!');
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function showEmptyState() {
    document.getElementById('empty-state').classList.remove('hidden');
    document.getElementById('stats').classList.add('hidden');
    document.getElementById('posts-list').classList.add('hidden');
}

function showError(message) {
    document.getElementById('error-state').classList.remove('hidden');
    document.getElementById('error-message').textContent = message;
    document.getElementById('stats').classList.add('hidden');
    document.getElementById('posts-list').classList.add('hidden');
}

function displayStats() {
    const totalCards = allPosts.reduce((sum, post) => sum + post.card_count, 0);
    const categories = [...new Set(allPosts.map(p => p.category))];
    document.getElementById('total-posts').textContent = allPosts.length;
    document.getElementById('total-cards').textContent = totalCards;
    document.getElementById('total-categories').textContent = categories.length;
    document.getElementById('stats').classList.remove('hidden');
}

function displayPosts() {
    const container = document.getElementById('posts-list');
    container.innerHTML = '';
    const sortedPosts = [...allPosts].sort((a, b) => b.timestamp - a.timestamp);
    sortedPosts.forEach(post => {
        const date = new Date(post.timestamp * 1000);
        const dateStr = date.toLocaleDateString('pt-BR');
        const timeStr = date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
        const div = document.createElement('div');
        div.className = 'bg-gray-800 rounded-xl p-4 border border-gray-700 hover:border-sky-500 transition-all cursor-pointer active:scale-98';
        div.onclick = () => viewPost(post.id);
        div.innerHTML = `
            <div class="flex items-center gap-2 mb-2">
                <span class="px-2 py-1 bg-sky-900/50 text-sky-400 text-xs rounded-full border border-sky-700">${post.category}</span>
                <span class="text-gray-500 text-xs">${post.card_count} cards</span>
            </div>
            <h3 class="text-white font-semibold text-base mb-2">${post.headline}</h3>
            <div class="flex items-center justify-between text-xs text-gray-500">
                <span>📅 ${dateStr} ${timeStr}</span>
                <span class="text-sky-400">Ver →</span>
            </div>
        `;
        container.appendChild(div);
    });
    container.classList.remove('hidden');
}

async function viewPost(postId) {
    currentPostId = postId;
    showLoading();
    try {
        const parts = postId.split('_');
        const date = parts[1];
        const dateFormatted = `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`;
        const metadataPath = `../generated_posts/${dateFormatted}/${postId}/metadata.json`;
        const response = await fetch(metadataPath);
        if (!response.ok) throw new Error('Falha ao carregar post');
        const post = await response.json();
        currentPostData = post;
        displayPostDetail(post, postId, dateFormatted);
        document.getElementById('posts-list').classList.add('hidden');
        document.getElementById('stats').classList.add('hidden');
        document.getElementById('post-detail').classList.remove('hidden');
        window.scrollTo(0, 0);
        hideLoading();
    } catch (error) {
        console.error('Error loading post detail:', error);
        showToast('❌ Erro ao carregar post');
        hideLoading();
    }
}

function displayPostDetail(post, postId, dateFormatted) {
    const container = document.getElementById('detail-content');
    const date = new Date(post.timestamp * 1000);
    const dateStr = date.toLocaleDateString('pt-BR');
    const title = post.tiktokTitle || post.headline;
    const summary = post.tiktokSummary || '';
    container.innerHTML = `
        <div class="bg-gray-800 rounded-2xl p-5 border border-gray-700 mb-4">
            <div class="flex items-center gap-2 mb-3">
                <span class="px-3 py-1 bg-sky-900/50 text-sky-400 text-sm rounded-full border border-sky-700">${post.category}</span>
                <span class="text-gray-500 text-sm">📅 ${dateStr}</span>
            </div>
            <h1 class="text-white font-bold text-xl md:text-2xl mb-3">${post.headline}</h1>
            ${post.tiktokTitle ? `
            <div class="bg-gray-900 rounded-lg p-4 mb-3 border border-gray-700">
                <div class="mb-3">
                    <div class="flex items-start justify-between gap-2 mb-2">
                        <h3 class="text-sky-400 font-bold text-sm flex-1">📱 Título</h3>
                        <button onclick="copyToClipboard(\`${title.replace(/`/g, '\\`')}\`, 'Título')"
                            class="touch-button bg-sky-600 hover:bg-sky-500 text-white px-3 py-2 rounded-lg text-xs font-bold active:scale-95 transition-transform flex items-center gap-1">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                            </svg>
                            Copiar
                        </button>
                    </div>
                    <p class="text-gray-300 text-sm">${title}</p>
                </div>
                ${summary ? `
                <div>
                    <div class="flex items-start justify-between gap-2 mb-2">
                        <h3 class="text-purple-400 font-bold text-sm flex-1">📝 Resumo</h3>
                        <button onclick="copyToClipboard(\`${summary.replace(/`/g, '\\`').replace(/\n/g, '\\n')}\`, 'Resumo')"
                            class="touch-button bg-purple-600 hover:bg-purple-500 text-white px-3 py-2 rounded-lg text-xs font-bold active:scale-95 transition-transform flex items-center gap-1">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
                            </svg>
                            Copiar
                        </button>
                    </div>
                    <p class="text-gray-300 text-sm whitespace-pre-line">${summary}</p>
                </div>
                ` : ''}
            </div>
            ` : ''}
            <button onclick="downloadAllCardsAsZip('${postId}', currentPostData)"
                class="touch-button w-full bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white font-bold py-3 px-4 rounded-lg transition-all active:scale-95 flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Baixar Todos os Cards (ZIP)
            </button>
        </div>
        <h2 class="text-white font-semibold text-lg mb-3">🎴 Cards (${post.cards.length})</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            ${post.cards.map((card, i) => {
        const imgPath = `../generated_posts/${dateFormatted}/${postId}/card_${i + 1}.png`;
        return `
                    <div class="aspect-[9/16] bg-gray-800 rounded-lg overflow-hidden relative group">
                        <img src="${imgPath}" alt="Card ${i + 1}" class="w-full h-full object-cover" loading="lazy" />
                        <div class="absolute inset-0 bg-black/70 opacity-0 group-hover:opacity-100 group-active:opacity-100 transition-opacity flex items-center justify-center">
                            <a href="${imgPath}" download="card_${i + 1}.png"
                                class="touch-button bg-white text-black px-4 py-2 rounded-full font-bold text-sm active:scale-95 transition-transform">
                                ⬇️ Baixar
                            </a>
                        </div>
                    </div>
                `;
    }).join('')}
        </div>
    `;
}

function showPostsList() {
    document.getElementById('post-detail').classList.add('hidden');
    document.getElementById('posts-list').classList.remove('hidden');
    document.getElementById('stats').classList.remove('hidden');
    currentPostId = null;
    currentPostData = null;
    window.scrollTo(0, 0);
}
