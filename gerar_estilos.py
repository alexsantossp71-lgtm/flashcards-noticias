"""
Generate style preview images for the FlashNews style selector
"""
import requests
import base64
import json
from pathlib import Path

API_URL = "http://127.0.0.1:8000"

# Define styles with their prompts and example descriptions
styles = [
    {
        "name": "3d_pixar",
        "prompt": "colorful, vibrant, cartoon",
        "description": "a modern smartphone with social media icons",
        "filename": "style_3d_pixar.png"
    },
    {
        "name": "realista",
        "prompt": "photorealistic, high quality, detailed, professional photography",
        "description": "a newspaper on a wooden table",
        "filename": "style_realista.png"
    },
    {
        "name": "anime",
        "prompt": "anime style, manga, vibrant colors, detailed",
        "description": "a young person reading news on tablet",
        "filename": "style_anime.png"
    },
    {
        "name": "minimalista",
        "prompt": "minimalist, clean, simple, modern design",
        "description": "abstract geometric shapes, flat design",
        "filename": "style_minimalista.png"
    },
    {
        "name": "cyberpunk",
        "prompt": "cyberpunk style, neon, futuristic, dark",
        "description": "futuristic city with neon lights at night",
        "filename": "style_cyberpunk.png"
    },
    {
        "name": "aquarela",
        "prompt": "watercolor painting, artistic, soft colors",
        "description": "flowers in a garden, artistic brush strokes",
        "filename": "style_aquarela.png"
    }
]

# Create assets directory if it doesn't exist
assets_dir = Path("static/assets")
assets_dir.mkdir(parents=True, exist_ok=True)

print("Generating style preview images...")
print("=" * 50)

for i, style in enumerate(styles, 1):
    print(f"\n[{i}/6] Generating {style['name']}...")
    
    try:
        payload = {
            "prompt": style['description'],
            "stylePrompt": style['prompt'],
            "text": "",
            "cardNumber": 2
        }
        
        response = requests.post(
            f"{API_URL}/api/generate-image",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            image_base64 = data.get('imageBase64', '')  # Correct key
            
            if image_base64:
                # Decode and save
                image_data = base64.b64decode(image_base64)
                output_path = assets_dir / style['filename']
                
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                print(f"   ✓ Saved to {output_path}")
            else:
                print(f"   ✗ No image data in response")
        else:
            print(f"   ✗ Error {response.status_code}: {response.text[:100]}")
    
    except Exception as e:
        print(f"   ✗ Failed: {e}")

print("\n" + "=" * 50)
print("Done! All style previews generated.")
