
import requests
import base64
import time

def test_image():
    url = "http://localhost:8000/api/generate-image"
    payload = {
        "prompt": "Test image of a futuristic city",
        "stylePrompt": "cyberpunk"
    }
    
    print("Sending request...")
    start = time.time()
    try:
        resp = requests.post(url, json=payload, timeout=300)
        resp.raise_for_status()
        data = resp.json()
        print(f"Success! Time: {time.time() - start:.2f}s")
        print(f"Source: {data.get('imageSource')}")
        print(f"B64 Length: {len(data.get('imageBase64', ''))}")
    except Exception as e:
        print(f"Error: {e}")
        try:
            print(resp.text)
        except:
            pass

if __name__ == "__main__":
    test_image()
