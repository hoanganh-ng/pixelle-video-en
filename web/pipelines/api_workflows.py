"""Helpers for exposing direct API media models in Streamlit pipeline UIs."""

import os
from typing import Any

import streamlit as st
from loguru import logger

from web.i18n import get_language


def is_api_workflow(workflow_key: str | None) -> bool:
    """Return True for direct provider workflow keys such as api/dashscope/xxx."""
    return bool(workflow_key and workflow_key.startswith("api/"))


def is_source_workflow(workflow: dict, source: str) -> bool:
    """Return True when a workflow belongs to a concrete source namespace."""
    key = workflow.get("key") or workflow.get("path") or ""
    return key.startswith(f"{source}/") or workflow.get("source") == source


def workflow_source_label(source: str) -> str:
    """Human-facing label for workflow source selectors."""
    zh = get_language() == "zh_CN"
    labels = {
        "selfhost": "Local ComfyUI" if zh else "Local ComfyUI",
        "runninghub": "RunningHub",
        "api": "API models" if zh else "API models",
    }
    return labels.get(source, source)


def workflow_source_help(subject: str | None = None) -> str:
    """Common help text for workflow/model source selectors."""
    zh = get_language() == "zh_CN"
    subject_text = subject or ("this step" if zh else "this step")
    if zh:
        return (
            f"Choose the model service source for {subject_text}: "
            "RunningHub uses cloud workflows; Local ComfyUI uses selfhost workflows; "
            "API call directly requests model providers. The list below only shows workflows or models from the selected source."
        )
    return (
        f"Choose the model service source for {subject_text}: "
        "RunningHub uses cloud workflows; Local ComfyUI uses selfhost workflows; "
        "API call directly requests model providers. The list below only shows workflows or models from the selected source."
    )


def workflow_select_help() -> str:
    """Common help text for workflow/model select boxes."""
    if get_language() == "zh_CN":
        return "Only workflows or models from the selected model service source are shown here."
    return "Only workflows or models from the selected model service source are shown here."


def list_local_media_workflows(
    pixelle_video: Any,
    media_type: str,
    source: str,
    key_contains: str | None = None,
    key_prefix: str | None = None,
) -> list[dict]:
    """List non-API media workflows by source without mixing provider models."""
    try:
        workflows = []
        seen_keys = set()
        for workflow in pixelle_video.media.list_workflows():
            key = workflow.get("key") or workflow.get("path") or ""
            if not key or key.startswith("api/"):
                continue
            if not is_source_workflow(workflow, source):
                continue
            if key_contains and key_contains.lower() not in key.lower():
                continue
            if key_prefix:
                fname = os.path.basename(key)
                if not fname.startswith(key_prefix):
                    continue
            workflow_media_type = workflow.get("media_type")
            if media_type == "video":
                if workflow_media_type and workflow_media_type != "video":
                    continue
                if not workflow_media_type and "video_" not in key.lower() and not (key_prefix and os.path.basename(key).startswith(key_prefix)):
                    continue
            elif workflow_media_type and workflow_media_type != media_type:
                continue
            elif media_type == "image" and "video_" in key.lower():
                continue
            seen_keys.add(key)
            workflows.append({
                "key": key,
                "display_name": workflow.get("display_name") or key,
                **workflow,
            })

        if key_prefix:
            try:
                from pixelle_video.utils.os_util import get_resource_path, list_resource_files

                for filename in list_resource_files("workflows", source):
                    if not filename.startswith(key_prefix) or not filename.endswith(".json"):
                        continue
                    key = f"{source}/{filename}"
                    if key in seen_keys:
                        continue
                    seen_keys.add(key)
                    workflows.append({
                        "key": key,
                        "name": filename,
                        "display_name": f"{filename} - {source.title()}",
                        "source": source,
                        "path": get_resource_path("workflows", source, filename),
                        "media_type": media_type,
                    })
            except Exception as exc:
                logger.warning(f"Failed to list {source}/{key_prefix} workflows from files: {exc}")
        return workflows
    except Exception as exc:
        logger.warning(f"Failed to list {source} {media_type} workflows: {exc}")
        return []


def list_api_media_workflows(
    pixelle_video: Any,
    media_type: str,
    required_adapter_abilities: list[str] | tuple[str, ...] | set[str] | None = None,
    verified_only: bool = False,
) -> list[dict]:
    """List API-backed media workflows in the same option shape used by UIs."""
    api_media = getattr(pixelle_video, "api_media", None)
    if api_media is None:
        return []

    required = set(required_adapter_abilities or [])

    try:
        workflows = []
        for workflow in api_media.list_workflows():
            if workflow.get("media_type") != media_type:
                continue

            if verified_only and not workflow.get("api_contract_verified", True):
                continue

            adapter_abilities = set(workflow.get("adapter_ability_types") or [])
            if required and not required.intersection(adapter_abilities):
                continue

            workflows.append({
                "key": workflow["key"],
                "display_name": workflow.get("display_name") or workflow["key"],
                **workflow,
            })

        return workflows
    except Exception as exc:
        logger.warning(f"Failed to list API {media_type} workflows: {exc}")
        return []


def render_api_video_controls(
    workflow: dict | None,
    key_prefix: str,
    default_duration: int = 5,
    allow_audio_driven: bool = False,
    show_duration: bool = True,
    default_ratio: str | None = None,
) -> dict:
    """Render common API video controls based on verified adapter capability metadata."""
    if not workflow or not is_api_workflow(workflow.get("key")):
        return {}

    zh = get_language() == "zh_CN"
    capabilities = workflow.get("capabilities") or {}
    adapter_abilities = set(workflow.get("adapter_ability_types") or [])
    params: dict[str, Any] = {}

    title = "API video model options" if zh else "API video model options"
    with st.expander(title, expanded=False):
        ability_text = ", ".join(sorted(adapter_abilities)) or ("unknown" if zh else "unknown")
        st.caption(("Adapter abilities: " if zh else "Adapter abilities: ") + ability_text)

        if not workflow.get("api_contract_verified", False):
            st.warning(
                "This model's public API contract is not fully verified; only basic image-to-video parameters will be passed."
                if zh
                else "This model's public API contract is not fully verified; only basic image-to-video parameters will be passed."
            )

        duration_contract = capabilities.get("duration") or {}
        min_duration = int(duration_contract.get("min", 3))
        max_duration = int(duration_contract.get("max", 15))
        if show_duration:
            default_value = min(max(int(default_duration or min_duration), min_duration), max_duration)
            params["duration"] = st.slider(
                "Duration (seconds)" if zh else "Duration (seconds)",
                min_value=min_duration,
                max_value=max_duration,
                value=default_value,
                step=1,
                key=f"{key_prefix}_api_duration",
            )
        else:
            st.caption(
                f"Duration follows each scene's narration audio and is clamped to the model range {min_duration}-{max_duration}s."
                if zh
                else f"Duration follows each scene's narration audio and is clamped to the model range {min_duration}-{max_duration}s."
            )

        resolutions = capabilities.get("resolutions") or []
        if resolutions:
            params["resolution"] = st.selectbox(
                "Resolution" if zh else "Resolution",
                resolutions,
                index=0,
                key=f"{key_prefix}_api_resolution",
            )

        ratios = capabilities.get("ratios") or []
        if ratios:
            preferred_ratio = default_ratio or "9:16"
            default_ratio_index = ratios.index(preferred_ratio) if preferred_ratio in ratios else 0
            params["video_ratio"] = st.selectbox(
                "Aspect ratio" if zh else "Aspect ratio",
                ratios,
                index=default_ratio_index,
                key=f"{key_prefix}_api_ratio",
            )

        negative_prompt = st.text_area(
            "Negative prompt (optional)" if zh else "Negative prompt (optional)",
            value="",
            height=70,
            key=f"{key_prefix}_api_negative_prompt",
        )
        if negative_prompt.strip():
            params["negative_prompt"] = negative_prompt.strip()

        if workflow.get("api_contract_verified", False):
            params["watermark"] = st.checkbox(
                "Add watermark" if zh else "Add watermark",
                value=False,
                key=f"{key_prefix}_api_watermark",
            )

        if workflow.get("provider") == "seedance" and workflow.get("api_contract_verified", False):
            params["generate_audio"] = st.checkbox(
                "Generate native audio" if zh else "Generate native audio",
                value=False,
                key=f"{key_prefix}_api_generate_audio",
            )

        if workflow.get("provider") == "kling" and workflow.get("api_contract_verified", False):
            params["sound"] = "on" if st.checkbox(
                "Generate native audio" if zh else "Generate native audio",
                value=False,
                key=f"{key_prefix}_api_kling_sound",
            ) else "off"

        if allow_audio_driven and "audio_driven_i2v" in adapter_abilities:
            params["use_narration_audio_as_driving_audio"] = st.checkbox(
                "Use narration audio as driving audio" if zh else "Use narration audio as driving audio",
                value=False,
                help=(
                    "Only applies to verified API models that support driving_audio."
                    if zh
                    else "Only applies to verified API models that support driving_audio."
                ),
                key=f"{key_prefix}_api_audio_driven",
            )

    return {key: value for key, value in params.items() if value not in (None, "")}
