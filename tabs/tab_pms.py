#副界面3，包含了光度立体法的部分
# tabs/tab_pms.py
import customtkinter as ctk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES
import os
from PIL import Image

TAB_LABEL = "光度立体法"

class PhotometricStereoTab:
    def __init__(self, tabview):
        self.frame = ctk.CTkFrame(tabview.tab(TAB_LABEL))

        self.image_paths = [None] * 4
        self.target_image_paths = [None] * 4
        self.image_labels = []
        self.target_labels = []
        self.manual_inputs = []

        self.main_container = ctk.CTkFrame(self.frame)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        self.main_container.grid_columnconfigure((0, 1, 2), weight=1)

        self.left_frame = ctk.CTkFrame(self.main_container)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10)

        self.middle_frame = ctk.CTkFrame(self.main_container)
        self.middle_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        self.right_frame = ctk.CTkFrame(self.main_container)
        self.right_frame.grid(row=0, column=2, sticky="nsew", padx=10)

        self.init_calibration_ui()
        self.init_target_ui()
        self.init_manual_ui()
        self.init_result_ui()

    def init_calibration_ui(self):
        ctk.CTkLabel(self.left_frame, text="小球光源标定", font=ctk.CTkFont(size=16)).pack(pady=10)

        grid = ctk.CTkFrame(self.left_frame)
        grid.pack()

        for i in range(4):
            frame = ctk.CTkFrame(grid, width=140, height=140, border_width=1, border_color="gray")
            frame.grid(row=i//2, column=i%2, padx=5, pady=5)
            frame.pack_propagate(False)

            label = ctk.CTkLabel(frame, text=f"图像{i+1}")
            label.pack(expand=True)
            label.drop_target_register(DND_FILES)
            label.dnd_bind("<<Drop>>", lambda e, idx=i: self.on_drop(e, idx, mode='calib'))
            self.image_labels.append(label)

        ctk.CTkButton(self.left_frame, text="选择图像", command=self.select_images).pack(pady=10)

    def init_target_ui(self):
        ctk.CTkLabel(self.middle_frame, text="目标物体图像", font=ctk.CTkFont(size=16)).pack(pady=10)

        grid = ctk.CTkFrame(self.middle_frame)
        grid.pack()

        for i in range(4):
            frame = ctk.CTkFrame(grid, width=140, height=140, border_width=1, border_color="gray")
            frame.grid(row=i//2, column=i%2, padx=5, pady=5)
            frame.pack_propagate(False)

            label = ctk.CTkLabel(frame, text=f"目标图{i+1}")
            label.pack(expand=True)
            label.drop_target_register(DND_FILES)
            label.dnd_bind("<<Drop>>", lambda e, idx=i: self.on_drop(e, idx, mode='target'))
            self.target_labels.append(label)

        ctk.CTkButton(self.middle_frame, text="选择目标图像", command=self.select_target_images).pack(pady=10)
        ctk.CTkButton(self.middle_frame, text="执行标定", command=self.calculate_light_direction).pack(pady=10)

    def init_manual_ui(self):
        ctk.CTkLabel(self.right_frame, text="手动输入光源方向", font=ctk.CTkFont(size=16)).pack(pady=10)

        for i in range(4):
            row = ctk.CTkFrame(self.right_frame)
            row.pack(pady=5, fill="x")
            ctk.CTkLabel(row, text=f"光源{i+1}:").pack(side="left", padx=5)
            entry = ctk.CTkEntry(row, placeholder_text="x y z")
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.manual_inputs.append(entry)

    def init_result_ui(self):
        ctk.CTkLabel(self.right_frame, text="计算结果展示区域", font=ctk.CTkFont(size=16)).pack(pady=(30, 5))
        ctk.CTkLabel(self.right_frame, text="（法线图/深度图 可在此处展示）", font=ctk.CTkFont(size=12)).pack(pady=5)

    def select_images(self):
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        for i, path in enumerate(paths[:4]):
            self.load_image(i, path, mode='calib')

    def select_target_images(self):
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        for i, path in enumerate(paths[:4]):
            self.load_image(i, path, mode='target')

    def on_drop(self, event, idx, mode):
        path = self.frame.winfo_toplevel().tk.splitlist(event.data)[0]
        self.load_image(idx, path, mode)

    def load_image(self, idx, path, mode):
        if not os.path.isfile(path):
            return
        try:
            img = Image.open(path).convert("RGB")
            img.thumbnail((140, 140))
            tk_img = ctk.CTkImage(light_image=img.copy(), dark_image=img.copy(), size=img.size)

            save_dir = os.path.join(os.path.dirname(__file__), "..", "save", "pms")
            os.makedirs(save_dir, exist_ok=True)
            ext = os.path.splitext(path)[-1].lower()

            if mode == 'calib':
                self.image_labels[idx].configure(image=tk_img, text="")
                self.image_labels[idx].image = tk_img
                save_name = f"image_{idx+1}{ext}"
                self.image_paths[idx] = os.path.join(save_dir, save_name)
                img.save(self.image_paths[idx])

            elif mode == 'target':
                self.target_labels[idx].configure(image=tk_img, text="")
                self.target_labels[idx].image = tk_img
                save_name = f"target_{idx+1}{ext}"
                self.target_image_paths[idx] = os.path.join(save_dir, save_name)
                img.save(self.target_image_paths[idx])

        except Exception as e:
            print(f"加载图像失败: {e}")

    def calculate_light_direction(self):
        print("[DEBUG] 执行标定")
        print("小球图像路径:")
        for i, p in enumerate(self.image_paths):
            print(f"球{i+1}: {p}")
        print("目标图像路径:")
        for i, p in enumerate(self.target_image_paths):
            print(f"目标{i+1}: {p}")
        print("手动输入向量:")
        for i, e in enumerate(self.manual_inputs):
            print(f"光源{i+1}: {e.get()}")
