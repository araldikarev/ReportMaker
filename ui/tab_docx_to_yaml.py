"""Tab 1 — DOCX → YAML."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QFileDialog, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget,
)

from core.docx_to_yaml import parse_docx_to_yaml
from core.paths import YAMLS_DIR
from ui import icons


class DocxToYamlTab(QWidget):
    def __init__(self):
        super().__init__()
        lo = QVBoxLayout(self)
        lo.setSpacing(12)
        lo.setContentsMargins(20, 20, 20, 20)

        h = QLabel("DOCX → YAML")
        h.setObjectName("heading")
        lo.addWidget(h)

        s = QLabel("Преобразование документа Word в YAML-структуру")
        s.setObjectName("sub")
        lo.addWidget(s)

        lo.addSpacing(4)

        row = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("Путь к .docx файлу…")
        row.addWidget(self.path_edit)

        browse = QPushButton(" Обзор")
        browse.setIcon(icons.folder_open())
        browse.clicked.connect(self._browse)
        row.addWidget(browse)
        lo.addLayout(row)

        cb = QPushButton(" Конвертировать")
        cb.setIcon(icons.bolt())
        cb.setObjectName("accentBtn")
        cb.clicked.connect(self._convert)
        lo.addWidget(cb)

        lo.addSpacing(2)

        self.result = QPlainTextEdit()
        self.result.setReadOnly(True)
        self.result.setPlaceholderText("YAML появится здесь…")
        lo.addWidget(self.result, 1)

        self.status = QLabel("")
        self.status.setObjectName("sub")
        lo.addWidget(self.status)

    def _browse(self):
        p, _ = QFileDialog.getOpenFileName(self, "DOCX", "", "Word (*.docx)")
        if p:
            self.path_edit.setText(p)

    def _convert(self):
        src = self.path_edit.text()
        if not src or not Path(src).exists():
            QMessageBox.warning(self, "Ошибка", "Выберите .docx файл")
            return
        try:
            name = Path(src).stem
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_dir = YAMLS_DIR / f"{name}_{ts}"
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / "doc.yaml"
            txt = parse_docx_to_yaml(src, str(out))
            self.result.setPlainText(txt)
            self.status.setText(f"✓  Сохранено: {out}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))