#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强日志记录器 - 提供结构化的日志功能
"""

import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

class EnhancedLogger:
    """增强日志记录器类"""

    def __init__(self, log_dir: str = "logs"):
        """
        初始化日志记录器

        Args:
            log_dir: 日志目录
        """
        self.log_dir = log_dir
        self.ensure_log_dir()
        self.setup_loggers()

    def ensure_log_dir(self):
        """确保日志目录存在"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def setup_loggers(self):
        """设置日志记录器"""
        # 应用日志
        self.app_logger = logging.getLogger("app")
        self.app_logger.setLevel(logging.INFO)

        # 用户操作日志
        self.user_logger = logging.getLogger("user")
        self.user_logger.setLevel(logging.INFO)

        # 错误日志
        self.error_logger = logging.getLogger("error")
        self.error_logger.setLevel(logging.ERROR)

        # 创建文件处理器
        today = datetime.now().strftime("%Y-%m-%d")

        app_handler = logging.FileHandler(
            os.path.join(self.log_dir, f"app_{today}.log"),
            encoding='utf-8'
        )
        user_handler = logging.FileHandler(
            os.path.join(self.log_dir, f"user_{today}.log"),
            encoding='utf-8'
        )
        error_handler = logging.FileHandler(
            os.path.join(self.log_dir, f"error_{today}.log"),
            encoding='utf-8'
        )

        # 设置格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        app_handler.setFormatter(formatter)
        user_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)

        # 添加处理器
        self.app_logger.addHandler(app_handler)
        self.user_logger.addHandler(user_handler)
        self.error_logger.addHandler(error_handler)

    def log_app(self, message: str, level: str = "info"):
        """
        记录应用日志

        Args:
            message: 日志消息
            level: 日志级别
        """
        if level.lower() == "error":
            self.app_logger.error(message)
        elif level.lower() == "warning":
            self.app_logger.warning(message)
        else:
            self.app_logger.info(message)

    def log_user_action(self, action: str, details: Optional[Dict[str, Any]] = None):
        """
        记录用户操作

        Args:
            action: 操作描述
            details: 操作详情
        """
        message = f"用户操作: {action}"
        if details:
            message += f" - 详情: {details}"
        self.user_logger.info(message)

    def log_error(self, error: Exception, context: Optional[str] = None):
        """
        记录错误

        Args:
            error: 异常对象
            context: 错误上下文
        """
        message = f"错误: {str(error)}"
        if context:
            message = f"上下文: {context} - {message}"
        self.error_logger.error(message, exc_info=True)

    def log_novel_creation(self, title: str, genre: str, success: bool):
        """
        记录小说创建

        Args:
            title: 小说标题
            genre: 小说类型
            success: 是否成功
        """
        status = "成功" if success else "失败"
        self.log_app(f"小说创建{status}: {title} ({genre})")
        self.log_user_action(f"创建小说", {"title": title, "genre": genre, "success": success})

    def log_chapter_creation(self, novel_title: str, chapter_num: int, success: bool):
        """
        记录章节创建

        Args:
            novel_title: 小说标题
            chapter_num: 章节号
            success: 是否成功
        """
        status = "成功" if success else "失败"
        self.log_app(f"章节创建{status}: {novel_title} 第{chapter_num}章")
        self.log_user_action(f"创建章节", {
            "novel_title": novel_title,
            "chapter_num": chapter_num,
            "success": success
        })

    def log_optimization(self, novel_title: str, chapter_num: int, success: bool):
        """
        记录章节优化

        Args:
            novel_title: 小说标题
            chapter_num: 章节号
            success: 是否成功
        """
        status = "成功" if success else "失败"
        self.log_app(f"章节优化{status}: {novel_title} 第{chapter_num}章")
        self.log_user_action(f"优化章节", {
            "novel_title": novel_title,
            "chapter_num": chapter_num,
            "success": success
        })

    def log_system_event(self, event: str, level: str = "INFO"):
        """
        记录系统事件

        Args:
            event: 事件描述
            level: 日志级别
        """
        self.log_app(f"系统事件: {event}", level.lower())

    def log_agent_activity(self, agent_name: str, activity: str, details: Optional[Dict[str, Any]] = None):
        """
        记录智能体活动

        Args:
            agent_name: 智能体名称
            activity: 活动描述
            details: 活动详情
        """
        message = f"[{agent_name}] {activity}"
        if details:
            message += f" - 详情: {details}"
        self.log_app(message)
        self.user_logger.info(f"智能体活动: {message}")

# 全局日志记录器实例
enhanced_logger = EnhancedLogger()