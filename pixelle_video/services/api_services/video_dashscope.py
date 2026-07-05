"""
Tongyi Wan (Wan) video generation client
Built on the DashScope SDK (dashscope.VideoSynthesis)
Supports image-to-video generation for wan2.7-i2v, wan2.6-i2v-flash, etc.
"""

import os
import logging
import time
import threading
from contextlib import contextmanager
from typing import Optional
from http import HTTPStatus

try:
    import dashscope
    from dashscope import VideoSynthesis
except ImportError:
    dashscope = None
    VideoSynthesis = None
import requests
from requests import exceptions as requests_exceptions

logger = logging.getLogger(__name__)


class DashscopeVideoClient:
    """
    Alibaba Cloud Tongyi Wan video generation client.
    Uses the dashscope SDK's VideoSynthesis interface.
    """

    _proxy_env_lock = threading.Lock()

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        local_proxy: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        self.base_url = base_url or os.getenv("DASHSCOPE_BASE_URL")
        self.local_proxy = local_proxy

        if dashscope and self.api_key:
            dashscope.api_key = self.api_key
        if dashscope and self.base_url:
            dashscope.base_http_api_url = self.base_url

    @contextmanager
    def _proxy_env(self):
        if not self.local_proxy:
            yield
            return

        with self._proxy_env_lock:
            keys = ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy")
            old_values = {key: os.environ.get(key) for key in keys}
            try:
                for key in keys:
                    os.environ[key] = self.local_proxy
                yield
            finally:
                for key, value in old_values.items():
                    if value is None:
                        os.environ.pop(key, None)
                    else:
                        os.environ[key] = value

    _RETRYABLE_EXCEPTIONS = (
        requests_exceptions.ConnectionError,
        requests_exceptions.Timeout,
        requests_exceptions.SSLError,
        requests_exceptions.ChunkedEncodingError,
        requests_exceptions.ContentDecodingError,
        TimeoutError,
        ConnectionError,
    )

    def _with_network_retry(self, action_name: str, func, max_attempts: int = 5, base_delay: float = 3.0):
        """Retry transient network failures without hiding provider-side task failures."""
        last_error = None
        for attempt in range(1, max_attempts + 1):
            try:
                with self._proxy_env():
                    return func()
            except self._RETRYABLE_EXCEPTIONS as exc:
                last_error = exc
            except Exception as exc:
                if not self._is_retryable_error(exc):
                    raise
                last_error = exc

            if attempt >= max_attempts:
                break
            delay = min(base_delay * attempt, 20)
            logger.warning(
                "DashscopeVideoClient: %s network error, retrying %s/%s in %.1fs: %s",
                action_name,
                attempt,
                max_attempts,
                delay,
                last_error,
            )
            time.sleep(delay)

        raise RuntimeError(
            f"DashScope {action_name} failed after {max_attempts} attempts due to network error: {last_error}"
        ) from last_error

    def _is_retryable_error(self, exc: Exception) -> bool:
        message = str(exc).lower()
        retry_markers = (
            "ssleoferror",
            "unexpected_eof",
            "eof occurred in violation of protocol",
            "connection reset",
            "connection aborted",
            "remote disconnected",
            "max retries exceeded",
            "read timed out",
            "connect timed out",
            "temporarily unavailable",
        )
        return any(marker in message for marker in retry_markers)

    def generate_video(
        self,
        prompt: str,
        image_path: Optional[str],
        save_path: str,
        model: str = "wan2.7-i2v",
        duration: int = 10,
        shot_type: str = "multi",
        video_ratio: Optional[str] = None,
        last_image_path: Optional[str] = None,
        first_clip_path: Optional[str] = None,
        reference_image_path: Optional[str] = None,
        reference_image_paths: Optional[list[str]] = None,
        reference_video_paths: Optional[list[str]] = None,
        reference_audio_path: Optional[str] = None,
        audio_path: Optional[str] = None,
        negative_prompt: Optional[str] = None,
        resolution: Optional[str] = None,
        prompt_extend: Optional[bool] = None,
        watermark: bool = False,
        seed: Optional[int] = None,
        audio: Optional[bool] = None,
    ) -> str:
        """
        Image-to-video: submit task -> wait for completion -> download to local.

        Args:
            prompt: Text prompt describing the video.
            image_path: Local path of the input first-frame image.
            save_path: Output video save path.
            model: Wan video model name.
            duration: Video duration in seconds.
            shot_type: Shot type, "single" or "multi".
            video_ratio: Output aspect ratio, e.g., 9:16 / 16:9.
            last_image_path: Optional last-frame image path (wan2.7).
            first_clip_path: Optional first-clip video path (wan2.7 video continuation).
            reference_image_path: Optional reference image path (videoedit).
            reference_image_paths: Optional list of reference images (r2v).
            reference_video_paths: Optional list of reference videos (r2v).
            reference_audio_path: Optional reference audio/voice path (r2v).
            audio_path: Optional driving audio path (wan2.7).

        Returns:
            video_url: Remote video URL.

        Raises:
            FileNotFoundError: Raised when the input image does not exist.
            RuntimeError: Raised when the API call or download fails.
        """
        if VideoSynthesis is None:
            raise RuntimeError("dashscope package not installed. Run: pip install dashscope")

        if image_path and not os.path.exists(image_path):
            raise FileNotFoundError(f"Input image not found: {image_path}")
        if last_image_path and not os.path.exists(last_image_path):
            raise FileNotFoundError(f"Last-frame image not found: {last_image_path}")
        if first_clip_path and not os.path.exists(first_clip_path):
            raise FileNotFoundError(f"Input video clip not found: {first_clip_path}")
        if reference_image_path and not os.path.exists(reference_image_path):
            raise FileNotFoundError(f"Reference image not found: {reference_image_path}")
        for ref_image_path in reference_image_paths or []:
            if ref_image_path and not os.path.exists(ref_image_path):
                raise FileNotFoundError(f"Reference image not found: {ref_image_path}")
        for ref_video_path in reference_video_paths or []:
            if ref_video_path and not os.path.exists(ref_video_path):
                raise FileNotFoundError(f"Reference video not found: {ref_video_path}")
        if reference_audio_path and not os.path.exists(reference_audio_path):
            raise FileNotFoundError(f"Reference audio not found: {reference_audio_path}")
        if audio_path and not os.path.exists(audio_path):
            raise FileNotFoundError(f"Driving audio not found: {audio_path}")

        logger.info(f"DashscopeVideoClient: model={model}, prompt={prompt[:60]}...")

        if self._is_text_to_video_model(model):
            call_kwargs = {
                "api_key": self.api_key,
                "model": model,
                "prompt": prompt,
                "duration": duration,
                "watermark": watermark,
            }
            if negative_prompt:
                call_kwargs["negative_prompt"] = negative_prompt
            if resolution:
                call_kwargs["resolution"] = resolution
            if video_ratio:
                call_kwargs["ratio"] = video_ratio
            if prompt_extend is not None:
                call_kwargs["prompt_extend"] = prompt_extend
            if seed is not None:
                call_kwargs["seed"] = seed
            if audio is not None:
                call_kwargs["audio"] = audio

            rsp = self._with_network_retry(
                "submit task",
                lambda: VideoSynthesis.call(**call_kwargs),
            )
        elif self._is_reference_to_video_model(model):
            media = self._build_reference_to_video_media(
                image_path=image_path,
                reference_image_path=reference_image_path,
                reference_image_paths=reference_image_paths,
                reference_video_paths=reference_video_paths,
                reference_audio_path=None if "happyhorse" in model.lower() else reference_audio_path,
            )
            if not media:
                raise ValueError("DashScope reference-to-video models require at least one reference_image or reference_video input.")

            call_kwargs = {
                "api_key": self.api_key,
                "model": model,
                "prompt": prompt,
                "media": media,
                "duration": duration,
                "watermark": watermark,
            }
            if audio is not None:
                call_kwargs["audio"] = audio
            if negative_prompt:
                call_kwargs["negative_prompt"] = negative_prompt
            if resolution:
                call_kwargs["resolution"] = resolution
            if video_ratio:
                call_kwargs["ratio"] = video_ratio
            if prompt_extend is not None:
                call_kwargs["prompt_extend"] = prompt_extend
            if seed is not None:
                call_kwargs["seed"] = seed

            rsp = self._with_network_retry(
                "submit task",
                lambda: VideoSynthesis.call(**call_kwargs),
            )
        elif self._is_video_edit_model(model):
            media = self._build_video_edit_media(
                video_path=first_clip_path,
                reference_image_path=reference_image_path or last_image_path or image_path,
            )
            if not media:
                raise ValueError("DashScope video edit models require video input and may use reference_image input.")

            call_kwargs = {
                "api_key": self.api_key,
                "model": model,
                "prompt": prompt,
                "media": media,
                "duration": duration,
                "watermark": watermark,
            }
            if negative_prompt:
                call_kwargs["negative_prompt"] = negative_prompt
            if resolution:
                call_kwargs["resolution"] = resolution
            if video_ratio:
                call_kwargs["ratio"] = video_ratio
            if prompt_extend is not None:
                call_kwargs["prompt_extend"] = prompt_extend
            if seed is not None:
                call_kwargs["seed"] = seed

            rsp = self._with_network_retry(
                "submit task",
                lambda: VideoSynthesis.call(**call_kwargs),
            )
        elif model.startswith("wan2.7") or "happyhorse" in model:
            # wan2.7 series use the new API format with 'media'
            media = self._build_media(
                image_path=image_path,
                last_image_path=last_image_path,
                first_clip_path=first_clip_path,
                audio_path=audio_path,
            )
            if not media:
                raise ValueError("DashScope wan2.7 video generation requires first_frame or first_clip input.")
            self._validate_media_combination(media)

            call_kwargs = {
                "api_key": self.api_key,
                "model": model,
                "prompt": prompt,
                "media": media,
                "duration": duration,
                "watermark": watermark,
            }
            if negative_prompt:
                call_kwargs["negative_prompt"] = negative_prompt
            if resolution:
                call_kwargs["resolution"] = resolution
            if video_ratio:
                call_kwargs["ratio"] = video_ratio
            if prompt_extend is not None:
                call_kwargs["prompt_extend"] = prompt_extend
            if seed is not None:
                call_kwargs["seed"] = seed

            rsp = self._with_network_retry(
                "submit task",
                lambda: VideoSynthesis.call(**call_kwargs),
            )
        else:
            # Older models (wan2.1, wan2.6 etc.) use 'img_url' and 'shot_type'
            if not image_path:
                raise ValueError("DashScope legacy video models require image_path.")

            call_kwargs = {
                "api_key": self.api_key,
                "model": model,
                "prompt": prompt,
                "img_url": self._to_media_url(image_path),
                "duration": duration,
                "shot_type": shot_type,
            }
            if negative_prompt:
                call_kwargs["negative_prompt"] = negative_prompt
            if resolution:
                call_kwargs["resolution"] = resolution
            if video_ratio:
                call_kwargs["ratio"] = video_ratio
            if prompt_extend is not None:
                call_kwargs["prompt_extend"] = prompt_extend
            if watermark is not None:
                call_kwargs["watermark"] = watermark
            if seed is not None:
                call_kwargs["seed"] = seed

            rsp = self._with_network_retry(
                "submit task",
                lambda: VideoSynthesis.call(**call_kwargs),
            )

        if rsp.status_code != HTTPStatus.OK:
            raise RuntimeError(
                f"Wan video API error: status={rsp.status_code}, "
                f"code={rsp.code}, message={rsp.message}"
            )

        video_url = self._extract_video_url(rsp)
        if not video_url:
            task_id = self._extract_task_id(rsp)
            task_status = self._extract_task_status(rsp)
            if not task_id:
                raise RuntimeError(
                    "Wan video API did not return video_url or task_id; cannot query the result: "
                    f"status={rsp.status_code}, code={rsp.code}, message={rsp.message}, "
                    f"task_status={task_status}"
                )

            logger.info(f"DashscopeVideoClient: task submitted task_id={task_id}, status={task_status}; waiting for completion...")
            rsp = self._with_network_retry(
                f"wait task {task_id}",
                lambda: VideoSynthesis.wait(task=rsp, api_key=self.api_key),
                max_attempts=8,
                base_delay=5.0,
            )
            if rsp.status_code != HTTPStatus.OK:
                raise RuntimeError(
                    f"Wan video task query failed: status={rsp.status_code}, "
                    f"code={rsp.code}, message={rsp.message}, task_id={task_id}"
                )

            video_url = self._extract_video_url(rsp)
            task_status = self._extract_task_status(rsp)
            if not video_url:
                raise RuntimeError(
                    "Wan video task completed but no video_url was returned: "
                    f"code={rsp.code}, message={rsp.message}, task_id={task_id}, task_status={task_status}, "
                    f"output={self._safe_output_repr(rsp)}"
                )

        logger.info(f"DashscopeVideoClient: video generated successfully: {video_url}")

        # Ensure the output directory exists.
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Download the video.
        resp = self._with_network_retry(
            "download video",
            lambda: requests.get(
                video_url,
                stream=True,
                timeout=120,
                proxies={"http": self.local_proxy, "https": self.local_proxy} if self.local_proxy else None,
            ),
            max_attempts=5,
            base_delay=3.0,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"Video download failed: HTTP {resp.status_code}")

        with open(save_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        logger.info(f"DashscopeVideoClient: video saved to: {save_path}")
        return video_url

    def _is_video_edit_model(self, model: str) -> bool:
        """Return True for DashScope video-edit model IDs."""
        model_lower = model.lower()
        return "videoedit" in model_lower or "video-edit" in model_lower

    def _is_reference_to_video_model(self, model: str) -> bool:
        """Return True for DashScope reference-to-video model IDs."""
        return "r2v" in model.lower()

    def _is_text_to_video_model(self, model: str) -> bool:
        """Return True for DashScope text-to-video model IDs."""
        return "t2v" in model.lower()

    def _extract_video_url(self, rsp) -> Optional[str]:
        """Extract video_url from DashScope SDK response variants."""
        output = getattr(rsp, "output", None)
        if output is None:
            return None
        if isinstance(output, dict):
            return output.get("video_url")
        return getattr(output, "video_url", None)

    def _extract_task_id(self, rsp) -> Optional[str]:
        """Extract async task_id from DashScope SDK response variants."""
        output = getattr(rsp, "output", None)
        if output is None:
            return None
        if isinstance(output, dict):
            return output.get("task_id")
        return getattr(output, "task_id", None)

    def _extract_task_status(self, rsp) -> Optional[str]:
        """Extract async task status from DashScope SDK response variants."""
        output = getattr(rsp, "output", None)
        if output is None:
            return None
        if isinstance(output, dict):
            return output.get("task_status")
        return getattr(output, "task_status", None)

    def _safe_output_repr(self, rsp) -> str:
        """Best-effort output representation for provider-side task failures."""
        output = getattr(rsp, "output", None)
        try:
            if isinstance(output, dict):
                return str(output)
            if hasattr(output, "__dict__"):
                return str(output.__dict__)
            return str(output)
        except Exception:
            return "<unprintable output>"

    def _build_media(
        self,
        image_path: Optional[str],
        last_image_path: Optional[str],
        first_clip_path: Optional[str],
        audio_path: Optional[str],
    ) -> list[dict[str, str]]:
        """Build DashScope wan2.7 media array using official media types."""
        media = []
        if first_clip_path:
            media.append({"type": "first_clip", "url": self._to_media_url(first_clip_path)})
        elif image_path:
            media.append({"type": "first_frame", "url": self._to_media_url(image_path)})

        if last_image_path:
            media.append({"type": "last_frame", "url": self._to_media_url(last_image_path)})
        if audio_path:
            media.append({"type": "driving_audio", "url": self._to_media_url(audio_path)})
        return media

    def _build_video_edit_media(
        self,
        video_path: Optional[str],
        reference_image_path: Optional[str],
    ) -> list[dict[str, str]]:
        """Build DashScope video-edit media array using official media types."""
        media = []
        if video_path:
            media.append({"type": "video", "url": self._to_media_url(video_path)})
        if reference_image_path:
            media.append({"type": "reference_image", "url": self._to_media_url(reference_image_path)})
        return media

    def _build_reference_to_video_media(
        self,
        image_path: Optional[str],
        reference_image_path: Optional[str],
        reference_image_paths: Optional[list[str]],
        reference_video_paths: Optional[list[str]],
        reference_audio_path: Optional[str],
    ) -> list[dict[str, str]]:
        """Build DashScope r2v media array using reference_image/reference_video items."""
        media = []
        image_refs = []
        if reference_image_paths:
            image_refs.extend(reference_image_paths)
        if reference_image_path:
            image_refs.append(reference_image_path)
        if image_path:
            image_refs.append(image_path)

        seen = set()
        for index, ref_path in enumerate(image_refs):
            if not ref_path or ref_path in seen:
                continue
            seen.add(ref_path)
            item = {"type": "reference_image", "url": self._to_media_url(ref_path)}
            if index == 0 and reference_audio_path:
                item["reference_voice"] = self._to_media_url(reference_audio_path)
            media.append(item)

        for ref_video_path in reference_video_paths or []:
            if ref_video_path:
                media.append({"type": "reference_video", "url": self._to_media_url(ref_video_path)})

        return media

    def _validate_media_combination(self, media: list[dict[str, str]]) -> None:
        """Validate combinations documented by DashScope wan2.7 i2v."""
        media_types = {item["type"] for item in media}
        allowed = [
            {"first_frame"},
            {"first_frame", "driving_audio"},
            {"first_frame", "last_frame"},
            {"first_frame", "last_frame", "driving_audio"},
            {"first_clip"},
            {"first_clip", "last_frame"},
        ]
        if media_types not in allowed:
            raise ValueError(
                "Invalid DashScope media combination: "
                f"{'+'.join(sorted(media_types))}. "
                "Allowed: first_frame, first_frame+driving_audio, first_frame+last_frame, "
                "first_frame+last_frame+driving_audio, first_clip, first_clip+last_frame."
            )

    def _to_media_url(self, path_or_url: str) -> str:
        """Convert a local path to file:// while preserving URL/data/OSS inputs."""
        if path_or_url.startswith(("http://", "https://", "file://", "oss://", "data:")):
            return path_or_url
        return f"file://{os.path.abspath(path_or_url)}"


if __name__ == "__main__":
    import sys
    import time
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import Config

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # -- Test parameters (modify as needed) --
    IMAGE_PATH = "code/result/image/test_avail/test_input_human.jpg"
    OUTPUT_DIR = "code/result/video/test_avail"
    PROMPT = "A woman hands a financial report to a man in an office; the man examines the numbers on the report and breaks into a satisfied smile. Office background, realistic style, high-definition detail. Background music: upbeat electronic track with a strong rhythm, suited to an office environment."
    # MODELS = ["wan2.7-i2v", "wan2.6-i2v-flash", "happyhorse-1.0-i2v"]
    MODELS = ["happyhorse-1.0-i2v"]
    DURATION = 5               # 5 / 10
    SHOT_TYPE = "multi"        # single / multi

    print("=== Dashscope Video Client Availability Test ===")
    ak = Config.DASHSCOPE_API_KEY
    base_url = Config.DASHSCOPE_BASE_URL
    if not ak:
        print("✗ DASHSCOPE_API_KEY not set; please check your .env configuration")
        sys.exit(1)

    if not os.path.exists(IMAGE_PATH):
        print(f"✗ Input image not found: {IMAGE_PATH}")
        sys.exit(1)

    for model in MODELS:
        output_path = os.path.join(OUTPUT_DIR, f"{model}.mp4")
        print(f"\nTest model: {model}")
        print(f"  API Key    : {ak[:6]}***{ak[-4:]}")
        print(f"  Base URL   : {base_url}")
        print(f"  Input image: {IMAGE_PATH}")
        print(f"  Output path: {output_path}")
        print(f"  Model      : {model}")
        print(f"  Duration   : {DURATION}s")
        print(f"  Shot type  : {SHOT_TYPE}")
        if PROMPT:
            print(f"  Prompt     : {PROMPT[:80]}")
        print("-" * 40)

        try:
            client = DashscopeVideoClient(api_key=ak, base_url=base_url)
            print("✓ Client initialized successfully")

            start = time.time()
            video_url = client.generate_video(
                prompt=PROMPT,
                image_path=IMAGE_PATH,
                save_path=output_path,
                model=model,
                duration=DURATION,
                shot_type=SHOT_TYPE,
            )
            elapsed = time.time() - start

            print(f"✓ Video generation completed! Elapsed {elapsed:.1f}s")
            print(f"  Remote URL : {video_url}")
            print(f"  Local file : {os.path.abspath(output_path)}")
            print(f"  File size  : {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")
        except Exception as e:
            print(f"✗ Failed: {e}")
            sys.exit(1)
