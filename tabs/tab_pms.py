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
        self.image_labels = []
        self.manual_inputs = []

        self.mode_switch = ctk.CTkSegmentedButton(self.frame, values=["小球标定", "手动输入"], command=self.switch_mode)
        self.mode_switch.pack(pady=10)

        self.container = ctk.CTkFrame(self.frame)
        self.container.pack(fill="both", expand=True)

        self.calib_frame = ctk.CTkFrame(self.container)
        self.manual_frame = ctk.CTkFrame(self.container)

        self.init_calibration_ui()
        self.init_manual_ui()

        self.calib_frame.pack(fill="both", expand=True)

    def switch_mode(self, mode):
        for widget in self.container.winfo_children():
            widget.pack_forget()
        if mode == "小球标定":
            self.calib_frame.pack(fill="both", expand=True)
        else:
            self.manual_frame.pack(fill="both", expand=True)

    def init_calibration_ui(self):
        ctk.CTkLabel(self.calib_frame, text="拖入或选择4张小球图像", font=ctk.CTkFont(size=16)).pack(pady=10)

        self.image_grid = ctk.CTkFrame(self.calib_frame)
        self.image_grid.pack()

        for i in range(4):
            frame = ctk.CTkFrame(self.image_grid, width=150, height=150, border_width=1, border_color="gray")
            frame.grid(row=i//2, column=i%2, padx=10, pady=10)
            frame.pack_propagate(False)

            label = ctk.CTkLabel(frame, text=f"图像{i+1}", font=ctk.CTkFont(size=14))
            label.pack(expand=True)
            label.drop_target_register(DND_FILES)
            label.dnd_bind("<<Drop>>", lambda e, idx=i: self.on_drop(e, idx))
            self.image_labels.append(label)

        select_btn = ctk.CTkButton(self.calib_frame, text="选择图片", command=self.select_images)
        select_btn.pack(pady=10)

        calc_btn = ctk.CTkButton(self.calib_frame, text="执行标定", command=self.calculate_light_direction)
        calc_btn.pack(pady=10)

    def init_manual_ui(self):
        ctk.CTkLabel(self.manual_frame, text="手动输入4个光源方向", font=ctk.CTkFont(size=16)).pack(pady=10)

        input_grid = ctk.CTkFrame(self.manual_frame)
        input_grid.pack(pady=10)

        for i in range(4):
            row = ctk.CTkFrame(input_grid)
            row.pack(pady=5)
            label = ctk.CTkLabel(row, text=f"光源 {i+1}: ")
            label.pack(side="left", padx=(0, 5))
            entry = ctk.CTkEntry(row, placeholder_text="x y z")
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.manual_inputs.append(entry)

    def select_images(self):
        paths = filedialog.askopenfilenames(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        for i, path in enumerate(paths[:4]):
            self.load_image(i, path)

    def on_drop(self, event, idx):
        path = self.frame.winfo_toplevel().tk.splitlist(event.data)[0]
        self.load_image(idx, path)

    def load_image(self, idx, path):
        if not os.path.isfile(path):
            return
        try:
            img = Image.open(path).convert("RGB")
            img.thumbnail((140, 140))
            tk_img = ctk.CTkImage(light_image=img.copy(), dark_image=img.copy(), size=img.size)

            self.image_labels[idx].configure(image=tk_img, text="")
            self.image_labels[idx].image = tk_img

            save_dir = os.path.join(os.path.dirname(__file__), "..", "save", "pms")
            os.makedirs(save_dir, exist_ok=True)
            ext = os.path.splitext(path)[-1].lower()
            save_name = f"image_{idx+1}{ext}"
            save_path = os.path.join(save_dir, save_name)
            img.save(save_path)

            self.image_paths[idx] = save_path

        except Exception as e:
            print(f"加载图像失败: {e}")

    def calculate_light_direction(self):
        print("[DEBUG] 调用光照方向计算函数")
        print("已保存图像路径:")
        for i, p in enumerate(self.image_paths):
            print(f"图像{i+1}: {p}")
        print("手动输入光源向量:")
        for i, entry in enumerate(self.manual_inputs):
            print(f"光源{i+1}: {entry.get()}")
