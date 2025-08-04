# tabs/tab_example.py
import customtkinter as ctk
from tkinter import filedialog

TAB_LABEL = "示例功能"

class Example:
    def __init__(self, tabview):
        self.frame = ctk.CTkFrame(tabview.tab(TAB_LABEL))
        ctk.CTkLabel(self.frame, text="欢迎使用示例模块", font=ctk.CTkFont(size=16)).pack(pady=20)

        self.button = ctk.CTkButton(self.frame, text="点击我", command=self.say_hello)
        self.button.pack(pady=10)

        self.save_button = ctk.CTkButton(self.frame, text="保存内容到文件", command=self.save_text_to_file)
        self.save_button.pack(pady=5)

        self.textbox = ctk.CTkTextbox(self.frame, height=150)
        self.textbox.pack(fill="both", expand=True, padx=20, pady=10)

    def say_hello(self):
        self.textbox.insert("end", "👋 你好，欢迎使用示例功能！\n")
        self.textbox.see("end")

    def save_text_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.textbox.get("1.0", "end-1c"))
            except Exception as e:
                print(f"保存失败: {e}")