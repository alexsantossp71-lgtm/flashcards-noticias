import React from 'react';
import type { FlashcardData } from '../types';

interface FlashcardProps {
  card: FlashcardData;
  isActive: boolean;
}

const Flashcard: React.FC<FlashcardProps> = ({ card, isActive }) => {
  return (
    <div className={`absolute w-full h-full transition-opacity duration-700 ease-in-out ${isActive ? 'opacity-100' : 'opacity-0'}`}>
       {/* 
         O imageBase64 sempre existirá neste ponto e já conterá o texto.
         Será a imagem gerada com texto ou uma tela cinza com texto em caso de falha.
         Portanto, não precisamos mais de uma interface de fallback complexa aqui.
       */}
       {card.imageBase64 ? (
        <img 
            src={`data:image/jpeg;base64,${card.imageBase64}`} 
            alt={card.imagePrompt} 
            className="w-full h-full object-cover rounded-2xl" 
        />
      ) : (
        // Este caso não deve ocorrer se a lógica no App.tsx estiver correta,
        // mas é um substituto seguro.
        <div className="w-full h-full bg-gray-800 rounded-2xl flex items-center justify-center">
            <p className="text-gray-400">Carregando card...</p>
        </div>
      )}
    </div>
  );
};

export default Flashcard;