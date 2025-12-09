
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ChevronLeftIcon } from '../components/IconComponents';
import { getSavedPostDetails, getPostImageUrl } from '../services/apiService';

const PostDetailPage: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!id) return;
        loadDetails();
    }, [id]);

    const loadDetails = async () => {
        try {
            setLoading(true);
            const details = await getSavedPostDetails(id!);
            setData(details);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-gray-900 flex items-center justify-center">
                <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 text-white">
                <p className="text-red-400 mb-4">{error || "Post não encontrado"}</p>
                <button onClick={() => navigate('/saved')} className="text-primary-400 underline">Voltar para salvos</button>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-900 flex flex-col p-4">
            <div className="flex items-center mb-6">
                <button onClick={() => navigate('/saved')} className="p-2 -ml-2 text-gray-400">
                    <ChevronLeftIcon />
                </button>
                <h2 className="text-xl font-bold text-white ml-2">Detalhes do Post</h2>
            </div>

            {/* Title / Header */}
            <div className="mb-6">
                <h1 className="text-2xl md:text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-secondary-400">
                    {data.tiktokTitle || data.headline || "Flashcards Gerados"}
                </h1>
                <p className="text-gray-400 text-sm mt-1">
                    Gerado em {new Date(data.timestamp || Date.now()).toLocaleDateString()}
                </p>
                {data.url && (
                    <a href={data.url} target="_blank" rel="noopener noreferrer" className="text-xs text-primary-400 hover:underline block mt-1">
                        Fonte Original
                    </a>
                )}
            </div>

            {/* Grid Layout */}
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2 pb-safe">
                {data.cards && data.cards.map((card: any, idx: number) => {
                    // Use helper to get image URL for this specific card
                    const imgUrl = getPostImageUrl(data.id, idx);

                    return (
                        <div key={idx} className="relative aspect-[9/16] bg-gray-800 rounded-lg overflow-hidden shadow-lg group">
                            <img
                                src={imgUrl}
                                alt={`Flashcard ${idx + 1}`}
                                className="w-full h-full object-cover"
                                onError={(e) => {
                                    (e.target as HTMLImageElement).src = 'https://placehold.co/400x600/1f2937/white?text=Image+Error';
                                }}
                            />

                            {/* Overlay Text */}
                            <div className="absolute inset-x-0 bottom-0 p-3 bg-gradient-to-t from-black/90 via-black/60 to-transparent pt-10">
                                <div className="text-white text-xs md:text-sm font-medium leading-relaxed drop-shadow-md">
                                    {card.text || "Sem legenda"}
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default PostDetailPage;
