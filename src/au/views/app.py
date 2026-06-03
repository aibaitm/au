"""主窗口组装模块。

职责：
- 创建 Tk 主窗口并应用全局配置
- 组装顶栏 + 侧边栏 + 内容区 + 底栏四段布局
- 管理页面注册与切换
"""

import tkinter as tk
from tkinter import ttk

from au.utils.config import (
    COLOR_BG,
    COLOR_BORDER,
    COLOR_STATUSBAR_BG,
    COLOR_TEXT_SECONDARY,
    COLOR_TOPBAR_BG,
    FONT_STATUS,
    FONT_TITLE,
    SEPARATOR_HEIGHT,
    STATUSBAR_HEIGHT,
    TOPBAR_HEIGHT,
    WINDOW_TITLE,
    window_config,
)
from au.views.base_page import BasePage
from au.views.settings import SettingsPage
from au.views.sidebar import Sidebar
from au.views.task_list import TaskListPage


class App:
    """应用程序主窗口。

    布局结构：
    ┌──────────────────────────────────┐
    │  topbar                          │
    ├────────┬─────────────────────────┤
    │sidebar │  content                │
    │        │                         │
    ├────────┴─────────────────────────┤
    │  statusbar                       │
    └──────────────────────────────────┘
    """

    def __init__(self) -> None:
        self._window = tk.Tk()
        self._pages: dict[str, BasePage] = {}

        self._setup_window()
        # self._build_topbar() # 暂时隐藏顶栏
        self._build_statusbar()
        self._build_main_area()
        self._register_pages()
        self._select_default()

    # ------------------------------------------------------------------
    # 运行
    # ------------------------------------------------------------------

    def run(self) -> None:
        """启动主事件循环。"""
        self._window.mainloop()

    # ------------------------------------------------------------------
    # 布局构建
    # ------------------------------------------------------------------

    def _setup_window(self) -> None:
        style = ttk.Style()
        window_config(self._window, style)

    def _build_topbar(self) -> None:
        """顶部导航栏。"""
        bar = tk.Frame(self._window, bg=COLOR_TOPBAR_BG, height=TOPBAR_HEIGHT)
        bar.pack(side=tk.TOP, fill=tk.X)
        bar.pack_propagate(False)

        # 标题
        tk.Label(
            bar,
            text=f"  {WINDOW_TITLE}",
            bg=COLOR_TOPBAR_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_TITLE,
            anchor=tk.W,
        ).pack(side=tk.LEFT)

    def _build_main_area(self) -> None:
        """中间区域：侧边栏 + 内容区。"""
        main = tk.Frame(self._window, bg=COLOR_BG)
        main.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 侧边栏
        self._sidebar = Sidebar(main, on_select=self._switch_page)
        self._sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # 内容区
        self._content = tk.Frame(main, bg=COLOR_BG)
        self._content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _build_statusbar(self) -> None:
        """底部状态栏。"""
        bar = tk.Frame(self._window, bg=COLOR_STATUSBAR_BG, height=STATUSBAR_HEIGHT)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        bar.pack_propagate(False)

        # 分隔线
        tk.Frame(bar, bg=COLOR_BORDER, height=SEPARATOR_HEIGHT).pack(side=tk.TOP, fill=tk.X)

        # 状态标签（后续动态更新）
        self._status_label = tk.Label(
            bar,
            text="  就绪",
            bg=COLOR_STATUSBAR_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_STATUS,
            anchor=tk.W,
        )
        self._status_label.pack(side=tk.LEFT)

    # ------------------------------------------------------------------
    # 页面管理
    # ------------------------------------------------------------------

    def _register_pages(self) -> None:
        """注册所有功能页面。"""
        self._register("tasks", "任务列表", "📋", TaskListPage)
        self._register("settings", "设置", "⚙", SettingsPage)

    def _register(self, key: str, label: str, icon: str, page_cls: type[BasePage]) -> None:
        """注册一个页面及其对应的导航项。"""
        self._sidebar.add_item(key, label, icon)
        page = page_cls(self._content)
        self._pages[key] = page

    def _select_default(self) -> None:
        """默认显示第一个页面。"""
        first_key = next(iter(self._pages))
        self._switch_page(first_key)

    # ------------------------------------------------------------------
    # 页面切换
    # ------------------------------------------------------------------

    def _switch_page(self, key: str) -> None:
        """切换内容区显示的页面。"""
        self._sidebar.select(key)
        for k, page in self._pages.items():
            if k == key:
                page.show()
                page.refresh()
            else:
                page.hide()


# ------------------------------------------------------------------
# 模块入口（保持向后兼容）
# ------------------------------------------------------------------

def app() -> None:
    """启动 GUI 应用程序。"""
    App().run()
