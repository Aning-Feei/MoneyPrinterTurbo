from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from json import JSONDecodeError
from typing import Any


DEFAULT_DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
DEFAULT_DEEPSEEK_MODEL = "deepseek-chat"


class DeepSeekClientError(Exception):
    """Base error for DeepSeek planner calls."""


class MissingDeepSeekAPIKey(DeepSeekClientError):
    """Raised when no DeepSeek API key is available."""


class DeepSeekClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout_seconds: int = 45,
        max_retries: int = 2,
    ) -> None:
        self.api_key = api_key or _get_config_value(
            env_key="DEEPSEEK_API_KEY",
            config_keys=("deepseek_api_key",),
        )
        if not self.api_key:
            raise MissingDeepSeekAPIKey(
                "DeepSeek API key is missing. Set DEEPSEEK_API_KEY or local config.toml."
            )

        self.base_url = (
            base_url
            or _get_config_value(
                env_key="DEEPSEEK_BASE_URL",
                config_keys=("deepseek_base_url",),
            )
            or DEFAULT_DEEPSEEK_BASE_URL
        )
        self.model = (
            model
            or _get_config_value(
                env_key="DEEPSEEK_MODEL",
                config_keys=("deepseek_model", "deepseek_model_name"),
            )
            or DEFAULT_DEEPSEEK_MODEL
        )
        self.timeout_seconds = timeout_seconds
        self.max_retries = max(1, max_retries)
        self.external_api_called = False

    def generate_json(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        text = self.generate_text(messages=messages, temperature=temperature)
        return parse_json_from_text(text)

    def generate_text(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.2,
    ) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url=_build_chat_completions_url(self.base_url),
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )

        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                self.external_api_called = True
                with urllib.request.urlopen(
                    request,
                    timeout=self.timeout_seconds,
                ) as response:
                    response_body = response.read().decode("utf-8")
                return _extract_content(response_body)
            except urllib.error.HTTPError as exc:
                last_error = DeepSeekClientError(
                    f"DeepSeek API request failed with HTTP {exc.code}."
                )
            except urllib.error.URLError as exc:
                last_error = DeepSeekClientError(f"DeepSeek API request failed: {exc.reason}")
            except TimeoutError as exc:
                last_error = DeepSeekClientError("DeepSeek API request timed out.")
            except DeepSeekClientError as exc:
                last_error = exc

            if attempt < self.max_retries - 1:
                time.sleep(1)

        if last_error is not None:
            raise last_error
        raise DeepSeekClientError("DeepSeek API request failed.")


def parse_json_from_text(text: str) -> dict[str, Any]:
    value = text.strip()
    if value.startswith("```"):
        value = _strip_json_code_fence(value)

    try:
        parsed = json.loads(value)
    except JSONDecodeError:
        parsed = _extract_first_json_object(value)

    if not isinstance(parsed, dict):
        raise DeepSeekClientError("DeepSeek response JSON must be an object.")
    return parsed


def _extract_content(response_body: str) -> str:
    try:
        data = json.loads(response_body)
    except JSONDecodeError as exc:
        raise DeepSeekClientError("DeepSeek API returned invalid JSON.") from exc

    choices = data.get("choices")
    if not choices or not isinstance(choices, list):
        raise DeepSeekClientError("DeepSeek API response has no choices.")

    message = choices[0].get("message") if isinstance(choices[0], dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, str) or not content.strip():
        raise DeepSeekClientError("DeepSeek API response has no content.")
    return content.strip()


def _extract_first_json_object(text: str) -> dict[str, Any]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "{":
            continue
        try:
            parsed, _ = decoder.raw_decode(text[index:])
        except JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    raise DeepSeekClientError("DeepSeek response did not contain a valid JSON object.")


def _strip_json_code_fence(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _build_chat_completions_url(base_url: str) -> str:
    normalized = (base_url or DEFAULT_DEEPSEEK_BASE_URL).strip().rstrip("/")
    if normalized.endswith("/chat/completions"):
        return normalized
    return f"{normalized}/chat/completions"


def _get_config_value(env_key: str, config_keys: tuple[str, ...]) -> str:
    env_value = os.getenv(env_key, "").strip()
    if env_value:
        return env_value

    try:
        from app.config import config
    except Exception:
        return ""

    for config_key in config_keys:
        value = str(config.app.get(config_key, "") or "").strip()
        if value:
            return value
    return ""
