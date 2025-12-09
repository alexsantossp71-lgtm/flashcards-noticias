
export const newsCategories = ["Brasil", "Mundo", "Política", "Esportes", "Tecnologia", "Economia"] as const;

export type NewsCategory = typeof newsCategories[number];

export interface Headline {
  headline: string;
  source: string;
  url: string;
}

export interface FlashcardData {
  text: string;
  source?: string;
  isFirstCard: boolean;
  imagePrompt: string;
  imageBase64: string | null;
}

export interface MapsLink {
  title: string;
  uri: string;
}

export interface GeneratedContent {
  flashcards: { text: string; imagePrompt: string; }[];
  tiktokTitle: string;
  tiktokSummary: string;
  mapsLinks?: MapsLink[];
}

export interface ImageStyle {
  id: string;
  label: string;
  prompt: string;
  previewColor: string;
  previewEmoji: string;
}