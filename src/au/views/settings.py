"""设置页面 — 占位，后续实现全局配置管理。"""

import tkinter as tk

from au.views.base_page import BasePage
from au.views.widgets import Placeholder


class SettingsPage(BasePage):
    """全局设置页面。

    未来功能：
    - 浏览器路径配置
    - 默认 URL 配置
    - 日志级别设置
    - 外观主题切换
    """

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        Placeholder(
            self,
            icon="⚙",
            title="设置",
            description="全局配置与偏好设置\n将在此处统一管理",
        ).pack(fill=tk.BOTH, expand=True)
