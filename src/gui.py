import sys
import os
import webbrowser

# Add src to path if running directly
sys.path.append(os.path.dirname(__file__))

import config
import cli_forge

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QComboBox, QCheckBox, QStackedWidget, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox, QDialog, QAbstractItemView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor

PRINTERS_RAW = [
    ("psc008", "COM1, Basement (outside Programming Lab 3) | LEXMARK MS821DN, A4"),
    ("psc008-sx", "COM1, Basement (outside Programming Lab 3) | LEXMARK MS821DN, A4"),
    ("psc008-nb", "COM1, Basement (outside Programming Lab 3) | LEXMARK MS821DN, A4"),
    ("psc011", "LEXMARK MS821DN, A4"),
    ("psc011-sx", "LEXMARK MS821DN, A4"),
    ("psc011-nb", "LEXMARK MS821DN, A4"),
    ("psts", "COM1, Level 1, Printer Area | LEXMARK MS821DN, A4"),
    ("psts-sx", "COM1, Level 1, Printer Area | LEXMARK MS821DN, A4"),
    ("psts-nb", "COM1, Level 1, Printer Area | LEXMARK MS821DN, A4"),
    ("pstsb", "COM1, Level 1, Printer Area | LEXMARK MS821DN, A4"),
    ("pstsb-sx", "COM1, Level 1, Printer Area | LEXMARK MS821DN, A4"),
    ("pstsb-nb", "COM1, Level 1, Printer Area | LEXMARK MS821DN, A4"),
    ("pstsc", "COM1, Level 1, Printer Area | LEXMARK MS821DN, A4"),
    ("pstsc-sx", "COM1, Level 1, Printer Area | LEXMARK MS821DN, A4"),
    ("pstsc-nb", "COM1, Level 1, Printer Area | LEXMARK MS821DN, A4"),
    ("cptsc", "COM1-01-06, Technical Services | LEXMARK CS921DE, Colour A4"),
    ("cptsc-dx", "COM1-01-06, Technical Services | LEXMARK CS921DE, Colour A4"),
    ("cptsc-a3", "LEXMARK CS921DE, Colour A3"),
    ("cptsc-a3-dx", "LEXMARK CS921DE, Colour A3"),
    ("pse124", "COM3-01-24, Printer Room | LEXMARK MS810, A4"),
    ("pse124-sx", "COM3-01-24, Printer Room | LEXMARK MS810, A4"),
    ("psf204", "COM4, Level 2, Printer Area (corridor) | LEXMARK MS810, A4"),
    ("psf204-sx", "COM4, Level 2, Printer Area (corridor) | LEXMARK MS810, A4"),
]

PRINTER_DISPLAY_LIST = [f"{p[0]} ({p[1]})" for p in PRINTERS_RAW]
CHECK_QUOTA_URL = "https://mysoc.nus.edu.sg/~eprint/forms/quota.php"
BUY_QUOTA_URL = "https://socpay.comp.nus.edu.sg/"

MATERIAL_QSS = """
QWidget {
    background-color: #ffffff;
    color: #202124;
}

QLabel {
    font-size: 16px;
}

QLabel#Title {
    font-size: 42px;
    font-weight: bold;
    color: #1a73e8;
    padding-bottom: 15px;
}

QLabel#Subtitle {
    font-size: 18px;
    font-weight: bold;
    color: #5f6368;
    margin-top: 5px;
}

QPushButton {
    font-size: 15px;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
}

QPushButton#Primary {
    background-color: #1a73e8;
    color: #ffffff;
    border: none;
}
QPushButton#Primary:hover {
    background-color: #1b66c9;
}

QPushButton#Secondary {
    background-color: transparent;
    color: #1a73e8;
    border: 1px solid #dadce0;
}
QPushButton#Secondary:hover {
    background-color: #f8f9fa;
    border: 1px solid #1a73e8;
}

QPushButton#Danger {
    background-color: transparent;
    color: #d93025;
    border: 1px solid #dadce0;
}
QPushButton#Danger:hover {
    background-color: #fce8e6;
    border: 1px solid #d93025;
}

QLineEdit, QComboBox {
    font-size: 16px;
    border: 1px solid #dadce0;
    border-radius: 8px;
    padding: 10px;
    background-color: #f8f9fa;
}
QLineEdit:focus, QComboBox:focus {
    border: 2px solid #1a73e8;
    background-color: #ffffff;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QTableWidget {
    border: 1px solid #dadce0;
    border-radius: 8px;
    font-size: 15px;
}
QHeaderView::section {
    font-size: 14px;
    font-weight: bold;
    background-color: #f1f3f4;
    padding: 8px;
}
"""

class AddAccountDialog(QDialog):
    def __init__(self, parent=None, username="", password=""):
        super().__init__(parent)
        self.setWindowTitle("Manage Account")
        self.setFixedSize(500, 380)
        self.setStyleSheet(MATERIAL_QSS)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        
        title = QLabel("Account Details")
        title.setObjectName("Subtitle")
        layout.addWidget(title)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("NUSNET Username")
        self.user_input.setText(username)
        layout.addWidget(self.user_input)
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setText(password)
        layout.addWidget(self.pass_input)
        
        layout.addStretch()
        
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("Secondary")
        cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("Primary")
        self.save_btn.clicked.connect(self.accept)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)
        
    def get_data(self):
        return self.user_input.text().strip(), self.pass_input.text().strip()

class SettingsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 60, 60, 60)
        layout.setSpacing(30)
        
        header_layout = QHBoxLayout()
        title = QLabel("Manage Accounts")
        title.setObjectName("Title")
        header_layout.addWidget(title)
        
        done_btn = QPushButton("Done")
        done_btn.setObjectName("Primary")
        done_btn.clicked.connect(lambda: self.main_window.stack.setCurrentIndex(0))
        header_layout.addWidget(done_btn, alignment=Qt.AlignRight | Qt.AlignVCenter)
        layout.addLayout(header_layout)
        
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Username", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Account")
        add_btn.setObjectName("Secondary")
        add_btn.clicked.connect(self.add_account)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setObjectName("Secondary")
        edit_btn.clicked.connect(self.edit_account)
        
        del_btn = QPushButton("Remove")
        del_btn.setObjectName("Danger")
        del_btn.clicked.connect(self.delete_account)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(del_btn)
        layout.addLayout(btn_layout)

    def refresh_data(self):
        self.table.setRowCount(0)
        for cred in config.get_credentials():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setRowHeight(row, 50)
            self.table.setItem(row, 0, QTableWidgetItem(cred["username"]))
            self.table.setItem(row, 1, QTableWidgetItem("Ready"))

    def add_account(self):
        dialog = AddAccountDialog(self)
        if dialog.exec_():
            u, p = dialog.get_data()
            if u and p:
                config.add_credential(u, p)
                self.refresh_data()
                self.main_window.main_page.refresh_users()

    def edit_account(self):
        selected = self.table.selectedItems()
        if not selected: return
        username = selected[0].text()
        password = next((c["password"] for c in config.get_credentials() if c["username"] == username), "")
        dialog = AddAccountDialog(self, username, password)
        if dialog.exec_():
            u, p = dialog.get_data()
            if u and p:
                config.edit_credential(username, u, p)
                self.refresh_data()
                self.main_window.main_page.refresh_users()

    def delete_account(self):
        selected = self.table.selectedItems()
        if not selected: return
        username = selected[0].text()
        if QMessageBox.question(self, "Remove", f"Remove '{username}'?") == QMessageBox.Yes:
            config.delete_credential(username)
            self.refresh_data()
            self.main_window.main_page.refresh_users()

class MainPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        
        lp, _ = config.get_last_settings()
        for i in range(self.printer_cb.count()):
            if self.printer_cb.itemText(i).startswith(lp + " ("):
                self.printer_cb.setCurrentIndex(i)
                break
        
        self.refresh_users()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(80, 60, 80, 60)
        layout.setSpacing(25)
        
        title = QLabel("SoC Print Service")
        title.setObjectName("Title")
        layout.addWidget(title, alignment=Qt.AlignHCenter)
        layout.addSpacing(20)
        
        doc_label = QLabel("1. Select Document")
        doc_label.setObjectName("Subtitle")
        layout.addWidget(doc_label)
        
        doc_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("No file selected...")
        self.file_input.setReadOnly(True)
        doc_layout.addWidget(self.file_input, stretch=1)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("Secondary")
        browse_btn.clicked.connect(self.browse_file)
        doc_layout.addWidget(browse_btn)
        layout.addLayout(doc_layout)
        
        layout.addSpacing(15)
        
        print_label = QLabel("2. Select Printer")
        print_label.setObjectName("Subtitle")
        layout.addWidget(print_label)
        
        self.printer_cb = QComboBox()
        self.printer_cb.addItems(PRINTER_DISPLAY_LIST)
        layout.addWidget(self.printer_cb)
        
        layout.addSpacing(15)
        
        set_label = QLabel("3. Select Account")
        set_label.setObjectName("Subtitle")
        layout.addWidget(set_label)
        
        set_layout = QHBoxLayout()
        acct_label = QLabel("Print as:")
        acct_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        set_layout.addWidget(acct_label)
        
        self.user_cb = QComboBox()
        self.user_cb.setMinimumWidth(250)
        set_layout.addWidget(self.user_cb)
        set_layout.addStretch()
        layout.addLayout(set_layout)
        
        layout.addStretch()
        
        action_layout = QHBoxLayout()
        manage_btn = QPushButton("Manage Accounts")
        manage_btn.setObjectName("Secondary")
        manage_btn.clicked.connect(lambda: self.main_window.stack.setCurrentIndex(1))
        
        quota_btn = QPushButton("Check Quota")
        quota_btn.setObjectName("Secondary")
        quota_btn.clicked.connect(lambda: webbrowser.open(CHECK_QUOTA_URL))
        
        buy_btn = QPushButton("Buy Quota")
        buy_btn.setObjectName("Secondary")
        buy_btn.clicked.connect(lambda: webbrowser.open(BUY_QUOTA_URL))
        
        self.print_btn = QPushButton("Print Document")
        self.print_btn.setObjectName("Primary")
        self.print_btn.clicked.connect(self.do_print)
        
        action_layout.addWidget(manage_btn)
        action_layout.addWidget(quota_btn)
        action_layout.addWidget(buy_btn)
        action_layout.addStretch()
        action_layout.addWidget(self.print_btn)
        layout.addLayout(action_layout)

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Document")
        if path: self.file_input.setText(path)

    def refresh_users(self):
        curr = self.user_cb.currentText()
        self.user_cb.clear()
        names = [c["username"] for c in config.get_credentials()]
        self.user_cb.addItems(names)
        if curr in names: self.user_cb.setCurrentText(curr)

    def do_print(self):
        f = self.file_input.text()
        p_full = self.printer_cb.currentText()
        p = p_full.split(" (")[0]
        u = self.user_cb.currentText()
        
        if not f:
            QMessageBox.critical(self, "Error", "Please select a document.")
            return
        if not u:
            QMessageBox.critical(self, "Error", "Please select an account.")
            return
            
        pw = next((c["password"] for c in config.get_credentials() if c["username"] == u), None)
        config.save_last_settings(p, False)
        
        self.print_btn.setText("Sending...")
        self.print_btn.setEnabled(False)
        QApplication.processEvents()
        
        out, ok = cli_forge.execute_printing(f, u, pw, p, False)
        
        self.print_btn.setText("Print Document")
        self.print_btn.setEnabled(True)
        
        if ok: QMessageBox.information(self, "Success", "Sent successfully.")
        else: QMessageBox.critical(self, "Failed", f"Error:\n\n{out}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NUS SoC Print Client")
        self.setMinimumSize(950, 750)
        self.setStyleSheet(MATERIAL_QSS)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        self.main_page = MainPage(self)
        self.settings_page = SettingsPage(self)
        
        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.settings_page)
        self.stack.currentChanged.connect(self.on_stack_change)
        self.check_dependencies()

    def on_stack_change(self, idx):
        if idx == 1: self.settings_page.refresh_data()
        else: self.main_page.refresh_users()

    def check_dependencies(self):
        missing = cli_forge.check_dependencies()
        if missing: QMessageBox.warning(self, "Missing Tools", f"Install: {', '.join(missing)}")

def main():
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    
    # Use Fusion style to avoid system theme font mapping bugs on Linux
    app.setStyle("Fusion")
    
    # Explicitly set a default font to prevent invalid system font descriptions
    default_font = QFont("Sans Serif", 11)
    app.setFont(default_font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
