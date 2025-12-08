// Main Application Entry Point
import { router } from './router.js';
import { state } from './state.js';
import {
    renderHomePage,
    renderHeadlinesPage,
    renderStylePage,
    renderResultPage,
    renderSavedPostsPage,
    renderPostDetailPage,
    renderAboutPage
} from './pages.js';

// Initialize app
function init() {
    console.log('FlashNews AI - Vanilla JS Version');

    // Initialize state
    state.set('imageStyles', []);
    state.set('selectedIndices', new Set());

    // Register routes
    router.register('/', () => renderHomePage());
    router.register('/headlines', () => renderHeadlinesPage());
    router.register('/style', () => renderStylePage());
    router.register('/result', () => renderResultPage());
    router.register('/saved', () => renderSavedPostsPage());
    router.register('/saved', (params) => renderPostDetailPage(params)); // With ID param
    router.register('/about', () => renderAboutPage());

    // Trigger initial route
    router.handleRouteChange();
}

// Start app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
