from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .models import (
    NarrationLine,
    NarrationPlan,
    Storyboard,
    StoryboardContractIssue,
    TTSContractReport,
)


SPEECH_RATE_CJK_PER_SECOND = 4.0
MAX_TIMING_OVERFLOW_SECONDS = 3.0


def build_narration_plan(
    storyboard: Storyboard,
    speech_rate_cjk_per_second: float = SPEECH_RATE_CJK_PER_SECOND,
) -> NarrationPlan:
    lines = []
    for scene in storyboard.scenes:
        narration = str(scene.narration or scene.mock_narration or "").strip()
        cjk_count = count_cjk_chars(narration)
        estimated_speech_seconds = estimate_speech_seconds(
            narration,
            speech_rate_cjk_per_second=speech_rate_cjk_per_second,
        )
        lines.append(
            NarrationLine(
                scene_index=scene.index,
                image_name=scene.image_name,
                duration_seconds=scene.duration_seconds,
                narration=narration,
                cjk_char_count=cjk_count,
                estimated_tts_seconds=estimated_speech_seconds,
                estimated_speech_seconds=estimated_speech_seconds,
                recommended_max_cjk_chars=int(
                    scene.duration_seconds * speech_rate_cjk_per_second
                ),
            )
        )

    return NarrationPlan(
        project_id=storyboard.project_id,
        version="narration-plan-v1",
        lines=lines,
        target_duration_seconds=storyboard.total_duration_seconds,
        total_scene_duration_seconds=sum(line.duration_seconds for line in lines),
        total_duration_seconds=storyboard.total_duration_seconds,
        total_estimated_speech_seconds=round(
            sum(line.estimated_speech_seconds for line in lines),
            2,
        ),
        speech_rate_cjk_per_second=speech_rate_cjk_per_second,
        notes=(
            "Local narration plan only. No TTS, audio generation, or external API "
            "was called."
        ),
    )


def validate_tts_contract(
    narration_plan: NarrationPlan,
    scene_count: int,
) -> TTSContractReport:
    errors: list[StoryboardContractIssue] = []
    warnings: list[StoryboardContractIssue] = []

    if len(narration_plan.lines) != scene_count:
        errors.append(
            _error(
                "narration_line_count_mismatch",
                (
                    f"narration plan has {len(narration_plan.lines)} lines, "
                    f"expected {scene_count} scenes."
                ),
            )
        )

    for line in narration_plan.lines:
        _validate_narration_line(line, errors, warnings)

    return TTSContractReport(
        passed=not errors,
        errors=errors,
        warnings=warnings,
        line_count=len(narration_plan.lines),
        scene_count=scene_count,
        total_duration_seconds=narration_plan.total_duration_seconds,
        total_estimated_speech_seconds=narration_plan.total_estimated_speech_seconds,
    )


def narration_plan_to_dict(plan: NarrationPlan) -> dict[str, Any]:
    return asdict(plan)


def tts_contract_report_to_dict(report: TTSContractReport) -> dict[str, Any]:
    return asdict(report)


def estimate_speech_seconds(
    narration: str,
    speech_rate_cjk_per_second: float = SPEECH_RATE_CJK_PER_SECOND,
) -> float:
    cjk_count = count_cjk_chars(narration)
    if speech_rate_cjk_per_second <= 0:
        return 0.0
    return round(cjk_count / speech_rate_cjk_per_second, 2)


def count_cjk_chars(text: str) -> int:
    return sum(1 for char in str(text or "") if "\u4e00" <= char <= "\u9fff")


def _validate_narration_line(
    line: NarrationLine,
    errors: list[StoryboardContractIssue],
    warnings: list[StoryboardContractIssue],
) -> None:
    if not line.narration:
        errors.append(
            _error(
                "empty_tts_narration",
                f"scene {line.scene_index} narration must not be empty for TTS.",
            )
        )
        return

    if line.cjk_char_count <= 0:
        errors.append(
            _error(
                "non_chinese_tts_narration",
                f"scene {line.scene_index} narration must contain Chinese text.",
            )
        )

    if line.duration_seconds <= 0:
        errors.append(
            _error(
                "invalid_tts_duration",
                f"scene {line.scene_index} duration_seconds must be positive.",
            )
        )
        return

    if line.estimated_speech_seconds > line.duration_seconds:
        warnings.append(
            StoryboardContractIssue(
                level="warning",
                code="tts_narration_over_scene_duration",
                message=(
                    f"scene {line.scene_index} estimated speech is "
                    f"{line.estimated_speech_seconds}s for a "
                    f"{line.duration_seconds}s scene."
                ),
            )
        )

    if line.estimated_speech_seconds > (
        line.duration_seconds + MAX_TIMING_OVERFLOW_SECONDS
    ):
        errors.append(
            _error(
                "tts_narration_far_too_long",
                (
                    f"scene {line.scene_index} estimated speech is "
                    f"{line.estimated_speech_seconds}s, too long for a "
                    f"{line.duration_seconds}s scene."
                ),
            )
        )


def _error(code: str, message: str) -> StoryboardContractIssue:
    return StoryboardContractIssue(level="error", code=code, message=message)
