from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import os
import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com/'))

        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navb = QToolBar("Navigation")
        navb.setIconSize(QSize(16, 16))
        self.addToolBar(navb)

        back_btn = QAction(QIcon(os.path.join('images', 'arrow-180.png')), "Back", self)
        back_btn.setStatusTip("Back to page")
        back_btn.triggered.connect(self.browser.back)
        navb.addAction(back_btn)

        forward_btn = QAction(QIcon(os.path.join('images', 'arrow-000.png')), "Forward", self)
        forward_btn.setStatusTip("Forward to next page")
        forward_btn.triggered.connect(self.browser.forward)
        navb.addAction(forward_btn)

        reload_btn = QAction(QIcon(os.path.join('images', 'reload.png')), "Reload", self)
        reload_btn.setStatusTip("Reload the page")
        reload_btn.triggered.connect(self.browser.reload)
        navb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('images', 'home.png')), "Home", self)
        home_btn.setStatusTip("Go to the home page")
        home_btn.triggered.connect(self.navigate_home)
        navb.addAction(home_btn)

        navb.addSeparator()
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap.scaled(QPixmap(os.path.join('images', 'icons8-lock-40.png')), 16, 16))
        navb.addWidget(self.httpsicon)

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.navigate_to_url)
        navb.addWidget(self.urlBar)

        stop_btn = QAction(QIcon(os.path.join('images', 'icons8-cross-64.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading")
        stop_btn.triggered.connect(self.browser.stop)
        navb.addAction(stop_btn)

        file_menu = self.menuBar().addMenu('&File')

        open_file = QAction(QIcon(os.path.join('images', 'icons8-save-64.png')), "Open file", self)
        open_file.setStatusTip("Open file")
        open_file.triggered.connect(self.open_file)
        navb.addAction(open_file)

        save_file = QAction(QIcon(os.path.join('images', 'icons8-save-as-48.png')), "Save file", self)
        save_file.setStatusTip("Save file")
        save_file.triggered.connect(self.save_file)
        navb.addAction(save_file)

        help_menu = self.menuBar().addMenu('&Help')

        about_action = QAction(QIcon(os.path.join('images', 'icons8-question-maerk-48.png')), "About my browser", self)
        about_action.setStatusTip("About browser")
        about_action.triggered.connect(self.about_action)
        navb.addAction(about_action)

        self.show()
        self.setWindowIcon(QIcon(os.path.join('images', 'icons8-microsoft-edge-48.png')))

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - KEK4ok" % title)

    def about_action(self):
        pass

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                  "*.htm *.html"
                                                  "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

                self.browser.setHtml(html)
                self.urlBar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                                                  "*.htm *.html"
                                                  "All files (*.*)")

        if filename:
            html = self.browser.page().toHtml()
            with open(filename, 'w') as f:
                f.write(html)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com/"))

    def navigate_to_url(self):
        q = QUrl(self.urlBar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_urlbar(self, q):

        if q.scheme() == "https":
            self.httpsicon.setPixmap(QPixmap.scaled(QPixmap(os.path.join('images', 'icons8-ssl-64.png')), 16, 16))
        else:
            self.httpsicon.setPixmap(QPixmap.scaled(QPixmap(os.path.join('images', 'icons8-no-ssl-64.png')), 16, 16))

        self.urlBar.setText(q.toString())
        self.urlBar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("Kek4ok Browser")
app.setOrganizationName("KEK4OK")

window = MainWindow()
app.exec_()
