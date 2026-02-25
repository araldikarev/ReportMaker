"""Prompt template assembly — single-string template."""
from __future__ import annotations

from pathlib import Path

DEFAULT_INSTRUCTION = (
    "Так вот, задача такая - напиши НОВЫЙ yaml, который ИДЕАЛЬНО копирует мои сообщения (1 сообщения - 1 шаг с текстом и ниже картинкой с подписью в нужных стилях!!!) и преобразит их в новый отчёт. Твоя задача - лишь адаптировать МОЙ стиль (из моего прошлого отчёта) и идеально его скопировать, составляя новый."
    "Важное замечание - картинки указаны к каждому шагу. Если не указаны - пиши замещающий текст (Картинка X) со стилем изображения, а я сам всё доставлю."
    "Условились?"
    "yaml присылай в ```."
)

PROMPT_TEMPLATE = """
Изучи лабу. затем:

Смотри - у меня есть yaml - это твой код, как ты кодишь мне отчёты:
{yaml_ref}

Теперь посмотри на шаги - в каждом шаге там есть Картинка (путь к ней указан под текстом):
{steps}

И вот код программы:
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
            lines.append(f"image: image/{Path(img).name}")
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