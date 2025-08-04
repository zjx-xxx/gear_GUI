# tabs/tab_file_manager.py
import customtkinter as ctk
import os
from tkinter import filedialog
from tkinterdnd2 import DND_FILES
from PIL import Image
import shutil
import datetime

TAB_LABEL = "文件管理"

class FileManager:
    def __init__(self, tabview):
        self.frame = ctk.CTkFrame(tabview.tab(TAB_LABEL))

        ctk.CTkLabel(self.frame, text="图片上传器", font=ctk.CTkFont(size=16)).pack(pady=10)

        # 按钮行容器
        button_row = ctk.CTkFrame(self.frame)
        button_row.pack(pady=5)

        self.upload_button = ctk.CTkButton(button_row, text="选择图片文件", command=self.select_and_upload_file)
        self.upload_button.pack(side="left", padx=(0, 10))

        self.delete_button = ctk.CTkButton(button_row, text="删除已上传图片", command=self.delete_uploaded_image)
        self.delete_button.pack(side="left")

        self.label = ctk.CTkLabel(self.frame, text="未上传任何图片")
        self.label.pack(pady=5)

        ctk.CTkLabel(self.frame, text="拖动图片区域", font=ctk.CTkFont(size=16)).pack(pady=(20, 5))
        self.drop_frame = ctk.CTkFrame(self.frame, width=500, height=300, corner_radius=8, border_width=2, border_color="gray")
        self.drop_frame.pack(pady=10)
        self.drop_frame.pack_propagate(False)

        self.drop_label = ctk.CTkLabel(self.drop_frame, text="请将图片拖放到此区域", font=ctk.CTkFont(size=14))
        self.drop_label.pack(expand=True)
        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind("<<Drop>>", self.on_image_drop)

        self.save_dir = os.path.join(os.path.dirname(__file__), "..", "save", "file_manager")
        os.makedirs(self.save_dir, exist_ok=True)

        self.last_uploaded_path = None

    def select_and_upload_file(self):
        file = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file:
            self.handle_image_input(file)

    def on_image_drop(self, event):
        paths = self.frame.winfo_toplevel().tk.splitlist(event.data)
        for path in paths:
            if os.path.isfile(path) and self.is_image_file(path):
                self.handle_image_input(path)

    def handle_image_input(self, path):
        ext = os.path.splitext(path)[-1].lower()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{timestamp}{ext}"
        save_path = os.path.join(self.save_dir, filename)
        shutil.copy(path, save_path)
        self.label.configure(text=f"已上传图片：{filename}")
        self.last_uploaded_path = save_path
        self.show_image_in_drop_area(save_path)

    def is_image_file(self, filepath):
        ext = os.path.splitext(filepath)[-1].lower()
        return ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp"]

    def show_image_in_drop_area(self, img_path):
        try:
            pil_img = Image.open(img_path).convert("RGB")
            pil_img.thumbnail((400, 250), Image.Resampling.LANCZOS)
            width, height = pil_img.size

            tk_img = ctk.CTkImage(
                light_image=pil_img.copy(),
                dark_image=pil_img.copy(),
                size=(width, height)
            )

            for widget in self.drop_frame.winfo_children():
                widget.destroy()

            img_label = ctk.CTkLabel(self.drop_frame, image=tk_img, text="")
            img_label.image = tk_img
            img_label.pack(expand=True)

        except Exception as e:
            print(f"显示图片失败: {e}")

    def delete_uploaded_image(self):
        if self.last_uploaded_path and os.path.exists(self.last_uploaded_path):
            try:
                os.remove(self.last_uploaded_path)
                self.label.configure(text="已删除上传图片")
                self.last_uploaded_path = None

                for widget in self.drop_frame.winfo_children():
                    widget.destroy()
                self.drop_label = ctk.CTkLabel(self.drop_frame, text="请将图片拖放到此区域", font=ctk.CTkFont(size=14))
                self.drop_label.pack(expand=True)
                self.drop_label.drop_target_register(DND_FILES)
                self.drop_label.dnd_bind("<<Drop>>", self.on_image_drop)

            except Exception as e:
                print(f"删除失败: {e}")
        else:
            self.label.configure(text="无图片可删除")