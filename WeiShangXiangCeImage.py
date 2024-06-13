import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, pyqtSlot, QDateTime, QTimer
from PyQt5.QtWebChannel import QWebChannel
import json
from PyQt5.QtWebEngineCore import QWebEngineCookieStore

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
        self.start_button = QPushButton("开始")
        left_layout.addWidget(self.start_button)

        # 添加结束按钮
        self.end_button = QPushButton("结束")
        left_layout.addWidget(self.end_button)

        # 添加表格区域
        self.table = QTableWidget(0, 1)  # 初始表格有0行1列
        self.table.setHorizontalHeaderLabels(["请求链接"])
        left_layout.addWidget(self.table)

        # 添加保存 cookies 按钮
        self.save_cookies_button = QPushButton("保存 Cookies")
        left_layout.addWidget(self.save_cookies_button)
        self.save_cookies_button.clicked.connect(self.save_cookies)

        splitter.addWidget(left_widget)

        # 右边网页浏览框
        self.webview = QWebEngineView()
        self.load_cookies()
        self.webview.setUrl(QUrl("https://www.szwego.com/static/index.html#/pc_login"))
        splitter.addWidget(self.webview)

        # 设置 WebChannel
        self.channel = QWebChannel()
        self.webview.page().setWebChannel(self.channel)
        self.channel.registerObject("handler", self)

        # 设置分割器的比例
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        # 将分割器添加到布局中
        layout.addWidget(splitter)

        # 连接按钮点击事件
        self.start_button.clicked.connect(self.start_capture)
        self.end_button.clicked.connect(self.end_capture)

        self.capturing = False

        # 定时器定期保存 cookies
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.save_cookies)
        self.timer.start(60000)  # 每分钟保存一次

    def start_capture(self):
        self.capturing = True
        self.webview.page().runJavaScript("""
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

    def end_capture(self):
        self.capturing = False

    @pyqtSlot(str)
    def handleRequest(self, url):
        if self.capturing:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(url))

    def save_cookies(self):
        self.webview.page().profile().cookieStore().allCookies(self.handle_all_cookies)

    def handle_all_cookies(self, cookies):
        cookies_list = []
        for cookie in cookies:
            cookies_list.append({
                'name': cookie.name().data().decode('utf-8'),
                'value': cookie.value().data().decode('utf-8'),
                'domain': cookie.domain(),
                'path': cookie.path(),
                'expiry': cookie.expirationDate().toSecsSinceEpoch(),
                'secure': cookie.isSecure(),
                'httpOnly': cookie.isHttpOnly()
            })
        with open("cookies.json", "w") as file:
            json.dump(cookies_list, file)

    def load_cookies(self):
        try:
            with open("cookies.json", "r") as file:
                cookies_list = json.load(file)
                for cookie_dict in cookies_list:
                    cookie = QWebEngineCookieStore.Cookie()
                    cookie.setName(cookie_dict['name'].encode('utf-8'))
                    cookie.setValue(cookie_dict['value'].encode('utf-8'))
                    cookie.setDomain(cookie_dict['domain'])
                    cookie.setPath(cookie_dict['path'])
                    cookie.setExpirationDate(QDateTime.fromSecsSinceEpoch(cookie_dict['expiry']))
                    cookie.setSecure(cookie_dict['secure'])
                    cookie.setHttpOnly(cookie_dict['httpOnly'])
                    self.webview.page().profile().cookieStore().setCookie(cookie)
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
