
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useNews } from '../contexts/NewsContext';
import { ChevronLeftIcon, SparklesIcon } from '../components/IconComponents';
import StyleSelector from '../components/StyleSelector';

const StylePage: React.FC = () => {
    const navigate = useNavigate();
    const { headlines, selectedHeadline, selectedStyle, setSelectedStyle, startGeneration } = useNews();

    return (
        <div className="min-h-screen bg-gray-900 flex flex-col relative">
            <div className="p-4 flex items-center">
                <button 
                    onClick={() => navigate(headlines.length > 0 ? '/headlines' : '/')} 
                    className="p-2 -ml-2 text-gray-400"
                >
                    <ChevronLeftIcon />
                </button>
                <h2 className="text-xl font-bold text-white ml-2">Estilo Visual</h2>
            </div>

            <div className="flex-1 overflow-y-auto px-4 pb-32">
                <div className="bg-gray-800 rounded-2xl p-5 mb-6 border border-gray-700">
                    <p className="text-gray-400 text-xs uppercase font-bold mb-2">Manchete Escolhida</p>
                    <p className="text-white italic">"{selectedHeadline?.headline}"</p>
                </div>
                
                <StyleSelector selectedStyle={selectedStyle} onSelectStyle={setSelectedStyle} />
            </div>

            <div className="fixed bottom-0 left-0 right-0 p-4 bg-gray-900/95 backdrop-blur border-t border-gray-800">
                <button
                    onClick={startGeneration}
                    className="w-full py-4 bg-gradient-to-r from-sky-500 to-blue-600 text-white rounded-xl font-bold text-lg shadow-lg flex items-center justify-center"
                >
                    <SparklesIcon className="w-6 h-6 mr-2" />
                    Gerar Flashcards
                </button>
            </div>
        </div>
    );
};

export default StylePage;
