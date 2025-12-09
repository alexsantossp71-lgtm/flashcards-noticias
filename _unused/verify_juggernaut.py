
import requests
import base64
import time
import json

def test_image_save():
    url = "http://localhost:8000/api/generate-image"
    payload = {
        "prompt": "A futuristic city with flying cars, neon lights, highly detailed, realistic, 8k",
        "stylePrompt": "cinematic realism"
    }
    
    print("Generating image with Juggernaut XL...")
    start = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=600) # 10 min timeout for CPU
        resp.raise_for_status()
        data = resp.json()
        print(f"Success! Time: {time.time() - start:.2f}s")
        
        # Save image
        img_data = base64.b64decode(data.get('imageBase64', ''))
        filename = "juggernaut_test.png"
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"Saved to {filename}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_image_save()
