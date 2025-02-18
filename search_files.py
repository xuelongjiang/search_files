import os
import glob
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext

def search_files(directory, keyword, result_text):
    # 获取所有文本文件
    text_extensions = ['.txt', '.md', '.py', '.java', '.cpp', '.h', '.c']
    result_text.delete(1.0, tk.END)
    
    total_files = 0
    total_matches = 0
    total_searched = 0
    keyword = keyword.lower()
    
    # 尝试不同的编码格式
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'ascii', 'iso-8859-1']
    
    try:
        for file_path in Path(directory).rglob('*'):
            if file_path.suffix.lower() in text_extensions:
                total_searched += 1
                file_has_match = False
                
                # 尝试不同的编码格式读取文件
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as file:
                            content = file.readlines()
                            for line_num, line in enumerate(content, 1):
                                if keyword in line.lower():
                                    if not file_has_match:
                                        result_text.insert(tk.END, f'\n文件: ')
                                        result_text.insert(tk.END, str(file_path), 'file_link')
                                        result_text.insert(tk.END, '\n')
                                        file_has_match = True
                                        total_files += 1
                                    result_text.insert(tk.END, f'行号: {line_num}\n')
                                    result_text.insert(tk.END, f'内容: {line.strip()}\n')
                                    total_matches += 1
                        break  # 如果成功读取文件，跳出编码尝试循环
                    except UnicodeDecodeError:
                        continue
                    except Exception as e:
                        result_text.insert(tk.END, f"处理文件 {file_path} 时出错: {str(e)}\n")
                        break
    
    except Exception as e:
        result_text.insert(tk.END, f"搜索过程中出错: {str(e)}\n")
    
    return total_files, total_matches, total_searched

class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件搜索工具")
        # 添加更多程序信息
        self.root.wm_iconbitmap(default="")  # 如果有图标的话
        self.root.geometry("800x600")
        
        # 创建框架
        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 设置默认搜索目录
        self.dir_path = tk.StringVar(value="D:/treenote")
        ttk.Label(self.frame, text="搜索目录:").grid(row=0, column=0, sticky=tk.W)
        self.dir_entry = ttk.Entry(self.frame, textvariable=self.dir_path, width=50)
        self.dir_entry.grid(row=0, column=1, padx=5)
        ttk.Button(self.frame, text="选择目录", command=self.choose_directory).grid(row=0, column=2)
        
        # 搜索关键词
        ttk.Label(self.frame, text="搜索关键词:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.keyword_entry = ttk.Entry(self.frame, width=50)
        self.keyword_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.frame, text="搜索", command=self.start_search).grid(row=1, column=2)
        
        # 结果显示区域
        self.result_text = scrolledtext.ScrolledText(self.frame, width=80, height=30)
        self.result_text.grid(row=2, column=0, columnspan=3, pady=10)
        
        # 添加文件链接的标签和绑定点击事件
        self.result_text.tag_configure('file_link', foreground='blue', underline=True)
        self.result_text.tag_bind('file_link', '<Button-1>', self.open_file)
        self.result_text.tag_bind('file_link', '<Enter>', lambda e: self.result_text.configure(cursor='hand2'))
        self.result_text.tag_bind('file_link', '<Leave>', lambda e: self.result_text.configure(cursor=''))
        
        # 配置grid权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        
        # 添加统计结果标签
        self.stats_label = ttk.Label(self.frame, text="")
        self.stats_label.grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # 添加版本信息
        version_label = ttk.Label(
            self.frame, 
            text="文件搜索工具 v1.0 | 作者：Trae | 仅用于文本文件搜索", 
            foreground="gray"
        )
        version_label.grid(row=4, column=0, columnspan=3, sticky=tk.E, pady=5)
    def open_file(self, event):
        try:
            # 获取点击位置的文件路径
            index = self.result_text.index(f"@{event.x},{event.y}")
            line_start = self.result_text.index(f"{index} linestart")
            line_end = self.result_text.index(f"{index} lineend")
            line = self.result_text.get(line_start, line_end)
            
            # 提取文件路径（去除"文件: "前缀）
            if line.startswith("文件: "):
                file_path = line[4:].strip()
                file_path = os.path.normpath(file_path)  # 规范化路径
                
                if os.path.exists(file_path):
                    try:
                        # 尝试使用系统默认程序打开
                        os.startfile(file_path)
                    except:
                        # 如果默认方法失败，尝试使用替代方法
                        import subprocess
                        subprocess.run(['explorer', file_path], check=True)
                else:
                    self.result_text.insert(tk.END, f"\n错误：文件不存在 - {file_path}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"\n打开文件时出错：{str(e)}\n")
    
    def choose_directory(self):
        directory = filedialog.askdirectory(
            title="选择搜索目录",
            initialdir=self.dir_path.get() or os.path.expanduser("~")
        )
        if directory:
            self.dir_path.set(directory)
    def start_search(self):
        directory = self.dir_path.get()
        keyword = self.keyword_entry.get()
        
        if not directory or not keyword:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "请选择目录并输入搜索关键词！\n")
            return
        
        if not os.path.exists(directory):
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "目录不存在！\n")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"正在搜索 '{keyword}' ...\n")
        total_files, total_matches, total_searched = search_files(directory, keyword, self.result_text)
        
        # 更新统计信息标签，添加搜索词
        self.stats_label.config(
            text=f"搜索完成！关键词 '{keyword}' 在 {total_searched} 个文件中搜索，"
                 f"找到 {total_files} 个匹配文件，共 {total_matches} 处匹配。"
        )
        self.result_text.insert(tk.END, "\n搜索完成！")

def main():
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()