import os
import math
import re
import sys
import webbrowser
from uuid import UUID, uuid4

import requests
import streamlit as st
from loguru import logger

# Add the root directory of the project to the system path to allow importing modules from the project
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)
    print("******** sys.path ********")
    print(sys.path)
    print("")

from app.config import config
from app.models.schema import (
    MaterialInfo,
    VideoAspect,
    VideoConcatMode,
    VideoParams,
    VideoTransitionMode,
)
from app.services import llm, voice
from app.services import task as tm
from app.utils import utils

st.set_page_config(
    page_title="TwinkleBite AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None,
    },
)


def hide_streamlit_dev_chrome_and_cache_popup():
    streamlit_style = """
    <style>
    h1 {
        padding-top: 0 !important;
    }
    #MainMenu,
    [data-testid="stToolbar"],
    [data-testid="stStatusWidget"],
    .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
    """
    st.markdown(streamlit_style, unsafe_allow_html=True)

    key_guard_js = """
    <script>
    (function () {
        function getTargetWindow() {
            try {
                return window.parent && window.parent.document
                    ? window.parent
                    : window;
            } catch (error) {
                return window;
            }
        }

        const targetWindow = getTargetWindow();
        if (targetWindow.__twinkleClearCacheKeyGuardInstalled) {
            return;
        }
        targetWindow.__twinkleClearCacheKeyGuardInstalled = true;

        function isEditableTarget(target) {
            if (!target) {
                return false;
            }
            const tag = (target.tagName || "").toLowerCase();
            if (tag === "input" || tag === "textarea" || target.isContentEditable) {
                return true;
            }
            return Boolean(
                target.closest && target.closest('[contenteditable="true"]')
            );
        }

        targetWindow.document.addEventListener(
            "keydown",
            function (event) {
                const key = (event.key || "").toLowerCase();
                const isC = key === "c";
                const hasPrimaryModifier = event.metaKey || event.ctrlKey;
                const hasCacheModifier = event.shiftKey || event.altKey;

                // Keep normal copy working: Cmd+C / Ctrl+C without Shift/Alt is allowed.
                if (!hasPrimaryModifier || !isC || !hasCacheModifier) {
                    return;
                }

                // Never block typing or copying inside editable controls.
                if (isEditableTarget(event.target)) {
                    return;
                }

                event.preventDefault();
                event.stopPropagation();
                if (event.stopImmediatePropagation) {
                    event.stopImmediatePropagation();
                }
            },
            true
        );
    })();
    </script>
    """
    st.components.v1.html(key_guard_js, height=0, width=0)

    dialog_guard_js = """
    <script>
    (function () {
        function getTargetDocument() {
            try {
                return window.parent && window.parent.document
                    ? window.parent.document
                    : document;
            } catch (error) {
                return document;
            }
        }

        const doc = getTargetDocument();
        const guardWindow = doc.defaultView || window;
        if (!doc.body || guardWindow.__twinkleClearCachesDialogGuardInstalled) {
            return;
        }
        guardWindow.__twinkleClearCachesDialogGuardInstalled = true;

        function isClearCachesDialog(element) {
            if (!element || !element.innerText) {
                return false;
            }
            const text = element.innerText;
            const hasTitle = text.includes("Clear caches");
            const hasCacheText =
                text.includes("Are you sure you want to clear the app") ||
                text.includes("@st.cache_data") ||
                text.includes("@st.cache_resource");
            return hasTitle && hasCacheText;
        }

        function closeDialog(dialog) {
            const buttons = Array.from(dialog.querySelectorAll("button"));
            const cancelButton = buttons.find(
                (button) => (button.innerText || "").trim() === "Cancel"
            );
            if (cancelButton) {
                cancelButton.click();
                return;
            }

            const closeButton = buttons.find((button) => {
                const label = (
                    button.getAttribute("aria-label") ||
                    button.title ||
                    button.innerText ||
                    ""
                ).toLowerCase();
                return (
                    label.includes("close") ||
                    label.includes("cancel") ||
                    label === "×"
                );
            });

            if (closeButton) {
                closeButton.click();
                return;
            }

            dialog.style.setProperty("display", "none", "important");
            dialog.style.setProperty("visibility", "hidden", "important");
            dialog.setAttribute("aria-hidden", "true");
        }

        function suppressClearCachesDialogs() {
            const dialogs = Array.from(
                doc.querySelectorAll(
                    [
                        '[role="dialog"]',
                        '[data-baseweb="modal"]',
                        '[data-testid="stModal"]',
                        '[data-testid*="Modal"]',
                    ].join(",")
                )
            );

            dialogs.forEach((dialog) => {
                if (isClearCachesDialog(dialog)) {
                    closeDialog(dialog);
                }
            });
        }

        suppressClearCachesDialogs();
        const observer = new MutationObserver(suppressClearCachesDialogs);
        observer.observe(doc.body, { childList: true, subtree: true });
    })();
    </script>
    """
    st.components.v1.html(dialog_guard_js, height=0, width=0)


hide_streamlit_dev_chrome_and_cache_popup()

# 定义资源目录
font_dir = os.path.join(root_dir, "resource", "fonts")
song_dir = os.path.join(root_dir, "resource", "songs")
i18n_dir = os.path.join(root_dir, "webui", "i18n")
config_file = os.path.join(root_dir, "webui", ".streamlit", "webui.toml")
system_locale = utils.get_system_locale()


if "video_subject" not in st.session_state:
    st.session_state["video_subject"] = ""
if "video_script" not in st.session_state:
    st.session_state["video_script"] = ""
if "video_script_input" not in st.session_state:
    st.session_state["video_script_input"] = st.session_state["video_script"]
if "video_script_was_clamped" not in st.session_state:
    st.session_state["video_script_was_clamped"] = False
if "video_terms" not in st.session_state:
    st.session_state["video_terms"] = ""
if "video_script_prompt" not in st.session_state:
    st.session_state["video_script_prompt"] = ""
if "custom_system_prompt" not in st.session_state:
    st.session_state["custom_system_prompt"] = llm.DEFAULT_SCRIPT_SYSTEM_PROMPT
if "use_custom_system_prompt" not in st.session_state:
    st.session_state["use_custom_system_prompt"] = False
if "ui_language" not in st.session_state:
    st.session_state["ui_language"] = config.ui.get("language", system_locale)
if "local_video_materials" not in st.session_state:
    # 记住用户最近一次已经落盘的本地素材，避免仅修改文案后二次生成时丢失素材列表。
    st.session_state["local_video_materials"] = []

# 加载语言文件
locales = utils.load_locales(i18n_dir)

# 创建一个顶部栏，包含标题和语言选择
title_col, lang_col = st.columns([3, 1])

with title_col:
    st.title("TwinkleBite AI")

with lang_col:
    display_languages = []
    selected_index = 0
    for i, code in enumerate(locales.keys()):
        display_languages.append(f"{code} - {locales[code].get('Language')}")
        if code == st.session_state.get("ui_language", ""):
            selected_index = i

    selected_language = st.selectbox(
        "Language / 语言",
        options=display_languages,
        index=selected_index,
        key="top_language_selector",
        label_visibility="collapsed",
    )
    if selected_language:
        code = selected_language.split(" - ")[0].strip()
        st.session_state["ui_language"] = code
        config.ui["language"] = code

support_locales = [
    "zh-CN",
    "zh-HK",
    "zh-TW",
    "de-DE",
    "en-US",
    "fr-FR",
    "ru-RU",
    "vi-VN",
    "th-TH",
    "tr-TR",
]


def get_all_fonts():
    fonts = []
    for root, dirs, files in os.walk(font_dir):
        for file in files:
            if file.endswith(".ttf") or file.endswith(".ttc"):
                fonts.append(file)
    fonts.sort()
    return fonts


def get_all_songs():
    songs = []
    for root, dirs, files in os.walk(song_dir):
        for file in files:
            if file.endswith(".mp3"):
                songs.append(file)
    return songs


def open_task_folder(task_id):
    try:
        # task_id 应始终是服务端生成的 UUID。这里先做格式校验，避免异常值
        # 通过路径拼接访问任务目录之外的位置，也避免后续打开目录时触发
        # 平台 shell 对特殊字符的解释。
        normalized_task_id = str(UUID(str(task_id)))
        tasks_root = os.path.abspath(os.path.join(root_dir, "storage", "tasks"))
        path = os.path.abspath(os.path.join(tasks_root, normalized_task_id))

        # 即使 UUID 校验通过，也再次确认最终路径仍在任务根目录内，避免
        # 未来调用方调整 task_id 来源时引入路径穿越风险。
        if not path.startswith(tasks_root + os.sep):
            logger.warning(f"invalid task folder path: {path}")
            return

        if os.path.isdir(path):
            webbrowser.open(f"file://{path}")
    except Exception as e:
        logger.error(e)


def scroll_to_bottom():
    js = """
    <script>
        console.log("scroll_to_bottom");
        function scroll(dummy_var_to_force_repeat_execution){
            var sections = parent.document.querySelectorAll('section.main');
            console.log(sections);
            for(let index = 0; index<sections.length; index++) {
                sections[index].scrollTop = sections[index].scrollHeight;
            }
        }
        scroll(1);
    </script>
    """
    st.components.v1.html(js, height=0, width=0)


def init_log():
    logger.remove()
    _lvl = "DEBUG"

    def format_record(record):
        # 获取日志记录中的文件全路径
        file_path = record["file"].path
        # 将绝对路径转换为相对于项目根目录的路径
        relative_path = os.path.relpath(file_path, root_dir)
        # 更新记录中的文件路径
        record["file"].path = f"./{relative_path}"
        # 返回修改后的格式字符串
        # 您可以根据需要调整这里的格式
        record["message"] = record["message"].replace(root_dir, ".")

        _format = (
            "<green>{time:%Y-%m-%d %H:%M:%S}</> | "
            + "<level>{level}</> | "
            + '"{file.path}:{line}":<blue> {function}</> '
            + "- <level>{message}</>"
            + "\n"
        )
        return _format

    logger.add(
        sys.stdout,
        level=_lvl,
        format=format_record,
        colorize=True,
    )


init_log()

locales = utils.load_locales(i18n_dir)


def tr(key):
    loc = locales.get(st.session_state["ui_language"], {})
    return loc.get("Translation", {}).get(key, key)


RESTAURANT_TARGET_DURATIONS = [30, 40, 50, 60]
RESTAURANT_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
RESTAURANT_SCRIPT_EXTENSION_SENTENCES = [
    "这里适合朋友小聚，也适合下班后放松用餐。",
    "热气腾腾的锅底配上新鲜食材，让整顿饭更有氛围。",
    "从环境到菜品，都能感受到轻松热闹的用餐体验。",
    "如果想找一顿有温度的晚餐，这里会是不错的选择。",
    "整体体验轻松又有氛围。",
    "适合约上朋友一起慢慢享用。",
    "每一口都更有烟火气。",
    "值得一试。",
]


def set_params_runtime_field(params: VideoParams, field_name: str, value):
    try:
        setattr(params, field_name, value)
    except ValueError:
        # Streamlit may hot-reload Main.py while keeping an older imported
        # VideoParams class in memory. Avoid crashing the page before restart.
        object.__setattr__(params, field_name, value)


def is_restaurant_image_file(file_name: str) -> bool:
    return os.path.splitext(file_name or "")[1].lower() in RESTAURANT_IMAGE_SUFFIXES


def count_uploaded_image_files(files) -> int:
    return sum(1 for file in files if is_restaurant_image_file(getattr(file, "name", "")))


def count_material_image_files(materials) -> int:
    count = 0
    for material in materials or []:
        url = material.get("url", "") if isinstance(material, dict) else getattr(material, "url", "")
        if is_restaurant_image_file(url):
            count += 1
    return count


def get_restaurant_image_count(files, persisted_materials) -> int:
    uploaded_count = count_uploaded_image_files(files)
    if uploaded_count:
        return uploaded_count
    return count_material_image_files(persisted_materials)


def get_restaurant_image_range(target_duration_seconds: int) -> tuple[int, int]:
    min_images = max(6, math.ceil(target_duration_seconds / 6))
    max_images = math.floor(target_duration_seconds / 3)
    return min_images, max_images


def recommend_restaurant_clip_duration(
    target_duration_seconds: int, image_count: int
) -> int | None:
    if image_count <= 0:
        return None
    raw_clip_duration = math.ceil(target_duration_seconds / image_count)
    return min(max(raw_clip_duration, 3), 6)


def lock_restaurant_video_params(params: VideoParams, image_count: int | None = None):
    set_params_runtime_field(params, "restaurant_mode", True)
    set_params_runtime_field(params, "video_language", "zh-CN")
    set_params_runtime_field(params, "video_source", "local")
    set_params_runtime_field(params, "video_concat_mode", VideoConcatMode.sequential.value)
    set_params_runtime_field(params, "video_count", 1)
    set_params_runtime_field(
        params,
        "video_aspect",
        params.video_aspect or VideoAspect.portrait.value,
    )
    recommended_clip_duration = None
    if image_count:
        recommended_clip_duration = recommend_restaurant_clip_duration(
            params.target_duration_seconds, image_count
        )
    set_params_runtime_field(params, "video_clip_duration", recommended_clip_duration or 5)
    return recommended_clip_duration


def count_cjk_chars(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text or ""))


def strip_script_noise(text: str) -> str:
    if not text:
        return ""
    cleaned_lines = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        line = line.strip().strip("*#`> ")
        line = re.sub(r"^[-\d一二三四五六七八九十]+[\.、：:）)]\s*", "", line)
        line = re.sub(r"^(旁白|文案|视频文案|最终旁白正文)\s*[：:]\s*", "", line)
        if line:
            cleaned_lines.append(line)
    return re.sub(r"\s+", " ", "".join(cleaned_lines)).strip()


def get_restaurant_script_char_range(target_duration_seconds: int) -> tuple[int, int]:
    min_chars = math.floor((target_duration_seconds - 6) * 4.0)
    max_chars = math.floor((target_duration_seconds - 3) * 4.0)
    return min_chars, max_chars


def get_narration_char_range(target_duration_seconds: int) -> tuple[int, int]:
    return get_restaurant_script_char_range(target_duration_seconds)


def _append_restaurant_sentence(script: str, sentence: str) -> str:
    script = script.strip()
    if not script:
        return sentence
    if script[-1] in "。！？!?":
        return f"{script}{sentence}"
    return f"{script}。{sentence}"


def extend_restaurant_script_locally(script: str, min_chars: int, max_chars: int) -> str:
    extended = strip_script_noise(script)
    while count_cjk_chars(extended) < min_chars:
        current_count = count_cjk_chars(extended)
        remaining_to_max = max_chars - current_count
        best_sentence = None
        for sentence in RESTAURANT_SCRIPT_EXTENSION_SENTENCES:
            sentence_len = count_cjk_chars(sentence)
            if sentence_len <= remaining_to_max:
                best_sentence = sentence
                break
        if best_sentence is None:
            best_sentence = "整体体验轻松又有氛围。"
        extended = _append_restaurant_sentence(extended, best_sentence)
        if best_sentence == "整体体验轻松又有氛围。" and count_cjk_chars(extended) > max_chars:
            break
    return extended


def _split_script_sentences(script: str) -> list[str]:
    parts = re.split(r"([。！？!?；;])", strip_script_noise(script))
    sentences = []
    for index in range(0, len(parts), 2):
        sentence = parts[index].strip()
        if not sentence:
            continue
        if index + 1 < len(parts):
            sentence += parts[index + 1]
        sentences.append(sentence)
    return sentences


def trim_script_to_max_chars(script: str, max_chars: int) -> str:
    cleaned = strip_script_noise(script)
    if count_cjk_chars(cleaned) <= max_chars:
        return cleaned
    kept = ""
    for sentence in _split_script_sentences(cleaned):
        candidate = f"{kept}{sentence}" if kept else sentence
        if count_cjk_chars(candidate) <= max_chars:
            kept = candidate
        elif not kept:
            break
        else:
            break
    if kept:
        return kept.strip()

    cjk_count = 0
    chars = []
    for char in cleaned:
        if "\u4e00" <= char <= "\u9fff":
            if cjk_count >= max_chars:
                break
            cjk_count += 1
        chars.append(char)
    trimmed = "".join(chars).rstrip("，,、；;：:")
    if trimmed and trimmed[-1] not in "。！？!?":
        trimmed += "。"
    return trimmed


def clamp_script_to_max_cjk_chars(text: str, max_chars: int) -> tuple[str, bool]:
    if count_cjk_chars(text) <= max_chars:
        return text, False
    cleaned = strip_script_noise(text)
    cjk_count = 0
    chars = []
    for char in cleaned:
        if "\u4e00" <= char <= "\u9fff":
            if cjk_count >= max_chars:
                break
            cjk_count += 1
        chars.append(char)
    clamped = "".join(chars).rstrip("，,、；;：:")
    if clamped and clamped[-1] not in "。！？!?":
        clamped += "。"
    return clamped, True


def build_local_restaurant_video_terms(video_subject: str) -> str:
    subject = (video_subject or "").lower()
    terms = ["restaurant food", "dining experience", "local restaurant"]
    keyword_rules = [
        ("火锅", "hotpot"),
        ("hotpot", "hotpot"),
        ("川", "sichuan food"),
        ("sichuan", "sichuan food"),
        ("麻辣", "spicy food"),
        ("烧烤", "barbecue"),
        ("烤肉", "barbecue"),
        ("寿司", "sushi"),
        ("拉面", "ramen"),
        ("甜品", "dessert"),
        ("咖啡", "coffee shop"),
    ]
    for marker, term in keyword_rules:
        if marker in subject and term not in terms:
            terms.insert(0, term)
    return ", ".join(terms[:5])


def sync_video_script_input(max_chars: int | None = None):
    current_script = st.session_state.get("video_script_input", "")
    if max_chars is None:
        st.session_state["video_script"] = current_script
        return
    clamped_script, was_clamped = clamp_script_to_max_cjk_chars(
        current_script, max_chars
    )
    if was_clamped and clamped_script != current_script:
        st.session_state["video_script_input"] = clamped_script
        st.session_state["video_script_was_clamped"] = True
    st.session_state["video_script"] = st.session_state.get(
        "video_script_input", clamped_script
    )


def install_weibo_style_script_limiter(min_chars: int, max_chars: int):
    js = f"""
    <script>
    (function() {{
        const minChars = {min_chars};
        const maxChars = {max_chars};
        const anchorId = "restaurant-video-script-anchor";
        const counterId = "restaurant-video-script-live-counter";
        const cjkPattern = /[\\u4e00-\\u9fff]/;

        function countCjk(text) {{
            const matches = (text || "").match(/[\\u4e00-\\u9fff]/g);
            return matches ? matches.length : 0;
        }}

        function clampToMaxCjk(text, max) {{
            let count = 0;
            let output = "";
            for (const char of Array.from(text || "")) {{
                if (cjkPattern.test(char)) {{
                    if (count >= max) {{
                        break;
                    }}
                    count += 1;
                    output += char;
                    continue;
                }}
                if (count >= max) {{
                    if ("。！？!?".includes(char) && !/[。！？!?]$/.test(output)) {{
                        output += char;
                    }}
                    break;
                }}
                output += char;
            }}
            return output;
        }}

        function formatCounter(count, minValue, maxValue) {{
            if (count < minValue) {{
                return {{
                    text: `当前中文字符数：${{count}} / 推荐范围：${{minValue}}–${{maxValue}}（还差 ${{minValue - count}} 字）`,
                    color: "#f59e0b",
                }};
            }}
            if (count >= maxValue) {{
                return {{
                    text: `当前中文字符数：${{count}} / 推荐范围：${{minValue}}–${{maxValue}}（已达上限）`,
                    color: "#ef4444",
                }};
            }}
            return {{
                text: `当前中文字符数：${{count}} / 推荐范围：${{minValue}}–${{maxValue}}（还可输入 ${{maxValue - count}} 字）`,
                color: "#22c55e",
            }};
        }}

        function getParentDocument() {{
            try {{
                return window.parent && window.parent.document;
            }} catch (error) {{
                return document;
            }}
        }}

        function findTextarea(doc) {{
            const anchor = doc.getElementById(anchorId);
            const textareas = Array.from(doc.querySelectorAll("textarea"));
            if (!anchor || textareas.length === 0) {{
                return null;
            }}
            const anchorTop = anchor.getBoundingClientRect().top;
            return textareas
                .map((textarea) => ({{
                    textarea,
                    top: textarea.getBoundingClientRect().top,
                }}))
                .filter((item) => item.top >= anchorTop - 8)
                .sort((a, b) => a.top - b.top)[0]?.textarea || null;
        }}

        function dispatchStreamlitInput(textarea) {{
            const textareaWindow = textarea.ownerDocument.defaultView || window;
            textarea.dispatchEvent(new textareaWindow.Event("input", {{ bubbles: true }}));
            textarea.dispatchEvent(new textareaWindow.Event("change", {{ bubbles: true }}));
        }}

        function setTextareaValue(textarea, value) {{
            if (textarea.value === value) {{
                return;
            }}
            const textareaWindow = textarea.ownerDocument.defaultView || window;
            const setter = Object.getOwnPropertyDescriptor(
                textareaWindow.HTMLTextAreaElement.prototype,
                "value"
            )?.set;
            if (setter) {{
                setter.call(textarea, value);
            }} else {{
                textarea.value = value;
            }}
            dispatchStreamlitInput(textarea);
        }}

        function updateCounter(doc, textarea) {{
            const counter = doc.getElementById(counterId);
            if (!counter) {{
                return;
            }}
            const min = Number(textarea.dataset.restaurantScriptMin || minChars);
            const max = Number(textarea.dataset.restaurantScriptMax || maxChars);
            const count = countCjk(textarea.value);
            const status = formatCounter(count, min, max);
            counter.textContent = status.text;
            counter.style.color = status.color;
            counter.style.textAlign = "right";
            counter.style.fontSize = "0.9rem";
            counter.style.marginTop = "-0.25rem";
        }}

        function applyCandidate(textarea, candidate) {{
            const max = Number(textarea.dataset.restaurantScriptMax || maxChars);
            const clamped = clampToMaxCjk(candidate, max);
            if (clamped !== textarea.value) {{
                setTextareaValue(textarea, clamped);
            }}
        }}

        function getCandidateValue(textarea, insertedText) {{
            const start = textarea.selectionStart ?? textarea.value.length;
            const end = textarea.selectionEnd ?? textarea.value.length;
            return (
                textarea.value.slice(0, start) +
                (insertedText || "") +
                textarea.value.slice(end)
            );
        }}

        function attachLimiter() {{
            const doc = getParentDocument();
            const textarea = findTextarea(doc);
            if (!textarea) {{
                return false;
            }}

            textarea.dataset.restaurantScriptMax = String(maxChars);
            textarea.dataset.restaurantScriptMin = String(minChars);

            if (textarea.dataset.restaurantScriptLimiterInstalled !== "true") {{
                textarea.dataset.restaurantScriptLimiterInstalled = "true";

                textarea.addEventListener("beforeinput", function(event) {{
                    if (event.inputType && event.inputType.startsWith("delete")) {{
                        return;
                    }}
                    if (event.isComposing) {{
                        return;
                    }}
                    const data = event.data || "";
                    if (!data) {{
                        return;
                    }}
                    const candidate = getCandidateValue(textarea, data);
                    if (countCjk(candidate) > Number(textarea.dataset.restaurantScriptMax || maxChars)) {{
                        event.preventDefault();
                        applyCandidate(textarea, candidate);
                        updateCounter(doc, textarea);
                    }}
                }});

                textarea.addEventListener("paste", function(event) {{
                    const pastedText = event.clipboardData?.getData("text") || "";
                    if (!pastedText) {{
                        return;
                    }}
                    const candidate = getCandidateValue(textarea, pastedText);
                    if (countCjk(candidate) > Number(textarea.dataset.restaurantScriptMax || maxChars)) {{
                        event.preventDefault();
                        applyCandidate(textarea, candidate);
                        updateCounter(doc, textarea);
                    }}
                }});

                textarea.addEventListener("input", function() {{
                    const max = Number(textarea.dataset.restaurantScriptMax || maxChars);
                    if (countCjk(textarea.value) > max) {{
                        setTextareaValue(textarea, clampToMaxCjk(textarea.value, max));
                    }}
                    updateCounter(doc, textarea);
                }});
            }}

            if (countCjk(textarea.value) > maxChars) {{
                setTextareaValue(textarea, clampToMaxCjk(textarea.value, maxChars));
            }}
            updateCounter(doc, textarea);
            return true;
        }}

        let attempts = 0;
        const interval = window.setInterval(function() {{
            attempts += 1;
            if (attachLimiter() || attempts > 30) {{
                window.clearInterval(interval);
            }}
        }}, 100);
    }})();
    </script>
    """
    st.components.v1.html(js, height=0, width=0)


def normalize_restaurant_script_length(
    script: str, min_chars: int, max_chars: int
) -> tuple[str, str]:
    normalized = strip_script_noise(script)
    cjk_count = count_cjk_chars(normalized)
    if min_chars <= cjk_count <= max_chars:
        return normalized, "already_in_range"
    if cjk_count < min_chars:
        extended = extend_restaurant_script_locally(normalized, min_chars, max_chars)
        extended_count = count_cjk_chars(extended)
        if min_chars <= extended_count <= max_chars:
            return extended, "local_extended"
        if extended_count > max_chars:
            trimmed = trim_script_to_max_chars(extended, max_chars)
            if min_chars <= count_cjk_chars(trimmed) <= max_chars:
                return trimmed, "local_extended"
        return extended, "still_out_of_range"

    trimmed = trim_script_to_max_chars(normalized, max_chars)
    trimmed_count = count_cjk_chars(trimmed)
    if trimmed_count < min_chars:
        extended = extend_restaurant_script_locally(trimmed, min_chars, max_chars)
        if count_cjk_chars(extended) <= max_chars:
            return extended, "local_trimmed"
    if count_cjk_chars(trimmed) <= max_chars:
        return trimmed, "local_trimmed"
    return trimmed, "still_out_of_range"


def build_restaurant_script_prompt(params: VideoParams) -> str:
    min_chars, max_chars = get_restaurant_script_char_range(
        params.target_duration_seconds
    )
    restaurant_requirements = f"""
目标视频时长：{params.target_duration_seconds} 秒
建议中文旁白长度：{min_chars}–{max_chars} 个中文字符
请严格控制视频文案长度在该范围内。
不要明显超过上限，不要明显短于下限。
文案应适合中文 TTS 朗读。
不要输出分镜编号。
不要输出解释。
只输出可直接用于视频旁白的文案。
""".strip()

    if params.video_script_prompt:
        return f"{params.video_script_prompt}\n\n{restaurant_requirements}"
    return restaurant_requirements


def build_restaurant_script_revision_prompt(
    script: str,
    params: VideoParams,
    revision_type: str,
) -> str:
    min_chars, max_chars = get_restaurant_script_char_range(
        params.target_duration_seconds
    )
    action = "扩写" if revision_type == "expand" else "压缩"
    goal = (
        "保持餐厅宣传语气"
        if revision_type == "expand"
        else "保留核心卖点"
    )
    return f"""
请把下面文案{action}到 {min_chars}–{max_chars} 个中文字符之间。
{goal}，适合中文 TTS 朗读。
不能加入分镜编号。
不能加入解释。
只输出最终旁白正文。

原文案：
{script}
""".strip()


def revise_restaurant_script_if_needed(script: str, params: VideoParams) -> tuple[str, int, bool]:
    min_chars, max_chars = get_restaurant_script_char_range(
        params.target_duration_seconds
    )
    cjk_count = count_cjk_chars(script)
    if cjk_count >= min_chars and cjk_count <= max_chars:
        return script, cjk_count, False

    revision_type = "expand" if cjk_count < min_chars else "compress"
    revision_prompt = build_restaurant_script_revision_prompt(
        script=script,
        params=params,
        revision_type=revision_type,
    )
    revised_script = llm.generate_script(
        video_subject=params.video_subject,
        language=params.video_language,
        paragraph_number=params.paragraph_number,
        video_script_prompt=revision_prompt,
        custom_system_prompt=params.custom_system_prompt,
    )
    if "Error: " in revised_script:
        return script, cjk_count, True
    return revised_script, count_cjk_chars(revised_script), True


def show_restaurant_mode_guidance(
    params: VideoParams,
    uploaded_files,
    persisted_materials,
) -> dict[str, int | None]:
    target_duration = params.target_duration_seconds
    min_images, max_images = get_restaurant_image_range(target_duration)
    image_count = get_restaurant_image_count(uploaded_files, persisted_materials)
    recommended_clip_duration = recommend_restaurant_clip_duration(
        target_duration, image_count
    )
    min_chars, max_chars = get_restaurant_script_char_range(target_duration)
    cjk_count = count_cjk_chars(params.video_script)

    st.info(
        f"目标 {target_duration} 秒建议图片数量：{min_images}–{max_images} 张"
    )
    st.write(f"当前本地图片数量：{image_count} 张")

    if image_count == 0:
        st.info("上传图片后自动计算视频片段最大时长。")
    elif image_count < min_images:
        st.error(
            f"餐厅视频模式需要至少 {min_images} 张图片；当前只有 {image_count} 张，生成会被阻止。"
        )
    elif image_count > max_images:
        st.warning(
            f"当前图片数量 {image_count} 张，高于目标 {target_duration} 秒建议上限 {max_images} 张；可能节奏过快或视频超过目标时长。"
        )

    if recommended_clip_duration is not None:
        total_image_duration = image_count * recommended_clip_duration
        set_params_runtime_field(params, "video_clip_duration", recommended_clip_duration)
        st.write(
            f"推荐“视频片段最大时长(秒)”设置为 {recommended_clip_duration} 秒"
        )
        st.write(
            f"当前上传图片数 {image_count} 张，预计图片总覆盖时长 {total_image_duration} 秒"
        )
        st.caption("餐厅模式会自动使用该时长，不需要手动选择。")
    else:
        total_image_duration = None

    if params.video_script:
        if cjk_count < min_chars:
            st.warning("文案长度未达到当前目标视频时长要求。")
        elif cjk_count > max_chars:
            st.warning("文案长度超过当前目标视频时长要求。")
        else:
            st.success("文案字数符合目标时长要求。")
    return {
        "image_count": image_count,
        "min_images": min_images,
        "max_images": max_images,
        "recommended_clip_duration": recommended_clip_duration,
        "total_image_duration": total_image_duration,
        "min_chars": min_chars,
        "max_chars": max_chars,
        "cjk_count": cjk_count,
    }

@st.cache_data(ttl=300, show_spinner=False)
def get_groq_model_ids(api_key: str, base_url: str) -> list[str]:
    if not api_key:
        return []

    normalized_base_url = (base_url or "https://api.groq.com/openai/v1").strip().rstrip("/")
    models_url = f"{normalized_base_url}/models"

    try:
        response = requests.get(
            models_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        response.raise_for_status()
        payload = response.json()
        data = payload.get("data", [])

        model_ids = []
        for item in data:
            if isinstance(item, dict):
                model_id = item.get("id")
                if isinstance(model_id, str) and model_id.strip():
                    model_ids.append(model_id.strip())

        return sorted(set(model_ids))
    except Exception as e:
        logger.warning(f"failed to fetch groq models: {e}")
        return []

# 创建基础设置折叠框
if not config.app.get("hide_config", False):
    with st.expander(tr("Basic Settings"), expanded=False):
        config_panels = st.columns(3)
        left_config_panel = config_panels[0]
        middle_config_panel = config_panels[1]
        right_config_panel = config_panels[2]

        # 左侧面板 - 日志设置
        with left_config_panel:
            # 是否隐藏配置面板
            hide_config = st.checkbox(
                tr("Hide Basic Settings"), value=config.app.get("hide_config", False)
            )
            config.app["hide_config"] = hide_config

            # 是否禁用日志显示
            hide_log = st.checkbox(
                tr("Hide Log"), value=config.ui.get("hide_log", False)
            )
            config.ui["hide_log"] = hide_log

        # 中间面板 - LLM 设置

        with middle_config_panel:
            st.write(tr("LLM Settings"))
            # 下拉框需要展示“AIHubMix（推荐）”这类面向用户的文案，
            # 但配置文件和后端逻辑必须继续使用稳定的小写 provider id。
            # 因此这里显式维护 display label 和 provider id 的映射，避免
            # UI 文案变化污染 `config.app["llm_provider"]`。
            aihubmix_label = f"AIHubMix ({tr('Recommended')})"
            if config.ui.get("language") == "zh":
                aihubmix_label = "AIHubMix（推荐）"
            llm_provider_options = [
                ("OpenAI", "openai"),
                (aihubmix_label, "aihubmix"),
                ("Moonshot", "moonshot"),
                ("Azure", "azure"),
                ("Qwen", "qwen"),
                ("DeepSeek", "deepseek"),
                ("ModelScope", "modelscope"),
                ("Gemini", "gemini"),
                ("Grok", "grok"),
                ("Groq", "groq"),
                ("Ollama", "ollama"),
                ("G4f", "g4f"),
                ("OneAPI", "oneapi"),
                ("Cloudflare", "cloudflare"),
                ("ERNIE", "ernie"),
                ("MiniMax", "minimax"),
                ("MiMo", "mimo"),
                ("Pollinations", "pollinations"),
                ("LiteLLM", "litellm"),
            ]
            llm_provider_labels = [label for label, _ in llm_provider_options]
            llm_provider_values = {
                label: provider_id for label, provider_id in llm_provider_options
            }
            saved_llm_provider = config.app.get("llm_provider", "openai").lower()
            saved_llm_provider_index = 0
            for i, (_, provider_id) in enumerate(llm_provider_options):
                if provider_id == saved_llm_provider:
                    saved_llm_provider_index = i
                    break

            llm_provider_label = st.selectbox(
                tr("LLM Provider"),
                options=llm_provider_labels,
                index=saved_llm_provider_index,
            )
            llm_helper = st.container()
            llm_provider = llm_provider_values[llm_provider_label]
            config.app["llm_provider"] = llm_provider

            llm_api_key = config.app.get(f"{llm_provider}_api_key", "")
            llm_secret_key = config.app.get(
                f"{llm_provider}_secret_key", ""
            )  # only for baidu ernie
            llm_base_url = config.app.get(f"{llm_provider}_base_url", "")
            llm_model_name = config.app.get(f"{llm_provider}_model_name", "")
            llm_account_id = config.app.get(f"{llm_provider}_account_id", "")

            tips = ""
            if llm_provider == "ollama":
                if not llm_model_name:
                    llm_model_name = "qwen:7b"
                if not llm_base_url:
                    llm_base_url = config.get_default_ollama_base_url()

                with llm_helper:
                    docker_hint = ""
                    if config.is_running_in_container():
                        docker_hint = "\n                            > 检测到容器环境，未配置 Base Url 时会默认使用 `http://host.docker.internal:11434/v1`\n"
                    tips = f"""
                            ##### Ollama配置说明
                            - **API Key**: 随便填写，比如 123
                            - **Base Url**: 一般为 http://localhost:11434/v1
                                - 如果 `MoneyPrinterTurbo` 和 `Ollama` **不在同一台机器上**，需要填写 `Ollama` 机器的IP地址
                                - 如果 `MoneyPrinterTurbo` 是 `Docker` 部署，建议填写 `http://host.docker.internal:11434/v1`{docker_hint}
                            - **Model Name**: 使用 `ollama list` 查看，比如 `qwen:7b`
                            """

            if llm_provider == "openai":
                if not llm_model_name:
                    llm_model_name = "gpt-3.5-turbo"
                with llm_helper:
                    tips = """
                            ##### OpenAI 配置说明
                            > 需要VPN开启全局流量模式
                            - **API Key**: [点击到官网申请](https://platform.openai.com/api-keys)
                            - **Base Url**: 官方 OpenAI 可留空；如果使用 OpenAI 兼容供应商（例如 OpenRouter），请填写对应的兼容接口地址
                            - **Model Name**: 填写**有权限**的模型；如果使用兼容供应商，请填写该平台支持的模型 ID
                            """

            if llm_provider == "aihubmix":
                if not llm_model_name:
                    llm_model_name = "gpt-5.4-mini"
                if not llm_base_url:
                    llm_base_url = "https://aihubmix.com/v1"
                with llm_helper:
                    tips = """
                            ##### AIHubMix 配置说明
                            - **注册链接**: [点击注册 AIHubMix](https://aihubmix.com/?aff=CEve)
                            - **Base Url**: 预填 https://aihubmix.com/v1
                            - **推荐模型**: 默认 gpt-5.4-mini，也可以填写 AIHubMix 支持的免费模型或其它模型 ID

                            推荐理由：
                            - **模型全**: Claude、GPT、Gemini、Grok、DeepSeek、通义等 700+ 模型一站覆盖
                            - **稳定**: 无限并发，永远在线，集群部署于谷歌云，长期为众多知名应用提供高并发服务
                            - **能力完整**: 文本、图片生成、视频生成、TTS、STT、向量嵌入、Rerank，多模态场景全搞定
                            - **计费透明**: 按量付费，无会员无包月，免费模型可使用
                            """

            if llm_provider == "moonshot":
                if not llm_model_name:
                    llm_model_name = "moonshot-v1-8k"
                with llm_helper:
                    tips = """
                            ##### Moonshot 配置说明
                            - **API Key**: [点击到官网申请](https://platform.moonshot.cn/console/api-keys)
                            - **Base Url**: 固定为 https://api.moonshot.cn/v1
                            - **Model Name**: 比如 moonshot-v1-8k，[点击查看模型列表](https://platform.moonshot.cn/docs/intro#%E6%A8%A1%E5%9E%8B%E5%88%97%E8%A1%A8)
                            """
            if llm_provider == "oneapi":
                if not llm_model_name:
                    llm_model_name = (
                        "claude-3-5-sonnet-20240620"  # 默认模型，可以根据需要调整
                    )
                with llm_helper:
                    tips = """
                        ##### OneAPI 配置说明
                        - **API Key**: 填写您的 OneAPI 密钥
                        - **Base Url**: 填写 OneAPI 的基础 URL
                        - **Model Name**: 填写您要使用的模型名称，例如 claude-3-5-sonnet-20240620
                        """

            if llm_provider == "qwen":
                if not llm_model_name:
                    llm_model_name = "qwen-max"
                with llm_helper:
                    tips = """
                            ##### 通义千问Qwen 配置说明
                            - **API Key**: [点击到官网申请](https://dashscope.console.aliyun.com/apiKey)
                            - **Base Url**: 留空
                            - **Model Name**: 比如 qwen-max，[点击查看模型列表](https://help.aliyun.com/zh/dashscope/developer-reference/model-introduction#3ef6d0bcf91wy)
                            """

            if llm_provider == "g4f":
                if not llm_model_name:
                    llm_model_name = "gpt-3.5-turbo"
                with llm_helper:
                    tips = """
                            ##### gpt4free 配置说明
                            > [GitHub开源项目](https://github.com/xtekky/gpt4free)，可以免费使用GPT模型，但是**稳定性较差**
                            - **API Key**: 随便填写，比如 123
                            - **Base Url**: 留空
                            - **Model Name**: 比如 gpt-3.5-turbo，[点击查看模型列表](https://github.com/xtekky/gpt4free/blob/main/g4f/models.py#L308)
                            """
            if llm_provider == "azure":
                with llm_helper:
                    tips = """
                            ##### Azure 配置说明
                            > [点击查看如何部署模型](https://learn.microsoft.com/zh-cn/azure/ai-services/openai/how-to/create-resource)
                            - **API Key**: [点击到Azure后台创建](https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/OpenAI)
                            - **Base Url**: 留空
                            - **Model Name**: 填写你实际的部署名
                            """

            if llm_provider == "gemini":
                if not llm_model_name:
                    llm_model_name = "gemini-1.0-pro"

                with llm_helper:
                    tips = """
                            ##### Gemini 配置说明
                            > 需要VPN开启全局流量模式
                            - **API Key**: [点击到官网申请](https://ai.google.dev/)
                            - **Base Url**: 留空
                            - **Model Name**: 比如 gemini-1.0-pro
                            """

            if llm_provider == "grok":
                if not llm_model_name:
                    llm_model_name = "grok-4.3"
                if not llm_base_url:
                    llm_base_url = "https://api.x.ai/v1"

                with llm_helper:
                    tips = """
                            ##### Grok 配置说明
                            - **API Key**: 填写您的 GrokAPI 密钥
                            - **Base Url**: 填写 GrokAPI 的基础 URL
                            - **Model Name**: 比如 grok-4.3
                            """

            if llm_provider == "groq":
                if not llm_model_name:
                    llm_model_name = "llama-3.3-70b-versatile"
                if not llm_base_url:
                    llm_base_url = "https://api.groq.com/openai/v1"

                with llm_helper:
                    tips = """
                            ##### Groq 配置说明
                            - **API Key**: [点击到官网申请](https://console.groq.com/keys)
                            - **Base Url**: 固定为 https://api.groq.com/openai/v1
                            - **Model Name**: 比如 llama-3.3-70b-versatile
                            """

            if llm_provider == "deepseek":
                if not llm_model_name:
                    llm_model_name = "deepseek-chat"
                if not llm_base_url:
                    llm_base_url = "https://api.deepseek.com"
                with llm_helper:
                    tips = """
                            ##### DeepSeek 配置说明
                            - **API Key**: [点击到官网申请](https://platform.deepseek.com/api_keys)
                            - **Base Url**: 固定为 https://api.deepseek.com
                            - **Model Name**: 固定为 deepseek-chat
                            """

            if llm_provider == "mimo":
                if not llm_model_name:
                    llm_model_name = "mimo-v2.5-pro"
                if not llm_base_url:
                    llm_base_url = "https://api.xiaomimimo.com/v1"
                with llm_helper:
                    tips = """
                            ##### Xiaomi MiMo 配置说明
                            - **API Key**: [点击到官网申请](https://platform.xiaomimimo.com/docs/zh-CN/quick-start/first-api-call)
                            - **Base Url**: 固定为 https://api.xiaomimimo.com/v1
                            - **Model Name**: 默认 mimo-v2.5-pro，也可以按官方文档填写其它可用模型
                            """

            if llm_provider == "modelscope":
                if not llm_model_name:
                    llm_model_name = "Qwen/Qwen3-32B"
                if not llm_base_url:
                    llm_base_url = "https://api-inference.modelscope.cn/v1/"
                with llm_helper:
                    tips = """
                            ##### ModelScope 配置说明
                            - **API Key**: [点击到官网申请](https://modelscope.cn/docs/model-service/API-Inference/intro)
                            - **Base Url**: 固定为 https://api-inference.modelscope.cn/v1/
                            - **Model Name**: 比如 Qwen/Qwen3-32B，[点击查看模型列表](https://modelscope.cn/models?filter=inference_type&page=1)
                            """

            if llm_provider == "ernie":
                with llm_helper:
                    tips = """
                            ##### 百度文心一言 配置说明
                            - **API Key**: [点击到官网申请](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application)
                            - **Secret Key**: [点击到官网申请](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application)
                            - **Base Url**: 填写 **请求地址** [点击查看文档](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/jlil56u11#%E8%AF%B7%E6%B1%82%E8%AF%B4%E6%98%8E)
                            """

            if llm_provider == "pollinations":
                if not llm_model_name:
                    llm_model_name = "default"
                with llm_helper:
                    tips = """
                            ##### Pollinations AI Configuration
                            - **API Key**: Optional - Leave empty for public access
                            - **Base Url**: Default is https://text.pollinations.ai/openai
                            - **Model Name**: Use 'openai-fast' or specify a model name
                            """

            if llm_provider == "litellm":
                if not llm_model_name:
                    llm_model_name = "openai/gpt-4o-mini"
                with llm_helper:
                    tips = """
                            ##### LiteLLM Configuration
                            > [LiteLLM](https://github.com/BerriAI/litellm) routes to 100+ LLM providers via a unified interface.
                            > Set your provider's API key as an env var: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `AWS_ACCESS_KEY_ID`, etc.
                            - **Model Name**: LiteLLM format — `openai/gpt-4o`, `anthropic/claude-sonnet-4-20250514`, `bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0`, `gemini/gemini-2.5-flash`. See [full provider list](https://docs.litellm.ai/docs/providers)
                            """

            if tips and config.ui["language"] == "zh":
                # AIHubMix 自身就是 OpenAI-compatible 聚合平台；用户主动选择
                # 该 provider 时，再显示 DeepSeek/Moonshot 的通用推荐会造成
                # 信息干扰，也不利于保持合作入口的轻量、清晰。
                if llm_provider != "aihubmix":
                    st.warning(
                        "中国用户建议使用 **DeepSeek** 或 **Moonshot** 作为大模型提供商\n- 国内可直接访问，不需要VPN \n- 注册就送额度，基本够用"
                    )
                st.info(tips)

            st_llm_api_key = st.text_input(
                tr("API Key"), value=llm_api_key, type="password"
            )
            st_llm_base_url = st.text_input(tr("Base Url"), value=llm_base_url)
            st_llm_model_name = ""
            if llm_provider != "ernie":
                if llm_provider == "groq":
                    effective_api_key = st_llm_api_key or llm_api_key
                    effective_base_url = st_llm_base_url or llm_base_url
                    groq_models = get_groq_model_ids(
                        api_key=effective_api_key,
                        base_url=effective_base_url,
                    )

                    if groq_models:
                        selected_index = 0
                        if llm_model_name in groq_models:
                            selected_index = groq_models.index(llm_model_name)

                        st_llm_model_name = st.selectbox(
                            tr("Model Name"),
                            options=groq_models,
                            index=selected_index,
                            key="groq_model_name_select",
                        )
                    else:
                        st_llm_model_name = st.text_input(
                            tr("Model Name"),
                            value=llm_model_name,
                            key="groq_model_name_input",
                        )
                        if effective_api_key:
                            st.caption(
                                "Unable to load Groq model list right now. You can still enter a model name manually."
                            )
                        else:
                            st.caption(
                                "Add a Groq API key to load available models automatically."
                            )
                else:
                    st_llm_model_name = st.text_input(
                        tr("Model Name"),
                        value=llm_model_name,
                        key=f"{llm_provider}_model_name_input",
                    )
                if st_llm_model_name:
                    config.app[f"{llm_provider}_model_name"] = st_llm_model_name
            else:
                st_llm_model_name = None

            if st_llm_api_key:
                config.app[f"{llm_provider}_api_key"] = st_llm_api_key
            if st_llm_base_url:
                config.app[f"{llm_provider}_base_url"] = st_llm_base_url
            if st_llm_model_name:
                config.app[f"{llm_provider}_model_name"] = st_llm_model_name
            if llm_provider == "ernie":
                st_llm_secret_key = st.text_input(
                    tr("Secret Key"), value=llm_secret_key, type="password"
                )
                config.app[f"{llm_provider}_secret_key"] = st_llm_secret_key

            if llm_provider == "cloudflare":
                st_llm_account_id = st.text_input(
                    tr("Account ID"), value=llm_account_id
                )
                if st_llm_account_id:
                    config.app[f"{llm_provider}_account_id"] = st_llm_account_id

        # 右侧面板 - API 密钥设置
        with right_config_panel:

            def get_keys_from_config(cfg_key):
                api_keys = config.app.get(cfg_key, [])
                if isinstance(api_keys, str):
                    api_keys = [api_keys]
                api_key = ", ".join(api_keys)
                return api_key

            def save_keys_to_config(cfg_key, value):
                value = value.replace(" ", "")
                if value:
                    config.app[cfg_key] = value.split(",")

            st.write(tr("Video Source Settings"))

            pexels_api_key = get_keys_from_config("pexels_api_keys")
            pexels_api_key = st.text_input(
                tr("Pexels API Key"), value=pexels_api_key, type="password"
            )
            save_keys_to_config("pexels_api_keys", pexels_api_key)

            pixabay_api_key = get_keys_from_config("pixabay_api_keys")
            pixabay_api_key = st.text_input(
                tr("Pixabay API Key"), value=pixabay_api_key, type="password"
            )
            save_keys_to_config("pixabay_api_keys", pixabay_api_key)

llm_provider = config.app.get("llm_provider", "").lower()
panel = st.columns(3)
left_panel = panel[0]
middle_panel = panel[1]
right_panel = panel[2]

params = VideoParams(video_subject="")
set_params_runtime_field(params, "restaurant_mode", True)
uploaded_files = []
uploaded_audio_file = None
restaurant_ui_checks = None

with left_panel:
    with st.container(border=True):
        st.write(tr("Video Script Settings"))
        params.video_subject = st.text_input(
            tr("Video Subject"),
            key="video_subject",
        ).strip()

        set_params_runtime_field(
            params,
            "target_duration_seconds",
            st.selectbox(
                "目标视频时长",
                options=RESTAURANT_TARGET_DURATIONS,
                index=0,
                format_func=lambda seconds: f"{seconds}秒",
            ),
        )
        set_params_runtime_field(params, "video_language", "zh-CN")
        params.paragraph_number = 1
        params.video_script_prompt = ""
        params.custom_system_prompt = ""

        min_script_chars, max_script_chars = get_restaurant_script_char_range(
            params.target_duration_seconds
        )
        st.caption(
            f"AI 将按目标视频时长生成约 {min_script_chars}–{max_script_chars} 个中文字符的旁白文案。"
        )

        if st.button(
            tr("Generate Video Script and Keywords"), key="auto_generate_script"
        ):
            with st.spinner(tr("Generating Video Script and Keywords")):
                script_prompt = params.video_script_prompt
                if getattr(params, "restaurant_mode", False):
                    script_prompt = build_restaurant_script_prompt(params)
                script = llm.generate_script(
                    video_subject=params.video_subject,
                    language=params.video_language,
                    paragraph_number=params.paragraph_number,
                    video_script_prompt=script_prompt,
                    custom_system_prompt=params.custom_system_prompt,
                )
                if "Error: " in script:
                    st.error(tr(script))
                else:
                    if getattr(params, "restaurant_mode", False):
                        script, final_cjk_count, revised = revise_restaurant_script_if_needed(
                            script, params
                        )
                        min_chars, max_chars = get_restaurant_script_char_range(
                            params.target_duration_seconds
                        )
                        script, adjustment_note = normalize_restaurant_script_length(
                            script, min_chars, max_chars
                        )
                        script, was_clamped = clamp_script_to_max_cjk_chars(
                            script, max_chars
                        )
                        final_cjk_count = count_cjk_chars(script)
                        if adjustment_note == "local_extended":
                            st.info("已根据目标时长自动扩写文案，使其更接近推荐字数范围。")
                        elif adjustment_note == "local_trimmed":
                            st.info("已根据目标时长自动压缩文案，使其更接近推荐字数范围。")
                        if was_clamped:
                            st.info("已根据目标时长自动截断文案，使其不超过最大允许字数。")
                        st.caption(f"AI 文案中文字符数：{final_cjk_count}")
                        if final_cjk_count < min_chars or final_cjk_count > max_chars:
                            st.error("AI 文案仍未完全落入推荐范围，请手动微调后再生成。")
                    st.session_state["video_script"] = script
                    st.session_state["video_script_input"] = script
                    terms = llm.generate_terms(params.video_subject, script)
                    if "Error: " in terms:
                        st.warning("视频文案已生成，但关键词生成失败；将使用本地默认关键词继续。")
                        if not st.session_state.get("video_terms"):
                            st.session_state["video_terms"] = build_local_restaurant_video_terms(
                                params.video_subject
                            )
                    else:
                        st.session_state["video_terms"] = ", ".join(terms)
        if getattr(params, "restaurant_mode", False):
            if st.session_state.get("video_script_input", "") != st.session_state.get(
                "video_script", ""
            ):
                st.session_state["video_script_input"] = st.session_state["video_script"]
            st.markdown(
                '<div id="restaurant-video-script-anchor"></div>',
                unsafe_allow_html=True,
            )
        script_input = st.text_area(
            tr("Video Script"),
            key="video_script_input",
            height=280,
            on_change=sync_video_script_input,
            args=(max_script_chars if getattr(params, "restaurant_mode", False) else None,),
        )
        if getattr(params, "restaurant_mode", False):
            if st.session_state.pop("video_script_was_clamped", False):
                st.warning("文案已自动截断到当前目标视频时长允许的最大字数。")
            backend_script, backend_was_clamped = clamp_script_to_max_cjk_chars(
                script_input, max_script_chars
            )
            params.video_script = backend_script
            st.session_state["video_script"] = backend_script
            if backend_was_clamped:
                st.warning(
                    "文案超过最大中文字符数，已启用后端兜底；前端输入框会同步限制超出内容。"
                )
            current_script_chars = count_cjk_chars(params.video_script)
            if current_script_chars < min_script_chars:
                counter_note = f"还差 {min_script_chars - current_script_chars} 字"
                counter_color = "#f59e0b"
            elif current_script_chars >= max_script_chars:
                counter_note = "已达上限"
                counter_color = "#ef4444"
            else:
                counter_note = f"还可输入 {max_script_chars - current_script_chars} 字"
                counter_color = "#22c55e"
            st.markdown(
                f"""
                <div id="restaurant-video-script-live-counter"
                     style="text-align: right; font-size: 0.9rem; color: {counter_color}; margin-top: -0.25rem;">
                    当前中文字符数：{current_script_chars} / 推荐范围：{min_script_chars}–{max_script_chars}（{counter_note}）
                </div>
                """,
                unsafe_allow_html=True,
            )
            install_weibo_style_script_limiter(min_script_chars, max_script_chars)
        else:
            params.video_script = script_input
            st.session_state["video_script"] = script_input
        if getattr(params, "restaurant_mode", False):
            params.video_terms = st.session_state.get("video_terms", "")
        else:
            if st.button(tr("Generate Video Keywords"), key="auto_generate_terms"):
                if not params.video_script:
                    st.error(tr("Please Enter the Video Subject"))
                    st.stop()

                with st.spinner(tr("Generating Video Keywords")):
                    terms = llm.generate_terms(params.video_subject, params.video_script)
                    if "Error: " in terms:
                        st.error(tr(terms))
                    else:
                        st.session_state["video_terms"] = ", ".join(terms)

            params.video_terms = st.text_area(
                tr("Video Keywords"), value=st.session_state["video_terms"]
            )

with middle_panel:
    with st.container(border=True):
        st.write(tr("Video Settings"))
        video_concat_modes = [
            (tr("Sequential"), "sequential"),
            (tr("Random"), "random"),
        ]
        video_sources = [
            (tr("Pexels"), "pexels"),
            (tr("Pixabay"), "pixabay"),
            (tr("Local file"), "local"),
            (tr("TikTok"), "douyin"),
            (tr("Bilibili"), "bilibili"),
            (tr("Xiaohongshu"), "xiaohongshu"),
        ]

        restaurant_mode = getattr(params, "restaurant_mode", True)
        set_params_runtime_field(params, "restaurant_mode", True)

        if restaurant_mode:
            video_aspect_ratios = [
                (tr("Portrait"), VideoAspect.portrait.value),
                (tr("Landscape"), VideoAspect.landscape.value),
            ]
            selected_aspect_index = st.selectbox(
                tr("Video Ratio"),
                options=range(len(video_aspect_ratios)),
                format_func=lambda x: video_aspect_ratios[x][0],
                index=0,
            )
            params.video_aspect = VideoAspect(video_aspect_ratios[selected_aspect_index][1])

            # Streamlit 的文件类型校验对扩展名大小写敏感，这里同时放行大小写两种形式。
            local_file_types = ["mp4", "mov", "avi", "flv", "mkv", "jpg", "jpeg", "png"]
            uploaded_files = st.file_uploader(
                tr("Upload Local Files"),
                type=local_file_types + [file_type.upper() for file_type in local_file_types],
                accept_multiple_files=True,
            )
            image_count = get_restaurant_image_count(
                uploaded_files, st.session_state["local_video_materials"]
            )
            lock_restaurant_video_params(params, image_count)
            if image_count:
                st.write(
                    f"视频片段最大时长：{params.video_clip_duration} 秒（根据目标时长和图片数量自动计算）"
                )
                st.write(
                    f"图片总覆盖时长：{image_count} 张 × {params.video_clip_duration} 秒 = "
                    f"{image_count * params.video_clip_duration} 秒"
                )
            else:
                st.write("视频片段最大时长：上传图片后自动计算。")
            restaurant_ui_checks = show_restaurant_mode_guidance(
                params=params,
                uploaded_files=uploaded_files,
                persisted_materials=st.session_state["local_video_materials"],
            )
            config.app["video_source"] = "local"
        else:
            saved_video_source_name = config.app.get("video_source", "pexels")
            saved_video_source_index = [v[1] for v in video_sources].index(
                saved_video_source_name
            )

            selected_index = st.selectbox(
                tr("Video Source"),
                options=range(len(video_sources)),
                format_func=lambda x: video_sources[x][0],
                index=saved_video_source_index,
            )
            params.video_source = video_sources[selected_index][1]
            config.app["video_source"] = params.video_source

            if params.video_source == "local":
                # Streamlit 的文件类型校验对扩展名大小写敏感，这里同时放行大小写两种形式。
                local_file_types = ["mp4", "mov", "avi", "flv", "mkv", "jpg", "jpeg", "png"]
                uploaded_files = st.file_uploader(
                    tr("Upload Local Files"),
                    type=local_file_types + [file_type.upper() for file_type in local_file_types],
                    accept_multiple_files=True,
                )

            selected_index = st.selectbox(
                tr("Video Concat Mode"),
                index=1,
                options=range(
                    len(video_concat_modes)
                ),  # Use the index as the internal option value
                format_func=lambda x: video_concat_modes[x][
                    0
                ],  # The label is displayed to the user
            )
            params.video_concat_mode = VideoConcatMode(
                video_concat_modes[selected_index][1]
            )

        # 视频转场模式
        video_transition_modes = [
            (tr("None"), VideoTransitionMode.none.value),
            (tr("Shuffle"), VideoTransitionMode.shuffle.value),
            (tr("FadeIn"), VideoTransitionMode.fade_in.value),
            (tr("FadeOut"), VideoTransitionMode.fade_out.value),
            (tr("SlideIn"), VideoTransitionMode.slide_in.value),
            (tr("SlideOut"), VideoTransitionMode.slide_out.value),
        ]
        selected_index = st.selectbox(
            tr("Video Transition Mode"),
            options=range(len(video_transition_modes)),
            format_func=lambda x: video_transition_modes[x][0],
            index=0,
        )
        params.video_transition_mode = VideoTransitionMode(
            video_transition_modes[selected_index][1]
        )

        if not restaurant_mode:
            video_aspect_ratios = [
                (tr("Portrait"), VideoAspect.portrait.value),
                (tr("Landscape"), VideoAspect.landscape.value),
            ]
            selected_index = st.selectbox(
                tr("Video Ratio"),
                options=range(
                    len(video_aspect_ratios)
                ),  # Use the index as the internal option value
                format_func=lambda x: video_aspect_ratios[x][
                    0
                ],  # The label is displayed to the user
            )
            params.video_aspect = VideoAspect(video_aspect_ratios[selected_index][1])
            params.video_clip_duration = st.selectbox(
                tr("Clip Duration"), options=[2, 3, 4, 5, 6, 7, 8, 9, 10], index=1
            )
            params.video_count = st.selectbox(
                tr("Number of Videos Generated Simultaneously"),
                options=[1, 2, 3, 4, 5],
                index=0,
            )

        with st.expander(tr("Advanced Video Settings"), expanded=False):
            video_codec_options = [
                ("libx264 (CPU)", "libx264"),
                ("NVIDIA NVENC (h264_nvenc)", "h264_nvenc"),
                ("AMD AMF (h264_amf)", "h264_amf"),
                ("Intel QSV (h264_qsv)", "h264_qsv"),
                ("Windows MediaFoundation (h264_mf)", "h264_mf"),
                ("macOS VideoToolbox (h264_videotoolbox)", "h264_videotoolbox"),
            ]
            saved_video_codec = config.app.get("video_codec", "libx264")
            saved_video_codec_values = [item[1] for item in video_codec_options]
            if saved_video_codec not in saved_video_codec_values:
                saved_video_codec = "libx264"
            selected_codec_index = saved_video_codec_values.index(saved_video_codec)
            selected_codec_index = st.selectbox(
                tr("Video Encoder"),
                options=range(len(video_codec_options)),
                index=selected_codec_index,
                format_func=lambda x: video_codec_options[x][0],
                help=tr("Video Encoder Help"),
            )
            config.app["video_codec"] = video_codec_options[selected_codec_index][1]
    with st.container(border=True):
        st.write(tr("Audio Settings"))

        # 添加TTS服务器选择下拉框
        tts_servers = [
            (voice.NO_VOICE_NAME, tr("No Voice")),
            ("azure-tts-v1", "Azure TTS V1"),
            ("azure-tts-v2", "Azure TTS V2"),
            ("siliconflow", "SiliconFlow TTS"),
            ("gemini-tts", "Google Gemini TTS"),
            ("mimo-tts", "Xiaomi MiMo TTS"),
        ]

        # 获取保存的TTS服务器，默认为v1
        saved_tts_server = config.ui.get("tts_server", "azure-tts-v1")
        saved_tts_server_index = 0
        for i, (server_value, _) in enumerate(tts_servers):
            if server_value == saved_tts_server:
                saved_tts_server_index = i
                break

        selected_tts_server_index = st.selectbox(
            tr("TTS Servers"),
            options=range(len(tts_servers)),
            format_func=lambda x: tts_servers[x][1],
            index=saved_tts_server_index,
        )

        selected_tts_server = tts_servers[selected_tts_server_index][0]
        config.ui["tts_server"] = selected_tts_server

        # 根据选择的TTS服务器获取声音列表
        filtered_voices = []

        if selected_tts_server == voice.NO_VOICE_NAME:
            # 无配音是显式模式，只提供一个稳定 sentinel。这样普通 TTS 的空配置
            # 不会被误判为静音，后端也能继续通过同一条音频/字幕流程生成视频。
            filtered_voices = [voice.NO_VOICE_NAME]
        elif selected_tts_server == "siliconflow":
            # 获取硅基流动的声音列表
            filtered_voices = voice.get_siliconflow_voices()
        elif selected_tts_server == "gemini-tts":
            # 获取Gemini TTS的声音列表
            filtered_voices = voice.get_gemini_voices()
        elif selected_tts_server == "mimo-tts":
            # 获取 Xiaomi MiMo TTS 的预置音色列表
            filtered_voices = voice.get_mimo_voices()
        else:
            # 获取Azure的声音列表
            all_voices = voice.get_all_azure_voices(filter_locals=None)

            # 根据选择的TTS服务器筛选声音
            for v in all_voices:
                if selected_tts_server == "azure-tts-v2":
                    # V2版本的声音名称中包含"v2"
                    if "V2" in v:
                        filtered_voices.append(v)
                else:
                    # V1版本的声音名称中不包含"v2"
                    if "V2" not in v:
                        filtered_voices.append(v)

        if selected_tts_server == voice.NO_VOICE_NAME:
            friendly_names = {voice.NO_VOICE_NAME: tr("No Voice")}
        else:
            friendly_names = {
                v: v.replace("Female", tr("Female"))
                .replace("Male", tr("Male"))
                .replace("Neural", "")
                for v in filtered_voices
            }

        saved_voice_name = config.ui.get("voice_name", "")
        saved_voice_name_index = 0

        # 检查保存的声音是否在当前筛选的声音列表中
        if saved_voice_name in friendly_names:
            saved_voice_name_index = list(friendly_names.keys()).index(saved_voice_name)
        else:
            # 如果不在，则根据当前UI语言选择一个默认声音
            for i, v in enumerate(filtered_voices):
                if v.lower().startswith(st.session_state["ui_language"].lower()):
                    saved_voice_name_index = i
                    break

        # 如果没有找到匹配的声音，使用第一个声音
        if saved_voice_name_index >= len(friendly_names) and friendly_names:
            saved_voice_name_index = 0

        # 确保有声音可选
        if friendly_names:
            selected_friendly_name = st.selectbox(
                tr("Speech Synthesis"),
                options=list(friendly_names.values()),
                index=min(saved_voice_name_index, len(friendly_names) - 1)
                if friendly_names
                else 0,
            )

            voice_name = list(friendly_names.keys())[
                list(friendly_names.values()).index(selected_friendly_name)
            ]
            params.voice_name = voice_name
            config.ui["voice_name"] = voice_name
        else:
            # 如果没有声音可选，显示提示信息
            st.warning(
                tr(
                    "No voices available for the selected TTS server. Please select another server."
                )
            )
            params.voice_name = ""
            config.ui["voice_name"] = ""

        # 无配音模式会生成静音占位音频，不展示试听按钮，避免用户误以为需要测试声音。
        if (
            friendly_names
            and selected_tts_server != voice.NO_VOICE_NAME
            and st.button(tr("Play Voice"))
        ):
            play_content = params.video_subject
            if not play_content:
                play_content = params.video_script
            if not play_content:
                play_content = tr("Voice Example")
            with st.spinner(tr("Synthesizing Voice")):
                temp_dir = utils.storage_dir("temp", create=True)
                audio_file = os.path.join(temp_dir, f"tmp-voice-{str(uuid4())}.mp3")
                sub_maker = voice.tts(
                    text=play_content,
                    voice_name=voice_name,
                    voice_rate=params.voice_rate,
                    voice_file=audio_file,
                    voice_volume=params.voice_volume,
                )
                # if the voice file generation failed, try again with a default content.
                if not sub_maker:
                    play_content = "This is a example voice. if you hear this, the voice synthesis failed with the original content."
                    sub_maker = voice.tts(
                        text=play_content,
                        voice_name=voice_name,
                        voice_rate=params.voice_rate,
                        voice_file=audio_file,
                        voice_volume=params.voice_volume,
                    )

                if sub_maker and os.path.exists(audio_file):
                    st.audio(audio_file, format="audio/mp3")
                    if os.path.exists(audio_file):
                        os.remove(audio_file)

        # 当选择V2版本或者声音是V2声音时，显示服务区域和API key输入框
        if selected_tts_server == "azure-tts-v2" or (
            voice_name and voice.is_azure_v2_voice(voice_name)
        ):
            saved_azure_speech_region = config.azure.get("speech_region", "")
            saved_azure_speech_key = config.azure.get("speech_key", "")
            azure_speech_region = st.text_input(
                tr("Speech Region"),
                value=saved_azure_speech_region,
                key="azure_speech_region_input",
            )
            azure_speech_key = st.text_input(
                tr("Speech Key"),
                value=saved_azure_speech_key,
                type="password",
                key="azure_speech_key_input",
            )
            config.azure["speech_region"] = azure_speech_region
            config.azure["speech_key"] = azure_speech_key

        # 当选择硅基流动时，显示API key输入框和说明信息
        if selected_tts_server == "siliconflow" or (
            voice_name and voice.is_siliconflow_voice(voice_name)
        ):
            saved_siliconflow_api_key = config.siliconflow.get("api_key", "")

            siliconflow_api_key = st.text_input(
                tr("SiliconFlow API Key"),
                value=saved_siliconflow_api_key,
                type="password",
                key="siliconflow_api_key_input",
            )

            # 显示硅基流动的说明信息
            st.info(
                tr("SiliconFlow TTS Settings")
                + ":\n"
                + "- "
                + tr("Speed: Range [0.25, 4.0], default is 1.0")
                + "\n"
                + "- "
                + tr("Volume: Uses Speech Volume setting, default 1.0 maps to gain 0")
            )

            config.siliconflow["api_key"] = siliconflow_api_key

        # 当选择 Xiaomi MiMo TTS 时，复用 MiMo LLM provider 的 API Key。
        # 这样用户如果同时使用 MiMo 生成文案和语音，只需要维护一份密钥。
        if selected_tts_server == "mimo-tts" or (
            voice_name and voice.is_mimo_voice(voice_name)
        ):
            saved_mimo_api_key = config.app.get("mimo_api_key", "")

            mimo_api_key = st.text_input(
                tr("MiMo API Key"),
                value=saved_mimo_api_key,
                type="password",
                key="mimo_tts_api_key_input",
            )

            st.info(
                tr("MiMo TTS Settings")
                + ":\n"
                + "- "
                + tr("Uses Xiaomi MiMo V2.5 TTS preset voices")
                + "\n"
                + "- "
                + tr("Speed and volume are currently handled by the provider defaults")
            )

            config.app["mimo_api_key"] = mimo_api_key

        params.voice_volume = st.selectbox(
            tr("Speech Volume"),
            options=[0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, 4.0, 5.0],
            index=2,
        )

        params.voice_rate = st.selectbox(
            tr("Speech Rate"),
            options=[0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.5, 1.8, 2.0],
            index=2,
        )

        custom_audio_file_types = ["mp3", "wav", "m4a", "aac", "flac", "ogg"]
        uploaded_audio_file = st.file_uploader(
            tr("Custom Audio File"),
            type=custom_audio_file_types
            + [file_type.upper() for file_type in custom_audio_file_types],
            accept_multiple_files=False,
            key="custom_audio_file_uploader",
        )
        if uploaded_audio_file:
            st.audio(uploaded_audio_file, format="audio/mp3")
            st.info(
                tr(
                    "Custom audio will be used directly. TTS synthesis will be skipped for this task."
                )
            )

        bgm_options = [
            (tr("No Background Music"), ""),
            (tr("Random Background Music"), "random"),
            (tr("Custom Background Music"), "custom"),
        ]
        selected_index = st.selectbox(
            tr("Background Music"),
            index=1,
            options=range(
                len(bgm_options)
            ),  # Use the index as the internal option value
            format_func=lambda x: bgm_options[x][
                0
            ],  # The label is displayed to the user
        )
        # Get the selected background music type
        params.bgm_type = bgm_options[selected_index][1]

        # Show or hide components based on the selection
        if params.bgm_type == "custom":
            custom_bgm_file = st.text_input(
                tr("Custom Background Music File"), key="custom_bgm_file_input"
            )
            if custom_bgm_file:
                # 这里不直接用 os.path.exists 判断，因为用户常见输入是
                # output000.mp3，这个文件名需要由服务层映射到 resource/songs
                # 目录后再校验。服务层会统一限制目录和文件类型，避免任意路径读取。
                params.bgm_file = custom_bgm_file.strip()
                # st.write(f":red[已选择自定义背景音乐]：**{custom_bgm_file}**")
        params.bgm_volume = st.selectbox(
            tr("Background Music Volume"),
            options=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
            index=2,
        )

with right_panel:
    with st.container(border=True):
        st.write(tr("Subtitle Settings"))
        params.subtitle_enabled = st.checkbox(tr("Enable Subtitles"), value=True)
        font_names = get_all_fonts()
        saved_font_name = config.ui.get("font_name", "MicrosoftYaHeiBold.ttc")
        saved_font_name_index = 0
        if saved_font_name in font_names:
            saved_font_name_index = font_names.index(saved_font_name)
        params.font_name = st.selectbox(
            tr("Font"), font_names, index=saved_font_name_index
        )
        config.ui["font_name"] = params.font_name

        subtitle_positions = [
            (tr("Top"), "top"),
            (tr("Center"), "center"),
            (tr("Bottom"), "bottom"),
            (tr("Custom"), "custom"),
        ]
        saved_subtitle_position = config.ui.get("subtitle_position", "bottom")
        saved_position_index = 2
        for i, (_, pos_value) in enumerate(subtitle_positions):
            if pos_value == saved_subtitle_position:
                saved_position_index = i
                break
        selected_index = st.selectbox(
            tr("Position"),
            index=saved_position_index,
            options=range(len(subtitle_positions)),
            format_func=lambda x: subtitle_positions[x][0],
        )
        params.subtitle_position = subtitle_positions[selected_index][1]
        config.ui["subtitle_position"] = params.subtitle_position

        if params.subtitle_position == "custom":
            saved_custom_position = config.ui.get("custom_position", 70.0)
            custom_position = st.text_input(
                tr("Custom Position (% from top)"),
                value=str(saved_custom_position),
                key="custom_position_input",
            )
            try:
                params.custom_position = float(custom_position)
                if params.custom_position < 0 or params.custom_position > 100:
                    st.error(tr("Please enter a value between 0 and 100"))
                else:
                    config.ui["custom_position"] = params.custom_position
            except ValueError:
                st.error(tr("Please enter a valid number"))

        font_cols = st.columns([0.3, 0.7])
        with font_cols[0]:
            saved_text_fore_color = config.ui.get("text_fore_color", "#FFFFFF")
            params.text_fore_color = st.color_picker(
                tr("Font Color"), saved_text_fore_color
            )
            config.ui["text_fore_color"] = params.text_fore_color

        with font_cols[1]:
            saved_font_size = config.ui.get("font_size", 60)
            params.font_size = st.slider(tr("Font Size"), 30, 100, saved_font_size)
            config.ui["font_size"] = params.font_size

        stroke_cols = st.columns([0.3, 0.7])
        with stroke_cols[0]:
            params.stroke_color = st.color_picker(tr("Stroke Color"), "#000000")
        with stroke_cols[1]:
            params.stroke_width = st.slider(tr("Stroke Width"), 0.0, 10.0, 1.5)

        subtitle_bg_cols = st.columns([0.4, 0.6])
        saved_subtitle_background_enabled = config.ui.get(
            "subtitle_background_enabled", True
        )
        with subtitle_bg_cols[0]:
            subtitle_background_enabled = st.checkbox(
                tr("Enable Subtitle Background"),
                value=saved_subtitle_background_enabled,
            )
        config.ui["subtitle_background_enabled"] = subtitle_background_enabled
        if subtitle_background_enabled:
            with subtitle_bg_cols[1]:
                saved_subtitle_background_color = config.ui.get(
                    "subtitle_background_color", "#000000"
                )
                params.text_background_color = st.color_picker(
                    tr("Subtitle Background Color"),
                    saved_subtitle_background_color,
                )
                config.ui["subtitle_background_color"] = params.text_background_color
        else:
            params.text_background_color = False

        saved_rounded_subtitle_background = config.ui.get(
            "rounded_subtitle_background", False
        )
        # 背景关闭时，圆角背景没有可渲染的底色。这里禁用控件并保留原配置，
        # 用户下次重新开启字幕背景后，可以继续使用之前保存的圆角偏好。
        params.rounded_subtitle_background = st.checkbox(
            tr("Rounded Subtitle Background"),
            value=(
                saved_rounded_subtitle_background
                if subtitle_background_enabled
                else False
            ),
            help=tr("Rounded Subtitle Background Help"),
            disabled=not subtitle_background_enabled,
        )
        if subtitle_background_enabled:
            config.ui["rounded_subtitle_background"] = (
                params.rounded_subtitle_background
            )
    with st.expander(tr("Click to show API Key management"), expanded=False):
        st.subheader(tr("Manage Pexels and Pixabay API Keys"))

        col1, col2 = st.tabs([tr("Pexels API Keys"), tr("Pixabay API Keys")])

        with col1:
            st.subheader(tr("Pexels API Keys"))
            if config.app["pexels_api_keys"]:
                st.write(tr("Current Keys:"))
                for key in config.app["pexels_api_keys"]:
                    st.code(key)
            else:
                st.info(tr("No Pexels API Keys currently"))

            new_key = st.text_input(tr("Add Pexels API Key"), key="pexels_new_key")
            if st.button(tr("Add Pexels API Key")):
                if new_key and new_key not in config.app["pexels_api_keys"]:
                    config.app["pexels_api_keys"].append(new_key)
                    config.save_config()
                    st.success(tr("Pexels API Key added successfully"))
                elif new_key in config.app["pexels_api_keys"]:
                    st.warning(tr("This API Key already exists"))
                else:
                    st.error(tr("Please enter a valid API Key"))

            if config.app["pexels_api_keys"]:
                delete_key = st.selectbox(
                    tr("Select Pexels API Key to delete"), config.app["pexels_api_keys"], key="pexels_delete_key"
                )
                if st.button(tr("Delete Selected Pexels API Key")):
                    config.app["pexels_api_keys"].remove(delete_key)
                    config.save_config()
                    st.success(tr("Pexels API Key deleted successfully"))

        with col2:
            st.subheader(tr("Pixabay API Keys"))

            if config.app["pixabay_api_keys"]:
                st.write(tr("Current Keys:"))
                for key in config.app["pixabay_api_keys"]:
                    st.code(key)
            else:
                st.info(tr("No Pixabay API Keys currently"))

            new_key = st.text_input(tr("Add Pixabay API Key"), key="pixabay_new_key")
            if st.button(tr("Add Pixabay API Key")):
                if new_key and new_key not in config.app["pixabay_api_keys"]:
                    config.app["pixabay_api_keys"].append(new_key)
                    config.save_config()
                    st.success(tr("Pixabay API Key added successfully"))
                elif new_key in config.app["pixabay_api_keys"]:
                    st.warning(tr("This API Key already exists"))
                else:
                    st.error(tr("Please enter a valid API Key"))

            if config.app["pixabay_api_keys"]:
                delete_key = st.selectbox(
                    tr("Select Pixabay API Key to delete"), config.app["pixabay_api_keys"], key="pixabay_delete_key"
                )
                if st.button(tr("Delete Selected Pixabay API Key")):
                    config.app["pixabay_api_keys"].remove(delete_key)
                    config.save_config()
                    st.success(tr("Pixabay API Key deleted successfully"))

restaurant_can_generate = True
restaurant_generate_blockers = []
if getattr(params, "restaurant_mode", False):
    min_chars, max_chars = get_restaurant_script_char_range(
        params.target_duration_seconds
    )
    current_cjk_count = count_cjk_chars(params.video_script)
    script_length_ok = min_chars <= current_cjk_count <= max_chars
    if current_cjk_count < min_chars:
        restaurant_generate_blockers.append(
            f"生成前请先补足文案字数，还差 {min_chars - current_cjk_count} 个中文字符。"
        )
    elif current_cjk_count > max_chars:
        restaurant_generate_blockers.append(
            f"生成前请先缩短文案字数，已超出 {current_cjk_count - max_chars} 个中文字符。"
        )

    image_count = (
        restaurant_ui_checks.get("image_count", 0)
        if restaurant_ui_checks
        else get_restaurant_image_count(
            uploaded_files, st.session_state["local_video_materials"]
        )
    )
    min_images = (
        restaurant_ui_checks.get("min_images", 0)
        if restaurant_ui_checks
        else get_restaurant_image_range(params.target_duration_seconds)[0]
    )
    image_count_ok = image_count >= min_images
    if not image_count_ok:
        restaurant_generate_blockers.append(
            f"生成前请先上传足够图片，目标 {params.target_duration_seconds} 秒至少需要 "
            f"{min_images} 张；当前 {image_count} 张。"
        )

    restaurant_can_generate = script_length_ok and image_count_ok

for blocker in restaurant_generate_blockers:
    st.error(blocker)

start_button = st.button(
    tr("Generate Video"),
    use_container_width=True,
    type="primary",
    disabled=not restaurant_can_generate,
)
if start_button:
    config.save_config()
    task_id = str(uuid4())
    if not params.video_subject and not params.video_script:
        st.error(tr("Video Script and Subject Cannot Both Be Empty"))
        scroll_to_bottom()
        st.stop()

    if getattr(params, "restaurant_mode", False):
        image_count = get_restaurant_image_count(
            uploaded_files, st.session_state["local_video_materials"]
        )
        lock_restaurant_video_params(params, image_count)
        if not params.video_terms:
            params.video_terms = build_local_restaurant_video_terms(params.video_subject)
            st.session_state["video_terms"] = params.video_terms
        min_chars, max_chars = get_restaurant_script_char_range(
            params.target_duration_seconds
        )
        cjk_count = count_cjk_chars(params.video_script)
        if cjk_count < min_chars:
            st.error(
                f"当前文案偏短，还差 {min_chars - cjk_count} 个中文字符。请补足后再生成。"
            )
            scroll_to_bottom()
            st.stop()
        if cjk_count > max_chars:
            st.error(
                f"当前文案偏长，已超出 {cjk_count - max_chars} 个中文字符。请缩短后再生成。"
            )
            scroll_to_bottom()
            st.stop()

    if params.video_source not in ["pexels", "pixabay", "local"]:
        st.error(tr("Please Select a Valid Video Source"))
        scroll_to_bottom()
        st.stop()

    if params.video_source == "pexels" and not config.app.get("pexels_api_keys", ""):
        st.error(tr("Please Enter the Pexels API Key"))
        scroll_to_bottom()
        st.stop()

    if params.video_source == "pixabay" and not config.app.get("pixabay_api_keys", ""):
        st.error(tr("Please Enter the Pixabay API Key"))
        scroll_to_bottom()
        st.stop()

    if getattr(params, "restaurant_mode", False) and params.video_source == "local":
        restaurant_checks = show_restaurant_mode_guidance(
            params=params,
            uploaded_files=uploaded_files,
            persisted_materials=st.session_state["local_video_materials"],
        )
        if restaurant_checks["image_count"] < restaurant_checks["min_images"]:
            st.error(
                f"餐厅视频模式目标 {params.target_duration_seconds} 秒至少需要 "
                f"{restaurant_checks['min_images']} 张图片；当前只有 "
                f"{restaurant_checks['image_count']} 张。请补充图片后再生成。"
            )
            scroll_to_bottom()
            st.stop()

    if uploaded_audio_file:
        task_dir = utils.task_dir(task_id)
        # 上传文件名来自浏览器，不能直接拼到磁盘路径里；这里只保留扩展名，
        # 并使用固定文件名保存到当前任务目录，避免路径穿越或特殊字符问题。
        _, audio_ext = os.path.splitext(os.path.basename(uploaded_audio_file.name))
        audio_ext = audio_ext.lower() or ".mp3"
        custom_audio_path = os.path.join(task_dir, f"custom-audio{audio_ext}")
        with open(custom_audio_path, "wb") as f:
            f.write(uploaded_audio_file.getbuffer())
        params.custom_audio_file = custom_audio_path

    if uploaded_files:
        local_videos_dir = utils.storage_dir("local_videos", create=True)
        # 每次重新上传时都以本次选择的素材为准，避免旧素材不断重复追加。
        params.video_materials = []
        persisted_local_materials = []
        for file in uploaded_files:
            file_path = os.path.join(local_videos_dir, f"{file.file_id}_{file.name}")
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
                m = MaterialInfo()
                m.provider = "local"
                m.url = file_path
                params.video_materials.append(m)
                persisted_local_materials.append(
                    {
                        "provider": m.provider,
                        "url": m.url,
                        "duration": m.duration,
                    }
                )
        # 将已上传并保存到本地的视频素材写入会话，供后续只改文案时直接复用。
        st.session_state["local_video_materials"] = persisted_local_materials
    elif params.video_source == "local" and st.session_state["local_video_materials"]:
        # 当用户没有重新上传文件时，复用最近一次已经保存到磁盘的本地素材列表。
        params.video_materials = []
        for material in st.session_state["local_video_materials"]:
            m = MaterialInfo()
            m.provider = material.get("provider", "local")
            m.url = material.get("url", "")
            m.duration = material.get("duration", 0)
            if m.url:
                params.video_materials.append(m)

    log_container = st.empty()
    log_records = []

    def log_received(msg):
        if config.ui["hide_log"]:
            return
        with log_container:
            log_records.append(msg)
            st.code("\n".join(log_records))

    logger.add(log_received)

    st.toast(tr("Generating Video"))
    logger.info(tr("Start Generating Video"))
    logger.info(utils.to_json(params))
    scroll_to_bottom()

    result = tm.start(task_id=task_id, params=params)
    if not result or "videos" not in result:
        st.error(tr("Video Generation Failed"))
        logger.error(tr("Video Generation Failed"))
        scroll_to_bottom()
        st.stop()

    video_files = result.get("videos", [])
    st.success(tr("Video Generation Completed"))
    try:
        if video_files:
            player_cols = st.columns(len(video_files) * 2 + 1)
            for i, url in enumerate(video_files):
                player_cols[i * 2 + 1].video(url)
    except Exception:
        pass

    open_task_folder(task_id)
    logger.info(tr("Video Generation Completed"))
    scroll_to_bottom()

config.save_config()
