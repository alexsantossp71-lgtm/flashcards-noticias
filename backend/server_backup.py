"""
Main FastAPI Server - Local AI Backend
Coordinates Ollama, Image Generation, and Storage
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
    cards: List[Dict]  # [{text, imagePrompt, imageBase64, imageSource}]
    generationTime: float
    modelUsed: Dict


# --- API ENDPOINTS ---

@app.get("/")
async def root():
    return {
        "message": "FlashNews AI - Local Backend",
        "status": "running",
        "endpoints": {
            "headlines": "/api/headlines",
            "headline_from_url": "/api/headline-from-url",
            "generate_content": "/api/generate-content",
            "generate_guide": "/api/generate-guide",
            "generate_image": "/api/generate-image",
            "save_post": "/api/save-post",
            "posts": "/api/posts",
            "post_detail": "/api/posts/{post_id}"
        }
    }


@app.get("/api/status")
async def status():
    """
    Check server and Ollama status
    """
    ollama_status = ollama_service.check_health()
    return {
        "status": "online",
        "ollama": "connected" if ollama_status else "disconnected",
        "timestamp": time.time()
    }


@app.post("/api/headlines")
async def get_headlines(request: HeadlinesRequest):
    """
    Fetch and curate headlines from RSS feeds
    """
    try:
        logger.info(f"Fetching headlines for category: {request.category}")
        
        # Fetch raw headlines
        raw_headlines = rss_service.fetch_headlines(request.category)
        
        if not raw_headlines:
            raise HTTPException(status_code=404, message="No headlines found")
        
        # Curate with Ollama
        curated = ollama_service.curate_headlines(
            raw_headlines,
            request.category,
            request.count
        )
        
        return {"headlines": curated}
        
    except Exception as e:
        logger.error(f"Error fetching headlines: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/headline-from-url")
async def get_headline_from_url(request: HeadlineFromUrlRequest):
    """
    Extract headline info from a URL
    """
    try:
        result = ollama_service.extract_headline_from_url(request.url)
        return {
            "headline": result.get("headline", "Notícia Encontrada"),
            "source": result.get("source", "Web"),
            "url": request.url
        }
    except Exception as e:
        logger.error(f"Error extracting headline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-content")
async def generate_content(request: GenerateContentRequest):
    """
    Generate flashcard content using Ollama
    Now with web scraping for full article content!
    """
    try:
        logger.info(f"Generating content for: {request.headline}")
        start_time = time.time()
        
        # Try to scrape article content from URL
        article_text = None
        if request.url:
            from services.scraper_service import article_scraper
            article_data = article_scraper.scrape_article(request.url)
        
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-guide")
async def generate_guide(request: GenerateGuideRequest):
    """
    Generate educational guide content using Ollama
    """
    try:
        logger.info(f"Generating guide for: {request.topic}")
        start_time = time.time()
        
        content = ollama_service.generate_guide_content(
            topic=request.topic,
            style_prompt=request.stylePrompt
        )
        
        generation_time = time.time() - start_time
        
        return {
            **content,
            "generationTime": generation_time,
            "modelUsed": ollama_service.primary_model
        }
        
    except Exception as e:
        logger.error(f"Error generating guide: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-image")
def generate_image(request: GenerateImageRequest):
    """
    Generate image using local model or Pollinations with text overlay
    """
    try:
        logger.info(f"Generating image for prompt: {request.prompt[:50]}...")
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
    """
    Save generated post to filesystem
    """
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
            models_used=request.modelUsed
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Error saving post: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/posts")
async def get_posts(category: Optional[str] = None, limit: int = 50):
    """
    Get all saved posts (optionally filtered by category)
    """
    try:
        posts = storage_service.get_all_posts(category=category, limit=limit)
        return {"posts": posts}
    except Exception as e:
        logger.error(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/posts/{post_id}")
async def get_post(post_id: str):
    """
    Get full post data including metadata
    """
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
    """
    Delete a saved post
    """
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
    """
    Serve individual card image
    """
    try:
        post = storage_service.get_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Find card
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
