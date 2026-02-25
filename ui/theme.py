"""QSS dark theme — refined deep blue-gray, minimal accent."""

QSS = """
/* ── Global ── */
* {
    font-family: 'Segoe UI', 'Inter', 'Noto Sans', sans-serif;
    font-size: 13px;
}

QWidget {
    background-color: #14141e;
    color: #d0d4e0;
}
QMainWindow {
    background-color: #14141e;
}

/* ── Tabs ── */
QTabWidget::pane {
    border: 1px solid #2a2d3a;
    border-radius: 6px;
    background: #14141e;
    top: -1px;
}
QTabBar {
    background: transparent;
}
QTabBar::tab {
    background: #1c1e2c;
    color: #6b7394;
    padding: 10px 26px;
    margin-right: 1px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid #2a2d3a;
    border-bottom: none;
    font-weight: 500;
}
QTabBar::tab:selected {
    background: #1f2233;
    color: #e8ecf4;
    border-bottom: 2px solid #5b8af5;
    font-weight: 600;
}
QTabBar::tab:hover:!selected {
    background: #22253a;
    color: #9ba3c2;
}

/* ── Buttons ── */
QPushButton {
    background: #1f2233;
    color: #c8cde0;
    border: 1px solid #2e3148;
    border-radius: 5px;
    padding: 6px 14px;
    font-weight: 500;
}
QPushButton:hover {
    background: #282c42;
    border-color: #3d4260;
}
QPushButton:pressed {
    background: #343856;
}

QPushButton#accentBtn {
    background: #3a6df0;
    color: #f0f2fa;
    font-weight: 600;
    border: none;
    border-radius: 5px;
    padding: 7px 18px;
}
QPushButton#accentBtn:hover {
    background: #4b7df7;
}
QPushButton#accentBtn:pressed {
    background: #2f5cd0;
}

QPushButton#dangerBtn {
    background: #3a2030;
    color: #e85577;
    border: 1px solid #4a2a3a;
    font-weight: 600;
}
QPushButton#dangerBtn:hover {
    background: #4a2838;
    border-color: #e85577;
}

QPushButton#linkBtn {
    background: transparent;
    border: none;
    color: #5b8af5;
    padding: 2px 4px;
    font-weight: 500;
}
QPushButton#linkBtn:hover {
    color: #7da4fc;
}

QPushButton#toolBtn {
    background: #1a1d2e;
    border: 1px solid #2a2d3a;
    border-radius: 4px;
    padding: 4px;
}
QPushButton#toolBtn:hover {
    background: #252840;
    border-color: #3d4260;
}

/* ── Inputs ── */
QTextEdit, QPlainTextEdit {
    background: #111320;
    color: #d0d4e0;
    border: 1px solid #252840;
    border-radius: 5px;
    padding: 8px;
    selection-background-color: #2e3f6e;
    selection-color: #e8ecf4;
}
QLineEdit {
    background: #111320;
    color: #d0d4e0;
    border: 1px solid #252840;
    border-radius: 5px;
    padding: 6px 10px;
    selection-background-color: #2e3f6e;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #4070e0;
}
QLineEdit:read-only {
    color: #8890aa;
}

QComboBox {
    background: #1a1d2e;
    color: #c8cde0;
    border: 1px solid #2a2d3a;
    border-radius: 5px;
    padding: 6px 10px;
}
QComboBox::drop-down {
    border: none;
    width: 26px;
}
QComboBox::down-arrow {
    image: none;
    border: none;
}
QComboBox QAbstractItemView {
    background: #1a1d2e;
    color: #c8cde0;
    border: 1px solid #2a2d3a;
    selection-background-color: #252a44;
    selection-color: #e8ecf4;
    outline: none;
}
QComboBox:hover {
    border-color: #3d4260;
}

/* ── Labels ── */
QLabel {
    background: transparent;
    color: #b0b8d0;
}
QLabel#heading {
    font-size: 16px;
    font-weight: 700;
    color: #e8ecf4;
    letter-spacing: 0.3px;
}
QLabel#sub {
    font-size: 12px;
    color: #6b7394;
}

/* ── GroupBox ── */
QGroupBox {
    border: 1px solid #252840;
    border-radius: 6px;
    margin-top: 16px;
    padding: 18px 10px 10px 10px;
    font-weight: 600;
    color: #8890aa;
    font-size: 12px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 8px;
    color: #6b7394;
}

/* ── Progress ── */
QProgressBar {
    background: #1a1d2e;
    border: 1px solid #252840;
    border-radius: 4px;
    text-align: center;
    color: #8890aa;
    height: 20px;
    font-size: 11px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #3a6df0, stop:1 #5b8af5);
    border-radius: 3px;
}

/* ── Scroll ── */
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    background: #14141e;
    width: 6px;
    margin: 2px;
}
QScrollBar::handle:vertical {
    background: #2a2d3a;
    border-radius: 3px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover {
    background: #3d4260;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar:horizontal {
    background: #14141e;
    height: 6px;
    margin: 2px;
}
QScrollBar::handle:horizontal {
    background: #2a2d3a;
    border-radius: 3px;
    min-width: 24px;
}

/* ── Checkbox ── */
QCheckBox {
    spacing: 8px;
    color: #b0b8d0;
}
QCheckBox::indicator {
    width: 15px;
    height: 15px;
    border-radius: 3px;
    border: 1px solid #3d4260;
    background: #1a1d2e;
}
QCheckBox::indicator:checked {
    background: #3a6df0;
    border-color: #3a6df0;
}
QCheckBox::indicator:hover {
    border-color: #5b8af5;
}

/* ── Splitter ── */
QSplitter::handle {
    background: #252840;
    width: 1px;
}

/* ── Step card ── */
QFrame#stepCard {
    background: #1a1d2e;
    border: 1px solid #252840;
    border-radius: 6px;
}
QFrame#stepCard:hover {
    border-color: #3d4260;
}

/* ── Tooltip ── */
QToolTip {
    background: #1f2233;
    color: #d0d4e0;
    border: 1px solid #2e3148;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}
"""