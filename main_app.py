# main_app.py
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
import ctypes
import importlib
import os

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


def zh_font(size=14, weight="normal"):
    return ctk.CTkFont(family="Microsoft YaHei", size=size, weight=weight)


class AppMain:
    def __init__(self, root):
        self.root = root
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root.title("齿轮损伤识别与评估系统")
        self.root.geometry("1600x1050")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.load_tabs()

    def load_tabs(self):
        tab_dir = os.path.join(os.path.dirname(__file__), 'tabs')
        tab_order = [
            ("tab_file_manager", "FileManager"),
            ("tab_example", "Example"),
            ("tab_pms", "PhotometricStereoTab"),
        ]
        for module_name, class_name in tab_order:
            module = importlib.import_module(f"tabs.{module_name}") # import对应名字的python文件
            tab_class = getattr(module, class_name, None)  #从 module 模块中 获取名为 class_name 的类，如果找不到该类，则返回 None。
            tab_label = getattr(module, 'TAB_LABEL', class_name)  #从 module 模块中 获取名为 TAB_LABEL 的部分，如果找不到该名称，则返回 class_name,用class_name作为标签页的名称。
            if tab_class:
                self.tabview.add(tab_label)
                instance = tab_class(self.tabview)
                instance.frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = AppMain(root)
    root.mainloop()
