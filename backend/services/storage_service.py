"""
Storage Service - Manage generated posts filesystem
Handles saving, loading, and organizing generated content
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from config import GENERATED_POSTS_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self):
        self.posts_dir = GENERATED_POSTS_DIR
        self.index_file = self.posts_dir / "index.json"
        self._ensure_index()
    
    def _ensure_index(self):
        """Create index.json if doesn't exist"""
        if not self.index_file.exists():
            # Create in format expected by viewer: {"posts": [...]}
            self.index_file.write_text(json.dumps({"posts": []}, indent=2, ensure_ascii=False))
    
    def _load_index(self) -> List[Dict]:
        """Load the index of all posts"""
        try:
            data = json.loads(self.index_file.read_text(encoding='utf-8'))
            # Handle both formats: {"posts": [...]} or [...]
            if isinstance(data, dict):
                return data.get('posts', [])
            elif isinstance(data, list):
                return data
            else:
                logger.error(f"Invalid index format: {type(data)}")
                return []
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            return []
    
    def _save_index(self, index: List[Dict]):
        """Save the index in the format expected by viewer"""
        # Save in format: {"posts": [...]} for GitHub Pages viewer
        data = {"posts": index}
        self.index_file.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    
    def _generate_post_id(self, category: str, timestamp: datetime) -> str:
        """Generate unique post ID"""
        # Format: category_YYYYMMDD_HHMMSS
        category_slug = category.lower().replace(" ", "_")
        time_str = timestamp.strftime("%Y%m%d_%H%M%S")
        return f"{category_slug}_{time_str}"
    
    def save_post(
        self,
        category: str,
        headline: str,
        source: str,
        url: str,
        tiktok_title: str,
        tiktok_summary: str,
        cards: List[Dict],  # [{text, imagePrompt, imageBase64, imageSource}]
        generation_time: float,
        models_used: Dict,
        article_date: Optional[str] = None  # ✅ NOVO: Data da notícia
    ) -> Dict:
        """
        Save a complete post to filesystem
        Returns metadata with post_id and path
        """
        timestamp = datetime.now()
        post_id = self._generate_post_id(category, timestamp)
        
        # Create directory structure: YYYY-MM-DD/post_id/
        date_dir = self.posts_dir / timestamp.strftime("%Y-%m-%d")
        post_dir = date_dir / post_id
        post_dir.mkdir(parents=True, exist_ok=True)
        
        # Save images
        for i, card in enumerate(cards, 1):
            if card.get('imageBase64'):
                image_path = post_dir / f"card_{i}.png"
                
                # Decode base64 and save
                import base64
                image_data = base64.b64decode(card['imageBase64'])
                image_path.write_bytes(image_data)
                
                # Update card with relative path
                card['imagePath'] = f"card_{i}.png"
                # Remove base64 from metadata to save space
                del card['imageBase64']
        
        # Create metadata
        metadata = {
            "id": post_id,
            "timestamp": timestamp.isoformat(),
            "articleDate": article_date or timestamp.strftime("%Y-%m-%d"),  # ✅ NOVO
            "category": category,
            "headline": headline,
            "source": source,
            "url": url,
            "tiktokTitle": tiktok_title,
            "tiktokSummary": tiktok_summary,
            "cards": cards,
            "generationTime": generation_time,
            "modelUsed": models_used
        }
        
        # Save metadata.json
        metadata_path = post_dir / "metadata.json"
        metadata_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        # Update index
        index = self._load_index()
        index.append({
            "id": post_id,
            "timestamp": timestamp.isoformat(),
            "category": category,
            "headline": headline,
            "tiktokTitle": tiktok_title,
            "path": str(post_dir.relative_to(self.posts_dir))
        })
        self._save_index(index)
        
        logger.info(f"Saved post: {post_id}")
        
        return {
            "id": post_id,
            "path": str(post_dir),
            "metadata": metadata
        }
    
    def get_all_posts(self, category: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """
        Get all posts (or filtered by category)
        Returns list of post summaries from index
        """
        index = self._load_index()
        
        if category:
            index = [p for p in index if p.get('category') == category]
        
        # Sort by timestamp descending
        index.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        return index[:limit]
    
    def get_post(self, post_id: str) -> Optional[Dict]:
        """
        Get full post data including metadata
        """
        # Find in index first
        index = self._load_index()
        post_entry = next((p for p in index if p['id'] == post_id), None)
        
        if not post_entry:
            logger.warning(f"Post not found in index: {post_id}")
            return None
        
        # Load metadata
        post_path = self.posts_dir / post_entry['path']
        metadata_file = post_path / "metadata.json"
        
        if not metadata_file.exists():
            logger.error(f"Metadata file not found: {metadata_file}")
            return None
        
        try:
            metadata = json.loads(metadata_file.read_text(encoding='utf-8'))
            
            # Add absolute paths for images
            for card in metadata.get('cards', []):
                if 'imagePath' in card:
                    card['imageFullPath'] = str(post_path / card['imagePath'])
            
            return metadata
        except Exception as e:
            logger.error(f"Failed to load post metadata: {e}")
            return None
    
    def delete_post(self, post_id: str) -> bool:
        """
        Delete a post and remove from index
        """
        # Find in index
        index = self._load_index()
        post_entry = next((p for p in index if p['id'] == post_id), None)
        
        if not post_entry:
            return False
        
        # Delete directory
        post_path = self.posts_dir / post_entry['path']
        if post_path.exists():
            import shutil
            shutil.rmtree(post_path)
        
        # Remove from index
        index = [p for p in index if p['id'] != post_id]
        self._save_index(index)
        
        logger.info(f"Deleted post: {post_id}")
        return True
