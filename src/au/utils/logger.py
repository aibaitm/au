"""
日志系统模块
------------
提供统一的日志配置，支持同时输出到控制台和文件。
采用模块级单例模式，确保整个应用生命周期内只有一个 logger 实例，
避免重复创建 handler 导致日志重复输出或文件句柄泄漏。
"""

import logging
import os
from pathlib import Path


# ============================================
# 模块级单例：确保 logger 全局只初始化一次
# ============================================
_logger: logging.Logger | None = None


def _get_project_root() -> Path:
    """
    获取项目根目录的绝对路径。

    策略：
    1. 优先通过当前文件位置反推（适用于源码运行）：log.py 位于 src/b/ 下，
       因此向上爬三层即为项目根目录。
    2. 如果 __file__ 不可用（如被 PyInstaller 打包后），回退到当前工作目录。
    3. 最终尝试通过 pyproject.toml 文件定位项目根目录。

    Returns:
        Path: 项目根目录的绝对路径。
    """
    try:
        # 从当前文件路径向上找三层：src/b/log.py -> src/b -> src -> 项目根
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent
        if project_root.exists():
            return project_root
    except (NameError, AttributeError):
        # __file__ 不可用（如打包后的 frozen 环境）
        pass

    # 回退方案：从当前工作目录向上查找 pyproject.toml
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / "pyproject.toml").exists():
            return parent

    # 最终回退：使用当前工作目录
    return cwd


def _resolve_log_dir() -> Path:
    """
    解析日志目录路径。

    优先使用环境变量 BROWSER_AUTO_LOG_DIR 指定的目录；
    未设置时默认使用项目根目录下的 logs/ 目录。

    Returns:
        Path: 日志目录的绝对路径。
    """
    env_log_dir = os.environ.get("BROWSER_AUTO_LOG_DIR")
    if env_log_dir:
        return Path(env_log_dir).resolve()

    project_root = _get_project_root()
    return project_root / "logs"


def setup_logger(
    logger_name: str = "BrowserAutomation",
    log_filename: str = "browser_automation.log",
) -> logging.Logger:
    """
    配置并返回日志记录器（单例模式）。

    首次调用时完成所有初始化工作：
    - 创建日志目录（如不存在）
    - 配置文件处理器（DEBUG 级别）和控制台处理器（INFO 级别）
    - 设置统一的日志格式

    后续调用直接返回已缓存的 logger 实例，避免重复创建。

    Args:
        logger_name: logger 的名称标识，默认为 "BrowserAutomation"。
        log_filename: 日志文件名，默认为 "browser_automation.log"。

    Returns:
        logging.Logger: 配置完成的日志记录器实例。
    """
    global _logger

    # 如果已经初始化过，直接返回缓存的实例
    if _logger is not None:
        return _logger

    # ---- 解析日志目录 ----
    logs_dir = _resolve_log_dir()

    # ---- 创建日志目录（如不存在） ----
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        # 如果目录创建失败，回退到临时目录，保证程序不崩溃
        import tempfile
        logs_dir = Path(tempfile.gettempdir()) / "browser_automation_logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        # 此时无法使用 logger 记录警告（logger 尚未创建），
        # 使用 print 作为最后的回退通知
        print(f"[WARN] 无法创建日志目录，已回退到: {logs_dir}，原因: {e}")

    # ---- 日志文件完整路径 ----
    log_file = logs_dir / log_filename

    # ---- 创建 logger 实例 ----
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # 清除已有的 handlers（防御性编程，避免残留）
    for handler in list(logger.handlers):
        handler.flush()
        handler.close()
        logger.removeHandler(handler)

    # ---- 配置文件处理器（写入所有级别日志到文件） ----
    file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # ---- 配置控制台处理器（INFO 及以上级别输出到终端） ----
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # ---- 统一日志格式 ----
    # 格式说明：
    #   %(asctime)s   - 时间戳（精确到秒）
    #   %(name)s      - logger 名称
    #   %(levelname)s - 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
    #   %(message)s   - 日志消息正文
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # ---- 将处理器挂载到 logger ----
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # ---- 防止日志消息向上传播到根 logger 导致重复输出 ----
    logger.propagate = False

    # ---- 缓存实例 ----
    _logger = logger

    logger.debug(f"日志系统初始化完成，日志文件: {log_file}")
    return logger
