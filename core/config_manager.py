#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器 - 管理应用配置
"""

import json
import os
import yaml
from typing import Dict, Any, Optional

class ConfigManager:
    """配置管理器类"""

    def __init__(self, config_file: str = "config.yaml"):
        """
        初始化配置管理器

        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        加载配置

        Returns:
            Dict[str, Any]: 配置数据
        """
        default_config = {
            "model": {
                "source": "sensenova",
                "name": "DeepSeek-V3-1",
                "temperature": 0.7,
                "max_tokens": 4000
            },
            "novel": {
                "default_genre": "都市",
                "chapter_length": 2500,
                "auto_save": True
            },
            "ui": {
                "show_progress": True,
                "typewriter_effect": True,
                "language": "zh-CN"
            },
            "paths": {
                "projects_dir": "projects",
                "logs_dir": "logs"
            },
            "output": {
                "save_txt_files": True,
                "save_json_files": True,
                "create_folders_auto": True,
                "typewriter_effect": True
            }
        }

        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    if self.config_file.endswith('.yaml') or self.config_file.endswith('.yml'):
                        loaded_config = yaml.safe_load(f)
                    else:
                        loaded_config = json.load(f)
                    # 合并默认配置和加载的配置
                    config = {**default_config, **loaded_config}
                    return config
            except Exception as e:
                print(f"加载配置文件失败，使用默认配置: {str(e)}")

        return default_config

    def save_config(self) -> bool:
        """
        保存配置

        Returns:
            bool: 保存是否成功
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {str(e)}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值

        Returns:
            Any: 配置值
        """
        keys = key.split('.')
        value = self.config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> bool:
        """
        设置配置值

        Args:
            key: 配置键，支持点号分隔的嵌套键
            value: 配置值

        Returns:
            bool: 设置是否成功
        """
        keys = key.split('.')
        config = self.config

        try:
            # 导航到最后一级的父级
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]

            # 设置值
            config[keys[-1]] = value
            return self.save_config()
        except Exception as e:
            print(f"设置配置失败: {str(e)}")
            return False

    def get_model_config(self) -> Dict[str, Any]:
        """
        获取模型配置

        Returns:
            Dict[str, Any]: 模型配置
        """
        return self.get("model", {})

    def get_novel_config(self) -> Dict[str, Any]:
        """
        获取小说配置

        Returns:
            Dict[str, Any]: 小说配置
        """
        return self.get("novel", {})

    def get_ui_config(self) -> Dict[str, Any]:
        """
        获取UI配置

        Returns:
            Dict[str, Any]: UI配置
        """
        return self.get("ui", {})

# 全局配置管理器实例
config_manager = ConfigManager()