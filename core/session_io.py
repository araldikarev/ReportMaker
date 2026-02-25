from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


SESSION_YAML_NAME = "session.yaml"
PROMPT_TXT_NAME = "prompt.txt"
RESPONSE_YAML_NAME = "response.yaml"


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def create_session_dir(sessions_dir: Path, prefix: str = "session") -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = sessions_dir / f"{prefix}_{ts}"
    out = base
    i = 1
    while out.exists():
        i += 1
        out = sessions_dir / f"{prefix}_{ts}_{i}"
    out.mkdir(parents=True, exist_ok=True)
    return out


def list_sessions_any(sessions_dir: Path) -> list[Path]:
    """
    Возвращает список "точек входа" сессий:
    - для новых: путь к session.yaml
    - для старых: путь к папке с response.yaml
    """
    if not sessions_dir.exists():
        return []

    entries: list[Path] = []
    for d in sessions_dir.iterdir():
        if not d.is_dir():
            continue
        if (d / SESSION_YAML_NAME).exists():
            entries.append(d / SESSION_YAML_NAME)
        elif (d / RESPONSE_YAML_NAME).exists():
            entries.append(d)  # legacy

    # новые сверху (как правило timestamp в имени)
    return sorted(entries, reverse=True)

def load_legacy_session(session_dir: Path) -> dict[str, Any]:
    """
    Старый формат: <dir>/response.yaml + <dir>/image/*
    Восстанавливаем минимум: response_text + картинки (как шаги без текста).
    """
    session_dir = Path(session_dir)
    resp = session_dir / RESPONSE_YAML_NAME
    resp_text = resp.read_text(encoding="utf-8") if resp.exists() else None

    steps: list[dict[str, Any]] = []
    img_dir = session_dir / "image"
    if img_dir.exists():
        for p in sorted(img_dir.iterdir()):
            if p.is_file():
                steps.append({"text": "", "image": str(Path("image") / p.name)})

    prompt_text = None
    pt = session_dir / PROMPT_TXT_NAME
    if pt.exists():
        prompt_text = pt.read_text(encoding="utf-8")

    return {
        "__session_dir__": str(session_dir),
        "meta": {"version": 0, "legacy": True},
        "yaml_ref": {"abs": None, "rel": None},
        "template_docx": None,
        "instruction": "",
        "scripts": [],
        "steps": steps,
        "files": {},
        "prompt_text": prompt_text,
        "response_text": resp_text,
    }


def load_session_any(entry: Path) -> dict[str, Any]:
    """
    entry: либо session.yaml (новый формат), либо папка (legacy)
    """
    entry = Path(entry)
    if entry.is_dir():
        return load_legacy_session(entry)

    # новый формат — как раньше
    raw = yaml.safe_load(entry.read_text(encoding="utf-8")) or {}
    session_dir = entry.parent

    files = raw.get("files") or {}
    prompt_text = None
    resp_text = None

    p = files.get("prompt")
    if p and (session_dir / p).exists():
        prompt_text = (session_dir / p).read_text(encoding="utf-8")

    r = files.get("response")
    if r and (session_dir / r).exists():
        resp_text = (session_dir / r).read_text(encoding="utf-8")

    raw["__session_dir__"] = str(session_dir)
    raw["prompt_text"] = prompt_text
    raw["response_text"] = resp_text
    return raw

def list_session_yamls(sessions_dir: Path) -> list[Path]:
    if not sessions_dir.exists():
        return []
    items = sorted(sessions_dir.rglob(SESSION_YAML_NAME))
    # newest first by folder name (timestamp-based)
    return sorted(items, reverse=True)


def _copy_step_images_into_session(
    session_dir: Path, steps: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """
    Copies step images (if any) into <session>/image.
    Returns a NEW steps list where image paths are rewritten to relative: image/<name>.
    """
    out_steps: list[dict[str, Any]] = []
    img_dir = session_dir / "image"
    img_dir.mkdir(parents=True, exist_ok=True)

    for st in steps:
        st2 = dict(st)
        img = st2.get("image")
        if img:
            p = Path(str(img))
            if p.exists() and p.is_file():
                dst = img_dir / p.name
                if p.resolve() != dst.resolve():
                    shutil.copy2(p, dst)
                st2["image"] = str(Path("image") / p.name)
            else:
                # keep as-is (might be relative already, or missing)
                st2["image"] = str(img)
        out_steps.append(st2)

    return out_steps


def save_session(
    session_dir: Path,
    *,
    yaml_ref_path: str | None,
    yaml_ref_rel: str | None,
    template_docx: str | None,
    instruction: str,
    scripts: list[str],
    steps: list[dict[str, Any]],
    prompt_text: str | None,
    response_text: str | None,
) -> Path:
    """
    Writes:
      - <session>/session.yaml
      - <session>/prompt.txt (optional)
      - <session>/response.yaml (optional)
      - copies images into <session>/image/
    Returns path to <session>/session.yaml
    """
    session_dir.mkdir(parents=True, exist_ok=True)

    steps_saved = _copy_step_images_into_session(session_dir, steps)

    files: dict[str, str] = {}
    if prompt_text is not None:
        (session_dir / PROMPT_TXT_NAME).write_text(prompt_text, encoding="utf-8")
        files["prompt"] = PROMPT_TXT_NAME

    if response_text is not None:
        (session_dir / RESPONSE_YAML_NAME).write_text(
            response_text, encoding="utf-8"
        )
        files["response"] = RESPONSE_YAML_NAME

    data: dict[str, Any] = {
        "meta": {
            "version": 1,
            "updated_at": _now_iso(),
        },
        "yaml_ref": {
            "abs": yaml_ref_path,
            "rel": yaml_ref_rel,
        },
        "template_docx": template_docx,
        "instruction": instruction,
        "scripts": scripts,
        "steps": steps_saved,
        "files": files,
    }

    out = session_dir / SESSION_YAML_NAME
    out.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return out


def load_session(session_yaml: Path) -> dict[str, Any]:
    """
    Loads session.yaml, and (if present) reads prompt.txt / response.yaml into fields:
      - prompt_text
      - response_text
    Returns a dict with parsed fields.
    """
    session_yaml = Path(session_yaml)
    session_dir = session_yaml.parent

    raw = yaml.safe_load(session_yaml.read_text(encoding="utf-8")) or {}
    files = raw.get("files") or {}

    prompt_text = None
    resp_text = None

    p = files.get("prompt")
    if p and (session_dir / p).exists():
        prompt_text = (session_dir / p).read_text(encoding="utf-8")

    r = files.get("response")
    if r and (session_dir / r).exists():
        resp_text = (session_dir / r).read_text(encoding="utf-8")

    raw["__session_dir__"] = str(session_dir)
    raw["prompt_text"] = prompt_text
    raw["response_text"] = resp_text
    return raw