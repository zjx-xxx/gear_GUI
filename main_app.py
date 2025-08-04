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

        self.root.title("多标签项目管理器")
        self.root.geometry("1200x850")

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
            ("tab_settings", "Settings"),
        ]
        for module_name, class_name in tab_order:
            module = importlib.import_module(f"tabs.{module_name}")
            tab_class = getattr(module, class_name, None)
            tab_label = getattr(module, 'TAB_LABEL', class_name)
            if tab_class:
                self.tabview.add(tab_label)
                instance = tab_class(self.tabview)
                instance.frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = AppMain(root)
    root.mainloop()
