
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import JSZip from 'jszip';
import { useNews } from '../contexts/NewsContext';
import { savePost } from '../services/apiService';
import { sanitizeFilename } from '../utils/imageUtils';
import Spinner from '../components/Spinner';
import CopyableTextField from '../components/CopyableTextField';
import {
    ChevronLeftIcon, PhotoIcon, DocumentTextIcon, RefreshIcon,
    ArchiveIcon, MapPinIcon,
    PlusCircleIcon, ShareIcon
} from '../components/IconComponents';

const ResultPage: React.FC = () => {
    const navigate = useNavigate();
    const {
        flashcards, generatedContent, selectedHeadline,
        loadingMessage, error, generatingImageIndex,
        handleRegenerateCardImage, resetState
    } = useNews();

    const [resultTab, setResultTab] = useState<'feed' | 'details'>('feed');
    const [localLoading, setLocalLoading] = useState<string>('');
    const [regeneratingIndex, setRegeneratingIndex] = useState<number | null>(null);
    const [saveStatus, setSaveStatus] = useState<string>('');

    // Save post to local backend
    const handleSavePost = async () => {
        if (!generatedContent || !selectedHeadline) return;

        setLocalLoading('Salvando post...');
        try {
            const cardsData = flashcards.map(card => ({
                text: card.text,
                imagePrompt: card.imagePrompt,
                imageBase64: card.imageBase64 || '',
                imageSource: 'local' // or track this if available
            }));

            const result = await savePost({
                category: selectedHeadline.source || 'Geral',
                headline: selectedHeadline.headline,
                source: selectedHeadline.source,
                url: selectedHeadline.url,
                tiktokTitle: generatedContent.tiktokTitle,
                tiktokSummary: generatedContent.tiktokSummary,
                cards: cardsData,
                generationTime: 0, // TODO: track this
                modelUsed: { text: 'ollama', image: 'local' }
            });

            setSaveStatus(`Salvo! ID: ${result.id}`);
            setTimeout(() => setSaveStatus(''), 3000);
        } catch (e: any) {
            alert(`Erro ao salvar: ${e.message}`);
        } finally {
            setLocalLoading('');
        }
    };

    const downloadAllImages = async () => {
        if (!generatedContent) return;
        setLocalLoading("Gerando ZIP...");
        try {
            const zip = new JSZip();
            flashcards.forEach((card, index) => {
                if (card.imageBase64) zip.file(`story_${index + 1}.jpg`, card.imageBase64, { base64: true });
            });
            zip.file("roteiro.txt", `TÍTULO: ${generatedContent.tiktokTitle}\n\nRESUMO:\n${generatedContent.tiktokSummary}`);

            const content = await zip.generateAsync({ type: "blob" });
            const url = URL.createObjectURL(content);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${sanitizeFilename(generatedContent.tiktokTitle)}.zip`;
            a.click();
            URL.revokeObjectURL(url);
        } catch (e) {
            alert("Erro ao criar ZIP.");
        } finally {
            setLocalLoading('');
        }
    };

    const handleShare = async () => {
        if (!generatedContent) return;
        const shareText = `${generatedContent.tiktokTitle}\n\n${generatedContent.tiktokSummary}`.trim();
        const shareData = { title: 'FlashNews Story', text: shareText, url: selectedHeadline?.url || '' };

        try {
            if (navigator.share) {
                await navigator.share(shareData);
            } else {
                await navigator.clipboard.writeText(`${shareText}\n\n${selectedHeadline?.url || ''}`);
                alert("Texto copiado!");
            }
        } catch (err) {
            console.error(err);
        }
    };

    const onRegenerateImage = async (idx: number) => {
        setRegeneratingIndex(idx);
        try {
            await handleRegenerateCardImage(idx);
        } catch (e) {
            alert('Falha ao regerar imagem');
        } finally {
            setRegeneratingIndex(null);
        }
    };

    if (error) {
        return (
            <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 text-center">
                <div className="w-16 h-16 bg-red-900/30 rounded-full flex items-center justify-center mb-4 text-3xl">⚠️</div>
                <h2 className="text-xl font-bold text-white mb-2">Erro</h2>
                <p className="text-gray-400 text-sm mb-6">{error}</p>
                <button onClick={() => navigate('/')} className="px-6 py-3 bg-white text-gray-900 rounded-xl font-bold">Voltar ao Início</button>
            </div>
        );
    }

    const currentLoading = loadingMessage || localLoading;

    return (
        <div className="min-h-screen bg-gray-950 flex flex-col pb-24 relative">
            {currentLoading && <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center"><Spinner message={currentLoading} /></div>}

            {/* Header */}
            <div className="sticky top-0 bg-gray-900/95 backdrop-blur border-b border-gray-800 p-4 z-40 flex justify-between items-center shadow-md">
                <button onClick={() => navigate('/')} className="text-gray-400 hover:text-white flex items-center">
                    <ChevronLeftIcon className="w-5 h-5 mr-1" /> Início
                </button>

                <div className="flex bg-gray-800 p-1 rounded-lg">
                    <button
                        onClick={() => setResultTab('feed')}
                        className={`px-4 py-1.5 text-xs font-bold rounded-md transition-all flex items-center gap-2 ${resultTab === 'feed' ? 'bg-sky-600 text-white shadow' : 'text-gray-400 hover:text-white'}`}
                    >
                        <PhotoIcon className="w-4 h-4" /> Roteiro
                    </button>
                    <button
                        onClick={() => setResultTab('details')}
                        className={`px-4 py-1.5 text-xs font-bold rounded-md transition-all flex items-center gap-2 ${resultTab === 'details' ? 'bg-sky-600 text-white shadow' : 'text-gray-400 hover:text-white'}`}
                    >
                        <DocumentTextIcon className="w-4 h-4" /> Detalhes
                    </button>
                </div>
            </div>

            {/* Content */}
            <div className="flex-1 p-4">
                {resultTab === 'feed' && (
                    <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-2 h-full overflow-y-auto content-start animate-fade-in pb-20">
                        {flashcards.map((card, idx) => {
                            const isBusy = generatingImageIndex === idx || regeneratingIndex === idx;
                            return (
                                <div key={idx} className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden shadow-lg flex flex-col h-min">
                                    <div className="p-1.5 flex justify-between items-center bg-gray-800/50">
                                        <span className="bg-gray-700 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">#{idx + 1}</span>
                                        <button
                                            onClick={() => onRegenerateImage(idx)}
                                            disabled={isBusy}
                                            className="text-[10px] flex items-center text-sky-400 hover:text-white disabled:opacity-50"
                                        >
                                            <RefreshIcon className={`w-3 h-3 mr-1 ${isBusy ? 'animate-spin' : ''}`} />
                                            {isBusy ? '...' : 'Regerar'}
                                        </button>
                                    </div>

                                    <div className="relative aspect-[9/16] w-full bg-black group">
                                        {card.imageBase64 ? (
                                            <img src={`data:image/jpeg;base64,${card.imageBase64}`} alt={`Card ${idx + 1}`} className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" />
                                        ) : (
                                            <div className="flex items-center justify-center h-full text-gray-600"><PhotoIcon className="w-8 h-8" /></div>
                                        )}
                                        {/* Overlay text on hover or always if compact */}
                                        <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity p-2 flex flex-col justify-end">
                                            <p className="text-white text-[10px] leading-tight">{card.text}</p>
                                        </div>
                                    </div>
                                    {/* Small visible text below */}
                                    <div className="p-2 h-16 overflow-y-auto scrollbar-hide">
                                        <p className="text-gray-400 text-[10px] leading-tight line-clamp-4">{card.text}</p>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                )}

                {resultTab === 'details' && generatedContent && (
                    <div className="space-y-6 animate-fade-in max-w-lg mx-auto">
                        <div className="grid grid-cols-1 gap-3">
                            <button onClick={handleSavePost} className="w-full py-4 bg-purple-600 hover:bg-purple-500 text-white rounded-xl font-bold shadow-lg flex items-center justify-center transition-all">
                                <ArchiveIcon className="w-6 h-6 mr-2" /> Salvar Post
                            </button>
                            {saveStatus && <p className="text-green-400 text-sm text-center">{saveStatus}</p>}
                            <button onClick={downloadAllImages} className="w-full py-4 bg-green-600 hover:bg-green-500 text-white rounded-xl font-bold shadow-lg flex items-center justify-center transition-all">
                                <ArchiveIcon className="w-6 h-6 mr-2" /> Baixar Imagens (ZIP)
                            </button>
                        </div>
                        <hr className="border-gray-800" />
                        <CopyableTextField title="Título Viral" content={generatedContent.tiktokTitle} />
                        <CopyableTextField title="Legenda / Resumo" content={generatedContent.tiktokSummary} />
                        {generatedContent.mapsLinks && generatedContent.mapsLinks.length > 0 && (
                            <div className="bg-gray-800 p-4 rounded-xl border border-gray-700">
                                <h3 className="text-xs font-bold text-gray-400 uppercase mb-3 flex items-center"><MapPinIcon className="w-4 h-4 mr-1" /> Localização Relacionada</h3>
                                <div className="space-y-2">
                                    {generatedContent.mapsLinks.map((link, idx) => (
                                        <a key={idx} href={link.uri} target="_blank" className="block p-2 bg-gray-900 rounded-lg text-sky-400 text-sm truncate hover:bg-gray-700 transition-colors">
                                            {link.title}
                                        </a>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Bottom Actions */}
            <div className="fixed bottom-0 left-0 right-0 bg-gray-900 border-t border-gray-800 p-4 flex gap-3 z-50">
                <button
                    onClick={() => { resetState(); navigate('/'); }}
                    className="flex-1 py-3 bg-gray-800 text-white rounded-xl font-bold border border-gray-700 flex items-center justify-center"
                >
                    <PlusCircleIcon className="w-5 h-5 mr-2" /> Novo
                </button>
                <button
                    onClick={handleShare}
                    className="flex-1 py-3 bg-blue-600 text-white rounded-xl font-bold shadow-lg flex items-center justify-center"
                >
                    <ShareIcon className="w-5 h-5 mr-2" /> Compartilhar
                </button>
            </div>
        </div>
    );
};

export default ResultPage;
