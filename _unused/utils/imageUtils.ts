
import { FlashcardData } from '../types';

// Helper function to sanitize filenames
export const sanitizeFilename = (name: string): string => {
    // Remove invalid characters and limit length
    return name.replace(/[^a-z0-9_\-\s\.]/gi, '').trim().substring(0, 100) || 'download';
};

/**
 * Draws the flashcard text onto a base image or a gray background using a canvas.
 * This version includes specific styling for TikTok's 9:16 aspect ratio.
 */
export const drawTextOnImage = (imageBase64: string | null, card: FlashcardData): Promise<string> => {
    return new Promise((resolve, reject) => {
        const canvas = document.createElement('canvas');
        canvas.width = 1080;
        canvas.height = 1920;
        const ctx = canvas.getContext('2d');

        if (!ctx) {
            return reject(new Error('Could not get canvas context'));
        }

        const drawContent = () => {
            // Gradient overlay for all cards with images for better readability
            if (imageBase64) {
                const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
                gradient.addColorStop(0, 'rgba(0,0,0,0.8)'); // Top dark (Darker for top text)
                gradient.addColorStop(0.3, 'rgba(0,0,0,0.4)'); // Fade out
                gradient.addColorStop(0.5, 'rgba(0,0,0,0.0)'); // Middle clear
                gradient.addColorStop(1, 'rgba(0,0,0,0.4)'); // Bottom slight fade
                ctx.fillStyle = gradient;
                ctx.fillRect(0, 0, canvas.width, canvas.height);
            }

            // Common text properties
            ctx.fillStyle = 'white';
            ctx.textAlign = 'center';
            if (imageBase64) {
                ctx.shadowColor = 'rgba(0, 0, 0, 0.9)';
                ctx.shadowBlur = 10;
                ctx.shadowOffsetX = 3;
                ctx.shadowOffsetY = 3;
            }

            const maxWidth = canvas.width * 0.85; // Slightly tighter margins
            let fontSize, minFontSize, maxLines;
            let lines: string[] = [];
            let finalLineHeight = 0;

            if (card.isFirstCard) {
                fontSize = 85;
                minFontSize = 50;
                maxLines = 5;
            } else {
                fontSize = 70;
                minFontSize = 40;
                maxLines = 6; // Limiting lines visual capacity
            }

            // Dynamic font sizing loop
            while (fontSize >= minFontSize) {
                ctx.font = `bold ${fontSize}px sans-serif`;
                finalLineHeight = fontSize * 1.2;
                lines = [];
                const words = card.text.split(' ');
                if (words.length === 0) break;

                let currentLine = words[0];
                for (let i = 1; i < words.length; i++) {
                    const word = words[i];
                    const { width } = ctx.measureText(currentLine + " " + word);
                    if (width < maxWidth) {
                        currentLine += " " + word;
                    } else {
                        lines.push(currentLine);
                        currentLine = word;
                    }
                }
                lines.push(currentLine);

                if (lines.length <= maxLines) {
                    break; // Font size is good
                }

                if (fontSize === minFontSize) break;
                fontSize = Math.max(minFontSize, fontSize - 2);
            }

            // Calculate vertical position and draw text
            if (card.isFirstCard && card.source) {
                const sourceFontSize = fontSize * 0.7;
                const sourceLineHeight = sourceFontSize * 1.2;
                const spaceBetween = 30;

                const headlineBlockHeight = lines.length * finalLineHeight;
                const totalBlockHeight = headlineBlockHeight + spaceBetween + sourceLineHeight;

                // Center vertically relative to screen
                const startY = (canvas.height - totalBlockHeight) / 2;

                // Draw headline
                ctx.textBaseline = 'top';
                lines.forEach((line, index) => {
                    ctx.fillText(line, canvas.width / 2, startY + (index * finalLineHeight));
                });

                // Draw source
                const sourceY = startY + headlineBlockHeight + spaceBetween;
                ctx.font = `normal ${sourceFontSize}px sans-serif`;
                ctx.fillStyle = '#fb923c'; // Orange-400
                ctx.fillText(card.source, canvas.width / 2, sourceY);

            } else {
                // Other cards: Draw text at the TOP with a SAFE margin for TikTok UI
                // 100px is too high (gets cut by camera punch hole or UI).
                // 260px is a safe zone below the top interface elements.
                const startY = 260;
                ctx.textBaseline = 'top';
                lines.forEach((line, index) => {
                    ctx.fillText(line, canvas.width / 2, startY + (index * finalLineHeight));
                });
            }

            // --- LIKE STICKER (First Card Only) ---
            if (card.isFirstCard) {
                // Draw a "Like" sticker in the top-right corner, avoiding center
                const stickerX = canvas.width - 140;
                const stickerY = 180; // Still slightly high but mostly in corner
                const radius = 80;

                ctx.save();
                // White Circle Background
                ctx.beginPath();
                ctx.arc(stickerX, stickerY, radius, 0, 2 * Math.PI);
                ctx.fillStyle = 'white';
                ctx.shadowColor = 'rgba(0,0,0,0.5)';
                ctx.shadowBlur = 10;
                ctx.fill();

                // Red Heart Text/Emoji
                ctx.font = '80px sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.shadowColor = 'transparent'; // No shadow on emoji
                ctx.fillText('❤️', stickerX, stickerY - 15);

                // "Curta" text
                ctx.font = 'bold 24px sans-serif';
                ctx.fillStyle = '#ef4444'; // Red
                ctx.fillText('CURTA!', stickerX, stickerY + 35);
                ctx.restore();
            }


            // Draw watermark
            ctx.save();
            ctx.font = 'bold 80px sans-serif';
            ctx.fillStyle = 'rgba(255, 255, 255, 0.25)';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
            ctx.shadowBlur = 4;

            const watermarkX = 60;
            ctx.translate(watermarkX, canvas.height / 2);
            ctx.rotate(-Math.PI / 2);

            ctx.fillText('@noticiasemimagens', 0, 0);
            ctx.restore();

            resolve(canvas.toDataURL('image/jpeg', 0.9));
        };

        if (imageBase64) {
            const img = new Image();
            img.crossOrigin = 'anonymous';
            img.onload = () => {
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                drawContent();
            };
            img.onerror = (err) => {
                console.error("Image load error, drawing on gray background", err);
                ctx.fillStyle = '#374151';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                drawContent();
            };
            if (imageBase64.startsWith('data:')) {
                img.src = imageBase64;
            } else {
                img.src = `data:image/jpeg;base64,${imageBase64}`;
            }
        } else {
            ctx.fillStyle = '#374151';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            drawContent();
        }
    });
};
