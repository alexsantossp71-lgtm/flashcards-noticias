import os
import sys
from dotenv import load_dotenv

# Load params from .env first
load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))

# Force configuration before importing image_service
os.environ["IMAGE_BACKEND"] = "comfyui"
os.environ["POLLINATIONS_FALLBACK"] = "false"
os.environ["POLLINATIONS_ENABLED"] = "false"
os.environ["COMFYUI_URL"] = "http://localhost:8188"

# Handle imports
sys.path.append(os.path.join(os.getcwd(), 'backend'))
try:
    from services.image_service import ImageService
    print("Successfully imported ImageService")
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test_generate_card6():
    service = ImageService()
    
    # Prompt from Card 6 (Index 5)
    prompt = "um jornal com a capa da revista Neurology, com uma seta apontando para cima"
    style_prompt = "estilo vetorial moderno" 
    
    print(f"Attempting to generate image with backend: {service.backend}")
    print(f"Prompt: {prompt}")
    
    try:
        base64_data, source = service.generate_image(prompt, style_prompt)
        print(f"Success! Generated with {source}")
        print(f"Base64 length: {len(base64_data)}")
        
        # Save to file to verify
        import base64
        filename = "card6_comfyui_result.png"
        with open(filename, "wb") as f:
            f.write(base64.b64decode(base64_data))
        print(f"Saved to {filename}")
        
    except Exception as e:
        print(f"Error generating image: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_generate_card6()
