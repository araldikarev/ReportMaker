"""Tab 2 — YAML → DOCX."""
from __future__ import annotations

import os, sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QVBoxLayout, QWidget,
)
from docx import Document

from core.yaml_to_docx import build_docx_from_yaml
from ui import icons


class YamlToDocxTab(QWidget):
    def __init__(self):
        super().__init__()
        self._result_dir: Path | None = None
        lo = QVBoxLayout(self)
        lo.setSpacing(12)
        lo.setContentsMargins(20, 20, 20, 20)

        h = QLabel("YAML → DOCX")
        h.setObjectName("heading")
        lo.addWidget(h)

        s = QLabel("Сборка документа Word из YAML-структуры")
        s.setObjectName("sub")
        lo.addWidget(s)

        lo.addSpacing(4)

        for label_text, attr, filt in [
            ("YAML:", "yaml_edit", "YAML (*.yaml *.yml)"),
            ("Шаблон:", "tmpl_edit", "Word (*.docx)"),
        ]:
            r = QHBoxLayout()
            lb = QLabel(label_text)
            lb.setFixedWidth(60)
            r.addWidget(lb)
            ed = QLineEdit()
            ed.setReadOnly(True)
            ed.setPlaceholderText("Не выбрано…")
            r.addWidget(ed)
            setattr(self, attr, ed)
            b = QPushButton()
            b.setIcon(icons.folder_open())
            b.setObjectName("toolBtn")
            b.setFixedWidth(36)
            filt_copy = filt
            b.clicked.connect(lambda _, e=ed, f=filt_copy: self._pick(e, f))
            r.addWidget(b)
            lo.addLayout(r)

        r = QHBoxLayout()
        lb = QLabel("Вывод:")
        lb.setFixedWidth(60)
        r.addWidget(lb)
        self.out_edit = QLineEdit()
        self.out_edit.setPlaceholderText("result.docx")
        r.addWidget(self.out_edit)
        b = QPushButton()
        b.setIcon(icons.save())
        b.setObjectName("toolBtn")
        b.setFixedWidth(36)
        b.clicked.connect(self._pick_out)
        r.addWidget(b)
        lo.addLayout(r)

        lo.addSpacing(4)

        cb = QPushButton(" Собрать DOCX")
        cb.setIcon(icons.bolt())
        cb.setObjectName("accentBtn")
        cb.clicked.connect(self._convert)
        lo.addWidget(cb)

        self.status = QLabel("")
        self.status.setObjectName("sub")
        lo.addWidget(self.status)

        self.link_btn = QPushButton(" Открыть папку с результатом")
        self.link_btn.setIcon(icons.link_ext())
        self.link_btn.setObjectName("linkBtn")
        self.link_btn.setVisible(False)
        self.link_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.link_btn.clicked.connect(self._open_folder)
        lo.addWidget(self.link_btn)

        lo.addStretch()

    def _pick(self, edit, filt):
        p, _ = QFileDialog.getOpenFileName(self, "Открыть", "", filt)
        if p:
            edit.setText(p)

    def _pick_out(self):
        p, _ = QFileDialog.getSaveFileName(
            self, "Сохранить", "result.docx", "Word (*.docx)",
        )
        if p:
            self.out_edit.setText(p)

    def _convert(self):
        yp = self.yaml_edit.text()
        if not yp:
            QMessageBox.warning(self, "Ошибка", "Укажите YAML")
            return
        op = self.out_edit.text()
        if not op:
            QMessageBox.warning(self, "Ошибка", "Укажите путь вывода")
            return
        tp = self.tmpl_edit.text()
        if not tp:
            tmp = Path(op).parent / "__empty.docx"
            Document().save(str(tmp))
            tp = str(tmp)
        try:
            build_docx_from_yaml(yp, tp, op)
            self._result_dir = Path(op).parent
            self.status.setText(f"✓  {op}")
            self.link_btn.setVisible(True)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def _open_folder(self):
        if not self._result_dir:
            return
        p = str(self._result_dir)
        if sys.platform == "win32":
            os.startfile(p)
        elif sys.platform == "darwin":
            import subprocess; subprocess.Popen(["open", p])
        else:
            import subprocess; subprocess.Popen(["xdg-open", p])