from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .models import (
    ImageUnderstandingItem,
    ImageUnderstandingReport,
    RuleAssetGroups,
    RuleEngineReport,
    RuleEngineSummary,
    RuleFinding,
    StoryboardHints,
)


RULE_ENGINE_VERSION = "v0.1"
RULE_ENGINE_NAME = "local_static"

HERO_TYPES = {"intro", "storefront", "exterior", "hero"}
DISH_TYPES = {"dish", "food", "menu_item", "menu"}
INTERIOR_TYPES = {"interior", "dining", "environment"}


def build_rule_engine_report(
    image_understanding: ImageUnderstandingReport,
) -> RuleEngineReport:
    provider = str(image_understanding.provider or "unknown")
    analysis_source = detect_analysis_source(image_understanding)
    summary = RuleEngineSummary(
        image_count=image_understanding.image_count,
        category_counts=dict(image_understanding.category_counts),
        has_content_based_understanding=provider == "vision",
        has_filename_fallback=provider == "filename_fallback",
    )
    asset_groups = build_asset_groups(image_understanding.images)
    findings = build_findings(provider, analysis_source)
    storyboard_hints = build_storyboard_hints(provider, asset_groups)

    return RuleEngineReport(
        version=RULE_ENGINE_VERSION,
        engine=RULE_ENGINE_NAME,
        external_api_called=False,
        image_understanding_provider=provider,
        image_understanding_analysis_source=analysis_source,
        summary=summary,
        findings=findings,
        asset_groups=asset_groups,
        storyboard_hints=storyboard_hints,
        blocking=False,
    )


def detect_analysis_source(image_understanding: ImageUnderstandingReport) -> str:
    sources = {
        str(item.source or "").strip()
        for item in image_understanding.images
        if str(item.source or "").strip()
    }
    if len(sources) == 1:
        return next(iter(sources))
    if sources:
        return "mixed"
    return str(image_understanding.provider or "unknown")


def build_findings(provider: str, analysis_source: str) -> list[RuleFinding]:
    if provider == "mock":
        return [
            RuleFinding(
                code="NO_CONTENT_BASED_UNDERSTANDING",
                severity="warning",
                message=(
                    "Image understanding is using development mock output; it is "
                    "not based on image content and requires human review."
                ),
                image_ids=[],
            )
        ]
    if provider == "filename_fallback":
        return [
            RuleFinding(
                code="FILENAME_FALLBACK_USED",
                severity="warning",
                message=(
                    "Image categories come from filename fallback only; this is "
                    "not formal content-based image understanding."
                ),
                image_ids=[],
            )
        ]
    if provider == "vision":
        return []
    return [
        RuleFinding(
            code="UNKNOWN_IMAGE_UNDERSTANDING_PROVIDER",
            severity="warning",
            message=(
                "Image understanding provider is not recognized by the local "
                f"rule engine: {provider or analysis_source}."
            ),
            image_ids=[],
        )
    ]


def build_asset_groups(
    images: list[ImageUnderstandingItem],
) -> RuleAssetGroups:
    hero_candidates: list[int] = []
    dish_candidates: list[int] = []
    interior_candidates: list[int] = []
    fallback_candidates: list[int] = []

    for image in images:
        detected_type = str(image.detected_type or "unknown").strip().lower()
        if detected_type in HERO_TYPES:
            hero_candidates.append(image.image_id)
        elif detected_type in DISH_TYPES:
            dish_candidates.append(image.image_id)
        elif detected_type in INTERIOR_TYPES:
            interior_candidates.append(image.image_id)
        else:
            fallback_candidates.append(image.image_id)

    return RuleAssetGroups(
        hero_candidates=hero_candidates,
        dish_candidates=dish_candidates,
        interior_candidates=interior_candidates,
        fallback_candidates=fallback_candidates,
    )


def build_storyboard_hints(
    provider: str,
    asset_groups: RuleAssetGroups,
) -> StoryboardHints:
    preferred_opening_image_id = None
    if asset_groups.hero_candidates:
        preferred_opening_image_id = asset_groups.hero_candidates[0]
    elif asset_groups.fallback_candidates:
        preferred_opening_image_id = asset_groups.fallback_candidates[0]

    return StoryboardHints(
        preferred_opening_image_id=preferred_opening_image_id,
        avoid_repeating_same_image=True,
        requires_human_review=provider != "vision",
    )


def rule_engine_report_to_dict(report: RuleEngineReport) -> dict[str, Any]:
    return asdict(report)
