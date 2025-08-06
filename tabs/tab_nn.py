# 副界面1，包含了图像识别部分

# tabs/tab_nn.py
import customtkinter as ctk
from tkinter import filedialog
import os
from PIL import Image
import subprocess

TAB_LABEL = "损伤预测"

def zh_font(size=14, weight="normal"):
    return ctk.CTkFont(family="Microsoft YaHei", size=size, weight=weight)


class NNPrediction:
    def __init__(self, tabview):
        # --- 这里是关键修改 ---
        # 像 FileManager 一样，自己创建 frame 并指定正确的父组件
        self.frame = ctk.CTkFrame(tabview.tab(TAB_LABEL))
        self.frame.pack(fill="both", expand=True) # 自己管理自己的布局

        self.input_image_path = None
        
        # --- 创建主容器和布局 ---
        # 使用 grid 布局，分为左右两大块和底部日志区
        self.frame.grid_columnconfigure((0, 1), weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=0) 

        # --- 初始化界面模块 ---
        self.init_input_ui()
        self.init_output_ui()
        self.init_bottom_ui()


    def init_input_ui(self):
        """初始化左侧的输入图像区域"""
        container = ctk.CTkFrame(self.frame)
        container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(container, text="输入图像", font=zh_font(16, "bold")).pack(pady=10)

        # 这个框架依然是可伸缩的，占据主要空间
        image_container = ctk.CTkFrame(container, fg_color="transparent")
        image_container.pack(fill="both", expand=True, padx=20, pady=10)

        # --- 这里是关键修改 ---

        # 1. 图片标签依然在 image_container 中，但要让它填充并扩展，为下方的按钮留出空间
        self.input_image_label = ctk.CTkLabel(image_container, text="请选择一张图片", font=zh_font(14))
        self.input_image_label.pack(fill="both", expand=True, pady=(0, 10)) # 增加了 pady 让按钮和图片有间距

        # 2. 将 button_frame 的父组件从 container 改为 image_container
        #    并将其 pack 到 image_container 的底部
        button_frame = ctk.CTkFrame(image_container, fg_color="transparent") # 背景设为透明以融入
        button_frame.pack(side="bottom", fill="x")

        # 3. 按钮的 grid 布局保持不变，它现在会在 button_frame 内平分宽度
        button_frame.grid_columnconfigure((0, 1), weight=1)

        select_button = ctk.CTkButton(button_frame, text="选择图像", font=zh_font(14), command=self.select_input_image)
        select_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")

        predict_button = ctk.CTkButton(button_frame, text="执行预测", font=zh_font(14), command=self.run_prediction)
        predict_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")


    def init_output_ui(self):
        """初始化右侧的输出结果区域"""
        container = ctk.CTkFrame(self.frame)
        container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(container, text="预测结果图像", font=zh_font(16, "bold")).pack(pady=10)

        self.output_image_label = ctk.CTkLabel(container, text="等待预测结果", font=zh_font(14))
        self.output_image_label.pack(fill="both", expand=True, padx=20, pady=20)

    def init_bottom_ui(self):
        """初始化底部的“Annotation”和“日志”区域"""
        # 1. 创建一个容纳底部所有内容的父容器，它依然横跨整个界面
        bottom_container = ctk.CTkFrame(self.frame)
        bottom_container.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # 2. 在父容器内创建两列网格，并按 1:2 的权重分配宽度
        bottom_container.grid_columnconfigure(0, weight=2)  # 左侧日志区占2/3
        bottom_container.grid_columnconfigure(1, weight=1)  # 右侧标注区占1/3

        # --- 左侧：输出日志区域 ---
        log_frame = ctk.CTkFrame(bottom_container)
        log_frame.grid(row=0, column=0, padx=(0, 5), pady=0, sticky="nsew")
        
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)

        # --- 这里是关键修改 ---
        # 1. 创建一个新的框架来容纳标题和Clear按钮，以便将它们放在同一行
        title_frame = ctk.CTkFrame(log_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=10, pady=(5, 5), sticky="ew")

        # 2. 将“输出日志”标题放入这个新框架
        ctk.CTkLabel(title_frame, text="输出日志", font=zh_font(16, "bold")).pack(side="left")

        # 3. 在标题旁边添加Clear按钮
        clear_button = ctk.CTkButton(
            title_frame, 
            text="Clear", 
            font=zh_font(12), 
            width=60,  # 给一个较小的固定宽度
            command=self.clear_log_textbox # 绑定我们新创建的方法
        )
        clear_button.pack(side="right", padx=10)

        # 日志文本框的位置保持不变
        self.log_textbox = ctk.CTkTextbox(log_frame, font=zh_font(12), state="disabled")
        self.log_textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # --- 右侧：Annotation 区域 ---
        annotation_frame = ctk.CTkFrame(bottom_container)
        annotation_frame.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="nsew")
        
        # --- 使用 grid 布局来更精确地控制 Annotation 区域内部 ---
        annotation_frame.grid_columnconfigure(0, weight=1) # 让内容水平扩展

        # 标题
        ctk.CTkLabel(annotation_frame, text="Annotation", font=zh_font(16, "bold")).grid(row=0, column=0, padx=10, pady=(5, 10), sticky="w")
        
        # 损伤类型 (放在第1行)
        damage_type_frame = ctk.CTkFrame(annotation_frame, fg_color="transparent")
        damage_type_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(damage_type_frame, text="损伤类型:", font=zh_font(14)).pack(side="left")
        self.damage_type_combo = ctk.CTkComboBox(damage_type_frame, values=["pitting", "spalling", "scrape"], font=zh_font(12))
        self.damage_type_combo.pack(side="left", padx=10, expand=True, fill="x")
        self.damage_type_combo.set("pitting")

        # 寿命预测 (放在第2行)
        life_pred_frame = ctk.CTkFrame(annotation_frame, fg_color="transparent")
        life_pred_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(life_pred_frame, text="寿命预测:", font=zh_font(14)).pack(side="left")
        self.life_prediction_entry = ctk.CTkEntry(life_pred_frame, font=zh_font(12), placeholder_text="e.g., 1.5")
        self.life_prediction_entry.pack(side="left", padx=10, expand=True, fill="x")
        ctk.CTkLabel(life_pred_frame, text="年", font=zh_font(14)).pack(side="left")

        # --- 新增：Reasons 文本框 ---
        ctk.CTkLabel(annotation_frame, text="Reasons:", font=zh_font(14)).grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")
        self.reasons_textbox = ctk.CTkTextbox(annotation_frame, font=zh_font(14), height=75)
        self.reasons_textbox.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # --- 新增：Submit 按钮 ---
        submit_button = ctk.CTkButton(annotation_frame, text="Submit", command=self.submit_annotation)
        # 将按钮放在最后一行，并用 sticky="e" 使其靠右对齐
        submit_button.grid(row=5, column=0, padx=10, pady=10, sticky="e")

    def select_input_image(self):
        """打开文件对话框选择单个图像文件"""
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if not path:
            return
            
        self.input_image_path = path
        self.log_message(f"已选择输入图像: {self.input_image_path}")
        
        self.output_image_label.configure(image=None, text="等待预测结果")

        self._display_image(self.input_image_label, self.input_image_path)
        
    def run_prediction(self):
        """执行神经网络预测（占位符）"""
        if not self.input_image_path:
            self.log_message("错误：请先选择一张输入图像！")
            return
        
        self.log_message(f"开始对图像进行预测: {os.path.basename(self.input_image_path)}")
        self.log_message("...")
        
        def simulated_process():
            result_text = f"预测完成。\n损伤类型: 模拟结果-划痕\n置信度: 92.8%\n文件: {os.path.basename(self.input_image_path)}"
            self.log_message(result_text)

            try:
                img = Image.open(self.input_image_path)
                result_img = img.convert("L").convert("RGB") 
                
                save_dir = os.path.join(os.path.dirname(__file__), "..", "save", "nn_results")
                os.makedirs(save_dir, exist_ok=True)
                
                result_path = os.path.join(save_dir, "temp_result.png")
                result_img.save(result_path)
                
                self._display_image(self.output_image_label, result_path)

            except Exception as e:
                self.log_message(f"模拟生成结果时出错: {e}")
        
        self.frame.after(1000, simulated_process)

    def log_message(self, msg):
        """向日志文本框中添加信息"""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", msg + "\n")
        self.log_textbox.see("end") 
        self.log_textbox.configure(state="disabled")


    def clear_log_textbox(self):
        """清空日志文本框的内容"""
        # 必须先将状态设为"normal"才能修改内容
        self.log_textbox.configure(state="normal")
        # 删除从开头(1.0)到结尾(END)的所有文本
        self.log_textbox.delete("1.0", ctk.END)
        # 将状态设回"disabled"，防止用户直接编辑
        self.log_textbox.configure(state="disabled")


    def submit_annotation(self):
        """提交标注信息的占位符函数"""
        damage_type = self.damage_type_combo.get()
        life_pred = self.life_prediction_entry.get()
        # .get("1.0", ctk.END) 用于获取Textbox中的所有文本
        # .strip() 用于移除开头和结尾的空白符
        reasons = self.reasons_textbox.get("1.0", ctk.END).strip()

        # 在控制台打印获取到的信息，以验证功能
        print("--- Submitting Annotation ---")
        print(f"Damage Type: {damage_type}")
        print(f"Life Prediction: {life_pred} 年")
        print(f"Reasons: {reasons if reasons else 'N/A'}")
        print("TODO: Implement database saving logic here.")

        # 也可以在界面上给用户一个反馈
        self.log_message("Annotation data submitted (see console for details).")


    def _display_image(self, label_widget, image_path):
        """一个辅助函数，用于加载图像并显示在指定的CTkLabel上"""
        try:
            img = Image.open(image_path)
            widget_w = label_widget.winfo_width()
            widget_h = label_widget.winfo_height()
            
            if widget_w < 50 or widget_h < 50:
                widget_w, widget_h = 400, 400

            img.thumbnail((widget_w - 20, widget_h - 20)) 
            
            tk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            label_widget.configure(image=tk_img, text="")
        except Exception as e:
            self.log_message(f"加载图像失败: {image_path}\n错误: {e}")
        
        # --- 神经网络调用占位符 ---
        # TODO: 在此处替换为真实的神经网络命令行调用
        # 示例:
        # cmd = [
        #     "python", "path/to/your/predict_script.py",
        #     "--input", self.input_image_path,
        #     "--output", "path/to/save/result.png"
        # ]
        # try:
        #     result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        #     self.log_message("预测脚本标准输出:\n" + result.stdout)
        #     output_image_path = "path/to/save/result.png" # 从你的脚本逻辑中获取
        #     self._display_image(self.output_image_label, output_image_path)
        # except subprocess.CalledProcessError as e:
        #     self.log_message("错误：预测脚本执行失败！\n" + e.stderr)
        # except Exception as e:
        #     self.log_message(f"发生未知错误: {e}")
        
        # --- 以下为模拟的预测过程 ---
        