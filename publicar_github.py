"""
Publicar posts do FlashNews para GitHub Pages

Usage:
    python publicar_github.py <POST_ID>
    
Example:
    python publicar_github.py exemplo-20251208-143052
"""

import json
import shutil
from pathlib import Path
import sys
from datetime import datetime

def publicar_post(post_id: str):
    """
    Publish a saved post to GitHub Pages
    
    1. Copy post from generated_posts/ to docs/posts/
    2. Update docs/posts/index.json
    3. Print success message
    """
    
    # Paths
    source_dir = Path(f"generated_posts/{post_id}")
    dest_dir = Path(f"docs/posts/{post_id}")
    index_file = Path("docs/posts/index.json")
    
    # Verify source exists
    if not source_dir.exists():
        print(f"❌ Post não encontrado: {source_dir}")
        print(f"   Posts disponíveis em generated_posts/:")
        for p in Path("generated_posts").glob("*"):
            if p.is_dir():
                print(f"     - {p.name}")
        return False
    
    print(f"📁 Publicando post: {post_id}")
    print(f"   Origem: {source_dir}")
    print(f"   Destino: {dest_dir}")
    
    # Create destination
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy all files
    print(f"\n📋 Copiando arquivos...")
    for file in source_dir.glob("*"):
        if file.is_file():
            print(f"   - {file.name}")
            shutil.copy2(file, dest_dir / file.name)
    
    # Load metadata
    metadata_file = dest_dir / "metadata.json"
    if not metadata_file.exists():
        print(f"\n❌ metadata.json não encontrado!")
        return False
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    # Update index
    print(f"\n📝 Atualizando index...")
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
    else:
        index = []
    
    # Check if already exists
    existing = next((p for p in index if p['id'] == post_id), None)
    if existing:
        print(f"   ⚠️  Post já existe no index, atualizando...")
        index.remove(existing)
    
    # Add to index
    index_entry = {
        "id": post_id,
        "title": metadata.get("title", "Sem título"),
        "summary": metadata.get("summary", "")[:200] + "..." if len(metadata.get("summary", "")) > 200 else metadata.get("summary", ""),
        "category": metadata.get("category", "Geral"),
        "timestamp": metadata.get("timestamp", datetime.now().isoformat()),
        "cardCount": metadata.get("cardCount", 7)
    }
    
    index.append(index_entry)
    
    # Sort by timestamp (newest first)
    index.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Save index
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Post publicado com sucesso!")
    print(f"\n📊 Informações do post:")
    print(f"   Título: {index_entry['title']}")
    print(f"   Categoria: {index_entry['category']}")
    print(f"   Cards: {index_entry['cardCount']}")
    print(f"\n🌐 Para ver localmente:")
    print(f"   python -m http.server 8080 -d docs")
    print(f"   Abra: http://localhost:8080/post.html?id={post_id}")
    print(f"\n📤 Próximos passos:")
    print(f"   1. git add docs/")
    print(f"   2. git commit -m 'Publicar: {index_entry['title']}'")
    print(f"   3. git push")
    print(f"   4. Acessar: https://[USUARIO].github.io/[REPO]/post.html?id={post_id}")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Uso: python publicar_github.py <POST_ID>")
        print("\n📋 Posts disponíveis:")
        for p in Path("generated_posts").glob("*"):
            if p.is_dir():
                # Try to load metadata
                meta_file = p / "metadata.json"
                if meta_file.exists():
                    with open(meta_file, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                    print(f"   - {p.name}")
                    print(f"     Título: {meta.get('title', 'N/A')}")
                    print(f"     Data: {meta.get('timestamp', 'N/A')}")
                else:
                    print(f"   - {p.name} (sem metadata)")
        sys.exit(1)
    
    post_id = sys.argv[1]
    success = publicar_post(post_id)
    sys.exit(0 if success else 1)
