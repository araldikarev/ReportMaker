"""Main application window."""
from PyQt6.QtWidgets import QMainWindow, QTabWidget

from ui import icons
from ui.tab_docx_to_yaml import DocxToYamlTab
from ui.tab_yaml_to_docx import YamlToDocxTab
from ui.tab_report import ReportTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Report Prompt Builder")
        self.setMinimumSize(960, 640)
        self.resize(1200, 780)

        tabs = QTabWidget()
        tabs.addTab(DocxToYamlTab(), icons.file_word(),  " DOCX → YAML ")
        tabs.addTab(YamlToDocxTab(), icons.file_code(),  " YAML → DOCX ")
        tabs.addTab(ReportTab(),     icons.chart_bar(),  " Отчёт ")
        self.setCentralWidget(tabs)