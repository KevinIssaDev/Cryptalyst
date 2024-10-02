css = """
            #Container {
                background: #22262b;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #16191d;
                font-size: 13pt;
            }
            QListWidget::item {
                color: #c9d1d9;
            }
            QListWidget::item:hover {
                background-color: #16191d;
            }
            QListWidget::item:alternate {
                background-color: #21262c;
            }
            QListWidget::item:alternate:hover {
                background-color: #21262c;
            }
            QListWidget#ranges_list {
                font-size: 10pt;
            }
            QVBoxLayout {
                background-color: #22262b;
            }
            QScrollArea {
                background-color: #22262b;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #22262b;
            }
            QScrollBar:vertical {
                border: none;
                background: #2c3338;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3d444d;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical {
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                border: none;
                background: #2c3338;
                height: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:horizontal {
                background: #3d444d;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal {
                width: 0px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal {
                width: 0px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
            QPushButton {
                background-color: #3d444d;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #484f59;
            }
            QPushButton:pressed {
                background-color: #2980b9;
            }
            QListWidget, QTextEdit, QComboBox {
                background-color: #16191d;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QProgressBar {
                border: none;
                border-radius: 5px;
                background-color: #10141a;
                color: white;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #26a65b;
                border-radius: 5px;
            }
            QLabel {
                color: white;
            }
            QMessageBox {
                background-color: #1e2329;
                color: white;
            }
            QMessageBox QLabel {
                color: white;
            }
            QMessageBox QPushButton {
                background-color: #3d444d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 5px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #484f59;
            }
            QMessageBox QPushButton:pressed {
                background-color: #2980b9;
            }
"""
