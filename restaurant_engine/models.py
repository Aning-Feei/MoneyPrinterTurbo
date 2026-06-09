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
    duration_seconds: int = 0
    narration: str = ""
    visual_instruction: str = ""
    selling_point: str = ""
    transition_hint: str = ""


@dataclass
class Storyboard:
    project_id: str
    version: str
    scenes: list[StoryboardScene] = field(default_factory=list)
    total_mock_duration_seconds: int = 0
    total_duration_seconds: int = 0
    notes: str = ""


@dataclass(frozen=True)
class StoryboardContractIssue:
    level: str
    code: str
    message: str


@dataclass
class StoryboardContractReport:
    passed: bool
    errors: list[StoryboardContractIssue] = field(default_factory=list)
    warnings: list[StoryboardContractIssue] = field(default_factory=list)
    scene_count: int = 0
    image_count: int = 0
    target_duration_seconds: int = 30
    duration_sum: int = 0
    expected_image_order: list[str] = field(default_factory=list)
    actual_image_order: list[str] = field(default_factory=list)


@dataclass
class StoryboardQualityReport:
    passed: bool
    errors: list[StoryboardContractIssue] = field(default_factory=list)
    warnings: list[StoryboardContractIssue] = field(default_factory=list)
    scene_count: int = 0
    duplicate_narration_count: int = 0
    min_narration_cjk_chars: int = 0
    max_narration_cjk_chars: int = 0


@dataclass(frozen=True)
class NarrationLine:
    scene_index: int
    image_name: str
    duration_seconds: int
    narration: str
    cjk_char_count: int
    estimated_tts_seconds: float
    estimated_speech_seconds: float
    recommended_max_cjk_chars: int


@dataclass
class NarrationPlan:
    project_id: str
    version: str
    lines: list[NarrationLine] = field(default_factory=list)
    target_duration_seconds: int = 0
    total_scene_duration_seconds: int = 0
    total_duration_seconds: int = 0
    total_estimated_speech_seconds: float = 0.0
    speech_rate_cjk_per_second: float = 4.0
    notes: str = ""


@dataclass
class TTSContractReport:
    passed: bool
    errors: list[StoryboardContractIssue] = field(default_factory=list)
    warnings: list[StoryboardContractIssue] = field(default_factory=list)
    line_count: int = 0
    scene_count: int = 0
    total_duration_seconds: int = 0
    total_estimated_speech_seconds: float = 0.0


@dataclass(frozen=True)
class ImageUnderstandingItem:
    image_id: int
    filename: str
    image_path: str
    source: str
    detected_type: str
    quality_score: float
    cover_score: float
    video_score: float
    risk_score: float
    allowed_in_video: bool
    recommended_usage: str
    recommended_action: str
    reason: str


@dataclass
class ImageUnderstandingReport:
    project_id: str
    version: str
    provider: str
    image_dir: str
    image_count: int
    allowed_image_count: int
    rejected_image_count: int
    images: list[ImageUnderstandingItem] = field(default_factory=list)
    category_counts: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    notes: str = ""


@dataclass(frozen=True)
class RuleFinding:
    code: str
    severity: str
    message: str
    image_ids: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class RuleEngineSummary:
    image_count: int
    category_counts: dict[str, int] = field(default_factory=dict)
    has_content_based_understanding: bool = False
    has_filename_fallback: bool = False


@dataclass(frozen=True)
class RuleAssetGroups:
    hero_candidates: list[int] = field(default_factory=list)
    dish_candidates: list[int] = field(default_factory=list)
    interior_candidates: list[int] = field(default_factory=list)
    fallback_candidates: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class StoryboardHints:
    preferred_opening_image_id: int | None = None
    avoid_repeating_same_image: bool = True
    requires_human_review: bool = True


@dataclass
class RuleEngineReport:
    version: str
    engine: str
    external_api_called: bool
    image_understanding_provider: str
    image_understanding_analysis_source: str
    summary: RuleEngineSummary
    findings: list[RuleFinding] = field(default_factory=list)
    asset_groups: RuleAssetGroups = field(default_factory=RuleAssetGroups)
    storyboard_hints: StoryboardHints = field(default_factory=StoryboardHints)
    blocking: bool = False


@dataclass
class PipelineReport:
    ok: bool
    project_id: str
    project_json_path: str
    image_dir: str
    output_dir: str
    image_count: int
    image_understanding_path: str | None
    image_understanding_provider: str
    rule_engine_report_path: str | None
    storyboard_path: str | None
    narration_plan_path: str | None
    validation_passed: bool
    target_duration_seconds: int = 30
    scene_count: int = 0
    scene_durations: list[int] = field(default_factory=list)
    total_duration_seconds: int = 0
    duration_normalized: bool = False
    storyboard_contract_passed: bool = False
    storyboard_contract_errors: list[dict[str, Any]] = field(default_factory=list)
    storyboard_contract_warnings: list[dict[str, Any]] = field(default_factory=list)
    duration_sum: int = 0
    storyboard_quality_passed: bool = False
    storyboard_quality_errors: list[dict[str, Any]] = field(default_factory=list)
    storyboard_quality_warnings: list[dict[str, Any]] = field(default_factory=list)
    tts_contract_passed: bool = False
    tts_contract_errors: list[dict[str, Any]] = field(default_factory=list)
    tts_contract_warnings: list[dict[str, Any]] = field(default_factory=list)
    narration_line_count: int = 0
    total_estimated_speech_seconds: float = 0.0
    image_understanding_passed: bool = False
    allowed_image_count: int = 0
    rejected_image_count: int = 0
    image_category_counts: dict[str, int] = field(default_factory=dict)
    rule_engine_external_api_called: bool = False
    rule_engine_findings_count: int = 0
    rule_engine_blocking: bool = False
    rule_engine_version: str = ""
    planner: str = "mock"
    external_api_allowed: bool = False
    external_api_called: bool = False
    steps: list[PipelineStep] = field(default_factory=list)
    issues: list[dict[str, Any]] = field(default_factory=list)
