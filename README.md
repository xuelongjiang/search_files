# 文件搜索工具

对一个目录下的所有文本文件搜索关键字，支持多种文件格式和编码。

## 功能特点

- 支持多种文本文件格式（.txt, .md, .py, .java, .cpp, .h, .c）
- 自动识别多种文件编码
- 可点击搜索结果直接打开文件
- 显示详细的搜索统计信息

## 使用方法

1. 选择要搜索的目录
2. 输入搜索关键词
3. 点击搜索按钮
4. 在结果中点击文件名可直接打开文件

## 开发环境

- Python 3.x
- tkinter

生成exe程序 
  python -m PyInstaller --noconsole --onefile --name FileSearchTool --version-file version.txt search_files.py