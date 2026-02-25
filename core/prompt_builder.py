"""Prompt template assembly — single-string template."""
from __future__ import annotations

from pathlib import Path

DEFAULT_INSTRUCTION = (
    "Сгенерируй YAML-файл отчёта на основе предоставленной структуры, "
    "шагов и кода программы.\n"
    "Используй тот же формат блоков (heading, paragraph, image, table) "
    "что и в референсном YAML.\n"
    "Картинки указывай через путь image: в блоках type: image.\n"
    "Текст — грамотный, академический стиль."
)

PROMPT_TEMPLATE = """\
Yaml референсного docx файла:
{yaml_ref}

Шаги для отчёта:
{steps}

Код программы:
{scripts}

{instruction}\
"""


def build_prompt(
    yaml_text: str,
    steps: list[dict],
    script_paths: list[str],
    instruction: str,
) -> str:
    # ── steps ──
    lines: list[str] = []
    for st in steps:
        lines.append(st.get("text", ""))
        img = st.get("image")
        if img:
            lines.append(f"image: /image/{Path(img).name}")
        lines.append("")
    steps_txt = "\n".join(lines).strip()

    # ── scripts ──
    sc_parts: list[str] = []
    for fp in script_paths:
        p = Path(fp)
        if p.exists():
            sc_parts.append(f"# === {p.name} ===\n{p.read_text('utf-8')}")
    scripts_txt = "\n\n".join(sc_parts)

    return PROMPT_TEMPLATE.format(
        yaml_ref=yaml_text,
        steps=steps_txt,
        scripts=scripts_txt,
        instruction=instruction,
    )