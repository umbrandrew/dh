import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineCore import QWebEnginePage, QWebEngineProfile
from PyQt5.QtWebChannel import QWebChannel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("窗口程序")
        self.setGeometry(100, 100, 1200, 800)

        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # 创建垂直布局
        layout = QVBoxLayout(main_widget)

        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)

        # 左边布局区域
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        # 添加开始按钮
        start_button = QPushButton("开始")
        left_layout.addWidget(start_button)

        # 添加结束按钮
        end_button = QPushButton("结束")
        left_layout.addWidget(end_button)

        # 添加表格区域
        table = QTableWidget(10, 3)  # 假设表格有10行3列
        left_layout.addWidget(table)

        splitter.addWidget(left_widget)

        # 右边网页浏览框
        webview = QWebEngineView()
        webview.setUrl(QUrl("https://www.szwego.com/static/index.html#/pc_login"))
        splitter.addWidget(webview)

        # 设置 WebChannel
        channel = QWebChannel()
        webview.page().setWebChannel(channel)
        channel.registerObject("handler", self)

        # 注入 JavaScript 代码捕获请求
        webview.page().runJavaScript("""
            (function() {
                var open = XMLHttpRequest.prototype.open;
                XMLHttpRequest.prototype.open = function() {
                    this.addEventListener('load', function() {
                        if (this.responseURL.includes('https://www.szwego.com/album/personal/all')) {
                            handler.handleRequest(this.responseURL);
                        }
                    });
                    open.apply(this, arguments);
                };
            })();
        """)

        # 设置分割器的比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        # 将分割器添加到布局中
        layout.addWidget(splitter)

    def handleRequest(self, url):
        print("Captured URL:", url)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
