
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useNews } from '../contexts/NewsContext';
import { newsCategories } from '../types';
import Spinner from '../components/Spinner';
import { InformationCircleIcon, FireIcon, GlobeIcon, RssIcon, ExternalLinkIcon, SparklesIcon } from '../components/IconComponents';

const HomePage: React.FC = () => {
    const navigate = useNavigate();
    const { fetchHeadlines, handleUrlSubmit, handleGuideSubmit, loadingMessage, useGoogleSearch, setUseGoogleSearch } = useNews();

    const [inputTab, setInputTab] = useState<'categories' | 'link' | 'topic'>('categories');
    const [urlInput, setUrlInput] = useState<string>('');
    const [guideInput, setGuideInput] = useState<string>('');

    return (
        <div className="min-h-screen bg-gray-900 flex flex-col p-4 relative">
            {loadingMessage && <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center"><Spinner message={loadingMessage} /></div>}

            {/* Header */}
            <div className="flex justify-between items-center py-4 mb-2">
                <h1 className="text-2xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-sky-400 to-purple-500">
                    FlashNews AI
                </h1>
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => navigate('/saved')}
                        className="px-3 py-1 bg-gray-800 text-xs font-bold text-gray-300 rounded-full border border-gray-700 hover:border-primary-500 hover:text-white transition-all"
                    >
                        Meus Posts
                    </button>
                    <button onClick={() => navigate('/about')} className="p-2 text-gray-400 hover:text-white">
                        <InformationCircleIcon className="w-6 h-6" />
                    </button>
                </div>
            </div>

            <p className="text-gray-400 text-sm mb-6">Crie stories virais em segundos.</p>

            {/* Mobile Tab Switcher */}
            <div className="flex bg-gray-800 p-1 rounded-xl mb-6">
                <button onClick={() => setInputTab('categories')} className={`flex-1 py-2 text-sm font-medium rounded-lg transition-all ${inputTab === 'categories' ? 'bg-gray-700 text-white shadow' : 'text-gray-400'}`}>Categorias</button>
                <button onClick={() => setInputTab('link')} className={`flex-1 py-2 text-sm font-medium rounded-lg transition-all ${inputTab === 'link' ? 'bg-gray-700 text-white shadow' : 'text-gray-400'}`}>Link</button>
                <button onClick={() => setInputTab('topic')} className={`flex-1 py-2 text-sm font-medium rounded-lg transition-all ${inputTab === 'topic' ? 'bg-gray-700 text-white shadow' : 'text-gray-400'}`}>Tópico</button>
            </div>

            {/* Content based on Tab */}
            <div className="flex-1">
                {inputTab === 'categories' && (
                    <div className="animate-fade-in space-y-4">
                        <div className="flex justify-between items-center px-2">
                            <h2 className="text-white font-semibold flex items-center"><FireIcon className="w-5 h-5 mr-2 text-orange-400" /> Em alta</h2>
                            <button
                                onClick={() => setUseGoogleSearch(!useGoogleSearch)}
                                className={`flex items-center px-3 py-1 rounded-full text-xs font-bold transition-all ${useGoogleSearch ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
                            >
                                {useGoogleSearch ? <><GlobeIcon className="w-3 h-3 mr-1" /> Web</> : <><RssIcon className="w-3 h-3 mr-1" /> RSS</>}
                            </button>
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                            {newsCategories.map((cat) => (
                                <button
                                    key={cat}
                                    onClick={() => fetchHeadlines(cat)}
                                    className="p-4 bg-gray-800 active:bg-sky-700 rounded-xl border border-gray-700 hover:border-sky-500 transition-all text-left font-medium text-white shadow-sm"
                                >
                                    {cat}
                                </button>
                            ))}
                        </div>
                    </div>
                )}

                {inputTab === 'link' && (
                    <div className="animate-fade-in bg-gray-800 p-5 rounded-2xl border border-gray-700">
                        <h2 className="text-lg font-semibold text-white mb-4 flex items-center"><ExternalLinkIcon className="w-5 h-5 mr-2 text-green-400" /> Via Link</h2>
                        <input
                            type="text"
                            placeholder="Cole a URL da notícia..."
                            value={urlInput}
                            onChange={(e) => setUrlInput(e.target.value)}
                            className="w-full bg-gray-900 border border-gray-600 rounded-xl px-4 py-3 mb-4 focus:ring-2 focus:ring-sky-500 outline-none text-white placeholder-gray-500"
                        />
                        <button onClick={() => handleUrlSubmit(urlInput)} disabled={!urlInput} className="w-full bg-sky-600 text-white p-3 rounded-xl font-bold disabled:opacity-50">Analisar</button>
                    </div>
                )}

                {inputTab === 'topic' && (
                    <div className="animate-fade-in bg-gray-800 p-5 rounded-2xl border border-gray-700">
                        <h2 className="text-lg font-semibold text-white mb-4 flex items-center"><SparklesIcon className="w-5 h-5 mr-2 text-purple-400" /> Criar Guia</h2>
                        <input
                            type="text"
                            placeholder="Ex: História do Bitcoin..."
                            value={guideInput}
                            onChange={(e) => setGuideInput(e.target.value)}
                            className="w-full bg-gray-900 border border-gray-600 rounded-xl px-4 py-3 mb-4 focus:ring-2 focus:ring-purple-500 outline-none text-white placeholder-gray-500"
                        />
                        <button onClick={() => handleGuideSubmit(guideInput)} disabled={!guideInput} className="w-full bg-purple-600 text-white p-3 rounded-xl font-bold disabled:opacity-50">Criar</button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default HomePage;
