// API Service - All backend communication
const API_BASE_URL = 'http://localhost:8000';

export const api = {
    // Helper for API calls
    async call(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Headlines
    async getHeadlines(category, count = 15) {
        return this.call('/api/headlines', {
            method: 'POST',
            body: JSON.stringify({ category, count })
        });
    },

    async getHeadlineFromUrl(url) {
        return this.call('/api/headline-from-url', {
            method: 'POST',
            body: JSON.stringify({ url })
        });
    },

    // Content Generation
    async generateFlashcardContent(headline, url, stylePrompt, source = 'Web') {
        return this.call('/api/generate-content', {
            method: 'POST',
            body: JSON.stringify({ headline, url, stylePrompt, source })
        });
    },

    async generateGuideContent(topic, stylePrompt) {
        return this.call('/api/generate-guide', {
            method: 'POST',
            body: JSON.stringify({ topic, stylePrompt })
        });
    },

    // Image Generation
    async generateImage(prompt, stylePrompt, text = '', cardNumber = 1) {
        return this.call('/api/generate-image', {
            method: 'POST',
            body: JSON.stringify({ prompt, stylePrompt, text, cardNumber })
        });
    },

    // Saved Posts
    async savePost(data) {
        return this.call('/api/save-post', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    async getSavedPosts(category = null, limit = 50) {
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        params.append('limit', limit.toString());
        return this.call(`/api/posts?${params}`);
    },
    // API Service - All backend communication
    const API_BASE_URL = 'http://localhost:8000';

    export const api = {
        // Helper for API calls
        async call(endpoint, options = {}) {
            const url = `${API_BASE_URL}${endpoint}`;
            const config = {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            };

            try {
                const response = await fetch(url, config);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return await response.json();
            } catch (error) {
                console.error('API Error:', error);
                throw error;
            }
        },

        // Headlines
        async getHeadlines(category, count = 15) {
            return this.call('/api/headlines', {
                method: 'POST',
                body: JSON.stringify({ category, count })
            });
        },

        async getHeadlineFromUrl(url) {
            return this.call('/api/headline-from-url', {
                method: 'POST',
                body: JSON.stringify({ url })
            });
        },

        // Content Generation
        async generateFlashcardContent(headline, url, stylePrompt, source = 'Web') {
            return this.call('/api/generate-content', {
                method: 'POST',
                body: JSON.stringify({ headline, url, stylePrompt, source })
            });
        },

        async generateGuideContent(topic, stylePrompt) {
            return this.call('/api/generate-guide', {
                method: 'POST',
                body: JSON.stringify({ topic, stylePrompt })
            });
        },

        // Image Generation
        async generateImage(prompt, stylePrompt, text = '', cardNumber = 1) {
            return this.call('/api/generate-image', {
                method: 'POST',
                body: JSON.stringify({ prompt, stylePrompt, text, cardNumber })
            });
        },

        // Saved Posts
        async savePost(data) {
            return this.call('/api/save-post', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async getSavedPosts(category = null, limit = 50) {
            const params = new URLSearchParams();
            if (category) params.append('category', category);
            params.append('limit', limit.toString());
            return this.call(`/api/posts?${params}`);
        },

        async getSavedPostDetails(postId) {
            return this.call(`/api/posts/${postId}`);
        },

        async deletePost(postId) {
            return this.call(`/api/posts/${postId}`, {
                method: 'DELETE'
            });
        },

        // GitHub Push
        async pushToGitHub() {
            return this.call('/api/push-to-github', { method: 'POST' });
        },

        // Helper to get image URL for saved posts
        getPostImageUrl(postId, cardIndex) {
            return `${API_BASE_URL}/api/image/${postId}/${cardIndex + 1}`;
        }
    };
