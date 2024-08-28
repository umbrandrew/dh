import sys
import os
import json
import datetime
import sqlite3
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, \
    QLabel, QComboBox, \
    QTextEdit, QMessageBox, QSplitter
from PyQt5.QtGui import QFont, QScreen, QKeySequence, QColor, QPixmap
from PyQt5.QtCore import Qt

brand_dict = {
    'AM': ['Armani', '阿玛尼', 'ARMANI', 'EMPORIO ARMAN'],
    'BAL': ['Balenciaga',
            '巴黎世家',
            'BALENCIAGA',
            'balenciaga',
            'BALENCIAG',
            '𝐵𝑎𝑙𝑒𝑛𝑐𝑖𝑎𝑔𝑎'],
    'BB': ['Burberry', '巴宝莉', 'BURBERRY', '巴家', 'BURBERR'],
    'BC': ['Brunelle Cucineli'],
    'BLM': ['Balmain', '巴尔曼', 'BALMAIN'],
    'BM': ['BAlMAI', 'Balmal'],
    'BV': ['BottegaVeneta', '宝缇嘉', '宝缇', '宝家', '宝缇家', 'BOTTEGA VENET'],
    'BVG': ['Bvlgari', '宝格丽', 'BVLGARI', 'BVLGAR'],
    'CA': ['Cartier', '卡地亚', 'Cartie'],
    'CAR': ['Carrera', '卡雷拉', 'CARRERA'],
    'CAZ': ['CAZA', 'Caza', '卡扎', '卡扎眼镜', 'CAZA眼镜'],
    'CH': ['香奈儿', 'Chanel', '𝗖𝗛𝗔𝗡𝗘𝗟', '小香', '香家', 'Chane'],
    'CL': ['Celine', '赛琳', 'CELINE', 'CELIN', '瑟琳', '塞林'],
    'CO': ['COACH', '蔻驰', 'COACH', '蔻驰'],
    'CP': ['ChoPard', '肖邦', 'Chopar'],
    'CR': ['ChromeHearts', '克罗心', 'CHROMEHEARTS', '剋萝心', 'CHROME HEART'],
    'DB': ['David Beckha'],
    'DG': ['DolceGabbana', '杜嘉班纳', 'DOLCE GABBAN', 'DOLCEGABBAN', 'DG'],
    'DO': ['Dior', '迪奥', 'DIOR', 'DIO', '迪家', '𝐃𝐈𝐎𝐑'],
    'DT': ['Dita', '迪塔', 'DITA'],
    'FD': ['Fendi', '芬迪', 'FENDI', 'FEND'],
    'FRD': ['FRED', 'Fred', '弗雷德', '弗雷'],
    'FM': ['Fakeme', 'FAKEME'],
    'GM': ['GM', 'Gentle Monster', 'PGM', 'GENTLE* MONSTE'],
    'GU': ['Gucci', '古驰', 'GUCCI', 'GUCC', '古池', '古家'],
    'HE': ['赫姆斯', 'Hermes', '爱马仕', 'H家', 'HERME', '爱马士'],
    'HU': ['HUBLOT'],
    'JM': ['JimmyChoo', '卓美亚', 'JIMMY CHO', '吉米家'],
    'JMM': ['JacquesMarieMage',
            'Jacques Marie Mage',
            'JMM',
            'JACQUES MARIE MAGE',
            'JACQUESMARIE MAGE',
            'JACQUES MARIE MAG',
            'JACQUES MARIE'],
    'KR': ['KUB RAUM', 'KUB口RAUM', 'KUBRAUM'],
    'LAC': ['Lacoste', '鳄鱼', 'LACOSTE'],
    'LF': ['LINDA FARROW',
           'LindaFarrow',
           'LINDA FARROW',
           'LINDAFARROW',
           'LINDA FARRO'],
    'LO': ['Loewe', '罗意威', 'LOEWE', 'LOEW'],
    'LV': ['路易威登',
           'LV',
           'Louis Vuitton',
           'Louis Vuitto',
           'LOUIS VUITTO',
           'L家',
           'LOUIS',
           'L v'],
    'MAY': ['Maybach', '迈巴赫'],
    'MB': ['MontBlanc', '万宝龙', 'MB', 'Mont Blanc', 'MONT BLAN'],
    'ML': ['Moncle', 'Moncler'],
    'MM': ['Miumiu', '缪缪', 'MIUMIU', '缪家', '谬家', 'miumiu', 'MIU', 'MiuMi'],
    'MP': ['MAX PITTION', 'Max Pittion', 'MAXPITTION', 'MaxPittion'],
    'MS': ['MOSCOT'],
    'OF': ['Off-White', 'off white', 'off-white', 'offwhite', 'OFF WHITE'],
    'OK': ['Oakley', '奥克利', 'OAKLEY'],
    'PO': ['保时捷', 'Porsche', 'PORSCHE', 'Porsch'],
    'PR': ['Prada', '普拉达', '普家', 'PRAD', 'Prad', 'prada'],
    'RB': ['RayBan', '雷朋', 'RAYBAN'],
    'RC': ['罗伯特', 'Robert'],
    'SF': ['Salvatore Ferragamo', '菲拉格慕', 'SALVATORE FERRAGAMO', 'SALVATORE FERRAGAMO'],
    'SIL': ['Silhouette'],
    'SL': ['SaintLaurent',
           '圣罗兰',
           'SAINTLAURENT',
           'YSL',
           'SAINT LAUREN',
           'SAINT RAUREN'],
    'TB': ['TORY BURC'],
    'TF': ['Tiffany', '蒂芙尼', 'TIFFANY', 'Tiffany'],
    'TO': ['Tom Ford', '汤姆福特', 'TomFord', 'Tom For'],
    'VB': ['VICTORIABECKHAM'],
    'VE': ['范思哲', 'Versace', 'VERSACE', '范思家', 'VERSAC'],
    'VH': ['VEHL', 'Vehl', 'VEHL眼镜', 'Vehl眼镜'],
    'VL': ['Valentino', '华伦天奴', 'VALENYIN', 'VALENTIN'],
    'ZE': ['ZEGNA', 'Zegna', '杰尼亚', '杰尼亚眼镜', 'Zegna眼镜'],
}


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_brands()
        self.init_db()

    def initUI(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()

        path_layout = QHBoxLayout()
        self.path_label = QLabel("选择的文件夹路径:")
        self.path_label.setFont(QFont("Arial", 14, QFont.Bold))
        path_layout.addWidget(self.path_label)

        self.path_output = QLineEdit(self)
        self.path_output.setFont(QFont("Arial", 12))
        path_layout.addWidget(self.path_output)
        left_layout.addLayout(path_layout)

        self.open_button = QPushButton("打开文件夹", self)
        self.open_button.setFont(QFont("Arial", 12))
        self.open_button.setStyleSheet("background-color: lightblue;")
        self.open_button.clicked.connect(self.open_folder)
        self.open_button.setShortcut(QKeySequence("F1"))
        left_layout.addWidget(self.open_button)

        self.txt_display = QTextEdit(self)
        self.txt_display.setFont(QFont("Arial", 12))
        self.txt_display.setMinimumHeight(500)  # 设置最小高度为300
        left_layout.addWidget(self.txt_display)

        brand_layout = QHBoxLayout()
        self.brand_label = QLabel("品牌:")
        self.brand_label.setFont(QFont("Arial", 14, QFont.Bold))
        brand_layout.addWidget(self.brand_label)

        self.brand_combo = QComboBox(self)
        self.brand_combo.setFont(QFont("Arial", 12))
        self.brand_combo.setEditable(True)
        brand_layout.addWidget(self.brand_combo)
        left_layout.addLayout(brand_layout)

        # Add buttons for setting model
        model_buttons_layout = QHBoxLayout()
        self.unknown_button = QPushButton("未知", self)
        self.unknown_button.setFont(QFont("Arial", 12))
        self.unknown_button.clicked.connect(lambda: self.set_model_input("未知"))
        model_buttons_layout.addWidget(self.unknown_button)

        self.scarf_button = QPushButton("围巾", self)
        self.scarf_button.setFont(QFont("Arial", 12))
        self.scarf_button.clicked.connect(lambda: self.set_model_input("围巾"))
        model_buttons_layout.addWidget(self.scarf_button)

        self.hat_button = QPushButton("帽子", self)
        self.hat_button.setFont(QFont("Arial", 12))
        self.hat_button.clicked.connect(lambda: self.set_model_input("帽子"))
        model_buttons_layout.addWidget(self.hat_button)

        self.blanket_button = QPushButton("毯子", self)
        self.blanket_button.setFont(QFont("Arial", 12))
        self.blanket_button.clicked.connect(lambda: self.set_model_input("毯子"))
        model_buttons_layout.addWidget(self.blanket_button)

        left_layout.addLayout(model_buttons_layout)

        model_layout = QHBoxLayout()
        self.model_label = QLabel("型号:")
        self.model_label.setFont(QFont("Arial", 14, QFont.Bold))
        model_layout.addWidget(self.model_label)

        self.model_input = QLineEdit(self)
        self.model_input.setFont(QFont("Arial", 12))
        self.model_input.setText("未知")  # 设置型号的默认值为"未知"
        model_layout.addWidget(self.model_input)

        self.previous_button = QPushButton("上一个", self)
        self.previous_button.setFont(QFont("Arial", 12))
        self.previous_button.clicked.connect(self.load_last_model)
        model_layout.addWidget(self.previous_button)

        left_layout.addLayout(model_layout)

        number_layout = QHBoxLayout()
        self.number_label = QLabel("编号:")
        self.number_label.setFont(QFont("Arial", 14, QFont.Bold))
        number_layout.addWidget(self.number_label)

        self.number_input = QLineEdit(self)
        self.number_input.setFont(QFont("Arial", 12))
        number_layout.addWidget(self.number_input)
        left_layout.addLayout(number_layout)

        price_layout = QHBoxLayout()
        self.price_label = QLabel("原生价格:")
        self.price_label.setFont(QFont("Arial", 14, QFont.Bold))
        price_layout.addWidget(self.price_label)

        self.price_input = QLineEdit(self)
        self.price_input.setFont(QFont("Arial", 12))
        price_layout.addWidget(self.price_input)

        self.price_button = QPushButton("获取价格", self)
        self.price_button.setFont(QFont("Arial", 12))
        self.price_button.setStyleSheet("background-color: lightgreen;")
        self.price_button.clicked.connect(self.fetch_price_from_db)
        price_layout.addWidget(self.price_button)

        left_layout.addLayout(price_layout)

        self.generate_button = QPushButton("生成", self)
        self.generate_button.setFont(QFont("Arial", 12))
        self.generate_button.setStyleSheet("background-color: lightcoral;")
        self.generate_button.setFixedHeight(100)  # 增加按钮高度
        self.generate_button.clicked.connect(self.generate_output)
        self.generate_button.setShortcut(QKeySequence("F2"))

        self.convert_button = QPushButton("转换", self)
        self.convert_button.setFont(QFont("Arial", 12))
        self.convert_button.setStyleSheet("background-color: lightyellow;")
        self.convert_button.setFixedHeight(100)  # 增加按钮高度
        self.convert_button.clicked.connect(self.convert_folder_name)
        self.convert_button.setShortcut(QKeySequence("F3"))

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.convert_button)
        left_layout.addLayout(button_layout)

        output_layout = QHBoxLayout()
        self.output_label = QLabel("预览结果:")
        self.output_label.setFont(QFont("Arial", 14, QFont.Bold))
        output_layout.addWidget(self.output_label)

        self.output_edit = QTextEdit(self)
        self.output_edit.setFont(QFont("Arial", 12))
        self.output_edit.setFixedHeight(60)  # 调整高度为2-3行
        output_layout.addWidget(self.output_edit)
        left_layout.addLayout(output_layout)

        main_layout.addLayout(left_layout)

        # 增加日志显示区域
        log_layout = QVBoxLayout()
        self.log_label = QLabel("操作日志:")
        self.log_label.setFont(QFont("Arial", 14, QFont.Bold))
        log_layout.addWidget(self.log_label)

        self.log_display = QTextEdit(self)
        self.log_display.setFont(QFont("Arial", 12))
        self.log_display.setReadOnly(True)  # 设置为只读
        self.log_display.setMinimumWidth(500)
        self.log_display.cursorPositionChanged.connect(self.log_double_click)
        log_layout.addWidget(self.log_display)

        # 增加图片显示区域
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(500)  # 设置图片的高度最小值为500
        self.image_label.setMouseTracking(True)
        self.image_label.installEventFilter(self)
        log_layout.addWidget(self.image_label)

        self.change_image_button = QPushButton("切换图片", self)
        self.change_image_button.setFont(QFont("Arial", 12))
        self.change_image_button.clicked.connect(self.change_image)
        log_layout.addWidget(self.change_image_button)

        main_layout.addLayout(log_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('文件夹管理器')
        self.setGeometry(300, 800, 2000, 1600)
        self.center()

    def center(self):
        screen = QScreen.availableGeometry(QApplication.primaryScreen())
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", "G:/敦煌/眼镜/可乐/7月11日")
        if folder_path:
            self.path_output.setText(folder_path)
            self.clear_data()
            self.initialize_plugins(folder_path)
            self.display_random_image(folder_path)

    def clear_data(self):
        self.txt_display.clear()
        self.number_input.clear()
        self.price_input.clear()
        self.output_edit.clear()
        self.image_label.clear()

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
                        self.set_brand(txt_content)
                        self.set_model(txt_content)
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
        if not match:
            match = re.search(r'🅿️(\d+)', txt_content)
        if match:
            self.price_input.setText(match.group(1))
        else:
            self.log_display.append("<span style='color: red;'>未找到价格信息,开始查找数据</span>")
            brand = self.brand_combo.currentText()
            model = self.model_input.text()
            if brand and model:
                price = self.get_price_from_db(brand, model)
                self.log_display.append(f"<span style='color: green;'>数据库中查找到价格: {price}</span>")
                if price:
                    # 日志记录
                    self.log_operation("数据库中成功读取", brand, model, price)
                    self.price_input.setText(price)
                else:
                    self.log_display.append("<span style='color: red;'>数据库中未找到价格信息</span>")

    def set_brand(self, txt_content):
        for key, values in brand_dict.items():
            for value in values:
                if value.lower() in txt_content.lower():
                    self.brand_combo.setCurrentText(key)
                    return

    def set_model(self, txt_content):
        import re
        patterns = ['编号：', 'Model：', '型号：', 'MODEL：', '型号 ', 'Mod：', 'MODEL:', '型号', 'MODEL: ', 'MODEL:', 'Model: ',
                    'MOD:', 'MOD：', 'Model ：', 'MODEL: ', '型号：', '型号:', '型号 ', '型号:', '型号 ', '型号:', '型号 ', '型号：',
                    'MODEL: ', '型号：']
        patterns = list(set(patterns))  # 去除重复的模式
        match = None
        for pattern in patterns:
            match = re.search(fr'{pattern}(.+)', txt_content)
            if match:
                break
        if match:
            model = match.group(1)
            # 只取符号前面的部分(符号”-“除外)
            model = re.split(r'[^A-Za-z0-9-]', model)[0]
            self.model_input.setText(model)
        else:
            # 如果没有找到型号，则查找大于等于5个字符的字符串
            matches = re.findall(r'\b[A-Za-z0-9]{5,}\b', txt_content)
            if not matches:
                # 如果还是没有找到型号，则查找大于等于5个字符的字符串，并去除汉字部分
                matches = re.findall(r'[A-Za-z0-9]{5,}', re.sub(r'[\u4e00-\u9fa5]', '', txt_content))
            if matches:
                # 优先选择包含数字的字符串作为型号
                model = next((m for m in matches if any(char.isdigit() for char in m)), matches[0])
                self.model_input.setText(model)
            else:
                self.model_input.setText("未知")  # 如果没有找到型号，则设置为"未知"

    def set_model_input(self, value):
        self.model_input.setText(value)

    def generate_output(self):
        brand = self.brand_combo.currentText()
        model = self.model_input.text()
        number = self.number_input.text()
        price = self.price_input.text()
        result = f"{brand}-{model}-{number}-P{price}"
        if any(char in result for char in r'\/:*?"<>|'):
            QMessageBox.warning(self, "非法文件名", "文件夹名包含非法字符，请修改后重试。")
        else:
            self.output_edit.setText(result)
            self.save_brand(brand)
            self.log_operation("生成", brand, model, price)
            self.save_to_db(brand, model, price)
            self.save_last_model(model)

    def convert_folder_name(self):
        brand = self.brand_combo.currentText()
        model = self.model_input.text()
        price = self.price_input.text()
        if not brand or not model or not price:
            QMessageBox.warning(self, "警告", "品牌、型号或价格不能为空，请填写完整后重试。")
            return

        self.save_to_db(brand, model, price)

        current_path = self.path_output.text()
        new_name = self.output_edit.toPlainText()
        if current_path and new_name:
            new_path = os.path.join(os.path.dirname(current_path), new_name)
            os.rename(current_path, new_path)
            self.path_output.setText(new_path)
            self.rename_images(new_path, new_name)
            self.log_operation("转换", self.brand_combo.currentText(), self.model_input.text(), self.price_input.text())

    def rename_images(self, folder_path, new_name):
        brand, number = new_name.split('-')[:2]
        for idx, file_name in enumerate(os.listdir(folder_path)):
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.mp4')):
                new_file_name = f"{brand}-{number}-{idx + 1}{os.path.splitext(file_name)[1]}"
                os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, new_file_name))

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

    def log_operation(self, operation, brand, model, price):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - 操作: {operation}, 品牌: {brand}, 型号: {model}, 价格: {price}\n"
        if operation == "生成":
            self.log_display.append(f"<span style='color: blue;'>{log_entry}</span>")
        elif operation == "转换":
            self.log_display.append(f"<span style='color: orange;'>{log_entry}</span>")
        else:
            self.log_display.append(log_entry)
        with open("operation_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_entry)

    def log_double_click(self):
        cursor = self.log_display.textCursor()
        cursor.select(cursor.LineUnderCursor)
        selected_text = cursor.selectedText()
        if "型号:" in selected_text:
            model = selected_text.split("型号:")[1].split(",")[0].strip()
            self.model_input.setText(model)

    def init_db(self):
        self.conn = sqlite3.connect('products.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products
                               (date TEXT, brand TEXT, model TEXT, price TEXT)''')
        self.conn.commit()

    def save_to_db(self, brand, model, price):
        if not brand or not model or not price:
            self.log_display.append("<span style='color: red;'>品牌、型号或价格为空，不保存到数据库</span>")
            return
        if "围巾" in model or "未知" in model or "帽子" in model:
            self.log_display.append("<span style='color: red;'>型号包含'围巾'，'帽子’或'未知',不保存到数据库</span>")
            return
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("SELECT * FROM products WHERE brand=? AND model=? AND price=?", (brand, model, price))
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO products (date, brand, model, price) VALUES (?, ?, ?, ?)",
                                (date, brand, model, price))
            self.conn.commit()

    def get_price_from_db(self, brand, model):
        self.log_display.append(f"<span style='color: purple;'>查询数据库: 品牌={brand}, 型号={model}</span>")
        self.cursor.execute("SELECT price FROM products WHERE LOWER(brand)=LOWER(?) AND LOWER(model)=LOWER(?) ORDER BY date DESC", (brand, model))
        result = self.cursor.fetchone()
        if result:
            self.log_display.append(f"<span style='color: green;'>数据库查询结果: {result[0]}</span>")
            return result[0]
        self.log_display.append("<span style='color: red;'>数据库查询结果为空</span>")
        return None

    def fetch_price_from_db(self):
        brand = self.brand_combo.currentText()
        model = self.model_input.text()
        if brand and model:
            price = self.get_price_from_db(brand, model)
            if price:
                self.price_input.setText(price)
            else:
                self.log_display.append("<span style='color: red;'>数据库中未找到价格信息</span>")

    def save_last_model(self, model):
        with open("last_model.json", "w") as file:
            json.dump({"last_model": model}, file)

    def load_last_model(self):
        try:
            with open("last_model.json", "r") as file:
                data = json.load(file)
                self.model_input.setText(data.get("last_model", "未知"))
        except FileNotFoundError:
            self.model_input.setText("未知")

    def display_random_image(self, folder_path):
        image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        if image_files:
            random_image = random.choice(image_files)
            pixmap = QPixmap(os.path.join(folder_path, random_image))
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
            self.image_label.setToolTip(f"<img src='{os.path.join(folder_path, random_image)}'>")

    def change_image(self):
        folder_path = self.path_output.text()
        if folder_path:
            self.display_random_image(folder_path)

    def eventFilter(self, source, event):
        if event.type() == event.Enter and source is self.image_label:
            self.image_label.setPixmap(self.image_label.pixmap().scaledToHeight(self.image_label.pixmap().height()))
        elif event.type() == event.Leave and source is self.image_label:
            self.image_label.setPixmap(self.image_label.pixmap().scaled(self.image_label.size(), Qt.KeepAspectRatio))
        return super().eventFilter(source, event)

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
