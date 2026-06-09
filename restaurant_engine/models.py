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
    target_duration_seconds: int
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
    target_duration_seconds: int
    image_count_range: dict[str, int]
    image_count: int
    image_files: list[str] = field(default_factory=list)
    category_checks: dict[str, bool] = field(default_factory=dict)
    issues: list[ValidationIssue] = field(default_factory=list)
    passed: bool = False


@dataclass(frozen=True)
class Shot:
    index: int
    role: str
    image_name: str
    image_path: str
    recommended_duration: int


@dataclass
class ShotPlan:
    shots: list[Shot] = field(default_factory=list)
    total_image_duration: int = 0
    missing_roles: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class TimingRecommendation:
    target_duration_seconds: int
    estimated_narration_seconds: float
    recommended_clip_duration: int
    total_image_duration: int
    narration_safe_seconds: int
    narration_max_cjk_chars: int
    will_loop: bool


@dataclass
class RenderParameterRecommendation:
    video_concat_mode: str
    video_clip_duration: int
    video_source: str
    notes: list[str] = field(default_factory=list)


@dataclass
class PreflightReport:
    ok: bool
    project_id: str
    shot_plan: ShotPlan
    timing: TimingRecommendation
    render_params: RenderParameterRecommendation
    issues: list[ValidationIssue] = field(default_factory=list)


@dataclass(frozen=True)
class PipelineStep:
    name: str
    status: str
    message: str


@dataclass(frozen=True)
class StoryboardScene:
    index: int
    role: str
    image_name: str
    image_path: str
    mock_duration_seconds: int
    mock_narration: str
    notes: str


@dataclass
class Storyboard:
    project_id: str
    version: str
    scenes: list[StoryboardScene] = field(default_factory=list)
    total_mock_duration_seconds: int = 0
    notes: str = ""


@dataclass
class PipelineReport:
    ok: bool
    project_id: str
    project_json_path: str
    image_dir: str
    output_dir: str
    image_count: int
    storyboard_path: str | None
    validation_passed: bool
    planner: str = "mock"
    external_api_allowed: bool = False
    external_api_called: bool = False
    steps: list[PipelineStep] = field(default_factory=list)
    issues: list[dict[str, Any]] = field(default_factory=list)
