from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProjectConfig:
    project_path: Path
    project_root: Path
    project_name: str
    user_request: str
    selected_title: str
    aspect_ratio: str
    voice_type: str
    voice_enabled: bool
    subtitle_enabled: bool
    bgm_type: str
    video_style: str
    image_dir: str
    raw: dict[str, Any]


@dataclass(frozen=True)
class ImageFile:
    name: str
    path: Path
    suffix: str


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    severity: str = "error"
    field: str | None = None
    file_name: str | None = None


@dataclass
class ValidationReport:
    project_path: str
    project_name: str
    image_dir: str
    image_count: int
    image_files: list[str] = field(default_factory=list)
    category_checks: dict[str, bool] = field(default_factory=dict)
    issues: list[ValidationIssue] = field(default_factory=list)
    passed: bool = False
