"""任务列表页面 — 使用标签栏管理多个任务面板。"""

import tkinter as tk

from au.utils.config import COLOR_BG
from au.views.base_page import BasePage
from au.views.widgets import Placeholder, TabBar


class TaskListPage(BasePage):
    """任务列表管理页面。

    通过标签栏切换不同任务视图。
    """

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)

        # 标签栏
        self._tabbar = TabBar(self, on_select=self._on_tab_select, on_close=self._on_tab_close)
        self._tabbar.pack(fill=tk.X)

        # 内容区（存放每个标签对应的内容）
        self._content = tk.Frame(self, bg=COLOR_BG)
        self._content.pack(fill=tk.BOTH, expand=True)

        # 默认标签
        self._panels: dict[str, tk.Widget] = {}
        self._add_tab("overview", "概览")
        self._add_tab("running", "运行中")
        self._add_tab("history", "历史记录")
        self._tabbar.select("overview")

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    def _add_tab(self, key: str, label: str) -> None:
        """添加一个标签及对应内容面板。"""
        self._tabbar.add(key, label, closable=False)

        panel = tk.Frame(self._content, bg=COLOR_BG)
        Placeholder(panel, icon="📋", title=label, description="此面板待实现").pack(fill=tk.BOTH, expand=True)
        self._panels[key] = panel

    def _on_tab_select(self, key: str) -> None:
        """切换标签内容。"""
        for k, panel in self._panels.items():
            if k == key:
                panel.pack(fill=tk.BOTH, expand=True)
            else:
                panel.pack_forget()

    def _on_tab_close(self, key: str) -> None:
        """关闭标签时清理对应面板。"""
        if key in self._panels:
            self._panels[key].destroy()
            del self._panels[key]
