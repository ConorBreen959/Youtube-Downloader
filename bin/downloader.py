import os
import sys
import ctypes
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from vimeo_downloader import Vimeo
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
        myappid = 'video.downloader'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle("Keeva's Video Downloader")
        widget = QWidget()
        self.grid = QGridLayout()
        self.title = QLabel("Add Youtube & Vimeo Links to Download", self)
        img_label = QLabel(self)
        pixmap = QPixmap("concon.jpg")
        img_label.resize(125, 125)
        img_label.setPixmap(pixmap.scaled(img_label.size()))
        img_label.setScaledContents(True)
        self.title.setAlignment(Qt.AlignCenter)
        self.status= QLabel("", self)
        self.status.setAlignment(Qt.AlignCenter)
        self.run_button = QPushButton("Download", self)
        self.run_button.clicked.connect(self.download)
        self.add_button = QPushButton("Add Video", self)
        self.add_button.clicked.connect(self.addurlbox)
        self.remove_button = QPushButton("Clear Video", self)
        self.remove_button.clicked.connect(self.removeurlbox)
        self.grid.addWidget(img_label, 0, 0)
        self.grid.addWidget(self.title, 1, 0, 1, 0)
        self.grid.addWidget(self.status, 2, 0, 1, 0)
        self.grid.addWidget(self.run_button, 3, 0, 1, 0)
        self.grid.addWidget(self.add_button, 4, 1)
        self.grid.addWidget(self.remove_button, 4, 0)
        widget.setLayout(self.grid)
        self.setCentralWidget(widget)
        self.show()
        
    def addurlbox(self):
        self.url_count += 1
        self.url_box = QLineEdit(self)
        self.grid.addWidget(self.url_box, self.url_count + 4, 0, 1, 0)
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
        valid_url_prefixes = ("https://you", "https://www.you", "https://vimeo")
        failed_downloads = []
        invalid_urls = [url for url in self.urls if not url.startswith(valid_url_prefixes)]
        self.urls = [url for url in self.urls if url.startswith(valid_url_prefixes)]
        self.url_count = len(self.urls)
        for url, count in zip(self.urls, range(self.url_count)):
            self.status.setText(f"Downloading {count + 1} of {self.url_count}...")
            self.status.repaint()
            print(url)
            print(count)
            try:
                if url.startswith(("https://you", "https://www.you")):
                    print(url)
                    yt = YouTube(url)
                    yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download(CONFIG["DOWNLOAD_DIR"])
                elif url.startswith("https://vimeo"):
                    v = Vimeo(url)
                    filename = "vimeo" + "-" + url.split("/")[-1]
                    s = v.streams
                    best_stream = s[-1]
                    best_stream.download(download_directory=CONFIG["DOWNLOAD_DIR"],
                                         filename=filename)
                else:
                    failed_downloads.append(url)
            except Exception as e:
                logging.error(e, exc_info=True)
                failed_downloads.append(url)
        finish_text = "Finished!"
        if failed_downloads:
            self.log_failed_downloads(failed_downloads)
        if invalid_urls:
            finish_text = finish_text + f"\n\n\nFound some invalid urls:\n\n\n{invalid_urls}\n\n"
        self.status.setText(finish_text)
            
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
