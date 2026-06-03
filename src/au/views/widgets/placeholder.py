"""占位提示组件。

用于功能尚未实现的页面或区域，居中显示图标、标题和描述。
"""

import tkinter as tk

from au.utils.config import (
    COLOR_BG,
    COLOR_TEXT_HINT,
    COLOR_TEXT_MUTED,
    COLOR_TEXT_SECONDARY,
    FONT_ICON,
    FONT_PLACEHOLDER_DESC,
    FONT_PLACEHOLDER_TITLE,
)


class Placeholder(tk.Frame):
    """居中占位提示。

    使用示例:
        Placeholder(parent, icon="📋", title="任务列表", description="即将上线")
    """

    def __init__(
        self,
        parent: tk.Widget,
        icon: str = "🔧",
        title: str = "",
        description: str = "",
    ) -> None:
        super().__init__(parent, bg=COLOR_BG)
        self._build(icon, title, description)

    def _build(self, icon: str, title: str, description: str) -> None:
        center = tk.Frame(self, bg=COLOR_BG)
        center.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(
            center,
            text=icon,
            font=FONT_ICON,
            bg=COLOR_BG,
            fg=COLOR_TEXT_MUTED,
        ).pack(pady=(0, 12))

        if title:
            tk.Label(
                center,
                text=title,
                font=FONT_PLACEHOLDER_TITLE,
                bg=COLOR_BG,
                fg=COLOR_TEXT_SECONDARY,
            ).pack(pady=(0, 6))

        if description:
            tk.Label(
                center,
                text=description,
                font=FONT_PLACEHOLDER_DESC,
                bg=COLOR_BG,
                fg=COLOR_TEXT_HINT,
            ).pack()
