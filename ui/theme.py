"""QSS dark theme — Compact, High Contrast, with Neon/Glow Focus Effects."""

QSS = """
* {
    font-family: 'Inter', '-apple-system', 'Segoe UI', 'Roboto', sans-serif;
    font-size: 13px;
}

/* ── Главный фон окна ── */
QWidget {
    background-color: #0d1017; 
    color: #cbd5e1;
}
QMainWindow {
    background-color: #0d1017;
}

/* ── Вкладки (Tabs) ── */
QTabWidget::pane {
    border: none;
    border-top: 1px solid #272e3d;
    background: transparent;
    top: -1px;
}
QTabBar {
    background: transparent;
}
QTabBar::tab {
    background: transparent;
    color: #64748b;
    padding: 8px 20px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: 600;
    border-bottom: 2px solid transparent;
}
QTabBar::tab:selected {
    color: #f8fafc;
    background-color: #121620;
    border-top: 1px solid #272e3d;
    border-left: 1px solid #272e3d;
    border-right: 1px solid #272e3d;
    /* Яркая синяя полоска у активной вкладки */
    border-bottom: 2px solid #3b82f6; 
}
QTabBar::tab:hover:!selected {
    color: #cbd5e1;
    background-color: #0f121a;
}

/* ── Панели (QGroupBox) — КОМПАКТНЫЕ ── */
QGroupBox {
    background-color: #121620; /* Чуть светлее фона, чтобы выделяться */
    border: 1px solid #272e3d;
    border-radius: 6px;
    margin-top: 14px; /* Убрали огромный отступ */
    padding: 14px 10px 10px 10px; /* Сжали padding */
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: -8px; /* Сажаем заголовок прямо на рамку */
    padding: 2px 8px;
    background-color: #0d1017; /* Перекрывает рамку цветом фона окна */
    color: #94a3b8;
    border: 1px solid #272e3d;
    border-radius: 4px;
    font-weight: 600;
    font-size: 11px;
}

/* ── Текстовые зоны (Промпт, Инструкции) — ВЫСОКИЙ КОНТРАСТ ── */
QTextEdit, QPlainTextEdit, QLineEdit {
    background-color: #050608; /* Очень тёмный, как терминал */
    color: #e2e8f0;
    border: 1px solid #272e3d;
    border-radius: 6px;
    padding: 6px 10px;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
}

/* 🔥 ТА САМАЯ ПОДСВЕТКА (GLOW) 🔥 */
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #3b82f6; /* Электрический синий */
    background-color: #0a1120; /* Лёгкий неоновый синий отлив фона */
    color: #ffffff;
}

QLineEdit:read-only, QPlainTextEdit:read-only {
    color: #94a3b8;
    background-color: #080a0f;
    border: 1px solid #1e2430;
}
/* Подсветка даже для read-only (например, зона сгенерированного промпта) */
QLineEdit:read-only:focus, QPlainTextEdit:read-only:focus {
    border: 1px solid #3b82f6;
    background-color: #0a1120;
}

/* ── Выпадающие списки (ComboBox) ── */
QComboBox {
    background-color: #050608;
    color: #e2e8f0;
    border: 1px solid #272e3d;
    border-radius: 6px;
    padding: 6px 10px;
}
QComboBox:hover {
    border-color: #475569;
}
QComboBox:focus {
    border: 1px solid #3b82f6; /* Glow эффект */
    background-color: #0a1120;
}
QComboBox::drop-down {
    border: none;
    width: 28px;
}
/* Компактная стрелочка */
QComboBox::down-arrow {
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='6 9 12 15 18 9'></polyline></svg>");
}
QComboBox QAbstractItemView {
    background-color: #121620;
    border: 1px solid #3b82f6; /* Рамка списка с подсветкой */
    border-radius: 6px;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    outline: none;
}

/* ── Кнопки ── */
QPushButton {
    background-color: #1e2430;
    color: #cbd5e1;
    border: 1px solid #333c4d;
    border-radius: 6px;
    padding: 6px 14px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #2a3345;
    border-color: #475569;
    color: #ffffff;
}
QPushButton:pressed {
    background-color: #161b24;
}

/* ── Главная кнопка (Акцент) ── */
QPushButton#accentBtn {
    background-color: #2563eb; /* Чистый синий акцент */
    color: #ffffff;
    font-weight: 600;
    border: none;
    border-radius: 6px;
    padding: 7px 18px;
}
QPushButton#accentBtn:hover {
    background-color: #3b82f6; /* При наведении светлеет (эффект свечения) */
}
QPushButton#accentBtn:pressed {
    background-color: #1d4ed8;
}

/* ── Маленькие кнопки-иконки ── */
QPushButton#toolBtn {
    background-color: transparent;
    border: 1px solid #272e3d;
    border-radius: 4px;
    padding: 4px;
}
QPushButton#toolBtn:hover {
    background-color: #1e2430;
    border-color: #3b82f6; /* Glow рамки при наведении */
}

/* ── Тексты ── */
QLabel {
    color: #cbd5e1;
}
QLabel#heading {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
}
QLabel#sub {
    font-size: 11px;
    color: #64748b;
}

/* ── Карточка шага ── */
QFrame#stepCard {
    background-color: #121620;
    border: 1px solid #272e3d;
    border-left: 3px solid #272e3d;
    border-radius: 6px;
}
QFrame#stepCard:hover {
    border-left: 3px solid #3b82f6; /* Подсветка левой грани при наведении */
    background-color: #161a26;
}

/* ── Исправленный CheckBox ── */
QCheckBox {
    spacing: 8px;
    color: #cbd5e1;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #333c4d;
    background-color: #050608;
}
QCheckBox::indicator:hover {
    border-color: #3b82f6; /* Подсветка чекбокса */
}
QCheckBox::indicator:checked {
    background-color: #3b82f6;
    border-color: #3b82f6;
    image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'><polyline points='20 6 9 17 4 12'></polyline></svg>");
}

/* ── Прогресс бар ── */
QProgressBar {
    background-color: #050608;
    border: 1px solid #272e3d;
    border-radius: 4px;
    text-align: center;
    color: #ffffff;
    font-weight: 600;
    height: 14px;
}
QProgressBar::chunk {
    background-color: #3b82f6;
    border-radius: 3px;
}

/* ── Скроллбары ── */
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #272e3d;
    border-radius: 4px;
    min-height: 20px;
    margin: 1px;
}
QScrollBar::handle:vertical:hover {
    background: #3b82f6; /* Скролл тоже подсвечивается при наведении */
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
    height: 0px;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 0px;
}
QScrollBar::handle:horizontal {
    background: #272e3d;
    border-radius: 4px;
    min-width: 20px;
    margin: 1px;
}
QScrollBar::handle:horizontal:hover {
    background: #3b82f6;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: transparent;
    width: 0px;
}

/* ── Разделитель (Сплиттер) ── */
QSplitter::handle {
    background-color: #272e3d;
    width: 2px;
}
QSplitter::handle:hover {
    background-color: #3b82f6; /* Glow сплиттера при захвате */
}
"""