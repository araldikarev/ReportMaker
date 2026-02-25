from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)

from core.paths import IMAGES_DIR
from ui import icons


def _is_image_path(p: Path) -> bool:
    return p.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff", ".webp"}


def _unique_image_name(prefix: str = "step") -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}_{ts}.png"


class StepTextEdit(QPlainTextEdit):
    """
    TextEdit для шага.
    Если в буфере обмена картинка — Ctrl+V сохранит её в data/images и привяжет к шагу.
    """

    def __init__(self, owner_step: "StepCard"):
        super().__init__()
        self._owner = owner_step

    def insertFromMimeData(self, source):  # type: ignore[override]
        # 1) Clipboard image (скриншот)
        if source and source.hasImage():
            img = source.imageData()
            # imageData может быть QImage или QPixmap; приводим к QImage
            if isinstance(img, QImage):
                qimg = img
            else:
                # QPixmap -> QImage (на всякий)
                try:
                    qimg = img.toImage()
                except Exception:
                    qimg = None

            if qimg and not qimg.isNull():
                IMAGES_DIR.mkdir(parents=True, exist_ok=True)
                out = IMAGES_DIR / _unique_image_name(prefix=f"step{self._owner.idx}")
                ok = qimg.save(str(out), "PNG")
                if ok:
                    self._owner.attach_image(out)
                    return  # не вставляем мусорный текст в поле
                # если не удалось сохранить — падаем в стандартную вставку

        # 2) Clipboard urls/files (вставка пути/файла картинки)
        if source and source.hasUrls():
            for url in source.urls():
                if not url.isLocalFile():
                    continue
                p = Path(url.toLocalFile())
                if p.exists() and _is_image_path(p):
                    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
                    dst = IMAGES_DIR / p.name
                    if not dst.exists():
                        shutil.copy2(p, dst)
                    self._owner.attach_image(dst)
                    return

        # 3) Default behavior (обычный текст)
        super().insertFromMimeData(source)


class StepCard(QFrame):
    removed = pyqtSignal(object)

    def __init__(self, idx: int = 1):
        super().__init__()
        self.setObjectName("stepCard")
        self.idx = idx
        self.image_path: str | None = None
        self._build()

    def _build(self):
        lo = QVBoxLayout(self)
        lo.setContentsMargins(10, 8, 10, 8)
        lo.setSpacing(4)

        top = QHBoxLayout()
        self.lbl = QLabel(f"Шаг {self.idx}")
        self.lbl.setStyleSheet("font-weight: 600; color: #8890aa; font-size: 12px;")
        top.addWidget(self.lbl)
        top.addStretch()

        ib = QPushButton()
        ib.setIcon(icons.image())
        ib.setObjectName("toolBtn")
        ib.setToolTip("Прикрепить изображение (или Ctrl+V из буфера)")
        ib.setFixedSize(28, 24)
        ib.clicked.connect(self._pick_img)
        top.addWidget(ib)

        db = QPushButton()
        db.setIcon(icons.times())
        db.setObjectName("dangerBtn")
        db.setFixedSize(24, 24)
        db.clicked.connect(lambda: self.removed.emit(self))
        top.addWidget(db)

        lo.addLayout(top)

        self.text = StepTextEdit(self)
        self.text.setPlaceholderText("Описание шага… (можно Ctrl+V вставить картинку)")
        self.text.setMaximumHeight(58)
        lo.addWidget(self.text)

        self.img_lbl = QLabel("")
        self.img_lbl.setStyleSheet("color: #5b8af5; font-size: 11px;")
        lo.addWidget(self.img_lbl)

    def attach_image(self, path: Path):
        """Привязать картинку к шагу (обновляет state + label)."""
        self.image_path = str(path)
        self.img_lbl.setText(f"  {path.name}")

    def _pick_img(self):
        p, _ = QFileDialog.getOpenFileName(
            self,
            "Изображение",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp)",
        )
        if not p:
            return
        src = Path(p)
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        dst = IMAGES_DIR / src.name
        if not dst.exists():
            shutil.copy2(src, dst)
        self.attach_image(dst)

    def set_idx(self, i: int):
        self.idx = i
        self.lbl.setText(f"Шаг {i}")

    def data(self) -> dict:
        return {"text": self.text.toPlainText(), "image": self.image_path}