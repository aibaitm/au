# ============================================
# 窗口配置常量
# ============================================
WINDOW_TITLE: str = "auto"
WINDOW_WIDTH: int = 1200
WINDOW_HEIGHT: int = 820
WINDOW_MIN_WIDTH: int = 600
WINDOW_MIN_HEIGHT: int = 500

# 配色方案
COLOR_BG: str = "#f0f2f5"              # 窗口背景
COLOR_PANEL_BG: str = "#ffffff"        # 面板背景
COLOR_PRIMARY: str = "#1677ff"         # 主色调（蓝色）
COLOR_PRIMARY_HOVER: str = "#4096ff"   # 主色调悬停
COLOR_SUCCESS: str = "#52c41a"         # 成功/启动
COLOR_DANGER: str = "#ff4d4f"          # 危险/停止
COLOR_TEXT_PRIMARY: str = "#1f1f1f"    # 主文字
COLOR_TEXT_SECONDARY: str = "#666666"  # 次要文字
COLOR_BORDER: str = "#e0e0e0"          # 边框
COLOR_LOG_BG: str = "#1e1e1e"          # 日志面板背景（暗色终端风格）
COLOR_LOG_FG: str = "#d4d4d4"          # 日志文字
COLOR_STATUS_READY: str = "#52c41a"    # 状态：就绪
COLOR_STATUS_RUNNING: str = "#1677ff"  # 状态：运行中
COLOR_STATUS_ERROR: str = "#ff4d4f"    # 状态：错误
COLOR_TEXT_MUTED: str = "#cccccc"      # 弱化文字（图标等）
COLOR_TEXT_HINT: str = "#999999"       # 提示文字（描述等）

# 侧边栏配色
COLOR_SIDEBAR_BG: str = "#ffffff"           # 侧边栏背景
COLOR_SIDEBAR_FG: str = "#666666"           # 导航项文字
COLOR_SIDEBAR_FG_SELECTED: str = "#ffffff"  # 导航项选中文字
COLOR_SIDEBAR_BG_HOVER: str = "#e6f0ff"     # 导航项悬停背景（浅蓝）
COLOR_SIDEBAR_BG_SELECTED: str = COLOR_PRIMARY  # 导航项选中背景（跟随主色调）
SIDEBAR_WIDTH: int = 140                    # 侧边栏宽度
SIDEBAR_NAV_ITEM_HEIGHT: int = 36           # 导航项高度

# 顶栏/底栏
COLOR_TOPBAR_BG: str = "#ffffff"            # 顶栏背景
COLOR_STATUSBAR_BG: str = "#fafafa"         # 底栏背景
TOPBAR_HEIGHT: int = 36                     # 顶栏高度
STATUSBAR_HEIGHT: int = 28                  # 底栏高度

# 字体（思源黑体，SIL Open Font License 1.1，可免费商用）
FONT_TITLE: tuple[str, int, str] = ("Noto Sans SC", 13, "bold")
FONT_LABEL: tuple[str, int] = ("Noto Sans SC", 10)
FONT_BUTTON: tuple[str, int] = ("Noto Sans SC", 10)
FONT_LOG: tuple[str, int] = ("Consolas", 9)
FONT_STATUS: tuple[str, int] = ("Noto Sans SC", 9)
FONT_ICON: tuple[str, int] = ("Noto Sans SC", 48)          # 占位图标
FONT_PLACEHOLDER_TITLE: tuple[str, int, str] = ("Noto Sans SC", 14, "bold")  # 占位标题
FONT_PLACEHOLDER_DESC: tuple[str, int] = ("Noto Sans SC", 10)                # 占位描述

# 默认配置值
DEFAULT_URL: str = "http://192.168.100.66:7000"

# ============================================
# 窗口关闭时的清理逻辑
# ============================================
def _on_window_close(window) -> None:
    """
    处理窗口关闭事件。
    守护线程会在主线程退出时自动终止。
    """
    window.destroy()


def window_config(window, style):
    window.title(WINDOW_TITLE)
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    window.configure(bg=COLOR_BG)

    # 注册窗口关闭协议
    window.protocol("WM_DELETE_WINDOW", lambda: _on_window_close(window))

    style.theme_use("clam")  # clam 主题对自定义颜色支持较好

    # 全局背景
    style.configure(".", background=COLOR_BG, font=FONT_LABEL)
    style.configure("TNotebook", background=COLOR_BG, borderwidth=0)
    style.configure("TNotebook.Tab", padding=(16, 8), font=FONT_LABEL)
    style.map(
        "TNotebook.Tab",
        background=[("selected", COLOR_PANEL_BG)],
        foreground=[("selected", COLOR_PRIMARY)],
    )
    style.configure("Panel.TLabelframe", background=COLOR_PANEL_BG, borderwidth=1)
    style.configure("Panel.TLabelframe.Label", font=FONT_LABEL, foreground=COLOR_TEXT_PRIMARY)
