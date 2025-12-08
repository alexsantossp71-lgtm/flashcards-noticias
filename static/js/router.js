// Hash-based Router
import { state } from './state.js';

class Router {
    constructor() {
        this.routes = new Map();
        this.currentRoute = null;

        // Listen to hash changes
        window.addEventListener('hashchange', () => this.handleRouteChange());
        window.addEventListener('load', () => this.handleRouteChange());
    }

    // Register a route
    register(path, handler) {
        this.routes.set(path, handler);
    }

    // Navigate to a route
    navigate(path, params = {}) {
        window.location.hash = path;
        state.set('currentRoute', path);
    }

    // Handle route changes
    handleRouteChange() {
        const hash = window.location.hash.slice(1) || '/';
        const [path, ...paramParts] = hash.split('/');
        const route = '/' + (path || '');

        // Extract route params (e.g., /saved/123 -> {id: '123'})
        const params = {};
        if (paramParts.length > 0) {
            params.id = paramParts[0];
        }

        this.currentRoute = route;
        state.set('currentRoute', route);

        // Find and execute handler
        const handler = this.routes.get(route);
        if (handler) {
            handler(params);
        } else {
            // Default to home
            this.navigate('/');
        }
    }

    // Get current route
    getCurrentRoute() {
        return this.currentRoute;
    }
}

// Export singleton instance
export const router = new Router();

// Navigation helpers
export function navigateTo(path) {
    router.navigate(path);
}

export function goBack() {
    window.history.back();
}
