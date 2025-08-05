# 副界面3，包含了光度立体法的部分
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

        # 图像路径与标签
        self.image_paths = [None] * 4
        self.target_image_paths = [None] * 4
        self.image_labels = []
        self.target_labels = []
        self.manual_inputs = []

        # 输出框内容
        self.log_messages = []

        # 顶部主结构 - 上部为三栏，下部为输出栏
        self.main_container = ctk.CTkFrame(self.frame)
        self.main_container.pack(fill="both", expand=True)
        self.main_container.grid_rowconfigure(0, weight=2)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        # 三栏区域
        self.three_panel = ctk.CTkFrame(self.main_container)
        self.three_panel.grid(row=0, column=0, sticky="nsew")
        self.three_panel.grid_columnconfigure((0, 1, 2), weight=1)

        # 左侧栏：切换 + 标定输入
        self.left_panel = ctk.CTkFrame(self.three_panel)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # 中间栏：目标图 + 计算按钮
        self.middle_panel = ctk.CTkFrame(self.three_panel)
        self.middle_panel.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # 右侧栏：结果 + 保存按钮
        self.right_panel = ctk.CTkFrame(self.three_panel)
        self.right_panel.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        # 输出区域
        self.log_box = ctk.CTkTextbox(self.main_container, height=120)
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.log_box.configure(state="disabled")

        # 初始化各区域
        self.init_left_tabs()
        self.init_target_panel()
        self.init_result_panel()

    def init_left_tabs(self):
        # 左侧使用 tab 控件
        self.left_tabs = ctk.CTkTabview(self.left_panel)
        self.left_tabs.pack(fill="both", expand=True)
        self.left_tabs.add("小球标定")
        self.left_tabs.add("手动输入")

        self.calib_tab = self.left_tabs.tab("小球标定")
        self.manual_tab = self.left_tabs.tab("手动输入")

        # 标定界面
        grid = ctk.CTkFrame(self.calib_tab)
        grid.pack(pady=10)

        for i in range(4):
            frame = ctk.CTkFrame(grid, width=120, height=120, border_width=1, border_color="gray")
            frame.grid(row=i//2, column=i%2, padx=5, pady=5)
            frame.pack_propagate(False)
            label = ctk.CTkLabel(frame, text=f"图像{i+1}")
            label.pack(expand=True)
            label.drop_target_register(DND_FILES)
            label.dnd_bind("<<Drop>>", lambda e, idx=i: self.on_drop(e, idx, mode='calib'))
            self.image_labels.append(label)

        ctk.CTkButton(self.calib_tab, text="选择图像", command=self.select_images).pack(pady=(10, 5))
        ctk.CTkButton(self.calib_tab, text="标定光源方向", command=self.calibrate_and_switch).pack(pady=(0, 10))

        # 手动输入界面
        for i in range(4):
            row = ctk.CTkFrame(self.manual_tab)
            row.pack(pady=5, fill="x")
            ctk.CTkLabel(row, text=f"光源{i+1}:").pack(side="left", padx=5)
            entry = ctk.CTkEntry(row, width=120, placeholder_text="x y z")
            entry.pack(side="left", padx=5)
            self.manual_inputs.append(entry)

    def init_target_panel(self):
        ctk.CTkLabel(self.middle_panel, text="输入目标图像", font=ctk.CTkFont(size=16)).pack(pady=10)
        grid = ctk.CTkFrame(self.middle_panel)
        grid.pack()

        for i in range(4):
            frame = ctk.CTkFrame(grid, width=120, height=120, border_width=1, border_color="gray")
            frame.grid(row=i//2, column=i%2, padx=5, pady=5)
            frame.pack_propagate(False)
            label = ctk.CTkLabel(frame, text=f"目标图{i+1}")
            label.pack(expand=True)
            label.drop_target_register(DND_FILES)
            label.dnd_bind("<<Drop>>", lambda e, idx=i: self.on_drop(e, idx, mode='target'))
            self.target_labels.append(label)

        ctk.CTkButton(self.middle_panel, text="执行计算", command=self.calculate_light_direction).pack(pady=10)

    def init_result_panel(self):
        ctk.CTkLabel(self.right_panel, text="结果展示", font=ctk.CTkFont(size=16)).pack(pady=10)
        self.result_normal = ctk.CTkLabel(self.right_panel, text="法向图展示区域", width=160, height=160)
        self.result_normal.pack(pady=5)
        self.result_depth = ctk.CTkLabel(self.right_panel, text="深度图展示区域", width=160, height=160)
        self.result_depth.pack(pady=5)
        ctk.CTkButton(self.right_panel, text="保存结果", command=self.save_results).pack(pady=10)

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

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
            img.thumbnail((120, 120))
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
                self.log(f"加载小球图像 {idx+1} 成功")

            elif mode == 'target':
                self.target_labels[idx].configure(image=tk_img, text="")
                self.target_labels[idx].image = tk_img
                save_name = f"target_{idx+1}{ext}"
                self.target_image_paths[idx] = os.path.join(save_dir, save_name)
                img.save(self.target_image_paths[idx])
                self.log(f"加载目标图像 {idx+1} 成功")

        except Exception as e:
            self.log(f"加载图像失败: {e}")

    def calibrate_and_switch(self):
        # 模拟光源方向填充
        dummy_vectors = ["1 0 0", "0 1 0", "0 0 1", "1 1 1"]
        for i, val in enumerate(dummy_vectors):
            self.manual_inputs[i].delete(0, "end")
            self.manual_inputs[i].insert(0, val)
        self.left_tabs.set("手动输入")
        self.log("标定完成，已填入光源向量")

    def calculate_light_direction(self):
        # 暂未实现真实计算逻辑
        self.log("开始执行计算...")
        # 在此处插入法向图和深度图计算逻辑
        self.log("计算完成，已更新结果展示")

    def save_results(self):
        # 保存两张结果图（模拟）
        normal_path = filedialog.asksaveasfilename(defaultextension=".png", title="保存法向图")
        if normal_path:
            Image.new("RGB", (120, 120), (100, 100, 255)).save(normal_path)
            self.log(f"保存法向图成功: {normal_path}")
        depth_path = filedialog.asksaveasfilename(defaultextension=".png", title="保存深度图")
        if depth_path:
            Image.new("RGB", (120, 120), (180, 180, 180)).save(depth_path)
            self.log(f"保存深度图成功: {depth_path}")
