"""页面基类，定义所有功能页面的统一接口。"""

import tkinter as tk

from au.utils.config import COLOR_BG


class BasePage(tk.Frame):
    """功能页面的抽象基类。

    所有侧边栏导航对应的内容页面都应继承此类。
    子类无需重写 show/hide，基类已通过 pack/pack_forget 管理可见性。
    """

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, bg=COLOR_BG)

    def show(self) -> None:
        """显示页面。"""
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self) -> None:
        """隐藏页面（保留状态，不销毁）。"""
        self.pack_forget()

    def refresh(self) -> None:
        """刷新页面数据（子类按需重写）。"""
        pass
