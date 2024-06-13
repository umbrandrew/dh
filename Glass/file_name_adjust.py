import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QComboBox, \
    QTextEdit
from PyQt5.QtGui import QFont, QScreen
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_brands()

    def initUI(self):
        layout = QVBoxLayout()

        path_layout = QHBoxLayout()
        self.path_label = QLabel("选择的文件夹路径:")
        self.path_label.setFont(QFont("Arial", 14, QFont.Bold))
        path_layout.addWidget(self.path_label)

        self.path_output = QLineEdit(self)
        self.path_output.setFont(QFont("Arial", 12))
        path_layout.addWidget(self.path_output)
        layout.addLayout(path_layout)

        self.open_button = QPushButton("打开文件夹", self)
        self.open_button.setFont(QFont("Arial", 12))
        self.open_button.setStyleSheet("background-color: lightblue;")
        self.open_button.clicked.connect(self.open_folder)
        layout.addWidget(self.open_button)

        self.read_txt_button = QPushButton("读取txt", self)
        self.read_txt_button.setFont(QFont("Arial", 12))
        self.read_txt_button.setStyleSheet("background-color: lightgreen;")
        self.read_txt_button.clicked.connect(self.read_txt_files)
        layout.addWidget(self.read_txt_button)

        self.txt_display = QTextEdit(self)
        self.txt_display.setFont(QFont("Arial", 12))
        self.txt_display.setMinimumHeight(300)  # 设置最小高度为300
        layout.addWidget(self.txt_display)

        brand_layout = QHBoxLayout()
        self.brand_label = QLabel("品牌:")
        self.brand_label.setFont(QFont("Arial", 14, QFont.Bold))
        brand_layout.addWidget(self.brand_label)

        self.brand_combo = QComboBox(self)
        self.brand_combo.setFont(QFont("Arial", 12))
        self.brand_combo.setEditable(True)
        brand_layout.addWidget(self.brand_combo)
        layout.addLayout(brand_layout)

        model_layout = QHBoxLayout()
        self.model_label = QLabel("型号:")
        self.model_label.setFont(QFont("Arial", 14, QFont.Bold))
        model_layout.addWidget(self.model_label)

        self.model_input = QLineEdit(self)
        self.model_input.setFont(QFont("Arial", 12))
        model_layout.addWidget(self.model_input)
        layout.addLayout(model_layout)

        number_layout = QHBoxLayout()
        self.number_label = QLabel("编号:")
        self.number_label.setFont(QFont("Arial", 14, QFont.Bold))
        number_layout.addWidget(self.number_label)

        self.number_input = QLineEdit(self)
        self.number_input.setFont(QFont("Arial", 12))
        number_layout.addWidget(self.number_input)
        layout.addLayout(number_layout)

        price_layout = QHBoxLayout()
        self.price_label = QLabel("原生价格:")
        self.price_label.setFont(QFont("Arial", 14, QFont.Bold))
        price_layout.addWidget(self.price_label)

        self.price_input = QLineEdit(self)
        self.price_input.setFont(QFont("Arial", 12))
        price_layout.addWidget(self.price_input)
        layout.addLayout(price_layout)

        self.generate_button = QPushButton("生成", self)
        self.generate_button.setFont(QFont("Arial", 12))
        self.generate_button.setStyleSheet("background-color: lightcoral;")
        self.generate_button.setFixedHeight(100)  # 增加按钮高度
        self.generate_button.clicked.connect(self.generate_output)

        self.convert_button = QPushButton("转换", self)
        self.convert_button.setFont(QFont("Arial", 12))
        self.convert_button.setStyleSheet("background-color: lightyellow;")
        self.convert_button.setFixedHeight(100)  # 增加按钮高度
        self.convert_button.clicked.connect(self.convert_folder_name)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.convert_button)
        layout.addLayout(button_layout)

        output_layout = QHBoxLayout()
        self.output_label = QLabel("预览结果:")
        self.output_label.setFont(QFont("Arial", 14, QFont.Bold))
        output_layout.addWidget(self.output_label)

        self.output_edit = QTextEdit(self)
        self.output_edit.setFont(QFont("Arial", 12))
        self.output_edit.setFixedHeight(60)  # 调整高度为2-3行
        output_layout.addWidget(self.output_edit)
        layout.addLayout(output_layout)

        self.setLayout(layout)
        self.setWindowTitle('文件夹管理器')
        self.setGeometry(300, 300, 1000, 1500)
        self.center()

    def center(self):
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "G:\\敦煌\\眼镜")
        if folder_path:
            self.path_output.setText(folder_path)
            self.clear_data()
            self.initialize_plugins(folder_path)

    def clear_data(self):
        self.txt_display.clear()
        self.model_input.clear()
        self.number_input.clear()
        self.price_input.clear()
        self.output_edit.clear()

    def initialize_plugins(self, folder_path):
        self.read_txt_files()
        self.number_input.setText(os.path.basename(folder_path))

    def read_txt_files(self):
        folder_path = self.path_output.text()
        if folder_path:
            txt_content = ""
            for file_name in os.listdir(folder_path):
                if file_name.endswith(".txt"):
                    with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
                        txt_content += file.read() + "\n"
                        self.set_default_price(txt_content)
            self.txt_display.setText(txt_content)
            self.adjust_txt_display_height(txt_content)

    def adjust_txt_display_height(self, txt_content):
        line_count = txt_content.count('\n') + 1
        line_height = 20  # 每行的高度估计为20像素
        new_height = max(min(line_count * line_height, 400), 300)  # 最大400，最小300
        self.txt_display.setFixedHeight(new_height)

    def set_default_price(self, txt_content):
        import re
        match = re.search(r'P(\d+)', txt_content)
        if match:
            self.price_input.setText(match.group(1))

    def generate_output(self):
        brand = self.brand_combo.currentText()
        model = self.model_input.text()
        number = self.number_input.text()
        price = self.price_input.text()
        result = f"{brand}-{model}-{number}-P{price}"
        self.output_edit.setText(result)
        self.save_brand(brand)

    def convert_folder_name(self):
        current_path = self.path_output.text()
        new_name = self.output_edit.toPlainText()
        if current_path and new_name:
            new_path = os.path.join(os.path.dirname(current_path), new_name)
            os.rename(current_path, new_path)
            self.path_output.setText(new_path)

    def load_brands(self):
        try:
            with open("brands.json", "r") as file:
                brands = json.load(file)
                brands.sort()  # 按字母顺序排序
                self.brand_combo.addItems(brands)
        except FileNotFoundError:
            pass

    def save_brand(self, brand):
        if brand and brand not in [self.brand_combo.itemText(i) for i in range(self.brand_combo.count())]:
            self.brand_combo.addItem(brand)
            brands = [self.brand_combo.itemText(i) for i in range(self.brand_combo.count())]
            brands.sort()  # 按字母顺序排序
            with open("brands.json", "w") as file:
                json.dump(brands, file)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
