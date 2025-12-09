/**
 * API Service - Local Backend Integration
 * Replaces Google Gemini cloud services with local backend calls
 */

import type { Headline, NewsCategory, GeneratedContent } from '../types';

// --- CONFIGURATION ---

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * Helper: Make API calls with error handling
 */
async function apiCall<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options?.headers,
        },
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(error.detail || `API Error: ${response.status}`);
    }

    return response.json();
}

// --- HEADLINE FETCHING ---

export const getSmartHeadlines = async (
    category: NewsCategory,
    useSearch: boolean = false
): Promise<Headline[]> => {
    try {
        const response = await apiCall<{ headlines: Headline[] }>('/api/headlines', {
            method: 'POST',
            body: JSON.stringify({ category, count: 15 }),
        });

        return response.headlines;
    } catch (error) {
        console.error('Failed to fetch headlines:', error);
        throw error;
    }
};

export const getHeadlineFromUrl = async (url: string): Promise<Headline> => {
    try {
        const response = await apiCall<Headline>('/api/headline-from-url', {
            method: 'POST',
            body: JSON.stringify({ url }),
        });

        return response;
    } catch (error) {
        console.error('Failed to extract headline from URL:', error);
        throw error;
    }
};

// --- CONTENT GENERATION ---

export const getPostImageUrl = (postId: string, cardIndex: number) => {
    return `${API_BASE_URL}/api/image/${postId}/${cardIndex + 1}`;
};

export const generateFlashcardContent = async (
    headline: string,
    url: string,
    stylePrompt: string,
    source: string = 'Web'
): Promise<GeneratedContent> => {
    try {
        const response = await apiCall<GeneratedContent>('/api/generate-content', {
            method: 'POST',
            body: JSON.stringify({ headline, url, stylePrompt, source }),
        });

        return response;
    } catch (error) {
        console.error('Failed to generate flashcard content:', error);
        throw error;
    }
};

export const generateGuideContent = async (
    topic: string,
    stylePrompt: string
): Promise<GeneratedContent> => {
    try {
        const response = await apiCall<GeneratedContent>('/api/generate-guide', {
            method: 'POST',
            body: JSON.stringify({ topic, stylePrompt }),
        });

        return response;
    } catch (error) {
        console.error('Failed to generate guide content:', error);
        throw error;
    }
};

// --- IMAGE GENERATION ---

export const generateImage = async (
    prompt: string,
    stylePrompt: string
): Promise<string> => {
    try {
        // Create AbortController with 10 minute timeout for local CPU generation
        // (Juggernaut XL on CPU can take 3-5 minutes per image)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 600000); // 10 minutes

        const response = await apiCall<{
            imageBase64: string;
            imageSource: string;
            generationTime: number;
        }>('/api/generate-image', {
            method: 'POST',
            body: JSON.stringify({ prompt, stylePrompt }),
            signal: controller.signal,
        });

        clearTimeout(timeoutId);
        console.log(`Image generated via ${response.imageSource} in ${response.generationTime.toFixed(1)}s`);

        // Return base64 with data URL prefix for compatibility
        return `data:image/png;base64,${response.imageBase64}`;
    } catch (error) {
        if (error instanceof Error && error.name === 'AbortError') {
            console.error('Image generation timeout after 2 minutes');
            throw new Error('Image generation timed out. Try again or use a faster backend.');
        }
        console.error('Failed to generate image:', error);
        throw error;
    }
};

// --- POST STORAGE ---

export const savePost = async (postData: {
    category: string;
    headline: string;
    source: string;
    url: string;
    tiktokTitle: string;
    tiktokSummary: string;
    cards: Array<{
        text: string;
        imagePrompt: string;
        imageBase64: string;
        imageSource: string;
    }>;
    generationTime: number;
    modelUsed: Record<string, any>;
}): Promise<{ id: string; path: string }> => {
    try {
        const response = await apiCall<{ id: string; path: string }>('/api/save-post', {
            method: 'POST',
            body: JSON.stringify(postData),
        });

        return response;
    } catch (error) {
        console.error('Failed to save post:', error);
        throw error;
    }
};

export const getSavedPosts = async (
    category?: string,
    limit: number = 50
): Promise<Array<any>> => {
    try {
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        params.append('limit', limit.toString());

        const response = await apiCall<{ posts: Array<any> }>(`/api/posts?${params}`);
        return response.posts;
    } catch (error) {
        console.error('Failed to fetch saved posts:', error);
        throw error;
    }
};

export const getPost = async (postId: string): Promise<any> => {
    try {
        return await apiCall<any>(`/api/posts/${postId}`);
    } catch (error) {
        console.error('Failed to fetch post:', error);
        throw error;
    }
};

export const deletePost = async (postId: string): Promise<void> => {
    try {
        await apiCall<{ message: string }>(`/api/posts/${postId}`, {
            method: 'DELETE',
        });
    } catch (error) {
        console.error('Failed to delete post:', error);
        throw error;
    }
};

// --- AUDIO GENERATION (Removed - Not supported locally yet) ---
// Note: Audio generation with TTS is removed for local version
// Can be added later with local TTS like Coqui TTS
