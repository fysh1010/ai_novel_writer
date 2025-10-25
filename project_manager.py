#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目管理器 - 负责小说项目的创建、加载、保存和管理
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class ProjectManager:
    """项目管理器类"""

    def __init__(self, projects_dir: str = "projects"):
        """
        初始化项目管理器

        Args:
            projects_dir: 项目存储目录
        """
        self.projects_dir = projects_dir
        self.ensure_projects_dir()

    def ensure_projects_dir(self):
        """确保项目目录存在"""
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)

    def create_project(self, project_data: Dict[str, Any]) -> str:
        """
        创建新项目

        Args:
            project_data: 项目数据

        Returns:
            str: 项目ID
        """
        project_id = str(uuid.uuid4())

        # 添加项目元数据
        project_data["project_id"] = project_id
        project_data["created_at"] = datetime.now().isoformat()
        project_data["updated_at"] = datetime.now().isoformat()
        project_data["chapters"] = project_data.get("chapters", [])

        # 保存项目
        self.save_project(project_data)

        return project_id

    def load_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        加载项目

        Args:
            project_id: 项目ID

        Returns:
            Dict[str, Any] or None: 项目数据
        """
        # 首先尝试新格式：直接的 .json 文件
        project_file = os.path.join(self.projects_dir, f"{project_id}.json")
        if os.path.exists(project_file):
            try:
                with open(project_file, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                return project_data
            except Exception as e:
                print(f"加载项目失败: {str(e)}")
                return None

        # 然后尝试旧格式：项目文件夹内的 project.json
        project_folder = os.path.join(self.projects_dir, project_id)
        if os.path.isdir(project_folder):
            project_json_path = os.path.join(project_folder, "project.json")
            if os.path.exists(project_json_path):
                try:
                    with open(project_json_path, 'r', encoding='utf-8') as f:
                        project_data = json.load(f)

                    # 加载其他相关文件
                    chapters_json_path = os.path.join(project_folder, "chapters.json")
                    if os.path.exists(chapters_json_path):
                        try:
                            with open(chapters_json_path, 'r', encoding='utf-8') as f:
                                chapters_data = json.load(f)
                            project_data["chapters"] = chapters_data.get("chapters", [])
                        except Exception as e:
                            print(f"加载章节数据失败: {str(e)}")
                            project_data["chapters"] = []

                    return project_data
                except Exception as e:
                    print(f"加载项目失败: {str(e)}")
                    return None

        return None

    def save_project(self, project_data: Dict[str, Any]) -> bool:
        """
        保存项目

        Args:
            project_data: 项目数据

        Returns:
            bool: 保存是否成功
        """
        try:
            project_id = project_data.get("project_id")
            if not project_id:
                project_id = str(uuid.uuid4())
                project_data["project_id"] = project_id

            # 更新时间戳
            project_data["updated_at"] = datetime.now().isoformat()

            project_file = os.path.join(self.projects_dir, f"{project_id}.json")

            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"保存项目失败: {str(e)}")
            return False

    def save_chapter(self, project_data: Dict[str, Any], chapter_num: int, chapter_data: Dict[str, Any]) -> bool:
        """
        保存章节

        Args:
            project_data: 项目数据
            chapter_num: 章节号
            chapter_data: 章节数据

        Returns:
            bool: 保存是否成功
        """
        try:
            # 确保chapters列表存在
            if "chapters" not in project_data:
                project_data["chapters"] = []

            chapters = project_data["chapters"]

            # 查找是否已存在该章节
            existing_index = -1
            for i, ch in enumerate(chapters):
                if ch.get("chapter_num") == chapter_num:
                    existing_index = i
                    break

            # 更新或添加章节
            chapter_data["chapter_num"] = chapter_num
            chapter_data["updated_at"] = datetime.now().isoformat()

            if existing_index >= 0:
                chapters[existing_index] = chapter_data
            else:
                chapters.append(chapter_data)

            # 按章节号排序
            chapters.sort(key=lambda x: x.get("chapter_num", 0))

            # 保存整个项目
            saved = self.save_project(project_data)

            # 章节与整书 TXT 导出（受配置控制）
            if saved:
                try:
                    self._export_txt_files(project_data, chapter_num)
                except Exception as e:
                    # TXT 导出失败不应影响主流程保存
                    print(f"导出 TXT 失败: {str(e)}")

            return saved

        except Exception as e:
            print(f"保存章节失败: {str(e)}")
            return False

    def list_projects(self) -> List[Dict[str, Any]]:
        """
        列出所有项目

        Returns:
            List[Dict[str, Any]]: 项目列表
        """
        projects = []

        try:
            # 首先检查项目文件夹内的 project.json 文件（兼容旧格式）
            for item in os.listdir(self.projects_dir):
                item_path = os.path.join(self.projects_dir, item)

                if os.path.isdir(item_path):
                    # 旧格式：项目文件夹，内有 project.json
                    project_json_path = os.path.join(item_path, "project.json")
                    if os.path.exists(project_json_path):
                        try:
                            with open(project_json_path, 'r', encoding='utf-8') as f:
                                project_data = json.load(f)
                            if project_data:
                                # 只返回基本信息
                                projects.append({
                                    "project_id": project_data.get("project_id", item),
                                    "title": project_data.get("title", item),
                                    "genre": project_data.get("genre", "未知类型"),
                                    "created_at": project_data.get("created_at", ""),
                                    "updated_at": project_data.get("updated_at", ""),
                                    "chapter_count": len(project_data.get("chapters", []))
                                })
                        except Exception as e:
                            print(f"加载项目 {item} 失败: {str(e)}")
                            continue

                elif item.endswith('.json'):

                    # 新格式：直接的 .json 文件

                    project_id = item[:-5]  # 移除 .json 后缀

                    project_data = self.load_project(project_id)

                    if project_data:

                        # 只返回基本信息

                        projects.append({

                            "project_id": project_data.get("project_id"),

                            "title": project_data.get("title", "未命名项目"),

                            "genre": project_data.get("genre", "未知类型"),

                            "created_at": project_data.get("created_at"),

                            "updated_at": project_data.get("updated_at"),

                            "chapter_count": len(project_data.get("chapters", [])),

                            "current_chapter": project_data.get("current_chapter", 0),

                            "target_length": project_data.get("target_length", 50)

                        })
        except Exception as e:
            print(f"列出项目失败: {str(e)}")

        # 按更新时间排序
        projects.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return projects

    def delete_project(self, project_id: str) -> bool:
        """
        删除项目

        Args:
            project_id: 项目ID

        Returns:
            bool: 删除是否成功
        """
        try:
            project_file = os.path.join(self.projects_dir, f"{project_id}.json")

            if os.path.exists(project_file):
                os.remove(project_file)
                return True
            else:
                return False

        except Exception as e:
            print(f"删除项目失败: {str(e)}")
            return False

    def get_project_stats(self, project_id: str) -> Optional[Dict[str, Any]]:
        """
        获取项目统计信息

        Args:
            project_id: 项目ID

        Returns:
            Dict[str, Any] or None: 统计信息
        """
        project_data = self.load_project(project_id)
        if not project_data:
            return None

        chapters = project_data.get("chapters", [])
        total_words = sum(len(ch.get("content", "")) for ch in chapters)

        return {
            "project_id": project_id,
            "title": project_data.get("title", "未命名项目"),
            "chapter_count": len(chapters),
            "total_words": total_words,
            "created_at": project_data.get("created_at"),
            "updated_at": project_data.get("updated_at"),
            "last_chapter": max(chapters, key=lambda x: x.get("chapter_num", 0)) if chapters else None
        }

    # ---------------------
    # TXT 导出相关私有方法
    # ---------------------
    def _export_txt_files(self, project_data: Dict[str, Any], last_chapter_num: int) -> None:
        """根据配置将章节与整书导出为 TXT 文件。

        说明：
        - 若 config.output.save_txt_files 为 true，则导出
        - 目录结构：projects/<书名>/txt/ 以及 projects/<书名>/<书名>.txt
        - 在新格式（projects/<project_id>.json）下，仍创建以书名命名的文件夹来放置可读文本
        """

        try:
            from core.config_manager import config_manager  # 延迟导入以避免潜在循环依赖
        except Exception:
            # 若配置加载异常，默认不导出
            return

        output_cfg = config_manager.config.get("output", {})
        save_txt = output_cfg.get("save_txt_files", False)
        auto_dirs = output_cfg.get("create_folders_auto", True)

        if not save_txt:
            return

        title = project_data.get("title") or project_data.get("project_id", "untitled")
        safe_title = self._sanitize_filename(title)

        # 目标目录
        base_dir = os.path.join(self.projects_dir, safe_title)
        txt_dir = os.path.join(base_dir, "txt")

        if auto_dirs:
            os.makedirs(txt_dir, exist_ok=True)
        else:
            if not (os.path.isdir(base_dir) and os.path.isdir(txt_dir)):
                return

        # 单章导出
        chapters = project_data.get("chapters", [])
        # 找到本次章节
        chapter = None
        for ch in chapters:
            if ch.get("chapter_num") == last_chapter_num:
                chapter = ch
                break

        if chapter is not None:
            # 🔧 修复：先删除该章节号的所有旧TXT文件（避免标题变更导致文件重复）
            chapter_idx = chapter.get("chapter_num", 0)
            chapter_prefix = f"{chapter_idx:02d}."
            
            # 删除所有以该章节号开头的txt文件
            if os.path.exists(txt_dir):
                for filename in os.listdir(txt_dir):
                    if filename.startswith(chapter_prefix) and filename.endswith('.txt'):
                        old_file_path = os.path.join(txt_dir, filename)
                        try:
                            os.remove(old_file_path)
                            print(f"🗑️  删除旧文件: {filename}")
                        except Exception as e:
                            print(f"⚠️  删除旧文件失败: {filename}, {e}")
            
            # 生成新文件
            chapter_title = chapter.get("title") or f"第{chapter.get('chapter_num', 0)}章"
            safe_chapter_title = self._sanitize_filename(chapter_title)
            chapter_filename = f"{chapter_idx:02d}.{safe_chapter_title}.txt"
            chapter_path = os.path.join(txt_dir, chapter_filename)

            content = chapter.get("content", "")
            self._write_text_file(chapter_path, content)
            print(f"💾 保存新文件: {chapter_filename}")

        # 整书导出（将所有章节按章节号拼接）
        if chapters:
            chapters_sorted = sorted(chapters, key=lambda x: x.get("chapter_num", 0))
            lines: List[str] = []
            for ch in chapters_sorted:
                ch_title = ch.get("title") or f"第{ch.get('chapter_num', 0)}章"
                lines.append(ch_title)
                lines.append("")
                lines.append(ch.get("content", ""))
                lines.append("\n" + "-" * 40 + "\n")

            full_text = "\n".join(lines).rstrip() + "\n"
            full_path = os.path.join(base_dir, f"{safe_title}.txt")
            self._write_text_file(full_path, full_text)

    def _sanitize_filename(self, name: str) -> str:
        """将任意字符串转为安全的文件名。"""
        if not name:
            return "untitled"
        invalid = '<>:"/\\|?*\n\r\t'
        safe = ''.join(c for c in name if c not in invalid)
        return safe.strip() or "untitled"

    def _write_text_file(self, path: str, content: str) -> None:
        """以 UTF-8 写文本文件。"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content or "")