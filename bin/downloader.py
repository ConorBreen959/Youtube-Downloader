import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from pytube import YouTube

from config import CONFIG

logging.basicConfig(
    filename=CONFIG["ERROR_LOG"],
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.INFO,
)


class GUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.url_count = 0
        self.urls = []
        self.setGeometry(250, 250, 250, 250)
        self.setWindowTitle("Keeva's Youtube Downloader")
        widget = QWidget()
        self.grid = QGridLayout()
        self.title = QLabel("Add Youtube Links to Download", self)
        self.title.setAlignment(Qt.AlignCenter)
        self.status= QLabel("", self)
        self.status.setAlignment(Qt.AlignCenter)
        self.run_button = QPushButton("Download", self)
        self.run_button.clicked.connect(self.download)
        self.add_button = QPushButton("Add Video", self)
        self.add_button.clicked.connect(self.addurlbox)
        self.remove_button = QPushButton("Clear Video", self)
        self.remove_button.clicked.connect(self.removeurlbox)
        self.grid.addWidget(self.title, 0, 0, 1, 0)
        self.grid.addWidget(self.status, 1, 0, 1, 0)
        self.grid.addWidget(self.run_button, 2, 0, 1, 0)
        self.grid.addWidget(self.add_button, 3, 1)
        self.grid.addWidget(self.remove_button, 3, 0)
        widget.setLayout(self.grid)
        self.setCentralWidget(widget)
        self.show()
        
    def addurlbox(self):
        self.url_count += 1
        self.url_box = QLineEdit(self)
        self.grid.addWidget(self.url_box, self.url_count + 3, 0, 1, 0)
        self.url_box.textChanged.connect(self.captureurl)
        print(self.urls)
        print(self.url_count)
    
    def removeurlbox(self):
        if self.url_count > 0:
            for n in range(self.url_count):
                self.grid.itemAt(n + 5).widget().deleteLater()
        self.url_count = 0
        self.urls = []
        
    def captureurl(self, url):
        self.urls.append(url)
    
    def download(self):
        failed_downloads = []
        self.urls = [url for url in self.urls if url.startswith("https://you")]
        self.url_count = len(self.urls)
        for url, count in zip(self.urls, range(self.url_count)):
            self.status.setText(f"Downloading {count + 1} of {self.url_count}...")
            self.status.repaint()
            print(url)
            print(count)
            try:
                yt = YouTube(url)
                yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download(CONFIG["DOWNLOAD_DIR"])
            except Exception as e:
                logging.error(e, exc_info=True)
                failed_downloads.append(url)
        if failed_downloads:
            self.log_failed_downloads(failed_downloads)
        self.status.setText("Finished!")
            
    def log_failed_downloads(self, failed_downloads):
        msg = QMessageBox(self)
        msg.setText(f"These URLs did not download, please try again or speak to Con Con:{os.linesep}{os.linesep}{os.linesep.join(map(str, failed_downloads))}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setWindowTitle("ERROR")
        msg.setIcon(QMessageBox.Critical)
        msg.show()        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    GUI = GUI()
    sys.exit(app.exec_())        
