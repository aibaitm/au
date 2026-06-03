"""
浏览器自动化工具
---
浏览器自动化工具，基于 Playwright + Tkinter。
提供一键启动 Chrome 浏览器并访问指定网页的 GUI 应用程序。

用法:
    python -m au
    或通过命令行入口:
    au
"""

from au.views import app

def main() -> None:
    """
    应用程序入口函数。

    启动 Tkinter GUI 窗口，进入主事件循环。
    用户点击按钮后，浏览器自动化任务在后台线程中执行。
    """
    app()