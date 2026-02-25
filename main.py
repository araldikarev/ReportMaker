#!/usr/bin/env python3
"""Report Prompt Builder — entry point."""

import sys

from PyQt6.QtWidgets import QApplication

from core.paths import ensure_dirs
from ui.theme import QSS
from ui.main_window import MainWindow


def main():
    ensure_dirs()
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()