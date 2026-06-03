"""侧边栏导航组件。

职责：
- 渲染导航菜单项
- 发出页面切换回调

所有颜色和字体均引用 au.utils.config，全局统一调整。
"""

import tkinter as tk
from typing import Callable

from au.utils.config import (
    COLOR_SIDEBAR_BG,
    COLOR_SIDEBAR_BG_HOVER,
    COLOR_SIDEBAR_BG_SELECTED,
    COLOR_SIDEBAR_FG,
    COLOR_SIDEBAR_FG_SELECTED,
    FONT_LABEL,
    SIDEBAR_NAV_ITEM_HEIGHT,
    SIDEBAR_WIDTH,
)


class Sidebar(tk.Frame):
    """左侧导航侧边栏。"""

    def __init__(self, parent: tk.Widget, on_select: Callable[[str], None]) -> None:
        """
        Args:
            parent: 父容器。
            on_select: 页面切换回调，接收被点击导航项的 key。
        """
        super().__init__(parent, bg=COLOR_SIDEBAR_BG, width=SIDEBAR_WIDTH)
        self.pack_propagate(False)
        self._on_select = on_select
        self._items: dict[str, tuple[tk.Frame, tk.Label]] = {}
        self._selected: str | None = None

    # ------------------------------------------------------------------
    # 公开方法
    # ------------------------------------------------------------------

    def add_item(self, key: str, label: str, icon: str = "") -> None:
        """添加一个导航项。

        Args:
            key: 导航项唯一标识。
            label: 显示文本。
            icon: 图标（emoji 或文字）。
        """
        item = tk.Frame(self, bg=COLOR_SIDEBAR_BG, height=SIDEBAR_NAV_ITEM_HEIGHT, cursor="hand2")
        item.pack(fill=tk.X)
        item.pack_propagate(False)

        # 文字标签
        display = f"  {icon}  {label}" if icon else f"  {label}"
        lbl = tk.Label(
            item,
            text=display,
            bg=COLOR_SIDEBAR_BG,
            fg=COLOR_SIDEBAR_FG,
            font=FONT_LABEL,
            anchor=tk.W,
            padx=16,
        )
        lbl.place(relwidth=1, relheight=1)

        # 事件绑定
        for w in (item, lbl):
            w.bind("<Enter>", lambda _, f=item, l=lbl, k=key: self._on_hover(f, l, True, k))
            w.bind("<Leave>", lambda _, f=item, l=lbl, k=key: self._on_hover(f, l, False, k))
            w.bind("<Button-1>", lambda _, k=key: self._on_click(k))

        self._items[key] = (item, lbl)

    def select(self, key: str) -> None:
        """选中指定导航项。"""
        if key not in self._items or key == self._selected:
            return

        # 取消旧选中
        if self._selected and self._selected in self._items:
            old_frame, old_lbl = self._items[self._selected]
            old_frame.configure(bg=COLOR_SIDEBAR_BG)
            old_lbl.configure(bg=COLOR_SIDEBAR_BG, fg=COLOR_SIDEBAR_FG)

        # 设置新选中
        frame, lbl = self._items[key]
        frame.configure(bg=COLOR_SIDEBAR_BG_SELECTED)
        lbl.configure(bg=COLOR_SIDEBAR_BG_SELECTED, fg=COLOR_SIDEBAR_FG_SELECTED)
        self._selected = key

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    def _on_click(self, key: str) -> None:
        """点击导航项。"""
        self.select(key)
        self._on_select(key)

    def _on_hover(self, frame: tk.Frame, label: tk.Label, entering: bool, key: str) -> None:
        """处理鼠标悬停效果，选中项不响应。"""
        if key == self._selected:
            return
        if entering:
            frame.configure(bg=COLOR_SIDEBAR_BG_HOVER)
            label.configure(bg=COLOR_SIDEBAR_BG_HOVER)
        else:
            frame.configure(bg=COLOR_SIDEBAR_BG)
            label.configure(bg=COLOR_SIDEBAR_BG)
