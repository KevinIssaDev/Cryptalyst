from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, 
                             QFileDialog, QTextEdit, QProgressBar, QListWidget, QComboBox, 
                             QMessageBox, QScrollArea, QLabel, QApplication, QToolButton, 
                             QAbstractItemView, QSizePolicy)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QEvent, QSize
from PyQt6.QtGui import QPainter, QColor, QPalette, QFont, QIcon
from queue import Queue
from .file_comparison import FileComparison
from .report_generator import export_html_report
import json
import os
from assets.css import css

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)
        self.title = QLabel(f"{parent.windowTitle()}", self)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(
            """
            QLabel { 
                font-size: 12pt; 
                margin-left: 48px; 
                margin-top: 4px;
                color: white; 
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: 500;
                letter-spacing: 0.5px;
            }
            """
        )

        title_bar_layout.addWidget(self.title)

        self.min_button = QToolButton(self)
        min_icon = QIcon("assets/min.svg")
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)
        
        self.max_button = QToolButton(self)
        max_icon = QIcon("assets/max.svg")
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)
        
        self.close_button = QToolButton(self)
        close_icon = QIcon("assets/close.svg")
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)
        
        self.normal_button = QToolButton(self)
        normal_icon = QIcon("assets/normal.svg")
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)
        
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        for button in buttons:
            button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            button.setFixedSize(QSize(22, 22))
            button.setStyleSheet(
                """
                QToolButton {
                    padding: 2px;
                    background: transparent;
                }
                QToolButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                }
                """
            )
            title_bar_layout.addWidget(button)

    def window_state_changed(self, state):
        if state == Qt.WindowState.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

class ComparisonThread(QThread):
    progress_update = pyqtSignal(int)
    comparison_complete = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, original_file, encrypted_file):
        super().__init__()
        self.original_file = original_file
        self.encrypted_file = encrypted_file

    def run(self):
        try:
            file_comparison = FileComparison(self.original_file, self.encrypted_file)
            result = file_comparison.compare(self.progress_update.emit)
            self.comparison_complete.emit(result)
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cryptalyst - Ransomware Analysis Tool")
        self.setGeometry(100, 100, 1200, 900)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.central_widget = QWidget()
        self.central_widget.setObjectName("Container")
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.title_bar = CustomTitleBar(self)
        self.main_layout.addWidget(self.title_bar)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)
        self.main_layout.addWidget(self.content_widget)
        self.setup_ui()
        self.comparison_queue = Queue()
        self.apply_theme()

    def setup_ui(self):
        
        file_selection_layout = QHBoxLayout()
        self.original_files_btn = QPushButton("📁 Select Original Files")
        self.encrypted_files_btn = QPushButton("📁 Select Encrypted Files")
        file_selection_layout.addWidget(self.original_files_btn)
        file_selection_layout.addWidget(self.encrypted_files_btn)
        self.content_layout.addLayout(file_selection_layout)
        
        lists_layout = QHBoxLayout()
        self.original_files_list = QListWidget()
        self.original_files_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.original_files_list.setAlternatingRowColors(True)
        self.original_files_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.encrypted_files_list = QListWidget()
        self.encrypted_files_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.encrypted_files_list.setAlternatingRowColors(True)
        self.encrypted_files_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        lists_layout.addWidget(self.original_files_list)
        lists_layout.addWidget(self.encrypted_files_list)
        self.content_layout.addLayout(lists_layout)
        
        self.compare_btn = QPushButton("🔍 Start Analysis")
        self.content_layout.addWidget(self.compare_btn)
        
        self.progress_bar = QProgressBar()
        self.content_layout.addWidget(self.progress_bar)
        
        self.results_scroll = QScrollArea()
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)

        self.results_scroll.setWidget(self.results_widget)
        self.results_scroll.setWidgetResizable(True)
        self.content_layout.addWidget(self.results_scroll)
        
        export_layout = QHBoxLayout()
        self.export_format = QComboBox()
        self.export_format.addItems(["HTML", "JSON"])
        self.export_btn = QPushButton("📄 Export Report")
        export_layout.addWidget(self.export_format)
        export_layout.addWidget(self.export_btn)
        self.content_layout.addLayout(export_layout)
        
        self.original_files_btn.clicked.connect(lambda: self.select_files("original"))
        self.encrypted_files_btn.clicked.connect(lambda: self.select_files("encrypted"))
        self.compare_btn.clicked.connect(self.compare_files)
        self.export_btn.clicked.connect(self.export_report)

        self.original_files = []
        self.encrypted_files = []
        self.comparison_results = []

    def apply_theme(self):
        self.setStyleSheet(css)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.position().toPoint() - self.initial_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)

    def select_files(self, file_type):
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(self, f"Select {file_type.capitalize()} Files")
        if file_paths:
            if file_type == "original":
                self.original_files = file_paths
                self.original_files_list.clear()
                self.original_files_list.addItems([path.split('/')[-1] for path in file_paths])
            else:
                self.encrypted_files = file_paths
                self.encrypted_files_list.clear()
                self.encrypted_files_list.addItems([path.split('/')[-1] for path in file_paths])

    def compare_files(self):
        if not self.original_files or not self.encrypted_files:
            QMessageBox.warning(self, "Error", "Please select both original and encrypted files.")
            return
        if len(self.original_files) != len(self.encrypted_files):
            QMessageBox.warning(self, "Error", "The number of original and encrypted files must be the same.")
            return

        self.comparison_results = []
        self.progress_bar.setValue(0)
        self.clear_results()

        for original_file, encrypted_file in zip(self.original_files, self.encrypted_files):
            self.comparison_queue.put((original_file, encrypted_file))

        self.process_next_comparison()

    def process_next_comparison(self):
        if not self.comparison_queue.empty():
            original_file, encrypted_file = self.comparison_queue.get()
            self.comparison_thread = ComparisonThread(original_file, encrypted_file)
            self.comparison_thread.progress_update.connect(self.update_progress)
            self.comparison_thread.comparison_complete.connect(self.handle_comparison_result)
            self.comparison_thread.error_occurred.connect(self.handle_comparison_error)
            self.comparison_thread.finished.connect(self.process_next_comparison)
            self.comparison_thread.start()
        else:
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Complete", "All file comparisons have been completed.")

    def clear_results(self):
        for i in reversed(range(self.results_layout.count())): 
            self.results_layout.itemAt(i).widget().setParent(None)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def handle_comparison_result(self, result):
        self.comparison_results.append(result)
        
        result_widget = QWidget()
        result_layout = QVBoxLayout(result_widget)
        

        info_layout = QHBoxLayout()
        original_file_path = os.path.join(os.path.basename(os.path.dirname(result['original_file'])), os.path.basename(result['original_file']))
        encrypted_file_path = os.path.join(os.path.basename(os.path.dirname(result['encrypted_file'])), os.path.basename(result['encrypted_file']))
        info_layout.addWidget(QLabel(f"{original_file_path} 🔀 {encrypted_file_path}"))
        info_layout.addWidget(QLabel(f"    File Size: {result['total_size_str']}"))
        info_layout.addWidget(QLabel(f"Percentage Encrypted: {result['percentage_encrypted']:.2f}%"))
        result_layout.addLayout(info_layout)
        
        visual = VisualRepresentation(result)
        result_layout.addWidget(visual)
        
        ranges_list = QListWidget()
        ranges_list.setObjectName("ranges_list")
        ranges_list.setAlternatingRowColors(True)
        ranges_list.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        
        for start, end in result['encrypted_ranges']:
            item_text = f"Decimal: [{start}, {end}] | Hex: [0x{start:X}, 0x{end:X}]"
            ranges_list.addItem(item_text)
        
        ranges_list.setFixedHeight(100)
        
        ranges_label = QLabel("Encrypted Ranges:")
        ranges_label.setStyleSheet("font-size: 10pt;")
        
        if ranges_list.count() > 0: 
            result_layout.addWidget(ranges_label)
            result_layout.addWidget(ranges_list)

        self.results_layout.addWidget(result_widget)

    def handle_comparison_error(self, error_message):
        QMessageBox.critical(self, "Error", f"An error occurred during comparison: {error_message}")

    def export_report(self):
        if not self.comparison_results:
            QMessageBox.warning(self, "Error", "No comparison results to export.")
            return

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Report")
        if not file_path:
            return

        export_format = self.export_format.currentText()
        try:
            if export_format == "JSON":
                with open(file_path, 'w') as f:
                    json.dump(self.comparison_results, f, indent=2)
            elif export_format == "HTML":
                export_html_report(self.comparison_results, file_path)
            QMessageBox.information(self, "Success", f"Report exported successfully as {export_format}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while exporting the report: {str(e)}")

class VisualRepresentation(QWidget):
    def __init__(self, result):
        super().__init__()
        self.setMinimumHeight(40)  
        self.encrypted_ranges = result['encrypted_ranges']
        self.total_size = result['total_size']
        self.percentage = result['percentage_encrypted']

    def paintEvent(self, event):
        if not self.total_size:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width()
        height = self.height()
        painter.fillRect(0, 0, width, height, QColor(44, 62, 80))
        for start, end in self.encrypted_ranges:
            x1 = int(start / self.total_size * width)
            x2 = int(end / self.total_size * width)
            painter.fillRect(x1, 0, x2 - x1, height, QColor(235, 110, 96))

        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        painter.drawText(0, 0, width, height, Qt.AlignmentFlag.AlignCenter, f"{self.percentage:.2f}%")