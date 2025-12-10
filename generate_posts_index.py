"""
Generate posts.json index file for GitHub Pages viewer
This file lists all generated posts for the web viewer
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path(__file__).parent
GENERATED_POSTS_DIR = BASE_DIR / "generated_posts"
OUTPUT_FILE = GENERATED_POSTS_DIR / "posts.json"

def scan_posts():
    """Scan all post directories and collect metadata"""
    posts = []
    
    if not GENERATED_POSTS_DIR.exists():
        print(f"⚠️  Directory not found: {GENERATED_POSTS_DIR}")
        return posts
    
    # Scan all date directories (YYYY-MM-DD)
    for date_dir in sorted(GENERATED_POSTS_DIR.iterdir(), reverse=True):
        if not date_dir.is_dir():
            continue
        
        # Scan all post directories in this date
        for post_dir in date_dir.iterdir():
            if not post_dir.is_dir():
                continue
            
            metadata_file = post_dir / "metadata.json"
            if not metadata_file.exists():
                continue
            
            try:
                # Read metadata
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                
                # Build post entry
                post_id = post_dir.name
                date_str = date_dir.name
                
                # Count cards
                cards_dir = post_dir / "cards"
                num_cards = len(list(cards_dir.glob("*.png"))) if cards_dir.exists() else 0
                
                post_entry = {
                    "id": f"{date_str}/{post_id}",
                    "date": date_str,
                    "timestamp": metadata.get("timestamp", 0),
                    "category": metadata.get("category", "Geral"),
                    "headline": metadata.get("headline", "Sem título"),
                    "source": metadata.get("source", "Desconhecido"),
                    "url": metadata.get("url", ""),
                    "tiktokTitle": metadata.get("tiktok_title", ""),
                    "numCards": num_cards,
                    "path": f"{date_str}/{post_id}"
                }
                
                posts.append(post_entry)
                print(f"✓ Found: {post_entry['headline'][:50]}...")
                
            except Exception as e:
                print(f"⚠️  Error reading {metadata_file}: {e}")
    
    return posts

def generate_posts_json():
    """Generate posts.json index file"""
    print("=" * 50)
    print("Generating posts.json index...")
    print("=" * 50)
    print()
    
    posts = scan_posts()
    
    # Sort by timestamp (newest first)
    posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Create output structure
    output = {
        "generated_at": datetime.now().isoformat(),
        "total_posts": len(posts),
        "posts": posts
    }
    
    # Write to file
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print()
    print("=" * 50)
    print(f"✅ Generated {OUTPUT_FILE}")
    print(f"📊 Total posts: {len(posts)}")
    print("=" * 50)
    print()
    
    return OUTPUT_FILE

if __name__ == "__main__":
    generate_posts_json()
