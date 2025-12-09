
import React, { useState, useRef, useEffect } from 'react';
import { CheckIcon, CopyIcon } from './IconComponents';

interface CopyableTextFieldProps {
    title: string;
    content: string;
}

export const CopyableTextField: React.FC<CopyableTextFieldProps> = ({ title, content }) => {
    const [copied, setCopied] = useState(false);
    const timeoutRef = useRef<number | null>(null);

    const handleCopy = () => {
        if (timeoutRef.current) {
            clearTimeout(timeoutRef.current);
        }
        navigator.clipboard.writeText(content).then(() => {
            setCopied(true);
            timeoutRef.current = window.setTimeout(() => {
                setCopied(false);
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    };
    
    useEffect(() => {
        return () => {
            if (timeoutRef.current) {
                clearTimeout(timeoutRef.current);
            }
        };
    }, []);

    const renderFormattedText = (text: string) => {
        const combinedRegex = /((?:#[\p{L}\p{N}_]+)|(?:https?:\/\/[^\s]+))/gu;
        const urlRegex = /https?:\/\/[^\s]+/;

        const parts = text.split(combinedRegex);
        
        return parts.filter(part => part).map((part, i) => {
            if (urlRegex.test(part)) {
                return <a key={i} href={part} target="_blank" rel="noopener noreferrer" className="text-green-400 hover:underline break-all" onClick={(e) => e.stopPropagation()}>{part}</a>;
            }
            if (part.startsWith('#')) {
                return <span key={i} className="text-sky-400 font-semibold">{part}</span>;
            }
            return part;
        });
    };


    return (
        <div className="bg-gray-800 p-4 rounded-lg shadow-md">
            <div className="flex justify-between items-center mb-2">
                <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider">{title}</h3>
                <button 
                    onClick={handleCopy} 
                    className={`p-2 rounded-full transition-all duration-200 ${copied ? 'bg-green-600' : 'bg-gray-700 hover:bg-sky-600'}`}
                    aria-label={`Copiar ${title}`}
                >
                    {copied ? <CheckIcon className="w-5 h-5 text-white" /> : <CopyIcon className="w-5 h-5 text-gray-300" />}
                </button>
            </div>
            <div className="bg-gray-900/50 p-3 rounded-md">
                <p className="text-gray-200 whitespace-pre-wrap text-base">
                    {renderFormattedText(content)}
                </p>
            </div>
        </div>
    );
};

export default CopyableTextField;
