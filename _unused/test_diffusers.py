
import logging
import base64
import torch
from io import BytesIO
from diffusers import AutoPipelineForText2Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DiffusersTest")

def test_diffusers_gen():
    logger.info("Initializing Diffusers pipeline...")
    
    # Use a lightweight model for testing, or SDXL Turbo if available
    # Using SDXL Turbo as it's fast and 512x512 friendly (though native is 512, works for test)
    model_id = "stabilityai/sdxl-turbo"
    
    try:
        # Check for CUDA
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        pipe = AutoPipelineForText2Image.from_pretrained(
            model_id, 
            torch_dtype=torch.float16 if device == "cuda" else torch.float32, 
            variant="fp16" if device == "cuda" else None
        )
        pipe.to(device)
        
        prompt = "um jornal com a capa da revista Neurology, com uma seta apontando para cima, estilo vetorial moderno"
        
        logger.info(f"Generating image for: {prompt}")
        
        # SDXL Turbo needs only 1-4 steps
        image = pipe(prompt=prompt, num_inference_steps=2, guidance_scale=0.0).images[0]
        
        # Convert to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        base64_data = base64.b64encode(buffered.getvalue()).decode()
        
        # Save to file
        filename = "card6_diffusers.png"
        image.save(filename)
        logger.info(f"Success! Image saved to {filename}")
        
    except Exception as e:
        logger.error(f"Diffusers generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_diffusers_gen()
