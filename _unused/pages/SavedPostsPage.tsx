
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeftIcon, TrashIcon } from '../components/IconComponents';
import { getSavedPosts, deletePost } from '../services/apiService';

const SavedPostsPage: React.FC = () => {
    const navigate = useNavigate();
    const [posts, setPosts] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadPosts();
    }, []);

    const loadPosts = async () => {
        try {
            setLoading(true);
            const data = await getSavedPosts();
            setPosts(data);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (e: React.MouseEvent, postId: string) => {
        e.stopPropagation();
        if (!window.confirm("Tem certeza que deseja apagar este post?")) return;

        try {
            await deletePost(postId);
            setPosts(posts.filter(p => p.id !== postId));
        } catch (err: any) {
            alert("Erro ao deletar: " + err.message);
        }
    };

    // Helper to format date
    const formatDate = (isoString: string) => {
        try {
            return new Date(isoString).toLocaleDateString('pt-BR', {
                day: '2-digit', month: '2-digit', year: '2-digit',
                hour: '2-digit', minute: '2-digit'
            });
        } catch {
            return isoString;
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 flex flex-col p-4 pb-24">
            <div className="flex items-center mb-6">
                <button onClick={() => navigate('/')} className="p-2 -ml-2 text-gray-400"><ChevronLeftIcon /></button>
                <h2 className="text-xl font-bold text-white ml-2">Posts Salvos</h2>
            </div>

            {loading && (
                <div className="flex justify-center p-10">
                    <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-primary-500"></div>
                </div>
            )}

            {error && (
                <div className="bg-red-500/10 border border-red-500/50 text-red-200 p-4 rounded-lg mb-4">
                    {error}
                </div>
            )}

            {!loading && posts.length === 0 && (
                <div className="text-center text-gray-500 mt-10">
                    Nenhum post salvo encontrado.
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {posts.map((post) => (
                    <div
                        key={post.id}
                        onClick={() => navigate(`/saved/${post.id}`)}
                        className="bg-gray-800 rounded-xl overflow-hidden border border-gray-700 shadow-sm hover:border-primary-500 transition-all cursor-pointer group"
                    >
                        {/* Thumbnail attempt - try to find first image path */}
                        <div className="h-32 bg-gray-700 flex items-center justify-center relative overflow-hidden">
                            {/* Since listing only gives summary, we might not have the image URL here unless we add it to the index.
                                 Ideally, the backend index should contain a thumbnail path. 
                                 For now, let's use a placeholder or check if the index has it. 
                                 Assuming the backend 'getSavedPosts' returns minimal info. 
                                 Let's verify apiService.ts. It returns whatever is in index.json.
                                 The index in storage_service.py has: id, timestamp, category, headline, tiktokTitle, path.
                                 It does NOT have an image path. 
                                 Future improvement: Add thumbnail to index. For now, use a generic gradient.
                             */}
                            <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900 group-hover:scale-105 transition-transform"></div>
                            <span className="relative text-3xl opacity-20">🖼️</span>

                            <div className="absolute top-2 right-2">
                                <span className="bg-black/50 text-white text-xs px-2 py-1 rounded backdrop-blur-sm">
                                    {post.category}
                                </span>
                            </div>
                        </div>

                        <div className="p-4">
                            <h3 className="font-bold text-white mb-2 line-clamp-2 leading-snug">{post.headline}</h3>
                            <div className="flex items-center justify-between text-xs text-gray-400 mt-3">
                                <span>{formatDate(post.timestamp)}</span>
                                <button
                                    onClick={(e) => handleDelete(e, post.id)}
                                    className="p-2 hover:bg-red-500/20 hover:text-red-400 rounded-full transition-colors"
                                >
                                    <TrashIcon />
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SavedPostsPage;
