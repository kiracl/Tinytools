# 批量文件重命名工具

这是一个使用Python和Tkinter开发的批量文件重命名工具，支持多种重命名规则，包括序号重命名、添加前缀/后缀、文本替换和正则表达式替换。

## 功能特点

- 序号重命名：可设置起始序号和序号位数
- 添加前缀/后缀：在文件名前/后添加指定文本
- 文本替换：替换文件名中的特定文本
- 正则表达式：使用正则表达式进行高级替换
- 预览功能：在执行前预览重命名结果
- 双列显示：清晰对比重命名前后的文件名

## 使用方法

1. 选择源文件夹
2. 选择输出文件夹
3. 选择重命名规则并设置参数
4. 点击"预览重命名结果"查看效果
5. 点击"执行重命名"完成操作

## 联系方式

如有使用建议，请联系作者：军安改办 蔡勒，13802722009

## 部署方式
- 确保安装了Python（建议Python 3.6+）
- 运行以下命令安装依赖（如果需要）：
```bash
    pip install tkinter
    pytyhon file_rename.py
```
- 封装
    - 首先安装pyinstaller，必要的打包工具，参数如下：
        - --onefile：将所有依赖打包到一个可执行文件中
        - --noconsole：不显示控制台窗口
        - --icon：指定可执行文件的图标  
    - 为了确保可执行文件的图标被正确打包，需要将图标文件（例如icon.ico）放在与脚本相同的目录下。
    - 为了确保所有依赖都被正确打包，可以创建一个requiremnets.txt:
```bash
    pip freeze > requirements.txt
```
    - 使用时，用以下命令安装所有依赖：
```bash
    pip install -r requirements.txt
```
    - 打包命令：
```bash
    pip install pyinstaller
    pyinstaller --name FileRenamer --windowed --onefile --clean --noupx --icon=app_icon.ico file_renamer.py
```
- 如果在安装 pyinstaller 时遇到了网络超时问题，files.pythonhosted.org 服务器超时，可以尝试以下方法：
    - 更换源：使用国内镜像源，例如：
```bash
    pip install pyinstaller -i https://mirrors.aliyun.com/pypi/simple/
    pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

## 版本历史
- 2025-3-6 0.1.0 初始版本
- 2025-3-6 0.3.2 取消正则表达式功能
- 2025-3-6 0.3.3 修正参数1显示问题
