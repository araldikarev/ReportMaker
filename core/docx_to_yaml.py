"""DOCX → YAML conversion."""
from __future__ import annotations

import re
from pathlib import Path

import yaml
from docx import Document

_NS_BLIP = "{http://schemas.openxmlformats.org/drawingml/2006/main}blip"
_NS_EMBED = (
    "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
)


def _iter_block_items(doc: Document):
    from docx.oxml.table import CT_Tbl
    from docx.oxml.text.paragraph import CT_P
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    for child in doc.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, doc)
        elif isinstance(child, CT_Tbl):
            yield Table(child, doc)


def _extract_images(paragraph, out_dir: Path) -> list[str]:
    imgs: list[str] = []
    for run in paragraph.runs:
        for blip in run._element.findall(f".//{_NS_BLIP}"):
            rId = blip.get(_NS_EMBED)
            if not rId:
                continue
            part = paragraph.part.related_parts[rId]
            ext = part.filename.split(".")[-1].lower()
            out_dir.mkdir(parents=True, exist_ok=True)
            idx = len(list(out_dir.glob("img_*"))) + 1
            fname = f"img_{idx:04d}.{ext}"
            (out_dir / fname).write_bytes(part.blob)
            imgs.append(str(Path("media") / fname))
    return imgs


def _looks_like_caption(p) -> bool:
    sn = (p.style.name if p.style else "") or ""
    txt = p.text.strip()
    if "Caption" in sn or "Подпись" in sn:
        return True
    return bool(re.match(r"^(Рисунок|Рис\.)\s*\d+", txt))


def parse_docx_to_yaml(docx_path: str, out_yaml: str) -> str:
    """Parse *docx_path* → write YAML to *out_yaml*, return YAML text."""
    doc = Document(str(docx_path))
    out_dir = Path(out_yaml).parent
    media_dir = out_dir / "media"

    blocks: list[dict] = []
    pend: int | None = None

    for item in _iter_block_items(doc):
        if item.__class__.__name__ == "Table":
            rows = [[c.text for c in r.cells] for r in item.rows]
            st = None
            if hasattr(item, "style") and item.style:
                st = item.style.name
            blocks.append({"type": "table", "style": st, "rows": rows})
            pend = None
            continue

        p = item
        imgs = _extract_images(p, media_dir)
        if imgs:
            for src in imgs:
                blocks.append(
                    {
                        "type": "image",
                        "src": src,
                        "width_mm": None,
                        "style": None,
                        "caption": None,
                    }
                )
                pend = len(blocks) - 1
            continue

        if _looks_like_caption(p) and pend is not None:
            blocks[pend]["caption"] = {
                "text": p.text.strip(),
                "style": p.style.name if p.style else None,
            }
            pend = None
            continue

        pend = None
        sn = p.style.name if p.style else None
        text = p.text

        if sn and (sn.lower().startswith("heading") or "Заголовок" in sn):
            m = re.search(r"(\d+)", sn)
            blocks.append(
                {
                    "type": "heading",
                    "level": int(m.group(1)) if m else 1,
                    "text": text,
                    "style": sn,
                }
            )
        elif text.strip():
            blocks.append({"type": "paragraph", "text": text, "style": sn})

    data = {"meta": {"source": Path(docx_path).name}, "blocks": blocks}
    yaml_text = yaml.safe_dump(data, allow_unicode=True, sort_keys=False)
    Path(out_yaml).parent.mkdir(parents=True, exist_ok=True)
    Path(out_yaml).write_text(yaml_text, encoding="utf-8")
    return yaml_text