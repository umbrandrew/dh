import sys
import os
import json
import requests
import random
import time
from threading import Event, Thread
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from typing import Callable

pause_event: Event = Event()  # 用于暂停和继续处理的事件


def custom_sleep():
    intervals = [(0, 1), (1, 2), (2, 3)]
    weights = [0.5, 0.35, 0.15]
    chosen_interval = random.choices(intervals, weights)[0]
    sleep_time = random.uniform(*chosen_interval)
    time.sleep(sleep_time)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        try:
            self.title("文件处理程序")  # 设置窗口标题
            self.geometry("800x600")  # 设置窗口大小和位置

            main_frame = ttk.Frame(self)  # 创建主窗口部件
            main_frame.pack(fill=tk.BOTH, expand=True)  # 设置主窗口部件

            layout = ttk.Frame(main_frame)  # 创建垂直布局
            layout.pack(fill=tk.BOTH, expand=True)

            self.path_input = ttk.Entry(layout)  # 创建输入框
            self.path_input.insert(0, "输入文件夹路径")  # 设置输入框的占位符文本
            self.path_input.pack(fill=tk.X, padx=5, pady=5)  # 将输入框添加到布局中

            self.log_display = ScrolledText(layout, state='disabled')  # 创建文本显示框
            self.log_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # 将文本显示框添加到布局中

            self.start_button = ttk.Button(layout, text="开始", command=self.start_processing)  # 创建开始按钮
            self.start_button.pack(side=tk.LEFT, padx=5, pady=5)  # 将开始按钮添加到布局中

            self.pause_button = ttk.Button(layout, text="暂停", command=self.pause_processing)  # 创建暂停按钮
            self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)  # 将暂停按钮添加到布局中

            self.resume_button = ttk.Button(layout, text="继续", command=self.resume_processing)  # 创建继续按钮
            self.resume_button.pack(side=tk.LEFT, padx=5, pady=5)  # 将继续按钮添加到布局中
        except Exception as e:
            print(f"Error initializing MainWindow: {e}")

    def log(self, message: str) -> None:
        try:
            self.log_display.config(state='normal')
            self.log_display.insert(tk.END, message + '\n')  # 在日志显示框中追加消息
            self.log_display.config(state='disabled')
            self.log_display.yview(tk.END)
        except Exception as e:
            print(f"Error logging message: {e}")

    def start_processing(self) -> None:
        try:
            folder_path: str = self.path_input.get()  # 获取输入的文件夹路径
            if not folder_path:
                self.log("请输入文件夹路径")  # 如果未输入路径，提示用户
                return

            self.log("开始处理...")  # 记录开始处理的日志
            pause_event.set()  # 设置继续事件，确保处理立即开始
            self.processing_thread: Thread = Thread(target=process_json_files, args=(folder_path, self.log))  # 创建处理线程
            self.processing_thread.start()  # 启动处理线程
        except Exception as e:
            self.log(f"Error starting processing: {e}")

    def pause_processing(self) -> None:
        try:
            pause_event.clear()  # 清除暂停事件
            self.log("已暂停")  # 记录暂停的日志
        except Exception as e:
            self.log(f"Error pausing processing: {e}")

    def resume_processing(self) -> None:
        try:
            pause_event.set()  # 设置继续事件
            self.log("继续处理")  # 记录继续处理的日志
        except Exception as e:
            self.log(f"Error resuming processing: {e}")


def sanitize_filename(filename: str) -> str:
    try:
        # 清理文件名，移除不合法字符
        sanitized = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()
        # 确保文件名长度不超过255个字符
        return sanitized[:255]
    except Exception as e:
        print(f"Error sanitizing filename: {e}")
        return filename


def download_image(url: str, folder_path: str, image_name: str, retries: int = 3) -> None:
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)  # 设置超时时间为10秒
            if response.status_code == 200:
                with open(os.path.join(folder_path, image_name), 'wb') as file:  # 将图片保存到指定路径
                    file.write(response.content)
                return  # 下载成功，退出函数
            else:
                raise Exception(f"Failed to download image: {url}, status code: {response.status_code}")
        except (requests.ConnectionError, requests.Timeout) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                custom_sleep()  # 等待一段时间后重试
            else:
                print(f"Error downloading image {url}: {e}")
                save_failed_image_info(url, folder_path, image_name)
        except Exception as e:
            print(f"Error downloading image {url}: {e}")
            save_failed_image_info(url, folder_path, image_name)
            break  # 对于其他异常，不进行重试
    custom_sleep()  # 使用自定义的暂停函数


def save_failed_image_info(url: str, folder_path: str, image_name: str) -> None:
    failed_folder = os.path.join(folder_path, "failed_downloads")
    os.makedirs(failed_folder, exist_ok=True)
    failed_image_path = os.path.join(failed_folder, f"failed_{image_name}.txt")
    with open(failed_image_path, 'w') as file:
        file.write(f"Failed to download image from: {url}\n")
        file.write(f"Original folder: {folder_path}\n")


def download_video(url: str, folder_path: str, video_name: str, retries: int = 3) -> None:
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)  # 设置超时时间为10秒
            if response.status_code == 200:
                with open(os.path.join(folder_path, video_name), 'wb') as file:  # 将视频保存到指定路径
                    file.write(response.content)
                return  # 下载成功，退出函数
            else:
                raise Exception(f"Failed to download video: {url}, status code: {response.status_code}")
        except (requests.ConnectionError, requests.Timeout) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                custom_sleep()  # 等待一段时间后重试
            else:
                print(f"Error downloading video {url}: {e}")
                save_failed_video_info(url, folder_path, video_name)
        except Exception as e:
            print(f"Error downloading video {url}: {e}")
            save_failed_video_info(url, folder_path, video_name)
            break  # 对于其他异常，不进行重试
    custom_sleep()  # 使用自定义的暂停函数


def save_failed_video_info(url: str, folder_path: str, video_name: str) -> None:
    failed_folder = os.path.join(folder_path, "failed_downloads")
    os.makedirs(failed_folder, exist_ok=True)
    failed_video_path = os.path.join(failed_folder, f"failed_{video_name}.txt")
    with open(failed_video_path, 'w') as file:
        file.write(f"Failed to download video from: {url}\n")
        file.write(f"Original folder: {folder_path}\n")


def process_product(product: dict, folder_path: str, log: Callable[[str], None], file_idx: int, total_files: int,
                    product_idx: int, total_products: int) -> None:
    try:
        title: str = product.get("title", "")  # 获取产品标题
        mark_code: str = product.get("mark_code", "").strip('"')  # 获取产品标记码
        update_time: str = str(product.get("update_time", ""))  # 获取更新时间
        folder_name: str = f"{update_time}-{mark_code}"  # 根据更新时间和标记码生成文件夹名

        product_folder_path: str = os.path.join(folder_path, folder_name)  # 生成产品文件夹路径

        # 检查当前文件夹中的文件名是否包含当前产品的mark_code
        if any(mark_code in file_name for file_name in os.listdir(folder_path)):
            log(f"Product with mark_code {mark_code} already exists in folder, skipping...")  # 如果文件名包含mark_code，跳过处理
            return

        if os.path.exists(product_folder_path):
            log(f"Folder {product_folder_path} already exists, skipping...")  # 如果文件夹已存在，跳过处理
            return

        os.makedirs(product_folder_path, exist_ok=True)  # 创建产品文件夹

        # 创建txt文件保存title内容
        with open(os.path.join(product_folder_path, f"{folder_name}.txt"), 'w', encoding='utf-8') as file:
            file.write(title)

        for idx, img_url in enumerate(product.get("imgsSrc", [])):
            image_name: str = f"image_{idx + 1}.jpg"  # 生成图片文件名
            download_image(img_url, product_folder_path, image_name)  # 下载图片
            log(f"正在处理第{file_idx + 1}/{total_files}个JSON文件的第{product_idx + 1}/{total_products}个产品的第{idx + 1}/{len(product.get('imgsSrc', []))}张图片")  # 记录处理进度

        video_url: str = product.get("videoURL", "")
        if video_url:
            video_name: str = "video.mp4"  # 生成视频文件名
            download_video(video_url, product_folder_path, video_name)  # 下载视频
            log(f"正在处理第{file_idx + 1}/{total_files}个JSON文件的第{product_idx + 1}/{total_products}个产品的视频")  # 记录处理进度

        log(f"Product {title} processed successfully!\n")  # 记录产品处理成功的日志
    except Exception as e:
        log(f"Error processing product: {e}")


def process_json_file(file_path: str, log: Callable[[str], None], file_idx: int, total_files: int) -> None:
    try:
        if "已完成" in file_path:
            log(f"Skipping already completed file: {file_path}")  # 跳过已完成的文件
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            data: list = json.load(file)  # 读取JSON文件
            total_products: int = len(data)  # 获取产品总数
            for idx, product in enumerate(data):
                pause_event.wait()  # 等待继续事件
                process_product(product, os.path.dirname(file_path), log, file_idx, total_files, idx,
                                total_products)  # 处理产品
                log(f"Processed {idx + 1}/{total_products} products in {file_path}")  # 记录处理进度
                if (idx + 1) % 20 == 0:
                    sleep_time: int = random.randint(2, 5)  # 随机生成暂停时间
                    log(f"Pausing for {sleep_time} seconds...")  # 记录暂停日志
                    time.sleep(sleep_time)  # 暂停处理

        # 修改JSON文件名，增加"已完成"
        new_file_path = file_path.replace(".json", "已完成.json")
        os.rename(file_path, new_file_path)
        log(f"JSON文件 {file_path} 已处理完毕，重命名为 {new_file_path}")
    except Exception as e:
        log(f"Error processing JSON file {file_path}: {e}")


def process_json_files(folder_path: str, log: Callable[[str], None]) -> None:
    try:
        json_files: list = [file_name for file_name in os.listdir(folder_path) if
                            file_name.endswith(".json")]  # 获取所有JSON文件
        total_files: int = len(json_files)  # 获取JSON文件总数
        for idx, file_name in enumerate(json_files):
            pause_event.wait()  # 等待继续事件
            process_json_file(os.path.join(folder_path, file_name), log, idx, total_files)  # 处理JSON文件
            log(f"Processed {idx + 1}/{total_files} JSON files")  # 记录处理进度
    except Exception as e:
        log(f"Error processing JSON files in folder {folder_path}: {e}")


if __name__ == "__main__":
    try:
        app = MainWindow()  # 创建应用程序
        app.mainloop()  # 运行应用程序
    except Exception as e:
        print(f"Error running application: {e}")