"""标签栏组件。

可复用的标签页导航，支持添加、切换、关闭标签。
所有颜色和字体均引用 au.utils.config。
"""

import tkinter as tk
from typing import Callable

from au.utils.config import (
    COLOR_BG,
    COLOR_BORDER,
    COLOR_PANEL_BG,
    COLOR_PRIMARY,
    COLOR_TEXT_HINT,
    COLOR_TEXT_PRIMARY,
    COLOR_TEXT_SECONDARY,
    FONT_LABEL,
    FONT_STATUS,
)


class TabBar(tk.Frame):
    """水平标签栏。

    使用示例:
        bar = TabBar(parent, on_select=handle_select, on_close=handle_close)
        bar.add("tab1", "页面1")
        bar.add("tab2", "页面2", closable=True)
        bar.select("tab1")
    """

    def __init__(
        self,
        parent: tk.Widget,
        on_select: Callable[[str], None] | None = None,
        on_close: Callable[[str], None] | None = None,
    ) -> None:
        """
        Args:
            parent: 父容器。
            on_select: 标签选中回调，接收 key。
            on_close: 标签关闭回调，接收 key。返回 False 可阻止关闭。
        """
        super().__init__(parent, bg=COLOR_BG, height=36)
        self.pack_propagate(False)
        self._on_select = on_select
        self._on_close = on_close
        self._tabs: dict[str, tk.Frame] = {}
        self._selected: str | None = None

        # 底部边框线
        tk.Frame(self, bg=COLOR_BORDER, height=1).pack(side=tk.BOTTOM, fill=tk.X)

    # ------------------------------------------------------------------
    # 公开方法
    # ------------------------------------------------------------------

    def add(self, key: str, label: str, closable: bool = False) -> None:
        """添加一个标签。

        Args:
            key: 标签唯一标识。
            label: 显示文本。
            closable: 是否显示关闭按钮。
        """
        if key in self._tabs:
            return

        tab = tk.Frame(self, bg=COLOR_BG, cursor="hand2")
        tab.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))

        # 文字
        lbl = tk.Label(
            tab,
            text=f"  {label}  ",
            bg=COLOR_BG,
            fg=COLOR_TEXT_SECONDARY,
            font=FONT_LABEL,
            padx=4,
        )
        lbl.pack(side=tk.LEFT)

        # 关闭按钮
        if closable:
            btn = tk.Label(
                tab,
                text="×",
                bg=COLOR_BG,
                fg=COLOR_TEXT_HINT,
                font=FONT_STATUS,
                cursor="hand2",
                padx=4,
            )
            btn.pack(side=tk.LEFT)
            btn.bind("<Button-1>", lambda _, k=key: self._do_close(k))
            # hover 效果
            btn.bind("<Enter>", lambda _, b=btn: b.configure(fg=COLOR_TEXT_PRIMARY))
            btn.bind("<Leave>", lambda _, b=btn: b.configure(fg=COLOR_TEXT_HINT))

        # 绑定事件
        for w in (tab, lbl):
            w.bind("<Button-1>", lambda _, k=key: self.select(k))
            w.bind("<Enter>", lambda _, t=tab, l=lbl: self._hover(t, l, True))
            w.bind("<Leave>", lambda _, t=tab, l=lbl: self._hover(t, l, False))

        self._tabs[key] = tab

    def select(self, key: str) -> None:
        """选中指定标签。"""
        if key not in self._tabs or key == self._selected:
            return

        # 取消旧选中
        if self._selected and self._selected in self._tabs:
            self._set_style(self._tabs[self._selected], selected=False)

        # 设置新选中
        self._set_style(self._tabs[key], selected=True)
        self._selected = key

        if self._on_select:
            self._on_select(key)

    def remove(self, key: str) -> None:
        """移除标签。"""
        if key not in self._tabs:
            return
        self._tabs[key].destroy()
        del self._tabs[key]
        if key == self._selected:
            self._selected = None

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    def _do_close(self, key: str) -> None:
        """处理关闭操作。"""
        if self._on_close:
            self._on_close(key)
        self.remove(key)

    def _hover(self, tab: tk.Frame, label: tk.Label, entering: bool) -> None:
        """悬停效果，选中项不响应。"""
        if tab is self._tabs.get(self._selected):
            return
        if entering:
            tab.configure(bg=COLOR_PANEL_BG)
            label.configure(bg=COLOR_PANEL_BG)
        else:
            tab.configure(bg=COLOR_BG)
            label.configure(bg=COLOR_BG)

    def _set_style(self, tab: tk.Frame, selected: bool) -> None:
        """设置标签样式。"""
        label = tab.winfo_children()[0]
        if selected:
            tab.configure(bg=COLOR_PANEL_BG)
            label.configure(bg=COLOR_PANEL_BG, fg=COLOR_PRIMARY)
        else:
            tab.configure(bg=COLOR_BG)
            label.configure(bg=COLOR_BG, fg=COLOR_TEXT_SECONDARY)
