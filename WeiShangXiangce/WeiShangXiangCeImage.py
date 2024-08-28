import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript, QWebEngineScriptCollection
from PyQt5.QtCore import Qt, QUrl, QDateTime, pyqtSlot
from PyQt5.QtWebChannel import QWebChannel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("窗口程序")
        self.showMaximized()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout(main_widget)
        splitter = QSplitter(Qt.Horizontal)

        self.left_layout = QVBoxLayout()
        self.left_widget = QWidget()
        self.left_widget.setFixedWidth(500)

        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start_detection)
        self.left_layout.addWidget(self.start_button)

        self.end_button = QPushButton("结束")
        self.left_layout.addWidget(self.end_button)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["URL", "请���时间"])
        self.left_layout.addWidget(self.table)

        self.left_widget.setLayout(self.left_layout)
        splitter.addWidget(self.left_widget)

        self.right_widget = QWidget()
        self.right_layout = QVBoxLayout(self.right_widget)

        self.webview = QWebEngineView()
        self.webview.setFixedWidth(1600)
        self.webview.setFixedHeight(1200)
        self.webview.setUrl(QUrl("https://www.szwego.com/static/index.html#/pc_login"))
        self.right_layout.addWidget(self.webview)

        splitter.addWidget(self.right_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        layout.addWidget(splitter)

        self.channel = QWebChannel()
        self.channel.registerObject("handler", self)
        self.webview.page().setWebChannel(self.channel)

        self.webview.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self):
        js_code = """
            (function() {
                var oldFetch = fetch;
                fetch = function() {
                    var url = arguments[0];
                    if (url.includes("szwego.com/album/personal/all")) {
                        new QWebChannel(qt.webChannelTransport, function(channel) {
                            channel.objects.handler.receiveUrl(url);
                        });
                    }
                    return oldFetch.apply(this, arguments);
                };
            })();
        """
        script = QWebEngineScript()
        script.setSourceCode(js_code)
        script.setWorldId(QWebEngineScript.MainWorld)
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setRunsOnSubFrames(True)

        self.webview.page().scripts().insert(script)

    def start_detection(self):
        self.webview.page().runJavaScript("""
            (function() {
                var oldFetch = fetch;
                fetch = function() {
                    var url = arguments[0];
                    if (url.includes("szwego.com/album/personal/all")) {
                        new QWebChannel(qt.webChannelTransport, function(channel) {
                            channel.objects.handler.receiveUrl(url);
                        });
                    }
                    return oldFetch.apply(this, arguments);
                };
            })();
        """)

    @pyqtSlot(str)
    def receiveUrl(self, url):
        print("Received URL:", url)
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(url))
        self.table.setItem(row_position, 1, QTableWidgetItem(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
