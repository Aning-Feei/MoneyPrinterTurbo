from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


COVER_BATCH_VERSION = "runninghub-cover-batch-v1"
COVER_PROVIDER = "runninghub"
COVER_OUTPUT_WIDTH = 1080
COVER_OUTPUT_HEIGHT = 1920
MIN_REQUIRED_IMAGES = 3


class RunningHubCoverConfigurationError(Exception):
    """Raised when RunningHub cover generation is not configured."""


class RunningHubCoverError(Exception):
    """Raised when RunningHub cover generation fails."""


@dataclass(frozen=True)
class RunningHubCoverConfig:
    api_key: str
    workflow_id: str
    image_node_id: str
    title_node_id: str
    image_node_field: str = "image"
    title_node_field: str = "prompt"
    output_node_id: str = ""
    output_node_field: str = "images"
    api_base: str = "https://www.runninghub.ai"
    poll_interval_seconds: float = 3.0
    timeout_seconds: float = 180.0
    node_info_json: str = ""
    upload_endpoint: str = "/task/openapi/upload"
    create_endpoint: str = "/task/openapi/create"
    status_endpoint: str = "/task/openapi/status"
    outputs_endpoint: str = "/task/openapi/outputs"

    @classmethod
    def from_env(cls) -> "RunningHubCoverConfig":
        api_key = os.environ.get("RUNNINGHUB_API_KEY", "").strip()
        workflow_id = os.environ.get("RUNNINGHUB_COVER_WORKFLOW_ID", "").strip()
        image_node_id = os.environ.get("RUNNINGHUB_COVER_IMAGE_NODE_ID", "").strip()
        title_node_id = os.environ.get("RUNNINGHUB_COVER_TITLE_NODE_ID", "").strip()
        node_info_json = os.environ.get("RUNNINGHUB_COVER_NODE_INFO_JSON", "").strip()
        missing = [
            name
            for name, value in (
                ("RUNNINGHUB_API_KEY", api_key),
                ("RUNNINGHUB_COVER_WORKFLOW_ID", workflow_id),
                ("RUNNINGHUB_COVER_IMAGE_NODE_ID", image_node_id or node_info_json),
                ("RUNNINGHUB_COVER_TITLE_NODE_ID", title_node_id or node_info_json),
            )
            if not value
        ]
        if missing:
            raise RunningHubCoverConfigurationError(
                "RunningHub 封面生成配置缺失，请配置 API Key 和 workflow 信息。"
            )

        return cls(
            api_key=api_key,
            workflow_id=workflow_id,
            image_node_id=image_node_id,
            title_node_id=title_node_id,
            image_node_field=os.environ.get(
                "RUNNINGHUB_COVER_IMAGE_NODE_FIELD", "image"
            ).strip()
            or "image",
            title_node_field=os.environ.get(
                "RUNNINGHUB_COVER_TITLE_NODE_FIELD", "prompt"
            ).strip()
            or "prompt",
            output_node_id=os.environ.get("RUNNINGHUB_COVER_OUTPUT_NODE_ID", "").strip(),
            output_node_field=os.environ.get(
                "RUNNINGHUB_COVER_OUTPUT_NODE_FIELD", "images"
            ).strip()
            or "images",
            api_base=os.environ.get("RUNNINGHUB_API_BASE", "https://www.runninghub.ai")
            .strip()
            .rstrip("/"),
            poll_interval_seconds=float(
                os.environ.get("RUNNINGHUB_POLL_INTERVAL_SECONDS", "3") or 3
            ),
            timeout_seconds=float(os.environ.get("RUNNINGHUB_TIMEOUT_SECONDS", "180") or 180),
            node_info_json=node_info_json,
            upload_endpoint=os.environ.get(
                "RUNNINGHUB_COVER_UPLOAD_ENDPOINT", "/task/openapi/upload"
            ).strip(),
            create_endpoint=os.environ.get(
                "RUNNINGHUB_COVER_CREATE_ENDPOINT", "/task/openapi/create"
            ).strip(),
            status_endpoint=os.environ.get(
                "RUNNINGHUB_COVER_STATUS_ENDPOINT", "/task/openapi/status"
            ).strip(),
            outputs_endpoint=os.environ.get(
                "RUNNINGHUB_COVER_OUTPUTS_ENDPOINT", "/task/openapi/outputs"
            ).strip(),
        )


class RunningHubCoverClient:
    def __init__(self, config: RunningHubCoverConfig | None = None):
        self.config = config or RunningHubCoverConfig.from_env()

    def upload_image(self, image_path: str | Path) -> dict[str, Any]:
        path = Path(image_path).expanduser().resolve()
        with path.open("rb") as file:
            response = requests.post(
                self._url(self.config.upload_endpoint),
                headers=self._headers(),
                data={"apiKey": self.config.api_key},
                files={"file": (path.name, file, "application/octet-stream")},
                timeout=30,
            )
        payload = self._json_response(response, "upload image")
        return {
            "upload_ref": extract_upload_ref(payload),
            "raw": payload,
        }

    def submit_cover_task(self, image_ref: str, title_text: str) -> dict[str, Any]:
        payload = {
            "apiKey": self.config.api_key,
            "workflowId": self.config.workflow_id,
            "nodeInfoList": self._node_info_list(image_ref, title_text),
        }
        response = requests.post(
            self._url(self.config.create_endpoint),
            headers=self._headers(),
            json=payload,
            timeout=30,
        )
        data = self._json_response(response, "submit task")
        return {
            "task_id": (
                data.get("taskId")
                or data.get("task_id")
                or data.get("id")
                or (data.get("data") or {}).get("taskId")
                or (data.get("data") or {}).get("task_id")
            ),
            "raw": data,
        }

    def wait_for_task(self, task_id: str) -> dict[str, Any]:
        started = time.monotonic()
        last_payload: dict[str, Any] = {}
        while time.monotonic() - started <= self.config.timeout_seconds:
            response = requests.post(
                self._url(self.config.status_endpoint),
                headers=self._headers(),
                json={"apiKey": self.config.api_key, "taskId": task_id},
                timeout=30,
            )
            payload = self._json_response(response, "poll task")
            last_payload = payload
            status = str(
                payload.get("status")
                or payload.get("taskStatus")
                or (payload.get("data") or {}).get("status")
                or ""
            ).lower()
            if status in {"success", "succeeded", "completed", "finish", "finished"}:
                output = self.get_task_output(task_id)
                return {
                    "status": "succeeded",
                    "remote_result_ref": output.get("remote_result_ref"),
                    "remote_result_url": output.get("remote_result_url"),
                    "raw": {"status": payload, "output": output.get("raw")},
                }
            if status in {"failed", "error", "canceled", "cancelled"}:
                return {"status": "failed", "raw": payload}
            time.sleep(self.config.poll_interval_seconds)
        return {"status": "timeout", "raw": last_payload}

    def get_task_output(self, task_id: str) -> dict[str, Any]:
        response = requests.post(
            self._url(self.config.outputs_endpoint),
            headers=self._headers(),
            json={"apiKey": self.config.api_key, "taskId": task_id},
            timeout=30,
        )
        payload = self._json_response(response, "fetch task output")
        result_url = extract_result_url(payload)
        return {
            "remote_result_ref": safe_remote_ref(result_url or task_id),
            "remote_result_url": safe_remote_url(result_url),
            "raw": payload,
        }

    def download_result_image(self, remote_result: dict[str, Any], output_path: str | Path):
        result_url = remote_result.get("remote_result_url")
        if not result_url:
            raise RunningHubCoverError("RunningHub task did not return a downloadable image URL.")
        response = requests.get(result_url, timeout=60)
        response.raise_for_status()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(response.content)

    def _url(self, endpoint: str) -> str:
        endpoint = str(endpoint or "").strip()
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.config.api_base}/{endpoint.lstrip('/')}"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
        }

    def _node_info_list(self, image_ref: str, title_text: str) -> list[dict[str, Any]]:
        if self.config.node_info_json:
            template = json.loads(self.config.node_info_json)
            if isinstance(template, dict) and "nodeInfoList" in template:
                template = template["nodeInfoList"]
            mapped = replace_node_placeholders(
                template, image_ref=image_ref, title_text=title_text
            )
            if isinstance(mapped, dict):
                mapped = [mapped]
            if not isinstance(mapped, list):
                raise RunningHubCoverConfigurationError(
                    "RunningHub 封面生成配置缺失，请配置 API Key 和 workflow 信息。"
                )
            return mapped
        return [
            {
                "nodeId": self.config.image_node_id,
                "fieldName": self.config.image_node_field,
                "fieldValue": image_ref,
            },
            {
                "nodeId": self.config.title_node_id,
                "fieldName": self.config.title_node_field,
                "fieldValue": title_text,
            },
        ]

    @staticmethod
    def _json_response(response, action: str) -> dict[str, Any]:
        try:
            response.raise_for_status()
            payload = response.json()
        except Exception as exc:
            raise RunningHubCoverError(f"RunningHub {action} failed.") from exc
        if isinstance(payload, dict):
            return payload
        return {"data": payload}


def replace_node_placeholders(value, image_ref: str, title_text: str):
    if isinstance(value, dict):
        return {
            key: replace_node_placeholders(item, image_ref, title_text)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [replace_node_placeholders(item, image_ref, title_text) for item in value]
    if isinstance(value, str):
        return value.replace("{{image}}", image_ref).replace("{{title}}", title_text)
    return value


def extract_upload_ref(payload: dict[str, Any]) -> str:
    candidates: list[Any] = [
        payload.get("fileName"),
        payload.get("file_name"),
        payload.get("file"),
        payload.get("url"),
        payload.get("id"),
    ]
    data = payload.get("data")
    if isinstance(data, dict):
        candidates.extend(
            [
                data.get("fileName"),
                data.get("file_name"),
                data.get("file"),
                data.get("url"),
                data.get("id"),
            ]
        )
    elif isinstance(data, str):
        candidates.append(data)
    for candidate in candidates:
        text = str(candidate or "").strip()
        if text:
            return text
    return ""


def extract_result_url(payload: dict[str, Any]) -> str:
    candidates: list[Any] = []

    def collect(value: Any):
        if isinstance(value, dict):
            for key, item in value.items():
                key_text = str(key).lower()
                if key_text in {
                    "url",
                    "imageurl",
                    "image_url",
                    "fileurl",
                    "file_url",
                    "originfileurl",
                    "origin_file_url",
                    "downloadurl",
                    "download_url",
                }:
                    candidates.append(item)
                collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, str):
            candidates.append(value)

    collect(payload)
    for candidate in candidates:
        candidate_text = str(candidate or "").strip()
        if candidate_text.startswith("http://") or candidate_text.startswith("https://"):
            return candidate_text
    return ""


def safe_remote_ref(value: str) -> str:
    text = str(value or "")
    if not text:
        return ""
    return text.split("?", 1)[0].rsplit("/", 1)[-1][:120]


def safe_remote_url(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    return text.split("?", 1)[0]


def generate_runninghub_cover_batch(
    *,
    theme_text: str,
    titles: list[dict[str, Any]],
    selected_images: list[dict[str, Any]],
    output_dir: str | Path,
    batch_index: int,
    client: Any | None = None,
) -> dict[str, Any]:
    output_path = Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []
    variants: list[dict[str, Any]] = []
    client = client or RunningHubCoverClient()

    if len(selected_images) < MIN_REQUIRED_IMAGES:
        raise RunningHubCoverError("At least 3 uploaded images are required.")
    if len(titles) < 3:
        raise RunningHubCoverError("At least 3 local title candidates are required.")

    for index, (title, image) in enumerate(zip(titles[:3], selected_images[:3]), start=1):
        variant_id = f"cover_{index}"
        local_cover_path = output_path / f"{variant_id}.png"
        task_id = ""
        remote_result_ref = ""
        remote_result_url = ""
        status = "failed"
        output_width = 0
        output_height = 0
        try:
            upload = client.upload_image(image["path"])
            submit = client.submit_cover_task(
                str(upload.get("upload_ref") or ""),
                str(title.get("text") or ""),
            )
            task_id = str(submit.get("task_id") or "")
            if not task_id:
                raise RunningHubCoverError("RunningHub did not return a task id.")
            result = client.wait_for_task(task_id)
            status = str(result.get("status") or "failed")
            remote_result_ref = str(result.get("remote_result_ref") or "")
            remote_result_url = str(result.get("remote_result_url") or "")
            if status != "succeeded":
                raise RunningHubCoverError(f"RunningHub task ended with status: {status}.")
            client.download_result_image(result, local_cover_path)
            output_width, output_height = inspect_image_size(local_cover_path)
            render_status = "rendered"
        except Exception as exc:
            render_status = "failed"
            warnings.append(f"{variant_id}: {str(exc)[:180]}")

        variants.append(
            {
                "variant_id": variant_id,
                "title_id": title.get("title_id") or f"title_{index}",
                "title_text": title.get("text") or "",
                "title_source": title.get("source") or "local_static",
                "source_image_path": image.get("path") or "",
                "source_image_name": image.get("display_name") or image.get("file_name") or "",
                "runninghub_task_id": task_id,
                "runninghub_status": status,
                "remote_result_ref": remote_result_ref,
                "remote_result_url": remote_result_url,
                "local_cover_image_path": str(local_cover_path) if local_cover_path.exists() else "",
                "render_status": render_status,
                "output_width": output_width,
                "output_height": output_height,
                "external_api_called": True,
            }
        )

    blocking = any(variant["render_status"] != "rendered" for variant in variants)
    selected_variant_id = (
        variants[0]["variant_id"] if variants and not blocking else ""
    )
    report = {
        "version": COVER_BATCH_VERSION,
        "provider": COVER_PROVIDER,
        "workflow_provider": COVER_PROVIDER,
        "workflow_id": getattr(client.config, "workflow_id", "") if hasattr(client, "config") else "",
        "image_node_id": getattr(client.config, "image_node_id", "") if hasattr(client, "config") else "",
        "image_node_field": getattr(client.config, "image_node_field", "") if hasattr(client, "config") else "",
        "title_node_id": getattr(client.config, "title_node_id", "") if hasattr(client, "config") else "",
        "title_node_field": getattr(client.config, "title_node_field", "") if hasattr(client, "config") else "",
        "output_node_id": getattr(client.config, "output_node_id", "") if hasattr(client, "config") else "",
        "output_node_field": getattr(client.config, "output_node_field", "") if hasattr(client, "config") else "",
        "external_api_called": True,
        "batch_index": batch_index,
        "theme_text": theme_text,
        "min_required_images": MIN_REQUIRED_IMAGES,
        "uploaded_image_count": len(selected_images),
        "selected_cover_variant_id": selected_variant_id,
        "variants": variants,
        "warnings": warnings,
        "blocking": blocking,
    }
    report_path = output_path / "cover_batch_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report["cover_batch_report_path"] = str(report_path)
    return report


def inspect_image_size(image_path: str | Path) -> tuple[int, int]:
    try:
        from PIL import Image

        with Image.open(image_path) as image:
            return image.size
    except Exception:
        return 0, 0


class FakeRunningHubCoverClient:
    """Test double used by AppTest; production WebUI never enables it implicitly."""

    def __init__(self):
        self.submitted_tasks: list[dict[str, Any]] = []

    def upload_image(self, image_path: str | Path) -> dict[str, Any]:
        return {"upload_ref": str(Path(image_path).name)}

    def submit_cover_task(self, image_ref: str, title_text: str) -> dict[str, Any]:
        task_id = f"fake-task-{len(self.submitted_tasks) + 1}"
        self.submitted_tasks.append(
            {"task_id": task_id, "image_ref": image_ref, "title_text": title_text}
        )
        return {"task_id": task_id}

    def wait_for_task(self, task_id: str) -> dict[str, Any]:
        return {
            "status": "succeeded",
            "remote_result_ref": task_id,
            "remote_result_url": f"fake://{task_id}",
        }

    def download_result_image(self, remote_result: dict[str, Any], output_path: str | Path):
        from PIL import Image, ImageDraw

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        index = len(list(output.parent.glob("cover_*.png"))) + 1
        image = Image.new(
            "RGB",
            (COVER_OUTPUT_WIDTH, COVER_OUTPUT_HEIGHT),
            (80 + index * 35, 90 + index * 25, 120 + index * 20),
        )
        draw = ImageDraw.Draw(image)
        draw.rectangle((40, 40, COVER_OUTPUT_WIDTH - 40, COVER_OUTPUT_HEIGHT - 40), outline="white", width=12)
        draw.text((80, 120), f"Fake RunningHub Cover {index}", fill="white")
        image.save(output, format="PNG")
