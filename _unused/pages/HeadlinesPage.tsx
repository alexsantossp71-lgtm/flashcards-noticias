import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useNews } from '../contexts/NewsContext';
import { ChevronLeftIcon, SparklesIcon } from '../components/IconComponents';

const HeadlinesPage: React.FC = () => {
    const navigate = useNavigate();
    const {
        headlines,
        headlineSourceTitle,
        setSelectedHeadline,
        processBatchHeadlines,
        isBatchProcessing,
        batchProgress
    } = useNews();

    // State for selected indices
    const [selectedIndices, setSelectedIndices] = useState<Set<number>>(new Set());

    const toggleSelection = (index: number) => {
        const newSelection = new Set(selectedIndices);
        if (newSelection.has(index)) {
            newSelection.delete(index);
        } else {
            newSelection.add(index);
        }
        setSelectedIndices(newSelection);
    };

    const toggleSelectAll = () => {
        if (selectedIndices.size === headlines.length) {
            setSelectedIndices(new Set());
        } else {
            setSelectedIndices(new Set(headlines.map((_, i) => i)));
        }
    };

    const handleBatchGeneration = async () => {
        const selectedHeadlines = headlines.filter((_, i) => selectedIndices.has(i));
        if (selectedHeadlines.length === 0) return;

        await processBatchHeadlines(selectedHeadlines);
    };

    // If processing, show progress overlay
    if (isBatchProcessing) {
        return (
            <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 text-white text-center">
                <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-primary-500 mb-6"></div>
                <h2 className="text-2xl font-bold mb-2">Gerando Flashcards em Lote...</h2>
                <div className="w-full max-w-md bg-gray-800 rounded-full h-4 mb-4">
                    <div
                        className="bg-primary-500 h-4 rounded-full transition-all duration-300"
                        style={{ width: `${(batchProgress.current / batchProgress.total) * 100}%` }}
                    ></div>
                </div>
                <p className="text-gray-400">
                    Processando {batchProgress.current} de {batchProgress.total}
                </p>
                <p className="text-sm text-gray-500 mt-2 truncate max-w-xs">{batchProgress.currentHeadline}</p>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-900 flex flex-col p-4 relative pb-24">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                    <button onClick={() => navigate('/')} className="p-2 -ml-2 text-gray-400"><ChevronLeftIcon /></button>
                    <h2 className="text-xl font-bold text-white ml-2">{headlineSourceTitle}</h2>
                </div>
                <button
                    onClick={toggleSelectAll}
                    className="text-sm text-primary-400 font-medium px-3 py-1 rounded hover:bg-gray-800"
                >
                    {selectedIndices.size === headlines.length ? "Desmarcar Todos" : "Selecionar Todos"}
                </button>
            </div>

            {/* List */}
            <div className="space-y-3 pb-safe">
                {headlines.map((item, idx) => {
                    const isSelected = selectedIndices.has(idx);
                    return (
                        <div
                            key={idx}
                            className={`
                                relative p-5 rounded-xl border shadow-sm transition-all
                                ${isSelected ? 'bg-gray-800 border-primary-500 ring-1 ring-primary-500' : 'bg-gray-800/50 border-gray-700 hover:bg-gray-800'}
                            `}
                        >
                            <div className="flex items-start gap-4">
                                {/* Checkbox area */}
                                <div className="pt-1">
                                    <input
                                        type="checkbox"
                                        checked={isSelected}
                                        onChange={() => toggleSelection(idx)}
                                        className="w-5 h-5 rounded border-gray-600 bg-gray-700 text-primary-600 focus:ring-primary-500 cursor-pointer"
                                    />
                                </div>

                                {/* Content Area - Clickable to generate single */}
                                <button
                                    onClick={() => { setSelectedHeadline(item); navigate('/style'); }}
                                    className="flex-1 text-left"
                                >
                                    <h3 className="font-semibold text-white mb-2 leading-snug">{item.headline}</h3>
                                    <span className="text-xs text-sky-400 uppercase font-bold">{item.source}</span>
                                </button>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Floating Batch Action Bar */}
            {selectedIndices.size > 0 && (
                <div className="fixed bottom-6 left-4 right-4 animate-in slide-in-from-bottom duration-300">
                    <button
                        onClick={handleBatchGeneration}
                        className="w-full bg-primary-600 hover:bg-primary-500 text-white font-bold py-4 px-6 rounded-xl shadow-lg flex items-center justify-center gap-2"
                    >
                        <SparklesIcon />
                        <span>Gerar {selectedIndices.size} Itens Selecionados</span>
                    </button>
                </div>
            )}
        </div>
    );
};

export default HeadlinesPage;
