# -*- coding: utf-8 -*-
"""
Qwen3.5-VL multimodal LLM API client (DashScope multimodal interface only).
Supports Qwen3.5-VL and any DashScope multimodal-compatible chat interface.
See official docs: https://help.aliyun.com/zh/model-studio/qwen-api-reference
"""

import os

try:
    import dashscope
    from dashscope import MultiModalConversation
except ImportError:
    dashscope = None
    MultiModalConversation = None
import logging

logger = logging.getLogger(__name__)
from typing import Any, Dict, List, Optional

class QwenVLClient:
    def __init__(self,
                 api_key: Optional[str] = None, 
                 base_url: Optional[str] = None):
        """
        Qwen3.5-VL multimodal client.
        :param api_key: DashScope / Qwen3.5 API Key.
        :param model: Model name (e.g., qwen3.5-plus / qwen3.5-max).
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")

    def chat(
        self,
        text: str,
        images: List[str],
        model: str,
        stream: bool = False,
        parameters: Optional[Dict] = None,
        videos: Optional[List[str]] = None,
        **kwargs
    ) -> Any:
        """
        Use the Alibaba Cloud dashscope SDK for multimodal chat (text + image/video), mirroring the style of image_dashscope.py.
        :param text: Text content.
        :param images: Image path list (local paths or URLs, internally converted to absolute file:// paths).
        :param videos: Video path list (local paths or URLs, internally converted to absolute file:// paths).
        :param model: Model name (supports qwen3.5-plus, qwen3-vl-plus).
        :param stream: Whether to stream output (streaming is not supported yet).
        :param parameters: Other API parameters.
        :return: API response content as a dict.
        """
        if dashscope is None or MultiModalConversation is None:
            raise RuntimeError("dashscope package not installed. Run: pip install dashscope")

        dashscope.api_key = self.api_key
        # Only non-streaming is supported.
        try:
            content = [
                {"text": text},
                *({"image": p} for p in images),
                *({"video": p} for p in videos or []),
            ]
            messages = [{"role": "user", "content": content}]
            response = MultiModalConversation.call(
                model=model,
                messages=messages,
                api_key=self.api_key,
                enable_thinking=False,
                **(parameters or {})
            )
            if hasattr(response, 'status_code') and response.status_code == 200:
                # qwen3.5-plus returns { choices: [ { message: { content: [...] } } ] }.
                resp = response.output.choices[0].message.content[0]
                if resp.get('text'):
                    return resp['text']
                return resp
            else:
                raise RuntimeError(f"DashScope QwenVLClient failed: {getattr(response, 'message', response)}")
        except Exception as e:
            raise RuntimeError(f"DashScope QwenVLClient error: {e}")


if __name__ == "__main__":
    import sys
    import time
    import json
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import Config

    # Supported VLM model list.
    MODELS = ["qwen3.6-plus", "qwen3.6-flash", "kimi-k2.6"]

    print("=== Qwen VL (DashScope) Multimodal Availability Test ===")
    api_key = getattr(Config, "DASHSCOPE_API_KEY", None) or os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        print("✗ DASHSCOPE_API_KEY not set, skipping")
        sys.exit(1)
    print(f"  API Key: {api_key[:6]}***{api_key[-4:]}")
    client = QwenVLClient(api_key=api_key)

    # Test image.
    img_path = ''
    abs_img_path = os.path.abspath(img_path)
    if not os.path.exists(img_path):
        img_path = "code/result/image/test_avail/test_input.png"
        abs_img_path = os.path.abspath(img_path)
        if not os.path.exists(img_path):
            print("✗ Test image not found, skipping")
            sys.exit(0)

    text = "Please describe the contents of this image."
    print(f"\n[Multimodal] Prompt: {text}")
    print(f"  Image: {img_path}")

    for model in MODELS:
        print(f"\n--- Test model: {model} ---")
        t0 = time.time()
        try:
            result = client.chat(text=text, images=[img_path], model=model, stream=False)
            elapsed = time.time() - t0
            if result:
                print(f"✓ Returned result ({elapsed:.1f}s): {str(result)[:200]}")
            else:
                print(f"✗ Returned empty result ({elapsed:.1f}s)")
        except Exception as e:
            print(f"✗ Failed: {e}")
