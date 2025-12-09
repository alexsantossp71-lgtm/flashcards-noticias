
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeftIcon, SparklesIcon } from '../components/IconComponents';

const AboutPage: React.FC = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
            <div className="max-w-md w-full bg-gray-800 rounded-3xl p-6 shadow-2xl border border-gray-700">
                <button onClick={() => navigate(-1)} className="mb-4 text-gray-400 hover:text-white flex items-center">
                    <ChevronLeftIcon className="w-5 h-5 mr-1" /> Voltar
                </button>
                <div className="flex justify-center mb-4">
                    <div className="w-14 h-14 bg-sky-600 rounded-2xl flex items-center justify-center shadow-lg rotate-3">
                       <SparklesIcon className="w-7 h-7 text-white" />
                    </div>
                </div>
                <h2 className="text-xl font-bold text-white text-center mb-2">FlashNews AI</h2>
                <p className="text-gray-300 text-center text-sm mb-6">
                    Inteligência Artificial transformando fatos em conteúdo visual.
                </p>
                <div className="space-y-3 text-sm">
                    <div className="flex items-center p-3 bg-gray-700/50 rounded-lg">
                        <span className="text-xl mr-3">🧠</span>
                        <div><h3 className="font-semibold text-white">Gemini 2.5 Flash</h3><p className="text-xs text-gray-400">Texto e Áudio</p></div>
                    </div>
                     <div className="flex items-center p-3 bg-gray-700/50 rounded-lg">
                        <span className="text-xl mr-3">🎨</span>
                        <div><h3 className="font-semibold text-white">Pollinations.ai</h3><p className="text-xs text-gray-400">Imagens (Flux)</p></div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AboutPage;
