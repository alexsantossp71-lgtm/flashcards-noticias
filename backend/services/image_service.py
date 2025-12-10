# -*- coding: utf-8 -*-
"""
Image Service - Generate images using local models or Pollinations fallback
Supports: ComfyUI, Automatic1111, Fooocus, Pollinations
✅ UTF-8 encoding garantido para acentuação em overlays de texto
"""

import requests
import base64
import logging
import time
from io import BytesIO
from PIL import Image
from typing import Tuple, Literal
from config import (
    IMAGE_BACKEND, 
    COMFYUI_URL, COMFYUI_TIMEOUT,
    A1111_URL, A1111_TIMEOUT,
    FOOOCUS_URL, FOOOCUS_TIMEOUT,
    POLLINATIONS_ENABLED,
    IMAGE_WIDTH, IMAGE_HEIGHT
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageService:
    def __init__(self):
        self.backend = IMAGE_BACKEND
        self.diffusers_pipe = None
    
    def add_text_overlay(self, image: Image, text: str, card_number: int) -> Image:
        """
        Add text overlay to flashcard image with custom styling
        
        All cards: Centered vertically and horizontally
        Card 1: Title (white) + Source (orange)
        Cards 2-7: Content text (white)
        All: Black stroke, Montserrat Bold font, large size
        
        ✅ SUPORTE COMPLETO A UTF-8: Acentuação, til (~), cedilha (ç), etc.
        """
        from PIL import ImageDraw, ImageFont
        import os
        
        # ✅ GARANTIR ENCODING UTF-8: Normalizar texto para garantir caracteres corretos
        # Isso resolve problemas com acentuação, til, cedilha, etc.
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        
        # Normalizar para garantir que caracteres compostos sejam processados corretamente
        import unicodedata
        text = unicodedata.normalize('NFC', text)  # Canonical decomposition + composition
        
        width, height = image.size
        
        # Create drawing context
        draw = ImageDraw.Draw(image)
        
        # Try to load Montserrat font with LARGER size
        try:
            # Get the directory of this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.dirname(current_dir)
            
            # ✅ Fontes com SUPORTE COMPLETO a acentuação/UTF-8
            # Ordem: Montserrat > Arial Bold > Arial (todas suportam caracteres latinos)
            font_paths = [
                # Downloaded Montserrat (melhor opção - moderna e legível)
                os.path.join(backend_dir, "fonts", "Montserrat-Bold.ttf"),
                # Windows system Montserrat (if installed)
                "C:\\Windows\\Fonts\\Montserrat-Bold.ttf",
                "C:\\Windows\\Fonts\\montserrat-bold.ttf",
                # Fallback to Arial
                "C:\\Windows\\Fonts\\arialbd.ttf",
                "C:\\Windows\\Fonts\\arial.ttf",
            ]
            
            font_size = 65  # Readable size that fits well
            font = None
            
            for path in font_paths:
                try:
                    if os.path.exists(path):
                        font = ImageFont.truetype(path, font_size)
                        logger.info(f"Loaded font: {path} at size {font_size}")
                        break
                except Exception as e:
                    logger.debug(f"Failed to load font {path}: {e}")
                    continue
            
            if not font:
                logger.warning("No custom font found, using default")
                font = ImageFont.load_default()
        except Exception as e:
            logger.error(f"Error loading font: {e}")
            font = ImageFont.load_default()
        
        if card_number == 1:
            # Card 1: Title + Source (centered vertically and horizontally)
            # IMPORTANTE: Garantir que fonte está em LINHA SEPARADA
            lines = text.split('\n', 1)
            title = lines[0].strip() if lines else text
            source = lines[1].strip() if len(lines) > 1 else ""
            
            # Wrap title text with generous padding for readability
            title_lines = self._wrap_text(title, font, width - 300)
            
            # Calculate line heights
            title_line_height = font.size + 20  # Spacing for title
            source_gap = 60  # MAIOR gap antes da fonte para separação visual clara
            
            # Source font - MENOR que título para hierarquia visual
            try:
                source_font_size = int(font.size * 0.7)  # 70% do tamanho do título
                source_font = ImageFont.truetype(font.path, source_font_size)
            except:
                source_font = font
            
            # Calculate total height
            total_height = len(title_lines) * title_line_height
            if source:
                bbox = draw.textbbox((0, 0), source, font=source_font)
                source_height = bbox[3] - bbox[1]
                total_height += source_gap + source_height
            
            # Start Y position (centered vertically)
            y = (height - total_height) // 2
            
            # Draw title (white with black stroke)
            for line in title_lines:
                self._draw_text_with_stroke(draw, line, font, width, y, (255, 255, 255), (0, 0, 0))
                y += title_line_height
            
            # Draw source (LARANJA VIBRANTE com black stroke) em LINHA SEPARADA
            if source:
                y += source_gap  # Gap grande para separação clara
                # COR LARANJA VIBRANTE: RGB(255, 120, 0) - alaranjado forte
                self._draw_text_with_stroke(draw, source, source_font, width, y, (255, 120, 0), (0, 0, 0))
        
        else:
            # Cards 2-7: UPPER THIRD (avoiding TikTok icons at top)
            # Wrap text to fit width
            wrapped_lines = self._wrap_text(text, font, width - 200)
            
            # Calculate total height of text block (just for reference, not used for Y centering)
            line_height = font.size + 30
            
            # Start Y position (Higher up - 10% down for better visibility)
            # TikTok icons are top ~150px. 10% of 1920 is 192px, which is safe.
            y = int(height * 0.10)
            
            # Draw each line centered horizontally
            for line in wrapped_lines:
                self._draw_text_with_stroke(draw, line, font, width, y, (255, 255, 255), (0, 0, 0))
                y += line_height
        
        return image
    
    def _wrap_text(self, text: str, font, max_width: int) -> list:
        """Wrap text to fit within max_width"""
        from PIL import ImageDraw
        
        words = text.split()
        lines = []
        current_line = []
        
        # Create temporary draw to measure text
        temp_img = Image.new('RGB', (1, 1))
        draw = ImageDraw.Draw(temp_img)
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _draw_text_with_stroke(self, draw, text: str, font, image_width: int, y: int, fill_color: tuple, stroke_color: tuple):
        """Draw text with stroke (outline) effect, centered horizontally"""
        from PIL import ImageDraw
        
        # Get text bounding box to center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (image_width - text_width) // 2
        
        # Draw stroke (black outline) - THICKER stroke for visibility
        stroke_width = 5  # Increased from 3 to 5 for better visibility
        for offset_x in range(-stroke_width, stroke_width + 1):
            for offset_y in range(-stroke_width, stroke_width + 1):
                if offset_x != 0 or offset_y != 0:
                    draw.text((x + offset_x, y + offset_y), text, font=font, fill=stroke_color)
        
        # Draw main text (white or orange)
        draw.text((x, y), text, font=font, fill=fill_color)
    
    def generate_image(self, prompt: str, style_prompt: str, text: str = "", card_number: int = 1) -> Tuple[str, str]:
        """
        Generate image with text overlay and return (base64_data, source)
        source can be: 'comfyui', 'automatic1111', 'fooocus', 'pollinations', 'diffusers'
        """
        full_prompt = self._build_full_prompt(prompt, style_prompt)
        
        # Generate base image
        image = None
        source = None
        
        # Try local backend first (if not pollinations)

        try:
            logger.info(f"Attempting image generation with {self.backend}")
            base64_data = self._generate_local(full_prompt, self.backend)
            # Decode base64 to PIL Image
            image_data = base64.b64decode(base64_data)
            image = Image.open(BytesIO(image_data))
            source = self.backend
        except Exception as e:
            logger.error(f"Local image generation failed: {e}")
            raise
        
        # Apply text overlay if text is provided
        if text:
            logger.info(f"Adding text overlay to card {card_number}")
            image = self.add_text_overlay(image, text, card_number)
        
        # Convert back to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        final_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return final_base64, source
    
    def _build_full_prompt(self, prompt: str, style_prompt: str) -> str:
        """Combine prompt with style and quality enhancers"""
        clean_prompt = self._clean_prompt(prompt)
        clean_style = self._clean_prompt(style_prompt)
        return f"{clean_prompt}. {clean_style}, 8k, uhd, highly detailed, sharp focus"
    
    def _clean_prompt(self, text: str) -> str:
        """Remove special characters that might break APIs"""
        return ''.join(c for c in text if c.isalnum() or c in ' ,.!?-')
    
    def _generate_local(self, prompt: str, backend: str) -> str:
        """
        Generate image using local model (ComfyUI/A1111/Fooocus)
        Returns base64 encoded image
        """
        if backend == "comfyui":
            return self._generate_comfyui(prompt)
        elif backend == "automatic1111":
            return self._generate_a1111(prompt)
        elif backend == "fooocus":
            return self._generate_fooocus(prompt)
        elif backend == "diffusers":
            return self._generate_diffusers(prompt)
        else:
            raise ValueError(f"Unknown backend: {backend}")
    
    def _generate_comfyui(self, prompt: str) -> str:
        """Generate via ComfyUI API with polling"""
        # Basic workflow for text-to-image
        workflow = {
            "3": {
                "class_type": "KSampler",
                "inputs": {
                    "seed": int(time.time()),
                    "steps": 20, # Increased steps for quality
                    "cfg": 8.0,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1.0,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                }
            },
            "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "SDXL-TURBO\\sd_xl_turbo_1.0_fp16.safetensors"}},
            "5": {"class_type": "EmptyLatentImage", "inputs": {"width": IMAGE_WIDTH, "height": IMAGE_HEIGHT, "batch_size": 1}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
            "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "low quality, blurry, watermark, text, signature", "clip": ["4", 1]}},
            "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
            "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "FlashNews", "images": ["8", 0]}}
        }
        
        # 1. Send Prompt
        prompt_payload = {"prompt": workflow}
        try:
            response = requests.post(f"{COMFYUI_URL}/prompt", json=prompt_payload, timeout=10)
            response.raise_for_status()
            prompt_id = response.json().get("prompt_id")
            if not prompt_id:
                raise Exception("No prompt_id received from ComfyUI")
            
            logger.info(f"ComfyUI task started: {prompt_id}")
        except Exception as e:
            logger.error(f"Failed to queue prompt in ComfyUI: {e}")
            raise

        # 2. Poll for completion
        # Use a reasonable timeout (e.g. 60 seconds)
        start_time = time.time()
        while time.time() - start_time < COMFYUI_TIMEOUT:
            try:
                history_resp = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=5)
                history_resp.raise_for_status()
                history_data = history_resp.json()
                
                if prompt_id in history_data:
                    # Task finished
                    outputs = history_data[prompt_id].get("outputs", {})
                    if "9" in outputs and "images" in outputs["9"]:
                        image_info = outputs["9"]["images"][0]
                        filename = image_info.get("filename")
                        subfolder = image_info.get("subfolder", "")
                        image_type = image_info.get("type", "output")
                        
                        # 3. Retrieve Image
                        params = {"filename": filename, "subfolder": subfolder, "type": image_type}
                        image_resp = requests.get(f"{COMFYUI_URL}/view", params=params, timeout=30)
                        image_resp.raise_for_status()
                        
                        # Convert to base64 (PNG is standard from ComfyUI view)
                        # Re-encode to ensure valid base64 string
                        return base64.b64encode(image_resp.content).decode("utf-8")
                    else:
                        raise Exception("Output node 9 not found in history data")
                
                # Wait before next poll
                time.sleep(1)
                
            except requests.RequestException as e:
                logger.warning(f"Error polling ComfyUI: {e}")
                time.sleep(1) # Wait and try again
        
        raise TimeoutError("ComfyUI generation timed out")
    
    def _generate_a1111(self, prompt: str) -> str:
        """Generate via Automatic1111 API"""
        payload = {
            "prompt": prompt,
            "negative_prompt": "low quality, blurry, distorted, ugly, bad anatomy",
            "steps": 20,
            "width": IMAGE_WIDTH,
            "height": IMAGE_HEIGHT,
            "cfg_scale": 7,
            "sampler_name": "Euler a",
            "seed": -1
        }
        
        response = requests.post(
            f"{A1111_URL}/sdapi/v1/txt2img",
            json=payload,
            timeout=A1111_TIMEOUT
        )
        response.raise_for_status()
        
        result = response.json()
        if 'images' in result and len(result['images']) > 0:
            return result['images'][0]  # Already base64
        else:
            raise Exception("No image in A1111 response")
    
    def _generate_fooocus(self, prompt: str) -> str:
        """Generate via Fooocus API"""
        # Fooocus API structure varies, this is a generic example
        payload = {
            "prompt": prompt,
            "negative_prompt": "low quality, blurry",
            "image_number": 1,
            "aspect_ratios_selection": "9:16"  # Vertical
        }
        
        response = requests.post(
            f"{FOOOCUS_URL}/v1/generation/text-to-image",
            json=payload,
            timeout=FOOOCUS_TIMEOUT
        )
        response.raise_for_status()
        
        # Assuming response contains base64 image
        result = response.json()
        if 'image' in result:
            return result['image']
        else:
            raise Exception("No image in Fooocus response")
    

    def _generate_diffusers(self, prompt: str) -> str:
        """
        Generate using Juggernaut XL Lightning with Optimized Workflow (512x768 + Upscale)
        Fixed for GTX 1060 6GB - Stable CUDA handling
        """
        try:
            import torch
            from diffusers import AutoPipelineForText2Image, DPMSolverMultistepScheduler
        except ImportError:
            raise ImportError("Diffusers/Torch not installed. Run 'pip install diffusers transformers accelerate torch'")

        # Lazy load pipeline if not already loaded
        if not hasattr(self, 'diffusers_pipe') or self.diffusers_pipe is None:
            logger.info("Initializing Juggernaut XL Lightning (GTX 1060 Optimized)...")
            
            # Try CUDA first, fallback to CPU if it fails
            try:
                if torch.cuda.is_available():
                    self.device = "cuda"
                    dtype = torch.float16
                    logger.info("CUDA available - attempting GPU generation")
                else:
                    self.device = "cpu"
                    dtype = torch.float32
                    logger.info("CUDA not available - using CPU")
                
                # Load pipeline - Juggernaut XL Lightning
                self.diffusers_pipe = AutoPipelineForText2Image.from_pretrained(
                    "RunDiffusion/Juggernaut-XL-Lightning", 
                    torch_dtype=dtype,
                    low_cpu_mem_usage=True
                )
                
                # GTX 1060 6GB: Use SEQUENTIAL CPU offload (more stable)
                # This avoids the '_hf_hook' error
                if self.device == "cuda":
                    try:
                        logger.info("Enabling sequential CPU offload for GTX 1060...")
                        # Sequential offload is more stable than model_cpu_offload
                        self.diffusers_pipe.enable_sequential_cpu_offload()
                        self.diffusers_pipe.enable_vae_tiling()  # Reduces VRAM usage
                        logger.info("✅ GPU offload configured successfully")
                    except Exception as offload_error:
                        logger.warning(f"GPU offload failed: {offload_error}. Falling back to CPU...")
                        self.device = "cpu"
                        self.diffusers_pipe.to("cpu")
                else:
                    # CPU mode
                    self.diffusers_pipe.to("cpu")
                
            except Exception as cuda_error:
                # CUDA initialization failed - force CPU
                logger.error(f"CUDA initialization failed: {cuda_error}")
                logger.info("Forcing CPU mode for stability...")
                self.device = "cpu"
                dtype = torch.float32
                
                self.diffusers_pipe = AutoPipelineForText2Image.from_pretrained(
                    "RunDiffusion/Juggernaut-XL-Lightning", 
                    torch_dtype=dtype,
                    low_cpu_mem_usage=True
                )
                self.diffusers_pipe.to("cpu")
            
            # Scheduler: DPM++ 2M Karras (User Request)
            self.diffusers_pipe.scheduler = DPMSolverMultistepScheduler.from_config(
                self.diffusers_pipe.scheduler.config, 
                use_karras_sigmas=True,
                algorithm_type="dpmsolver++"
            )
            
            # If on CPU, we don't enable offload as it's already there
            if self.device == "cpu":
                self.diffusers_pipe.to("cpu")

            logger.info(f"Pipeline loaded on {self.device} with DPM++ 2M Karras")
        
        # Optimized Workflow for Speed & Consistency
        # 1. Generate at lower resolution (512x768) - Faster & Less hallucinations
        gen_width, gen_height = 512, 768
        
        logger.info(f"Generating at {gen_width}x{gen_height} (Optimized)...")
        
        negative_prompt = "bad quality, blurry, distorted, ugly, pixelated, watermark, text, signature"
        
        image = self.diffusers_pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            height=gen_height,
            width=gen_width,
            num_inference_steps=6,    # Sweet spot: 6 steps for quality
            guidance_scale=1.5        # Moderate guidance for better coherence
        ).images[0]
        
        # 2. Smart Upscale (2x) -> 1024x1536
        # Using Lanczos as "Latent Upscaler" substitute for speed
        logger.info("Upscaling 2x...")
        image = image.resize((gen_width * 2, gen_height * 2), Image.LANCZOS)
        
        # 3. Final Crop/Resize to Target (1080x1920)
        image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS)
        
        # Convert to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
