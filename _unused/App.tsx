
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { NewsProvider } from './contexts/NewsContext';

import HomePage from './pages/HomePage';
import HeadlinesPage from './pages/HeadlinesPage';
import StylePage from './pages/StylePage';
import ResultPage from './pages/ResultPage';
import SavedPostsPage from './pages/SavedPostsPage';
import PostDetailPage from './pages/PostDetailPage';

const App: React.FC = () => {
    return (
        <NewsProvider>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/headlines" element={<HeadlinesPage />} />
                <Route path="/style" element={<StylePage />} />
                <Route path="/result" element={<ResultPage />} />
                <Route path="/about" element={<AboutPage />} />
                <Route path="/saved" element={<SavedPostsPage />} />
                <Route path="/saved/:id" element={<PostDetailPage />} />
                <Route path="*" element={<Navigate to="/" />} />
            </Routes>
        </NewsProvider>
    );
};

export default App;
