from __future__ import annotations

import re
from dataclasses import asdict
from typing import Any

from .models import (
    CoverCopy,
    CoverLayout,
    CoverPlan,
    CoverQualityFlags,
    CoverSelectedAssets,
    CoverSourceContracts,
    CoverWarning,
    ImageUnderstandingItem,
    ImageUnderstandingReport,
    RuleEngineReport,
    SelectedTitle,
    TitleCandidate,
    TitleGeneration,
)


COVER_PLAN_VERSION = "cover-plan-v1"
COVER_PLANNER_NAME = "local_static"
COVER_RENDER_STATUS = "not_rendered"
TITLE_PROVIDER = "local_static"
TITLE_QUALITY_VERSION = "cover-title-quality-v1"
DEFAULT_TITLES = (
    "这口好味越吃越香",
    "这一桌烟火气正好",
    "今晚就约这家餐厅",
)
WEAK_TITLE_TERMS = (
    "值得一试",
    "聚餐首选",
    "发现这家",
    "不容错过",
    "强烈推荐",
    "必吃",
    "宝藏",
    "绝了",
)
EXAGGERATED_TITLE_TERMS = (
    "全城第一",
    "天花板",
    "史上最强",
    "全网爆火",
    "100%好吃",
    "100% 好吃",
    "不吃后悔",
    "销量第一",
    "冠军",
    "最低价",
)
PLACEHOLDER_TITLE_TERMS = (
    "mock",
    "placeholder",
    "todo",
    "待填写",
    "标题",
    "示例",
)


def build_cover_plan(
    project: dict[str, Any],
    image_understanding: ImageUnderstandingReport,
    rule_engine_report: RuleEngineReport,
) -> CoverPlan:
    theme_text = get_theme_text(project)
    candidates = build_title_candidates(theme_text)
    selected_title, title_warnings = select_title(project, candidates)
    selected_assets, asset_warnings = select_primary_image(
        project=project,
        images=image_understanding.images,
        rule_engine_report=rule_engine_report,
    )

    warnings = map_rule_findings_to_cover_warnings(rule_engine_report)
    warnings.extend(title_warnings)
    warnings.extend(asset_warnings)

    has_primary_image = selected_assets.primary_image_id is not None
    blocking = not has_primary_image
    quality_flags = CoverQualityFlags(
        requires_human_review=True,
        content_based_understanding=(
            rule_engine_report.summary.has_content_based_understanding
        ),
        uses_filename_fallback=rule_engine_report.summary.has_filename_fallback,
        has_primary_image=has_primary_image,
        has_user_selected_title=selected_title.user_selected,
    )

    return CoverPlan(
        version=COVER_PLAN_VERSION,
        planner=COVER_PLANNER_NAME,
        external_api_called=False,
        render_status=COVER_RENDER_STATUS,
        cover_image_path=None,
        source_contracts=CoverSourceContracts(
            image_understanding_provider=image_understanding.provider,
            image_understanding_analysis_source=image_understanding.analysis_source,
            rule_engine_version=rule_engine_report.version,
            rule_engine=rule_engine_report.engine,
        ),
        title_generation=TitleGeneration(
            theme_text=theme_text,
            title_provider=TITLE_PROVIDER,
            external_api_called=False,
        ),
        title_candidates=candidates,
        selected_title=selected_title,
        selected_assets=selected_assets,
        cover_copy=build_cover_copy(project, selected_title),
        layout=build_default_layout(),
        quality_flags=quality_flags,
        warnings=warnings,
        blocking=blocking,
    )


def get_theme_text(project: dict[str, Any]) -> str:
    for key in ("theme_text", "topic_text", "brief", "description"):
        value = str(project.get(key) or "").strip()
        if value:
            return value
    return ""


def build_title_candidates(theme_text: str) -> list[TitleCandidate]:
    title_texts = build_high_quality_cover_title_texts(theme_text, batch_index=1)
    return [
        TitleCandidate(
            title_id=f"title_{index}",
            text=text,
            source=TITLE_PROVIDER,
        )
        for index, text in enumerate(title_texts, start=1)
    ]


def build_high_quality_cover_titles(
    theme_text: str, batch_index: int = 1, count: int = 6
) -> list[str]:
    """Build deterministic local_static cover title text candidates."""

    return list(
        build_high_quality_cover_title_texts(
            theme_text, batch_index=batch_index, count=count
        )
    )


def build_high_quality_cover_title_texts(
    theme_text: str, batch_index: int = 1, count: int = 3
) -> tuple[str, ...]:
    target_count = max(1, int(count or 3))
    groups = build_cover_title_groups(theme_text)
    offset = max(0, int(batch_index or 1) - 1)
    selected: list[str] = []
    max_group_len = max(len(group) for group in groups)
    for round_index in range(max_group_len):
        for group in groups:
            selected.append(group[(offset + round_index) % len(group)])
            if len(dict.fromkeys(selected)) >= target_count:
                break
        if len(dict.fromkeys(selected)) >= target_count:
            break

    fallback_groups = build_cover_title_groups("")
    fallback_max_group_len = max(len(group) for group in fallback_groups)
    for round_index in range(fallback_max_group_len):
        for group in fallback_groups:
            candidate = group[(offset + round_index) % len(group)]
            if candidate not in selected:
                selected.append(candidate)
            if len(dict.fromkeys(selected)) >= target_count:
                break
        if len(dict.fromkeys(selected)) >= target_count:
            break

    cleaned: list[str] = []
    for title in selected:
        candidate = sanitize_cover_title(title)
        quality = validate_cover_title_quality(candidate)
        if quality["passed"] and candidate not in cleaned:
            cleaned.append(candidate)
        if len(cleaned) == target_count:
            break

    if len(cleaned) < target_count:
        for title in DEFAULT_TITLES:
            candidate = sanitize_cover_title(title)
            if validate_cover_title_quality(candidate)["passed"] and candidate not in cleaned:
                cleaned.append(candidate)
            if len(cleaned) == target_count:
                break

    return tuple(cleaned[:target_count])


def build_cover_title_groups(theme_text: str) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    normalized = normalize_theme_text(theme_text)

    if contains_any(normalized, ("火锅",)):
        return (
            (
                "这锅川味越吃越上头",
                "热辣这一锅真香",
                "一口麻辣就开胃",
                "川味一上桌就馋",
            ),
            (
                "朋友聚餐就该吃这锅",
                "今晚就约这锅热辣",
                "热闹饭局从这锅开始",
                "这一锅适合凑齐朋友",
            ),
            (
                "藏不住的热辣火锅局",
                "烟火气里的热辣局",
                "热辣氛围一秒开场",
                "这一桌热辣有氛围",
            ),
        )

    if contains_any(normalized, ("烤鱼", "小龙虾")):
        return (
            (
                "招牌烤鱼一口入戏",
                "小龙虾上桌就热闹",
                "这一口鲜辣很开胃",
                "热辣招牌越吃越香",
            ),
            (
                "朋友聚餐就爱这一桌",
                "这桌热闹刚好开场",
                "下班就约这顿热辣",
                "这一桌适合慢慢吃",
            ),
            (
                "川味烟火气扑面而来",
                "热辣香气一秒到位",
                "越吃越有氛围的一桌",
                "藏不住的招牌香气",
            ),
        )

    if contains_any(normalized, ("川菜", "四川", "川味", "麻辣", "热辣")):
        return (
            (
                "这口川味越吃越上头",
                "川味一上桌就开胃",
                "麻辣鲜香一口入魂",
                "这一口热辣真带劲",
            ),
            (
                "朋友聚餐就爱这一桌",
                "热闹饭局就从这桌开始",
                "今晚就约这桌川味",
                "下班聚餐就想吃这口",
            ),
            (
                "藏不住的热辣川味",
                "一桌川味烟火气拉满",
                "这桌热辣氛围正好",
                "香气一上桌就热闹",
            ),
        )

    if contains_any(normalized, ("咖啡", "甜品", "下午茶", "蛋糕", "烘焙")):
        return (
            (
                "这口甜香刚好治愈",
                "咖啡香里慢慢发光",
                "甜品一上桌就心动",
                "这一口甜得很有氛围",
            ),
            (
                "下午茶就该这样拍",
                "和朋友慢慢坐一下午",
                "今天把甜品时间留给自己",
                "这家适合慢慢发呆",
            ),
            (
                "甜香氛围感刚刚好",
                "镜头里的下午茶很出片",
                "这一桌甜得很轻松",
                "咖啡甜品拍照正好",
            ),
        )

    if contains_any(normalized, ("烧烤", "烤肉", "串串")):
        return (
            (
                "烟火气一上来就饿了",
                "越烤越香的热闹局",
                "这一口炭火香很上头",
                "热辣串串越吃越香",
            ),
            (
                "朋友夜宵就约这一桌",
                "下班就来这桌烟火气",
                "今晚把热闹交给这一桌",
                "这顿适合边聊边吃",
            ),
            (
                "烟火气把氛围拉满",
                "烤香一出来就热闹",
                "这一桌夜晚刚刚好",
                "热闹食光从这桌开始",
            ),
        )

    return (
        (
            "这口好味越吃越香",
            "一上桌就有烟火气",
            "这一口很有记忆点",
            "好味道一秒开场",
        ),
        (
            "今晚就约这家餐厅",
            "朋友聚餐就坐这一桌",
            "下班后就想吃这一顿",
            "这一桌适合慢慢聊",
        ),
        (
            "这一桌烟火气正好",
            "藏在日常里的好味道",
            "镜头里的餐厅很有氛围",
            "这顿饭的氛围刚刚好",
        ),
    )


def build_short_video_cover_titles(theme_text: str) -> tuple[str, str, str]:
    return build_high_quality_cover_title_texts(theme_text, batch_index=1, count=3)  # type: ignore[return-value]


def validate_cover_title_quality(title_text: str) -> dict[str, Any]:
    title = sanitize_cover_title(title_text)
    warnings: list[str] = []
    passed = True

    cjk_count = count_cjk_chars(title)
    if cjk_count < 6:
        warnings.append("TITLE_TOO_SHORT")
        passed = False
    if cjk_count > 16:
        warnings.append("TITLE_TOO_LONG")
        passed = False
    if contains_any(title, WEAK_TITLE_TERMS):
        warnings.append("WEAK_TEMPLATE_TERM")
        passed = False
    if contains_any(title, EXAGGERATED_TITLE_TERMS):
        warnings.append("EXAGGERATED_CLAIM")
        passed = False
    lowered = title.lower()
    if any(term in lowered for term in PLACEHOLDER_TITLE_TERMS):
        warnings.append("PLACEHOLDER_TITLE")
        passed = False
    if re.search(r"\d+\s*(折|元|块|名|强|大)", title):
        warnings.append("RANKING_OR_PRICE_PROMISE")
        passed = False

    return {
        "version": TITLE_QUALITY_VERSION,
        "passed": passed,
        "warnings": warnings,
        "cjk_char_count": cjk_count,
    }


def normalize_theme_text(theme_text: str) -> str:
    return re.sub(r"\s+", "", str(theme_text or ""))


def sanitize_cover_title(title_text: str) -> str:
    return re.sub(r"\s+", "", str(title_text or "")).strip("，,。.!！?？：:；;")


def count_cjk_chars(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", str(text or "")))


def contains_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)


def extract_title_focus(theme_text: str) -> str:
    first_segment = re.split(r"[，,。；;！!？?\n]", theme_text.strip(), maxsplit=1)[0]
    cleaned = re.sub(r"\s+", "", first_segment)
    cleaned = re.sub(r"^(主打|突出|推荐|强调|围绕|适合)", "", cleaned)
    cleaned = re.sub(r"[^\w\u4e00-\u9fff]", "", cleaned)
    if not cleaned:
        return "这家餐厅"
    return cleaned[:8]


def limit_title(title: str) -> str:
    return str(title or "").strip()[:16] or DEFAULT_TITLES[0]


def select_title(
    project: dict[str, Any],
    candidates: list[TitleCandidate],
) -> tuple[SelectedTitle, list[CoverWarning]]:
    warnings: list[CoverWarning] = []
    selected_index = 0
    user_selected = False
    selection_source = "default_first_candidate"

    selected_id = str(project.get("selected_cover_title_id") or "").strip()
    selected_text = str(project.get("selected_cover_title") or "").strip()

    if selected_id:
        for index, candidate in enumerate(candidates):
            if candidate.title_id == selected_id:
                selected_index = index
                user_selected = True
                selection_source = "project_json_title_id"
                break
        else:
            warnings.append(
                CoverWarning(
                    code="INVALID_TITLE_SELECTION",
                    severity="warning",
                    message=(
                        "selected_cover_title_id did not match any generated "
                        "title candidate; defaulted to title_1."
                    ),
                )
            )
    elif selected_text:
        for index, candidate in enumerate(candidates):
            if candidate.text == selected_text:
                selected_index = index
                user_selected = True
                selection_source = "project_json_title_text"
                break
        else:
            warnings.append(
                CoverWarning(
                    code="INVALID_TITLE_SELECTION",
                    severity="warning",
                    message=(
                        "selected_cover_title did not match any generated title "
                        "candidate; defaulted to title_1."
                    ),
                )
            )

    for index, candidate in enumerate(candidates):
        object.__setattr__(candidate, "selected", index == selected_index)

    selected_candidate = candidates[selected_index]
    return (
        SelectedTitle(
            title_id=selected_candidate.title_id,
            text=selected_candidate.text,
            user_selected=user_selected,
            selection_source=selection_source,
        ),
        warnings,
    )


def select_primary_image(
    project: dict[str, Any],
    images: list[ImageUnderstandingItem],
    rule_engine_report: RuleEngineReport,
) -> tuple[CoverSelectedAssets, list[CoverWarning]]:
    warnings: list[CoverWarning] = []
    image_by_id = {image.image_id: image for image in images}

    selected_image_id = parse_image_id(project.get("selected_cover_image_id"))
    if selected_image_id is not None:
        image = image_by_id.get(selected_image_id)
        if image is not None:
            return (
                CoverSelectedAssets(
                    primary_image_id=image.image_id,
                    primary_image_path=image.image_path,
                    primary_asset_group="user_selected",
                    selection_reason="project_json_selected_cover_image_id",
                    user_selected_image=True,
                    fallback_used=False,
                ),
                warnings,
            )
        warnings.append(
            CoverWarning(
                code="INVALID_SELECTED_IMAGE",
                severity="warning",
                message=(
                    "selected_cover_image_id did not match any uploaded image; "
                    "fell back to rule engine candidates."
                ),
            )
        )

    fallback_candidates = build_image_candidate_order(rule_engine_report, images)
    for image_id, asset_group, reason in fallback_candidates:
        image = image_by_id.get(image_id)
        if image is not None:
            return (
                CoverSelectedAssets(
                    primary_image_id=image.image_id,
                    primary_image_path=image.image_path,
                    primary_asset_group=asset_group,
                    selection_reason=reason,
                    user_selected_image=False,
                    fallback_used=True,
                ),
                warnings,
            )

    warnings.append(
        CoverWarning(
            code="NO_PRIMARY_IMAGE",
            severity="error",
            message="No uploaded image was available for cover planning.",
        )
    )
    return (
        CoverSelectedAssets(
            primary_image_id=None,
            primary_image_path=None,
            primary_asset_group="none",
            selection_reason="no_uploaded_image",
            user_selected_image=False,
            fallback_used=True,
        ),
        warnings,
    )


def parse_image_id(raw_value: Any) -> int | None:
    value = str(raw_value or "").strip()
    if not value:
        return None
    if value.isdigit():
        return int(value)
    match = re.fullmatch(r"image[_-]?0*(\d+)", value, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def build_image_candidate_order(
    rule_engine_report: RuleEngineReport,
    images: list[ImageUnderstandingItem],
) -> list[tuple[int, str, str]]:
    hints = rule_engine_report.storyboard_hints
    groups = rule_engine_report.asset_groups
    candidates: list[tuple[int, str, str]] = []
    if hints.preferred_opening_image_id is not None:
        candidates.append(
            (
                hints.preferred_opening_image_id,
                "preferred_opening",
                "rule_engine_storyboard_hint",
            )
        )

    candidates.extend(
        (image_id, "hero_candidates", "rule_engine_hero_candidates")
        for image_id in groups.hero_candidates
    )
    candidates.extend(
        (image_id, "dish_candidates", "rule_engine_dish_candidates")
        for image_id in groups.dish_candidates
    )
    candidates.extend(
        (image_id, "interior_candidates", "rule_engine_interior_candidates")
        for image_id in groups.interior_candidates
    )
    candidates.extend(
        (image_id, "fallback_candidates", "rule_engine_fallback_candidates")
        for image_id in groups.fallback_candidates
    )
    candidates.extend(
        (image.image_id, "image_understanding_first", "image_understanding_order")
        for image in images[:1]
    )
    return dedupe_candidates(candidates)


def dedupe_candidates(
    candidates: list[tuple[int, str, str]],
) -> list[tuple[int, str, str]]:
    seen: set[int] = set()
    deduped: list[tuple[int, str, str]] = []
    for image_id, asset_group, reason in candidates:
        if image_id in seen:
            continue
        seen.add(image_id)
        deduped.append((image_id, asset_group, reason))
    return deduped


def build_cover_copy(
    project: dict[str, Any],
    selected_title: SelectedTitle,
) -> CoverCopy:
    subtitle = first_non_empty(project, ("subtitle", "slogan", "description"))
    return CoverCopy(
        title=selected_title.text,
        subtitle=limit_subtitle(subtitle or "精选美食与空间展示"),
        cta="立即了解",
        language=str(project.get("language") or "zh-CN").strip() or "zh-CN",
        copy_source="selected_title",
    )


def first_non_empty(project: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = str(project.get(key) or "").strip()
        if value:
            return value
    return ""


def limit_subtitle(text: str) -> str:
    return str(text or "").strip()[:24]


def build_default_layout() -> CoverLayout:
    return CoverLayout(
        format="vertical_9_16",
        safe_area={
            "top": 0.12,
            "bottom": 0.12,
            "left": 0.08,
            "right": 0.08,
        },
        text_zones={
            "title": "upper_third",
            "subtitle": "middle_third",
            "cta": "lower_third",
        },
    )


def map_rule_findings_to_cover_warnings(
    rule_engine_report: RuleEngineReport,
) -> list[CoverWarning]:
    return [
        CoverWarning(
            code=finding.code,
            severity=finding.severity,
            message=finding.message,
        )
        for finding in rule_engine_report.findings
    ]


def cover_plan_to_dict(cover_plan: CoverPlan) -> dict[str, Any]:
    return asdict(cover_plan)
