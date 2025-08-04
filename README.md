## 项目结构如下：
- 主界面
  - main_app.py
- 副界面1（图像识别与分割） 
  - tab_nn.py
- 副界面2（有限元计算）
  - tab_abaqus.py
- 副界面3（光度立体法）
  - tab_pms.py

## 项目文件：
```
your_project/
├── main_app.py
├── tabs/
│   ├── tab_example.py  # 含 class Example
│   ├── tab_xxx.py      # 含 class Xxx
```
## 项目所需软件包安装：
```
pip3 install customtkinter
pip install -r requirements.txt
```
## 项目示例功能：
- `main_app.py`文件是主要运行程序，提供了三个框架
- `tab_file_manager.py`文件提供了两种上传图片的示例
- `tab_example.py`提供了编辑文本框和保存到指定路径的示例
- `tab_settings.py`提供了设置系统模式的样例