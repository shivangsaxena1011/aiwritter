import os
import json
import time
import asyncio
import logging
from typing import Optional, Dict, Any
from google import genai
from google.genai import types
from backend.app.core.config import settings
from backend.app.services.ai.base import AIProvider

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)

    async def generate_text(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: Optional[int] = 16000
    ) -> str:
        def _call():
            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                system_instruction=system_instruction
            )
            retries = 3
            backoff = 2.0
            last_err = None
            for attempt in range(retries):
                try:
                    response = self.client.models.generate_content(
                        model=settings.TEXT_MODEL,
                        contents=prompt,
                        config=config
                    )
                    return response.text or ""
                except Exception as e:
                    last_err = e
                    logger.warning(f"Gemini API call attempt {attempt+1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(backoff)
                        backoff *= 2.0
            raise last_err or RuntimeError("Gemini text generation failed after retries")

        return await asyncio.to_thread(_call)

    async def generate_structured(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        def _call():
            config = types.GenerateContentConfig(
                temperature=temperature,
                response_mime_type="application/json",
                system_instruction=system_instruction
            )
            retries = 3
            backoff = 2.0
            last_err = None
            for attempt in range(retries):
                try:
                    response = self.client.models.generate_content(
                        model=settings.STRUCTURED_MODEL,
                        contents=prompt,
                        config=config
                    )
                    raw_text = (response.text or "").strip()
                    # Clean any accidental markdown code fences
                    if raw_text.startswith("```json"):
                        raw_text = raw_text[7:]
                    if raw_text.startswith("```"):
                        raw_text = raw_text[3:]
                    if raw_text.endswith("```"):
                        raw_text = raw_text[:-3]
                    return json.loads(raw_text.strip())
                except Exception as e:
                    last_err = e
                    logger.warning(f"Gemini structured call attempt {attempt+1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(backoff)
                        backoff *= 2.0
            raise last_err or RuntimeError("Gemini structured call failed after retries")

        return await asyncio.to_thread(_call)

    async def generate_image(
        self,
        prompt: str,
        output_path: str
    ) -> Dict[str, Any]:
        def _call():
            try:
                response = self.client.models.generate_images(
                    model=settings.IMAGE_MODEL,
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                    )
                )
                if response.generated_images and len(response.generated_images) > 0:
                    img = response.generated_images[0].image
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    try:
                        img.save(output_path)
                    except AttributeError:
                        raw_bytes = getattr(img, "image_bytes", None) or getattr(img, "_image_bytes", None)
                        if raw_bytes:
                            with open(output_path, "wb") as f:
                                f.write(raw_bytes)
                        else:
                            raise ValueError("No image bytes found in response")
                    return {"success": True, "path": output_path, "prompt": prompt}
                return {"success": False, "path": None, "prompt": prompt, "error": "No images returned"}
            except Exception as e:
                logger.warning(f"Imagen 3 generation failed for prompt: {prompt[:60]}... Error: {e}")
                return {"success": False, "path": None, "prompt": prompt, "error": str(e)}

        return await asyncio.to_thread(_call)
