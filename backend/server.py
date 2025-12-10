# -*- coding: utf-8 -*-
"""
Main FastAPI Server - Local AI Backend
Using Ollama for text generation
✅ UTF-8 encoding garantido para acentuação e caracteres especiais
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
import time
from pathlib import Path

from config import API_HOST, API_PORT, CORS_ORIGINS
from services.ollama_service import OllamaService
from services.rss_service import RSSService
from services.image_service import ImageService
from services.storage_service import StorageService
from services.prompt_enhancer_service import PromptEnhancerService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="FlashNews AI - Local Backend", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services - Ollama only
text_service = OllamaService()
logger.info("✅ Using Ollama for text generation")

rss_service = RSSService()
image_service = ImageService()  # Always local!
storage_service = StorageService()
prompt_enhancer = PromptEnhancerService()  # ✅ NEW: Auto-enhance prompts
logger.info("✅ Prompt Enhancer Service initialized")

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static")
    logger.info(f"✅ Static files mounted from {static_dir}")
else:
    logger.warning(f"⚠️ Static directory not found: {static_dir}")


# --- REQUEST/RESPONSE MODELS ---

class HeadlinesRequest(BaseModel):
    category: str
    count: int = 15

class HeadlineFromUrlRequest(BaseModel):
    url: str

class GenerateContentRequest(BaseModel):
    headline: str
    url: str
    source: str
    stylePrompt: str

class GenerateGuideRequest(BaseModel):
    topic: str
    stylePrompt: str

class GenerateImageRequest(BaseModel):
    prompt: str
    stylePrompt: str
    text: str = ""
    cardNumber: int = 1

class SavePostRequest(BaseModel):
    category: str
    headline: str
    source: str
    url: str
    tiktokTitle: str
    tiktokSummary: str
    cards: List[Dict]
    generationTime: float
    modelUsed: Dict
    articleDate: Optional[str] = None  # ✅ NOVO: Data da notícia

# --- API ENDPOINTS ---

@app.get("/")
async def root():
    return {
        "message": "FlashNews AI - Local Backend v2.0",
        "status": "running",
        "textBackend": "ollama",
        "imageBackend": "local (diffusers)"
    }

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon to avoid 404 errors"""
    favicon_path = Path(__file__).parent.parent / "static" / "assets" / "favicon.ico"
    if favicon_path.exists():
        return FileResponse(favicon_path)
    # Return 404 if not found (BytesIO não funciona com FileResponse)
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Favicon not found")

@app.get("/api/status")
async def status():
    text_status = text_service.check_health()
    return {
        "status": "online",
        "textService": "ollama",
        "textHealth": "connected" if text_status else "disconnected",
        "timestamp": time.time()
    }

@app.post("/api/push-to-github")
async def push_to_github():
    """
    Automatically commit and push new cards to GitHub
    + Sync to docs/ for GitHub Pages viewer
    """
    import subprocess
    import shutil
    import json
    from pathlib import Path
    
    try:
        repo_path = Path(__file__).parent.parent
        
        # ✅ SYNC GITHUB PAGES: Copiar index.json para docs/posts/
        logger.info("📋 Syncing GitHub Pages viewer...")
        source_index = repo_path / "generated_posts" / "index.json"
        dest_index = repo_path / "docs" / "posts" / "index.json"
        
        if source_index.exists():
            # Criar diretório se não existir
            dest_index.parent.mkdir(parents=True, exist_ok=True)
            
            # Copiar com preservação de metadados
            shutil.copy2(source_index, dest_index)
            
            # Contar posts para log
            with open(source_index, 'r', encoding='utf-8') as f:
                data = json.load(f)
                posts_count = len(data.get('posts', []))
                logger.info(f"✅ Synced {posts_count} posts to GitHub Pages viewer")
        else:
            logger.warning("⚠️ source index.json not found, skipping sync")
        
        # Check git status
        result = subprocess.run(
            ["git", "status", "--porcelain", "generated_posts/", "docs/"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if not result.stdout.strip():
            return {"success": True, "message": "No changes to commit"}
        
        # Add generated_posts AND docs
        subprocess.run(
            ["git", "add", "generated_posts/", "docs/"],
            cwd=repo_path,
            check=True,
            timeout=10
        )
        
        # Commit
        from datetime import datetime
        commit_msg = f"Auto-save: New flashcards + GitHub Pages sync on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=repo_path,
            check=True,
            timeout=10
        )
        
        # Push
        subprocess.run(
            ["git", "push"],
            cwd=repo_path,
            check=True,
            timeout=30
        )
        
        logger.info(f"✅ Auto-pushed to GitHub: {commit_msg}")
        return {
            "success": True,
            "message": "Cards pushed to GitHub + Pages viewer updated",
            "commit": commit_msg,
            "viewerSynced": True
        }
        
    except subprocess.TimeoutExpired:
        logger.error("Git operation timed out")
        raise HTTPException(status_code=500, detail="Git operation timed out")
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e}")
        raise HTTPException(status_code=500, detail=f"Git command failed: {e}")
    except Exception as e:
        logger.error(f"Error pushing to GitHub: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/headlines")
async def get_headlines(request: HeadlinesRequest):
    try:
        logger.info(f"Fetching headlines: {request.category}")
        raw_headlines = rss_service.fetch_headlines(request.category)
        
        if not raw_headlines:
            raise HTTPException(status_code=404, detail="No headlines found")
        
        curated = text_service.curate_headlines(
            raw_headlines,
            request.category,
            request.count
        )
        
        return {"headlines": curated}
    except Exception as e:
        logger.error(f"Error fetching headlines: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-content")
async def generate_content(request: GenerateContentRequest):
    try:
        logger.info(f"Generating content: {request.headline}")
        start_time = time.time()
        
        # Scrape article if possible
        article_text = None
        if request.url:
            from services.scraper_service import article_scraper
            article_data = article_scraper.scrape_article(request.url)
            if article_data and article_data.get('content'):
                article_text = article_data['content']
                logger.info(f"Scraped {len(article_text)} chars")
        
        # Generate with Gemini or Ollama
        content = text_service.generate_flashcard_content(
            headline=request.headline,
            url=request.url,
            style_prompt=request.stylePrompt,
            source=request.source,
            article_text=article_text
        )
        
        # ✅ AUTO-ENHANCE: Processar imagePrompts com PromptEnhancerService
        if 'flashcards' in content and content['flashcards']:
            logger.info("🎨 Enhancing image prompts automatically...")
            enhanced_cards = prompt_enhancer.batch_enhance(
                cards=content['flashcards'],
                headline=request.headline,
                article_text=article_text,
                style_prompt=request.stylePrompt
            )
            content['flashcards'] = enhanced_cards
            logger.info(f"✅ Enhanced {len(enhanced_cards)} prompts")
        
        generation_time = time.time() - start_time
        
        # Model name - Ollama only
        model_name = getattr(text_service, 'primary_model', 'Ollama')
        
        return {
            **content,
            "generationTime": generation_time,
            "modelUsed": model_name,
            "scrapedContent": bool(article_text),
            "promptsEnhanced": True  ##✅ Indicador de que prompts foram otimizados
        }
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-image")
def generate_image(request: GenerateImageRequest):
    try:
        logger.info(f"Generating image: {request.prompt[:50]}...")
        start_time = time.time()
        
        base64_data, source = image_service.generate_image(
            prompt=request.prompt,
            style_prompt=request.stylePrompt,
            text=request.text,
            card_number=request.cardNumber
        )
        
        generation_time = time.time() - start_time
        
        return {
            "imageBase64": base64_data,
            "imageSource": source,
            "generationTime": generation_time
        }
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save-post")
async def save_post(request: SavePostRequest):
    try:
        logger.info(f"Saving post: {request.headline}")
        
        result = storage_service.save_post(
            category=request.category,
            headline=request.headline,
            source=request.source,
            url=request.url,
            tiktok_title=request.tiktokTitle,
            tiktok_summary=request.tiktokSummary,
            cards=request.cards,
            generation_time=request.generationTime,
            models_used=request.modelUsed,
            article_date=request.articleDate  # ✅ NOVO
        )
        
        return result
    except Exception as e:
        logger.error(f"Error saving post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/posts")
async def get_posts(category: Optional[str] = None, limit: int = 50):
    try:
        posts = storage_service.get_all_posts(category=category, limit=limit)
        return {"posts": posts}
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/posts/{post_id}")
async def get_post(post_id: str):
    try:
        post = storage_service.get_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: str):
    try:
        success = storage_service.delete_post(post_id)
        if not success:
            raise HTTPException(status_code=404, detail="Post not found")
        return {"message": "Post deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/image/{post_id}/{card_number}")
async def get_image(post_id: str, card_number: int):
    try:
        post = storage_service.get_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        if card_number < 1 or card_number > len(post.get('cards', [])):
            raise HTTPException(status_code=404, detail="Card not found")
        
        card = post['cards'][card_number - 1]
        image_path = Path(card.get('imageFullPath', ''))
        
        if not image_path.exists():
            raise HTTPException(status_code=404, detail="Image file not found")
        
        return FileResponse(image_path)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
