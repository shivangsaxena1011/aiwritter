import os
import json
import time
import asyncio
import logging
from typing import Optional, Dict, Any, List
from google import genai
from google.genai import types
from backend.app.core.config import settings
from backend.app.services.ai.base import AIProvider

logger = logging.getLogger(__name__)

class GeminiProvider(AIProvider):
    def __init__(self, api_key: str, backup_keys: Optional[List[str]] = None):
        self.keys: List[str] = [api_key]
        if backup_keys:
            for k in backup_keys:
                if k and k not in self.keys:
                    self.keys.append(k)
        self.current_key_idx = 0
        self.api_key = self.keys[0]
        self._clients: Dict[str, genai.Client] = {}

    def _get_client(self, key: str) -> genai.Client:
        if key not in self._clients:
            self._clients[key] = genai.Client(api_key=key)
        return self._clients[key]

    @property
    def client(self) -> genai.Client:
        return self._get_client(self.keys[self.current_key_idx])

    def _rotate_key(self, reason: str = "") -> bool:
        if len(self.keys) > 1:
            old_idx = self.current_key_idx
            self.current_key_idx = (self.current_key_idx + 1) % len(self.keys)
            self.api_key = self.keys[self.current_key_idx]
            logger.warning(
                f"Rotating Gemini API Key (Key {old_idx + 1}/{len(self.keys)} -> {self.current_key_idx + 1}/{len(self.keys)}). Reason: {reason}"
            )
            return True
        return False

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
            retries = max(len(self.keys) * 2, 4)
            backoff = 1.5
            last_err = None
            models = [settings.effective_text_model]
            for alt in ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-2.0-flash"]:
                if alt not in models:
                    models.append(alt)

            for attempt in range(retries):
                model_name = models[0]
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
                        contents=prompt,
                        config=config
                    )
                    return response.text or ""
                except Exception as e:
                    last_err = e
                    err_str = str(e)
                    logger.warning(f"Gemini API call attempt {attempt+1} failed: {e}")
                    if "404" in err_str and len(models) > 1:
                        deprecated_m = models.pop(0)
                        logger.warning(f"Model {deprecated_m} unavailable, falling back to {models[0]}")
                    elif any(kw in err_str for kw in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]):
                        self._rotate_key(err_str[:120])
                    if attempt < retries - 1:
                        time.sleep(backoff)
                        backoff = min(backoff * 1.5, 10.0)
            raise last_err or RuntimeError("Gemini text generation failed after retries")

        return await asyncio.wait_for(asyncio.to_thread(_call), timeout=settings.AI_TIMEOUT_SECONDS)

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
            retries = max(len(self.keys) * 2, 4)
            backoff = 1.5
            last_err = None
            models = [settings.effective_text_model]
            for alt in ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-2.0-flash"]:
                if alt not in models:
                    models.append(alt)

            for attempt in range(retries):
                model_name = models[0]
                try:
                    response = self.client.models.generate_content(
                        model=model_name,
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
                    err_str = str(e)
                    logger.warning(f"Gemini structured call attempt {attempt+1} failed: {e}")
                    if "404" in err_str and len(models) > 1:
                        deprecated_m = models.pop(0)
                        logger.warning(f"Model {deprecated_m} unavailable, falling back to {models[0]}")
                    elif any(kw in err_str for kw in ["429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE"]):
                        self._rotate_key(err_str[:120])
                    if attempt < retries - 1:
                        time.sleep(backoff)
                        backoff = min(backoff * 1.5, 10.0)
            raise last_err or RuntimeError("Gemini structured call failed after retries")

        return await asyncio.wait_for(asyncio.to_thread(_call), timeout=settings.AI_TIMEOUT_SECONDS)

    async def generate_image(
        self,
        prompt: str,
        output_path: str
    ) -> Dict[str, Any]:
        def _call():
            retries = max(len(self.keys), 2)
            for attempt in range(retries):
                try:
                    response = self.client.models.generate_images(
                        model=settings.effective_image_model,
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
                    err_str = str(e)
                    logger.warning(f"Imagen 3 attempt {attempt+1} failed: {e}")
                    if any(kw in err_str for kw in ["429", "RESOURCE_EXHAUSTED"]):
                        self._rotate_key(err_str[:120])
                    if attempt == retries - 1:
                        return {"success": False, "path": None, "prompt": prompt, "error": str(e)}

        return await asyncio.wait_for(asyncio.to_thread(_call), timeout=settings.AI_TIMEOUT_SECONDS)
