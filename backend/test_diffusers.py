
import logging
import sys
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_generation():
    print("Testing Diffusers Generation...")
    
    try:
        import torch
        print(f"Torch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        
        from diffusers import AutoPipelineForText2Image, DPMSolverMultistepScheduler
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        print(f"Using device: {device}, dtype: {dtype}")

        print("Loading pipeline...")
        pipe = AutoPipelineForText2Image.from_pretrained(
            "RunDiffusion/Juggernaut-XL-Lightning", 
            torch_dtype=dtype,
            low_cpu_mem_usage=True
        )
        
        if device == "cuda":
            pipe.enable_model_cpu_offload()
            pipe.enable_vae_tiling()
            
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            pipe.scheduler.config, 
            use_karras_sigmas=True,
            algorithm_type="dpmsolver++"
        )
        
        if device == "cpu":
            pipe.to("cpu")
            
        print("Pipeline loaded. Generating test image...")
        image = pipe(
            prompt="a cat", 
            num_inference_steps=2, 
            guidance_scale=1.5
        ).images[0]
        
        print("Success! Image generated.")
        
    except Exception as e:
        print("\nCRITICAL ERROR:")
        traceback.print_exc()

if __name__ == "__main__":
    test_generation()
