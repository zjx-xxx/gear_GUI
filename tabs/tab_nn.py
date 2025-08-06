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
        self.init_log_ui()

    # ... (init_input_ui, init_output_ui, init_log_ui 等其他所有方法保持完全不变) ...
    def init_input_ui(self):
        """初始化左侧的输入图像区域"""
        container = ctk.CTkFrame(self.frame)
        container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(container, text="输入图像", font=zh_font(16, "bold")).pack(pady=10)

        # --- 这里是关键修改 ---
        # 1. 创建一个专门用于显示图片的可伸缩框架
        #    这个框架会占据大部分空间
        image_container = ctk.CTkFrame(container, fg_color="transparent")
        image_container.pack(fill="both", expand=True, padx=20, pady=10)

        # 2. 将图片标签放入这个新的框架中
        #    这样它的尺寸变化只会影响 image_container 内部
        self.input_image_label = ctk.CTkLabel(image_container, text="请选择一张图片", font=zh_font(14))
        self.input_image_label.pack(expand=True)
        
        # 3. 按钮框架现在被 pack 在 image_container 之后，不会被挤走
        button_frame = ctk.CTkFrame(container)
        button_frame.pack(pady=10, fill="x", padx=20)
        
        ctk.CTkButton(button_frame, text="选择图像", font=zh_font(14), command=self.select_input_image).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(button_frame, text="执行预测", font=zh_font(14), command=self.run_prediction).pack(side="left", expand=True, padx=5)    

    def init_output_ui(self):
        """初始化右侧的输出结果区域"""
        container = ctk.CTkFrame(self.frame)
        container.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(container, text="预测结果图像", font=zh_font(16, "bold")).pack(pady=10)

        self.output_image_label = ctk.CTkLabel(container, text="等待预测结果", font=zh_font(14))
        self.output_image_label.pack(fill="both", expand=True, padx=20, pady=20)

    def init_log_ui(self):
        """初始化底部的日志输出区域"""
        container = ctk.CTkFrame(self.frame)
        container.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(container, text="输出日志", font=zh_font(16, "bold")).pack(pady=(5, 5), anchor="w", padx=10)
        
        self.log_textbox = ctk.CTkTextbox(container, height=150, font=zh_font(12), state="disabled")
        self.log_textbox.pack(fill="x", expand=True, padx=10, pady=(0, 10))

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
        