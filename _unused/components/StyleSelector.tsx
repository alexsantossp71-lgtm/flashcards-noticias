
import React from 'react';
import { ImageStyle } from '../types';
import { imageStyles } from '../constants';

interface StyleSelectorProps {
  selectedStyle: ImageStyle;
  onSelectStyle: (style: ImageStyle) => void;
}

const StyleSelector: React.FC<StyleSelectorProps> = ({ selectedStyle, onSelectStyle }) => {
  return (
    <div className="mb-8 bg-gray-800 p-6 rounded-2xl shadow-lg">
      <h2 className="text-xl font-semibold mb-4 text-white flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6 mr-2 text-purple-400">
          <path strokeLinecap="round" strokeLinejoin="round" d="M9.53 16.122a3 3 0 0 0-5.78 1.128 2.25 2.25 0 0 1-2.4 2.245 4.5 4.5 0 0 0 8.4-2.245c0-.399-.078-.78-.22-1.128Zm0 0a15.998 15.998 0 0 0 3.388-1.62m-5.043-.025a15.994 15.994 0 0 1 1.622-3.395m3.42 3.42a15.995 15.995 0 0 0 4.764-4.648l3.876-5.814a1.151 1.151 0 0 0-1.597-1.597L14.85 6.361a15.996 15.996 0 0 0-4.647 4.761m3.42 3.42a6.776 6.776 0 0 0-3.42-3.42" />
        </svg>
        <span>Escolha o Estilo Visual</span>
      </h2>
      <div className="flex overflow-x-auto pb-4 gap-3 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent">
        {imageStyles.map((style) => (
          <button
            key={style.id}
            onClick={() => onSelectStyle(style)}
            className={`flex-shrink-0 p-3 rounded-xl border-2 transition-all duration-200 flex flex-col items-center w-32 group ${
              selectedStyle.id === style.id
                ? 'border-sky-500 bg-gray-700 scale-105'
                : 'border-transparent bg-gray-900 hover:bg-gray-700'
            }`}
          >
            {/* Visual Representation of Style */}
            <div 
              className="w-16 h-16 rounded-full mb-3 shadow-lg flex items-center justify-center text-3xl relative overflow-hidden"
              style={{ 
                  background: `linear-gradient(135deg, ${style.previewColor} 0%, #1f2937 100%)` 
              }}
            >
                <span className="relative z-10 transform transition-transform group-hover:scale-110">
                    {style.previewEmoji}
                </span>
            </div>
            <span className={`text-sm font-medium text-center leading-tight ${selectedStyle.id === style.id ? 'text-white' : 'text-gray-400'}`}>
              {style.label}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default StyleSelector;
