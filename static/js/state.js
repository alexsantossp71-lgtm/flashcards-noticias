// Global State Management
class AppState {
    constructor() {
        this.state = {
            // Navigation
            currentRoute: 'home',

            // Headlines
            headlines: [],
            headlineSourceTitle: '',
            selectedHeadline: null,

            // Styles
            imageStyles: [],
            selectedStyle: null,

            // Generation
            flashcards: [],
            generatingImageIndex: null,

            // Batch Processing
            isBatchProcessing: false,
            batchProgress: { current: 0, total: 0, currentHeadline: '' },
            selectedIndices: new Set(),

            // Loading
            loadingMessage: '',
            error: null,

            // Settings
            useGoogleSearch: false
        };

        this.listeners = new Map();
    }

    // Get state
    get(key) {
        return this.state[key];
    }

    // Set state and notify listeners
    set(key, value) {
        this.state[key] = value;
        this.notify(key, value);
    }

    // Update multiple state values
    update(updates) {
        Object.entries(updates).forEach(([key, value]) => {
            this.state[key] = value;
            this.notify(key, value);
        });
    }

    // Subscribe to state changes
    subscribe(key, callback) {
        if (!this.listeners.has(key)) {
            this.listeners.set(key, []);
        }
        this.listeners.get(key).push(callback);

        // Return unsubscribe function
        return () => {
            const callbacks = this.listeners.get(key);
            const index = callbacks.indexOf(callback);
            if (index > -1) callbacks.splice(index, 1);
        };
    }

    // Notify listeners
    notify(key, value) {
        const callbacks = this.listeners.get(key) || [];
        callbacks.forEach(cb => cb(value));
    }

    // Show loading
    showLoading(message) {
        this.set('loadingMessage', message);
        document.getElementById('loading-overlay')?.classList.remove('hidden');
        document.getElementById('loading-message').textContent = message;
    }

    // Hide loading
    hideLoading() {
        this.set('loadingMessage', '');
        document.getElementById('loading-overlay')?.classList.add('hidden');
    }

    // Show error
    showError(message) {
        this.set('error', message);
        alert(message); // Simple error display
    }
}

// Export singleton instance
export const state = new AppState();
