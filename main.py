import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTabWidget, QDialog, QLabel, QFileDialog, QProgressBar
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon, QPalette, QColor


class NebulaBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NebulaBrowser")
        self.setGeometry(100, 100, 1024, 768)

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)

        # Set IE8-like colors
        self.setStyleSheet("""
            QMainWindow { background-color: #F2F2F2; }
            QPushButton {
                background-color: #D4D0C8;
                border: 1px solid #808080;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
            QLineEdit {
                background-color: #FFFFFF;
                border: 1px solid #808080;
                padding: 3px;
            }
            QProgressBar {
                border: 1px solid gray;
                text-align: center;
                background: white;
            }
            QProgressBar::chunk {
                background: #0078D7;
                width: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #A0A0A0;
                background: #ECE9D8;
            }
        """)

        # Toolbar Layout (Horizontal like IE8)
        toolbar_layout = QHBoxLayout()

        self.back_button = QPushButton("◄", self)
        self.back_button.clicked.connect(self.go_back)
        toolbar_layout.addWidget(self.back_button)

        self.forward_button = QPushButton("►", self)
        self.forward_button.clicked.connect(self.go_forward)
        toolbar_layout.addWidget(self.forward_button)

        self.refresh_button = QPushButton("⟳", self)
        self.refresh_button.clicked.connect(self.reload_page)
        toolbar_layout.addWidget(self.refresh_button)

        self.url_bar = QLineEdit(self)
        self.url_bar.setPlaceholderText("Enter URL")
        self.url_bar.returnPressed.connect(self.load_url)
        toolbar_layout.addWidget(self.url_bar)

        self.new_tab_button = QPushButton("New Tab", self)
        self.new_tab_button.clicked.connect(self.add_new_tab)
        toolbar_layout.addWidget(self.new_tab_button)

        self.settings_button = QPushButton("⚙", self)
        self.settings_button.clicked.connect(self.open_settings)
        toolbar_layout.addWidget(self.settings_button)

        self.downloads_button = QPushButton("⬇", self)
        self.downloads_button.clicked.connect(self.open_downloads)
        toolbar_layout.addWidget(self.downloads_button)

        main_layout.addLayout(toolbar_layout)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        main_layout.addWidget(self.tabs)

        # Loading Bar (Safari-style)
        self.loading_bar = QProgressBar(self)
        self.loading_bar.setMaximum(100)
        main_layout.addWidget(self.loading_bar)

        self.add_new_tab(QUrl("https://www.google.com"))

    def add_new_tab(self, qurl=None):
        browser = QWebEngineView()
        browser.setUrl(qurl or QUrl("https://www.google.com"))
        browser.loadProgress.connect(self.update_progress)

        index = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(index)

        browser.urlChanged.connect(lambda url: self.update_tab_title(browser, url))

    def update_tab_title(self, browser, url):
        index = self.tabs.indexOf(browser)
        self.tabs.setTabText(index, url.toString())

    def update_progress(self, progress):
        self.loading_bar.setValue(progress)
        if progress == 100:
            self.loading_bar.hide()
        else:
            self.loading_bar.show()

    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.setUrl(QUrl(url))

    def go_back(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.back()

    def go_forward(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.forward()

    def reload_page(self):
        current_browser = self.tabs.currentWidget()
        if current_browser:
            current_browser.reload()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def open_settings(self):
        settings_dialog = SettingsDialog()
        settings_dialog.exec_()

    def open_downloads(self):
        downloads_dialog = DownloadsDialog()
        downloads_dialog.exec_()

    def closeEvent(self, event):
        """Ensure full exit when closing."""
        sys.exit(0)  # Force quit application


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 300, 250)

        layout = QVBoxLayout()

        self.about_button = QPushButton("About NebulaBrowser")
        self.about_button.clicked.connect(self.show_about)
        layout.addWidget(self.about_button)

        self.setLayout(layout)

    def show_about(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("About NebulaBrowser")
        self.setGeometry(300, 300, 250, 150)

        layout = QVBoxLayout()
        label = QLabel("NebulaBrowser 1.0 Build 1050", self)
        layout.addWidget(label)

        self.setLayout(layout)


class DownloadsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Downloads")
        self.setGeometry(250, 250, 300, 200)

        layout = QVBoxLayout()
        self.download_button = QPushButton("Download File", self)
        self.download_button.clicked.connect(self.download_file)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def download_file(self):
        file_url, _ = QFileDialog.getOpenFileName(self, "Select File to Download")
        if file_url:
            print(f"Downloading file: {file_url}")  # Simulated download


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NebulaBrowser()
    window.show()
    sys.exit(app.exec_())
