import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re

class FileRenamer:
    def __init__(self, root):
        self.root = root
        self.root.title("批量文件重命名工具 v0.3.3 -- 使用建议，联系作者：军安改办 蔡勒，13802722009")
        self.root.geometry("800x800")
        self.root.resizable(True, True)
        
        self.source_folder = ""
        self.output_folder = ""
        self.files = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 源文件夹选择
        source_frame = ttk.LabelFrame(main_frame, text="源文件夹", padding="5")
        source_frame.pack(fill=tk.X, pady=5)
        
        self.source_entry = ttk.Entry(source_frame, width=70)
        self.source_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        source_button = ttk.Button(source_frame, text="浏览...", command=self.browse_source)
        source_button.pack(side=tk.RIGHT, padx=5)
        
        # 输出文件夹选择
        output_frame = ttk.LabelFrame(main_frame, text="输出文件夹", padding="5")
        output_frame.pack(fill=tk.X, pady=5)
        
        self.output_entry = ttk.Entry(output_frame, width=70)
        self.output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        output_button = ttk.Button(output_frame, text="浏览...", command=self.browse_output)
        output_button.pack(side=tk.RIGHT, padx=5)
        
        # 重命名规则
        rules_frame = ttk.LabelFrame(main_frame, text="重命名规则", padding="5")
        rules_frame.pack(fill=tk.X, pady=5)
               
        # 规则类型选择
        self.rule_type = tk.StringVar(value="sequence")  # 修改默认值为sequence
        rule_type_frame = ttk.Frame(rules_frame)
        rule_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(rule_type_frame, text="序号重命名", variable=self.rule_type, value="sequence").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(rule_type_frame, text="添加前缀", variable=self.rule_type, value="prefix").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(rule_type_frame, text="添加后缀", variable=self.rule_type, value="suffix").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(rule_type_frame, text="替换文本", variable=self.rule_type, value="replace").pack(side=tk.LEFT, padx=10)
        # 删除正则表达式选项
     #   ttk.Radiobutton(rule_type_frame, text="正则表达式", variable=self.rule_type, value="regex").pack(side=tk.LEFT, padx=10)
           
        # 规则参数
        rule_params_frame = ttk.Frame(rules_frame)
        rule_params_frame.pack(fill=tk.X, pady=5)
        
        # 添加参数说明标签
        params_help_frame = ttk.Frame(rules_frame)
        params_help_frame.pack(fill=tk.X, pady=2)
        
        help_text = """参数说明：
序号重命名：参数1=起始序号(默认1)，参数2=序号位数(默认3)
添加前缀：参数1=要添加的前缀文本
添加后缀：参数1=要添加的后缀文本
替换文本：参数1=要替换的文本，参数2=替换后的文本"""
        
        help_label = ttk.Label(params_help_frame, text=help_text, justify=tk.LEFT)
        help_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(rule_params_frame, text="参数1:").pack(side=tk.LEFT, padx=5)
        self.param1_entry = ttk.Entry(rule_params_frame, width=30)
        self.param1_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(rule_params_frame, text="参数2:").pack(side=tk.LEFT, padx=5)
        self.param2_entry = ttk.Entry(rule_params_frame, width=30)
        self.param2_entry.pack(side=tk.LEFT, padx=5)
        # 文件列表
        files_frame = ttk.LabelFrame(main_frame, text="文件列表", padding="5")
        files_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建带滚动条的树形视图（用于两列显示）
        list_frame = ttk.Frame(files_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Treeview组件
        self.files_treeview = ttk.Treeview(list_frame, columns=("original", "renamed"), show="headings")
        self.files_treeview.heading("original", text="原文件名")
        self.files_treeview.heading("renamed", text="重命名后")
        self.files_treeview.column("original", width=300)
        self.files_treeview.column("renamed", width=300)
        self.files_treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加垂直滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.files_treeview.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_treeview.configure(yscrollcommand=scrollbar.set)
        
        # 预览按钮
        preview_button = ttk.Button(main_frame, text="预览重命名结果", command=self.preview_rename)
        preview_button.pack(pady=5)
        
        # 执行按钮
        execute_frame = ttk.Frame(main_frame)
        execute_frame.pack(fill=tk.X, pady=10)
        
        execute_button = ttk.Button(execute_frame, text="执行重命名", command=self.execute_rename)
        execute_button.pack(side=tk.RIGHT, padx=5)
        
        refresh_button = ttk.Button(execute_frame, text="刷新文件列表", command=self.refresh_files)
        refresh_button.pack(side=tk.RIGHT, padx=5)
    def refresh_files(self):
        if not self.source_folder:
            messagebox.showwarning("警告", "请先选择源文件夹")
            return
        
        self.files = []
        # 清空树形视图
        for item in self.files_treeview.get_children():
            self.files_treeview.delete(item)
        
        try:
            for filename in os.listdir(self.source_folder):
                file_path = os.path.join(self.source_folder, filename)
                if os.path.isfile(file_path):
                    self.files.append(filename)
                    self.files_treeview.insert("", "end", values=(filename, ""))
        except Exception as e:
            messagebox.showerror("错误", f"读取文件夹时出错: {str(e)}")
    def browse_source(self):
        folder = filedialog.askdirectory(title="选择源文件夹")
        if folder:
            self.source_folder = folder
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, folder)
            self.refresh_files()
    def browse_output(self):
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_folder = folder
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)
    def get_new_filename(self, old_filename):
        rule_type = self.rule_type.get()
        param1 = self.param1_entry.get()
        param2 = self.param2_entry.get()
        
        name, ext = os.path.splitext(old_filename)
        
        if rule_type == "prefix":
            return f"{param1}{name}{ext}"
        elif rule_type == "suffix":
            return f"{name}{param1}{ext}"
        elif rule_type == "replace":
            return f"{name.replace(param1, param2)}{ext}"
        elif rule_type == "sequence":
            try:
                # param1: 起始序号（如：1）
                # param2: 序号位数（如：3）
                start_num = int(param1) if param1.strip() else 1
                digits = int(param2) if param2.strip() else 3
                return f"{start_num:0{digits}d}_{name}{ext}"
            except ValueError:
                return f"ERROR_SEQ_{name}{ext}"
        
        return old_filename
    def preview_rename(self):
        if not self.files:
            messagebox.showwarning("警告", "没有文件可以重命名")
            return
        
        # 清空树形视图
        for item in self.files_treeview.get_children():
            self.files_treeview.delete(item)
        
        # 获取起始序号
        start_num = int(self.param1_entry.get()) if self.param1_entry.get().strip() else 1
        original_param1 = self.param1_entry.get()  # 保存原始参数值
        
        for i, old_filename in enumerate(self.files):
            current_num = start_num
            if self.rule_type.get() == "sequence":
                # 计算当前序号但不更新输入框
                current_num = start_num + i
                # 临时设置参数值用于生成文件名
                temp_param1 = str(current_num)
            else:
                temp_param1 = original_param1
                
            # 临时保存当前参数值
            original_value = self.param1_entry.get()
            # 设置临时值用于生成文件名
            self.param1_entry.delete(0, tk.END)
            self.param1_entry.insert(0, temp_param1)
            
            # 获取新文件名
            new_filename = self.get_new_filename(old_filename)
            
            # 恢复原始参数值
            self.param1_entry.delete(0, tk.END)
            self.param1_entry.insert(0, original_value)
            
            # 插入两列数据
            self.files_treeview.insert("", "end", values=(old_filename, new_filename))
        
        # 确保参数1恢复为原始值
        self.param1_entry.delete(0, tk.END)
        self.param1_entry.insert(0, original_param1)
    def execute_rename(self):
        if not self.files:
            messagebox.showwarning("警告", "没有文件可以重命名")
            return
        
        if not self.output_folder:
            messagebox.showwarning("警告", "请选择输出文件夹")
            return
        
        # 确保输出文件夹存在
        os.makedirs(self.output_folder, exist_ok=True)
        
        # 获取起始序号和原始参数值
        start_num = int(self.param1_entry.get()) if self.param1_entry.get().strip() else 1
        original_param1 = self.param1_entry.get()
        
        success_count = 0
        error_count = 0
        for i, old_filename in enumerate(self.files):
            if self.rule_type.get() == "sequence":
                # 临时设置当前序号
                current_num = start_num + i
                self.param1_entry.delete(0, tk.END)
                self.param1_entry.insert(0, str(current_num))
            
            new_filename = self.get_new_filename(old_filename)
            try:
                source_path = os.path.join(self.source_folder, old_filename)
                dest_path = os.path.join(self.output_folder, new_filename)
                # 复制文件到新位置并重命名
                shutil.copy2(source_path, dest_path)
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"重命名文件 {old_filename} 时出错: {str(e)}")
        
        # 恢复原始参数值
        self.param1_entry.delete(0, tk.END)
        self.param1_entry.insert(0, original_param1)
        
        messagebox.showinfo("完成", f"重命名完成！\n成功: {success_count}\n失败: {error_count}")
        
        # 刷新文件列表
        self.refresh_files()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamer(root)
    root.mainloop()