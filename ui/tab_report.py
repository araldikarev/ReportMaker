"""Tab 3 — Report builder (prompt + session)."""
from __future__ import annotations

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QFileDialog, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPlainTextEdit,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QSplitter, QVBoxLayout, QWidget,
)
from docx import Document

from core.paths import YAMLS_DIR, SCRIPTS_DIR, SESSIONS_DIR
from core.prompt_builder import DEFAULT_INSTRUCTION, build_prompt
from core.session_io import (
    create_session_dir,
    list_sessions_any,
    load_session_any,
    save_session,
)
from core.yaml_to_docx import build_docx_from_yaml
from ui import icons
from ui.step_card import StepCard


class ReportTab(QWidget):
    def __init__(self):
        super().__init__()
        self._steps: list[StepCard] = []
        self._session_dir: Path | None = None  # текущая (загруженная/созданная) сессия
        self._build()
        self._refresh_sessions()
        self._refresh_yamls()
        self._refresh_scripts()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(14, 14, 14, 14)
        root.setSpacing(8)

        title = QLabel("Сформировать отчёт")
        title.setObjectName("heading")
        root.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # ═══ LEFT ═══
        left = QWidget()
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 8, 0)
        ll.setSpacing(8)

        # — sessions —
        g0 = QGroupBox("Сессии")
        g0l = QVBoxLayout(g0)
        r0 = QHBoxLayout()

        self.sess_cb = QComboBox()
        self.sess_cb.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        r0.addWidget(self.sess_cb, 1)

        b0r = QPushButton()
        b0r.setIcon(icons.refresh())
        b0r.setObjectName("toolBtn")
        b0r.setFixedWidth(30)
        b0r.setToolTip("Обновить список сессий")
        b0r.clicked.connect(self._refresh_sessions)
        r0.addWidget(b0r)

        b0l = QPushButton(" Загрузить")
        b0l.setIcon(icons.folder_open())
        b0l.clicked.connect(self._load_selected_session)
        r0.addWidget(b0l)

        g0l.addLayout(r0)

        r0b = QHBoxLayout()
        self.sess_path_lbl = QLabel("")
        self.sess_path_lbl.setObjectName("sub")
        self.sess_path_lbl.setStyleSheet("font-size: 10px;")
        r0b.addWidget(self.sess_path_lbl, 1)

        b0s = QPushButton(" Сохранить")
        b0s.setIcon(icons.save())
        b0s.clicked.connect(self._save_current_session)
        r0b.addWidget(b0s)

        b0o = QPushButton(" Открыть папку")
        b0o.setIcon(icons.link_ext())
        b0o.setObjectName("linkBtn")
        b0o.clicked.connect(self._open_session_folder)
        r0b.addWidget(b0o)

        g0l.addLayout(r0b)
        ll.addWidget(g0)

        # — yaml selector —
        g1 = QGroupBox("Референсный YAML")
        g1l = QVBoxLayout(g1)
        r = QHBoxLayout()
        self.yaml_cb = QComboBox()
        self.yaml_cb.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.yaml_cb.currentIndexChanged.connect(self._on_yaml_changed)
        r.addWidget(self.yaml_cb)
        rb = QPushButton()
        rb.setIcon(icons.refresh())
        rb.setObjectName("toolBtn")
        rb.setFixedWidth(30)
        rb.setToolTip("Обновить список")
        rb.clicked.connect(self._refresh_yamls)
        r.addWidget(rb)
        g1l.addLayout(r)
        self.yaml_preview = QPlainTextEdit()
        self.yaml_preview.setReadOnly(True)
        self.yaml_preview.setMaximumHeight(130)
        self.yaml_preview.setPlaceholderText("Предпросмотр YAML…")
        g1l.addWidget(self.yaml_preview)
        ll.addWidget(g1)

        # — steps —
        g2 = QGroupBox("Шаги отчёта")
        g2l = QVBoxLayout(g2)
        ab = QPushButton(" Добавить шаг")
        ab.setIcon(icons.plus())
        ab.clicked.connect(self._add_step)
        g2l.addWidget(ab)
        self.steps_area = QScrollArea()
        self.steps_area.setWidgetResizable(True)
        sc = QWidget()
        self.steps_lo = QVBoxLayout(sc)
        self.steps_lo.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.steps_lo.setSpacing(6)
        self.steps_area.setWidget(sc)
        g2l.addWidget(self.steps_area)
        ll.addWidget(g2, 1)

        # — scripts —
        g3 = QGroupBox("Скрипты (.py)")
        g3l = QVBoxLayout(g3)
        sr = QHBoxLayout()
        sl = QLabel(str(SCRIPTS_DIR))
        sl.setObjectName("sub")
        sl.setStyleSheet("font-size: 10px;")
        sr.addWidget(sl, 1)
        srb = QPushButton()
        srb.setIcon(icons.refresh())
        srb.setObjectName("toolBtn")
        srb.setFixedWidth(30)
        srb.clicked.connect(self._refresh_scripts)
        sr.addWidget(srb)
        g3l.addLayout(sr)
        self.scripts_lo = QVBoxLayout()
        g3l.addLayout(self.scripts_lo)
        ll.addWidget(g3)

        # — instruction —
        g4 = QGroupBox("Инструкция")
        g4l = QVBoxLayout(g4)
        self.instr = QPlainTextEdit()
        self.instr.setPlainText(DEFAULT_INSTRUCTION)
        self.instr.setMaximumHeight(80)
        g4l.addWidget(self.instr)
        ll.addWidget(g4)

        splitter.addWidget(left)

        # ═══ RIGHT ═══
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(8, 0, 0, 0)
        rl.setSpacing(8)

        rh = QHBoxLayout()
        rhl = QLabel("Промпт")
        rhl.setObjectName("heading")
        rh.addWidget(rhl)
        rh.addStretch()
        gb = QPushButton(" Сгенерировать")
        gb.setIcon(icons.bolt())
        gb.setObjectName("accentBtn")
        gb.clicked.connect(self._gen_prompt)
        rh.addWidget(gb)
        cpb = QPushButton(" Копировать")
        cpb.setIcon(icons.copy())
        cpb.clicked.connect(self._copy)
        rh.addWidget(cpb)
        rl.addLayout(rh)

        self.prompt_out = QPlainTextEdit()
        self.prompt_out.setReadOnly(True)
        self.prompt_out.setPlaceholderText("Нажмите «Сгенерировать»…")
        rl.addWidget(self.prompt_out, 1)

        # — session —
        gs = QGroupBox("Сессия — ответ нейросети")
        gsl = QVBoxLayout(gs)

        self.resp_text = QPlainTextEdit()
        self.resp_text.setPlaceholderText(
            "Вставьте сюда YAML-ответ нейросети…"
        )
        self.resp_text.setMaximumHeight(120)
        gsl.addWidget(self.resp_text)

        sr2 = QHBoxLayout()
        sr2.addWidget(QLabel("Файл:"))
        self.resp_path = QLineEdit()
        self.resp_path.setReadOnly(True)
        self.resp_path.setPlaceholderText("response.yaml")
        sr2.addWidget(self.resp_path)
        lrb = QPushButton()
        lrb.setIcon(icons.folder_open())
        lrb.setObjectName("toolBtn")
        lrb.setFixedWidth(36)
        lrb.clicked.connect(self._load_resp)
        sr2.addWidget(lrb)
        gsl.addLayout(sr2)

        sr3 = QHBoxLayout()
        sr3.addWidget(QLabel("Шаблон:"))
        self.sess_tmpl = QLineEdit()
        self.sess_tmpl.setPlaceholderText("base.docx (опционально)")
        sr3.addWidget(self.sess_tmpl)
        tb = QPushButton()
        tb.setIcon(icons.folder_open())
        tb.setObjectName("toolBtn")
        tb.setFixedWidth(36)
        tb.clicked.connect(self._pick_tmpl)
        sr3.addWidget(tb)
        gsl.addLayout(sr3)

        bb = QPushButton(" Собрать DOCX из ответа")
        bb.setIcon(icons.hammer())
        bb.setObjectName("accentBtn")
        bb.clicked.connect(self._build_resp)
        gsl.addWidget(bb)

        self.progress = QProgressBar()
        self.progress.setMaximum(2)
        self.progress.setValue(0)
        gsl.addWidget(self.progress)

        self.sess_status = QLabel("")
        self.sess_status.setObjectName("sub")
        gsl.addWidget(self.sess_status)

        rl.addWidget(gs)
        splitter.addWidget(right)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        root.addWidget(splitter, 1)

    # ── sessions ──
    def _refresh_sessions(self):
        self.sess_cb.blockSignals(True)
        self.sess_cb.clear()
        self.sess_cb.addItem("— не выбрана —", "")
        for entry in list_sessions_any(SESSIONS_DIR):
            d = entry.parent if entry.name == "session.yaml" else entry
            rel = str(d.relative_to(SESSIONS_DIR))
            self.sess_cb.addItem(rel, str(entry))
        self.sess_cb.blockSignals(False)

    def _open_session_folder(self):
        if not self._session_dir:
            QMessageBox.information(self, "Сессия", "Сессия не выбрана/не создана")
            return
        p = str(self._session_dir)
        if sys.platform == "win32":
            os.startfile(p)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            import subprocess
            subprocess.Popen(["open", p])
        else:
            import subprocess
            subprocess.Popen(["xdg-open", p])

    def _load_selected_session(self):
        sy = self.sess_cb.currentData()
        if not sy:
            QMessageBox.information(self, "Сессия", "Выберите сессию в списке")
            return
        try:
            self._apply_session(Path(sy))
            self.sess_status.setText(f"✓  Загружена сессия: {Path(sy).parent.name}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def _apply_session(self, entry: Path):
        st = load_session_any(entry)
        sd = Path(st.get("__session_dir__", entry.parent))
        self._session_dir = sd
        self.sess_path_lbl.setText(str(sd))

        # yaml ref
        yr = st.get("yaml_ref") or {}
        yaml_abs = yr.get("abs")
        yaml_rel = yr.get("rel")

        # попытка выставить combobox на нужный yaml
        wanted = None
        if yaml_abs and Path(str(yaml_abs)).exists():
            wanted = str(Path(str(yaml_abs)))
        else:
            # если rel есть — пробуем собрать абсолютный внутри YAMLS_DIR
            if yaml_rel:
                cand = YAMLS_DIR / str(yaml_rel)
                if cand.exists():
                    wanted = str(cand)

        if wanted:
            idx = -1
            for i in range(self.yaml_cb.count()):
                if self.yaml_cb.itemData(i) == wanted:
                    idx = i
                    break
            if idx >= 0:
                self.yaml_cb.setCurrentIndex(idx)
            else:
                # не нашли в списке — просто подгрузим превью, если файл есть
                if Path(wanted).exists():
                    self.yaml_preview.setPlainText(Path(wanted).read_text("utf-8"))

        # instruction
        self.instr.setPlainText(st.get("instruction", DEFAULT_INSTRUCTION))

        # scripts selection
        scripts = set(st.get("scripts") or [])
        for i in range(self.scripts_lo.count()):
            w = self.scripts_lo.itemAt(i).widget()
            if isinstance(w, QCheckBox):
                w.setChecked(w.text() in scripts if scripts else True)

        # steps
        self._clear_steps()
        steps = st.get("steps") or []
        for i, s in enumerate(steps, start=1):
            card = StepCard(i)
            card.removed.connect(self._rm_step)
            card.text.setPlainText(s.get("text", ""))
            img = s.get("image")
            if img:
                p = sd / str(img)
                if p.exists():
                    card.attach_image(p)
                else:
                    # если путь абсолютный/внешний — попробуем как есть
                    p2 = Path(str(img))
                    if p2.exists():
                        card.attach_image(p2)
            self._steps.append(card)
            self.steps_lo.addWidget(card)

        # prompt + response
        if st.get("prompt_text"):
            self.prompt_out.setPlainText(st["prompt_text"])

        if st.get("response_text"):
            self.resp_text.setPlainText(st["response_text"])
            self.resp_path.setText(str(sd / "response.yaml"))

        # template
        tmpl = st.get("template_docx")
        if tmpl:
            self.sess_tmpl.setText(str(tmpl))

    def _save_current_session(self):
        try:
            sd = self._session_dir
            if sd is None:
                sd = create_session_dir(SESSIONS_DIR, prefix="session")
                self._session_dir = sd

            # yaml ref paths (abs + rel)
            yp = self.yaml_cb.currentData()
            yaml_abs = str(yp) if yp else None
            yaml_rel = None
            if yaml_abs:
                try:
                    yaml_rel = str(Path(yaml_abs).relative_to(YAMLS_DIR))
                except Exception:
                    yaml_rel = None

            # scripts
            script_names: list[str] = []
            for i in range(self.scripts_lo.count()):
                w = self.scripts_lo.itemAt(i).widget()
                if isinstance(w, QCheckBox) and w.isChecked():
                    script_names.append(w.text())

            # steps
            steps = [st.data() for st in self._steps]

            save_session(
                sd,
                yaml_ref_path=yaml_abs,
                yaml_ref_rel=yaml_rel,
                template_docx=self.sess_tmpl.text() or None,
                instruction=self.instr.toPlainText(),
                scripts=script_names,
                steps=steps,
                prompt_text=self.prompt_out.toPlainText() or None,
                response_text=self.resp_text.toPlainText().strip() or None,
            )

            self.sess_path_lbl.setText(str(sd))
            self._refresh_sessions()
            self.sess_status.setText(f"✓  Сессия сохранена: {sd.name}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def _clear_steps(self):
        # убрать виджеты из layout
        while self.steps_lo.count():
            it = self.steps_lo.takeAt(0)
            w = it.widget()
            if w:
                w.deleteLater()
        self._steps.clear()

    # ── YAML combo ──
    def _refresh_yamls(self):
        self.yaml_cb.blockSignals(True)
        self.yaml_cb.clear()
        self.yaml_cb.addItem("— выберите —", "")
        for f in sorted(YAMLS_DIR.rglob("*.yaml")):
            self.yaml_cb.addItem(str(f.relative_to(YAMLS_DIR)), str(f))
        self.yaml_cb.blockSignals(False)

    def _on_yaml_changed(self):
        p = self.yaml_cb.currentData()
        if p and Path(p).exists():
            self.yaml_preview.setPlainText(Path(p).read_text("utf-8"))
        else:
            self.yaml_preview.clear()

    # ── scripts ──
    def _refresh_scripts(self):
        while self.scripts_lo.count():
            w = self.scripts_lo.takeAt(0).widget()
            if w:
                w.deleteLater()
        for f in sorted(SCRIPTS_DIR.glob("*.py")):
            cb = QCheckBox(f.name)
            cb.setChecked(True)
            cb.setProperty("fp", str(f))
            self.scripts_lo.addWidget(cb)

    # ── steps ──
    def _add_step(self):
        card = StepCard(len(self._steps) + 1)
        card.removed.connect(self._rm_step)
        self._steps.append(card)
        self.steps_lo.addWidget(card)

    def _rm_step(self, card: StepCard):
        self._steps.remove(card)
        card.deleteLater()
        for i, c in enumerate(self._steps):
            c.set_idx(i + 1)

    # ── prompt ──
    def _gen_prompt(self):
        yp = self.yaml_cb.currentData()
        yaml_txt = (
            Path(yp).read_text("utf-8") if yp and Path(yp).exists() else ""
        )
        steps = [st.data() for st in self._steps]
        script_paths: list[str] = []
        for i in range(self.scripts_lo.count()):
            w = self.scripts_lo.itemAt(i).widget()
            if isinstance(w, QCheckBox) and w.isChecked():
                fp = w.property("fp")
                if fp:
                    script_paths.append(fp)
        prompt = build_prompt(
            yaml_text=yaml_txt,
            steps=steps,
            script_paths=script_paths,
            instruction=self.instr.toPlainText(),
        )
        self.prompt_out.setPlainText(prompt)

    def _copy(self):
        t = self.prompt_out.toPlainText()
        if t:
            QApplication.clipboard().setText(t)
            self.sess_status.setText("✓  Скопировано в буфер обмена")

    # ── session ──
    def _load_resp(self):
        p, _ = QFileDialog.getOpenFileName(
            self, "YAML ответ", "", "YAML (*.yaml *.yml)"
        )
        if p:
            self.resp_path.setText(p)
            self.resp_text.setPlainText(Path(p).read_text("utf-8"))

    def _pick_tmpl(self):
        p, _ = QFileDialog.getOpenFileName(
            self, "Шаблон", "", "Word (*.docx)"
        )
        if p:
            self.sess_tmpl.setText(p)

    def _build_resp(self):
        self.progress.setValue(0)
        txt = self.resp_text.toPlainText().strip()
        if not txt:
            QMessageBox.warning(self, "Ошибка", "Вставьте YAML ответ")
            return

        # Если сессия не выбрана/не загружена — создаём новую
        if self._session_dir is None:
            self._session_dir = create_session_dir(SESSIONS_DIR, prefix="session")

        sd = self._session_dir
        sd.mkdir(parents=True, exist_ok=True)

        # Сохраняем/обновляем сессию (response.yaml + prompt + steps + images)
        self._save_current_session()

        # гарантируем, что response.yaml лежит в сессии
        yf = sd / "response.yaml"
        yf.write_text(txt, encoding="utf-8")
        self.resp_path.setText(str(yf))

        # На всякий — создадим media (если YAML будет ссылаться на media/...)
        (sd / "media").mkdir(exist_ok=True)

        self.progress.setValue(1)

        tp = self.sess_tmpl.text()
        if not tp:
            tmp = sd / "__empty.docx"
            Document().save(str(tmp))
            tp = str(tmp)

        out = sd / "report.docx"
        try:
            build_docx_from_yaml(str(yf), tp, str(out))
            self.progress.setValue(2)
            self.sess_status.setText(f"✓  {out}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            self.sess_status.setText(f"✕  {e}")