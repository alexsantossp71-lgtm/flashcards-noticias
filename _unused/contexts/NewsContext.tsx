
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { Headline, FlashcardData, ImageStyle, NewsCategory, MapsLink, GeneratedContent } from '../types';
import { imageStyles } from '../constants';
import { getSmartHeadlines, getHeadlineFromUrl, generateFlashcardContent, generateGuideContent, generateImage, savePost } from '../services/apiService';
import { drawTextOnImage } from '../utils/imageUtils';

interface NewsContextType {
    headlines: Headline[];
    selectedHeadline: Headline | null;
    flashcards: FlashcardData[];
    generatedContent: { tiktokTitle: string; tiktokSummary: string; mapsLinks?: MapsLink[] } | null;
    selectedStyle: ImageStyle;
    loadingMessage: string;
    error: string | null;
    generatingImageIndex: number | null;
    useGoogleSearch: boolean;
    headlineSourceTitle: string;

    // Batch Processing
    isBatchProcessing: boolean;
    batchProgress: { current: number; total: number; currentHeadline: string };

    setUseGoogleSearch: (use: boolean) => void;
    setSelectedHeadline: (headline: Headline | null) => void;
    setSelectedStyle: (style: ImageStyle) => void;
    setError: (msg: string | null) => void;

    fetchHeadlines: (category: NewsCategory) => Promise<void>;
    handleUrlSubmit: (url: string) => Promise<void>;
    handleGuideSubmit: (topic: string) => void;
    startGeneration: () => Promise<void>;
    handleRegenerateCardImage: (index: number) => Promise<void>;
    processBatchHeadlines: (headlines: Headline[]) => Promise<void>;
    resetState: () => void;
}

const NewsContext = createContext<NewsContextType | undefined>(undefined);

export const NewsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const navigate = useNavigate();

    const [headlines, setHeadlines] = useState<Headline[]>([]);
    const [selectedHeadline, setSelectedHeadline] = useState<Headline | null>(null);
    const [flashcards, setFlashcards] = useState<FlashcardData[]>([]);
    const [generatedContent, setGeneratedContent] = useState<{ tiktokTitle: string; tiktokSummary: string; mapsLinks?: MapsLink[] } | null>(null);
    const [selectedStyle, setSelectedStyle] = useState<ImageStyle>(imageStyles[0]);
    const [loadingMessage, setLoadingMessage] = useState<string>('');
    const [error, setError] = useState<string | null>(null);
    const [generatingImageIndex, setGeneratingImageIndex] = useState<number | null>(null);
    const [useGoogleSearch, setUseGoogleSearch] = useState<boolean>(false);
    const [headlineSourceTitle, setHeadlineSourceTitle] = useState<string>('');

    const [isBatchProcessing, setIsBatchProcessing] = useState<boolean>(false);
    const [batchProgress, setBatchProgress] = useState<{ current: number; total: number; currentHeadline: string }>({ current: 0, total: 0, currentHeadline: '' });

    const handleError = (msg: string) => {
        setError(msg);
        setLoadingMessage('');
    };

    const resetState = () => {
        setHeadlines([]);
        setSelectedHeadline(null);
        setFlashcards([]);
        setGeneratedContent(null);
        setError(null);
        setGeneratingImageIndex(null);
        setIsBatchProcessing(false);
        setBatchProgress({ current: 0, total: 0, currentHeadline: '' });
    };

    const fetchHeadlines = async (category: NewsCategory) => {
        const sourceLabel = useGoogleSearch ? "Google Search" : "Feed RSS";
        setLoadingMessage(`Buscando em ${sourceLabel}...`);
        try {
            const result = await getSmartHeadlines(category, useGoogleSearch);
            setHeadlines(result);
            setHeadlineSourceTitle(category);
            navigate('/headlines');
        } catch (e: any) {
            handleError(e.message);
        } finally {
            setLoadingMessage('');
        }
    };

    const handleUrlSubmit = async (url: string) => {
        setLoadingMessage("Lendo Link...");
        try {
            const headline = await getHeadlineFromUrl(url);
            setSelectedHeadline(headline);
            navigate('/style');
        } catch (e: any) {
            handleError(e.message);
        } finally {
            setLoadingMessage('');
        }
    };

    const handleGuideSubmit = (topic: string) => {
        setSelectedHeadline({ headline: topic, source: "Guia Explicativo", url: "" });
        navigate('/style');
    };

    const startGeneration = async () => {
        if (!selectedHeadline) return;

        // Reset previous result data
        setFlashcards([]);
        setGeneratedContent(null);
        setGeneratingImageIndex(null);
        setError(null);

        // Navigate immediately to result page to show loading there if desired, 
        // or wait. Let's navigate to Result page which will show the spinner/progress.
        navigate('/result');

        try {
            setLoadingMessage("Criando roteiro...");
            let content;
            if (selectedHeadline.source === "Guia Explicativo") {
                content = await generateGuideContent(selectedHeadline.headline, selectedStyle.prompt);
            } else {
                content = await generateFlashcardContent(selectedHeadline.headline, selectedHeadline.url, selectedStyle.prompt);
            }

            let finalSummary = content.tiktokSummary;
            if (selectedHeadline.url) {
                finalSummary += `\n\nFonte: ${selectedHeadline.url}`;
            }

            setGeneratedContent({
                tiktokTitle: content.tiktokTitle,
                tiktokSummary: finalSummary,
                mapsLinks: content.mapsLinks
            });

            // Prepare initial cards (text only, no images yet)
            const initialCards: FlashcardData[] = content.flashcards.map((c, i) => ({
                text: c.text,
                imagePrompt: c.imagePrompt,
                isFirstCard: i === 0,
                source: i === 0 ? selectedHeadline.source : undefined,
                imageBase64: null
            }));

            // First pass: Draw text on placeholders
            const cardsWithPlaceholders = await Promise.all(initialCards.map(async (card) => {
                const finalImage = await drawTextOnImage(null, card);
                return { ...card, imageBase64: finalImage.split(',')[1] };
            }));

            setFlashcards(cardsWithPlaceholders);
            setLoadingMessage('');

            // Loop to generate images progressively
            for (let i = 0; i < initialCards.length; i++) {
                setGeneratingImageIndex(i);
                try {
                    await new Promise(resolve => setTimeout(resolve, 2000)); // Delay for API safety
                    const base64Data = await generateImage(initialCards[i].imagePrompt, selectedStyle.prompt);
                    const finalImageWithText = await drawTextOnImage(base64Data, initialCards[i]);

                    setFlashcards(prev => {
                        const newCards = [...prev];
                        newCards[i] = { ...newCards[i], imageBase64: finalImageWithText.split(',')[1] };
                        return newCards;
                    });
                } catch (err) {
                    console.error(`Error generating image for card ${i}`, err);
                }
            }
            setGeneratingImageIndex(null);

        } catch (e: any) {
            handleError(e.message);
        }
    };

    const handleRegenerateCardImage = async (index: number) => {
        try {
            const card = flashcards[index];
            const base64Data = await generateImage(card.imagePrompt, selectedStyle.prompt);
            const finalImageWithText = await drawTextOnImage(base64Data, card);

            setFlashcards(prev => {
                const newCards = [...prev];
                newCards[index] = { ...newCards[index], imageBase64: finalImageWithText.split(',')[1] };
                return newCards;
            });
        } catch (err: any) {
            console.error("Error regenerating specific card image", err);
            throw err; // Let component handle UI feedback
        }
    };

    const processBatchHeadlines = async (headlinesToProcess: Headline[]) => {
        if (headlinesToProcess.length === 0) return;

        setIsBatchProcessing(true);
        setBatchProgress({ current: 0, total: headlinesToProcess.length, currentHeadline: '' });
        setError(null);

        for (let i = 0; i < headlinesToProcess.length; i++) {
            const headline = headlinesToProcess[i];
            setBatchProgress({
                current: i + 1,
                total: headlinesToProcess.length,
                currentHeadline: headline.headline
            });

            try {
                // 1. Generate Content
                console.log(`Processing batch item ${i + 1}/${headlinesToProcess.length}: ${headline.headline}`);
                const startTime = Date.now();

                const content = await generateFlashcardContent(headline.headline, headline.url, selectedStyle.prompt, headline.source);

                // 2. Generate Images & Create Cards
                const cards: any[] = [];
                for (let j = 0; j < content.flashcards.length; j++) {
                    const cardData = content.flashcards[j];
                    // Generate Image
                    const base64Image = await generateImage(cardData.imagePrompt, selectedStyle.prompt);

                    // Draw Text
                    const cardForDrawing: FlashcardData = {
                        text: cardData.text,
                        imagePrompt: cardData.imagePrompt,
                        isFirstCard: j === 0,
                        source: j === 0 ? headline.source : undefined
                    };

                    const finalImageWithText = await drawTextOnImage(base64Image, cardForDrawing);

                    cards.push({
                        text: cardData.text,
                        imagePrompt: cardData.imagePrompt,
                        imageBase64: finalImageWithText.split(',')[1], // Save Post expects base64 without prefix usually, or let's check service
                        imageSource: 'generated'
                    });
                }

                // 3. Save Post
                const generationTime = (Date.now() - startTime) / 1000;

                let finalSummary = content.tiktokSummary;
                if (headline.url) {
                    finalSummary += `\n\nFonte: ${headline.url}`;
                }

                await savePost({
                    category: headlineSourceTitle || "Batch",
                    headline: headline.headline,
                    source: headline.source,
                    url: headline.url,
                    tiktokTitle: content.tiktokTitle,
                    tiktokSummary: finalSummary,
                    cards: cards,
                    generationTime: generationTime,
                    modelUsed: {}
                });

            } catch (err) {
                console.error(`Failed to process headline: ${headline.headline}`, err);
                // Continue to next item even if one fails
            }
        }

        setIsBatchProcessing(false);
        setBatchProgress({ current: 0, total: 0, currentHeadline: '' });
        // Optionally navigate to saved posts or show success message
        navigate('/saved');
    };

    return (
        <NewsContext.Provider value={{
            headlines,
            selectedHeadline,
            flashcards,
            generatedContent,
            selectedStyle,
            loadingMessage,
            error,
            generatingImageIndex,
            useGoogleSearch,
            headlineSourceTitle,
            isBatchProcessing,
            batchProgress,
            setUseGoogleSearch,
            setSelectedHeadline,
            setSelectedStyle,
            setError,
            fetchHeadlines,
            handleUrlSubmit,
            handleGuideSubmit,
            startGeneration,
            handleRegenerateCardImage,
            processBatchHeadlines,
            resetState
        }}>
            {children}
        </NewsContext.Provider>
    );
};

export const useNews = () => {
    const context = useContext(NewsContext);
    if (!context) {
        throw new Error("useNews must be used within a NewsProvider");
    }
    return context;
};
