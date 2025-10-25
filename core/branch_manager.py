#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分支管理器 - 管理故事的不同分支和版本
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class BranchManager:
    """分支管理器类"""

    def __init__(self, branches_dir: str = "branches"):
        """
        初始化分支管理器

        Args:
            branches_dir: 分支存储目录
        """
        self.branches_dir = branches_dir
        self.ensure_branches_dir()

    def ensure_branches_dir(self):
        """确保分支目录存在"""
        if not os.path.exists(self.branches_dir):
            os.makedirs(self.branches_dir)

    def create_branch(self, project_data: Dict[str, Any], branch_name: str,
                     branch_description: str = "") -> str:
        """
        创建新分支

        Args:
            project_data: 项目数据
            branch_name: 分支名称
            branch_description: 分支描述

        Returns:
            str: 分支ID
        """
        branch_id = str(uuid.uuid4())

        branch_data = {
            "branch_id": branch_id,
            "branch_name": branch_name,
            "branch_description": branch_description,
            "project_id": project_data.get("project_id"),
            "base_project_data": project_data,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "is_active": True,
            "changes": []
        }

        # 保存分支
        self.save_branch(branch_data)

        return branch_id

    def save_branch(self, branch_data: Dict[str, Any]) -> bool:
        """
        保存分支

        Args:
            branch_data: 分支数据

        Returns:
            bool: 保存是否成功
        """
        try:
            branch_id = branch_data.get("branch_id")
            if not branch_id:
                return False

            branch_data["updated_at"] = datetime.now().isoformat()
            branch_file = os.path.join(self.branches_dir, f"{branch_id}.json")

            with open(branch_file, 'w', encoding='utf-8') as f:
                json.dump(branch_data, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            print(f"保存分支失败: {str(e)}")
            return False

    def load_branch(self, branch_id: str) -> Optional[Dict[str, Any]]:
        """
        加载分支

        Args:
            branch_id: 分支ID

        Returns:
            Dict[str, Any] or None: 分支数据
        """
        branch_file = os.path.join(self.branches_dir, f"{branch_id}.json")

        if not os.path.exists(branch_file):
            return None

        try:
            with open(branch_file, 'r', encoding='utf-8') as f:
                branch_data = json.load(f)
            return branch_data
        except Exception as e:
            print(f"加载分支失败: {str(e)}")
            return None

    def list_branches(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        列出分支

        Args:
            project_id: 项目ID（可选）

        Returns:
            List[Dict[str, Any]]: 分支列表
        """
        branches = []

        try:
            for filename in os.listdir(self.branches_dir):
                if filename.endswith('.json'):
                    branch_id = filename[:-5]
                    branch_data = self.load_branch(branch_id)
                    if branch_data:
                        # 如果指定了项目ID，只返回该项目的分支
                        if project_id and branch_data.get("project_id") != project_id:
                            continue

                        # 只返回基本信息
                        branches.append({
                            "branch_id": branch_data.get("branch_id"),
                            "branch_name": branch_data.get("branch_name"),
                            "branch_description": branch_data.get("branch_description"),
                            "project_id": branch_data.get("project_id"),
                            "created_at": branch_data.get("created_at"),
                            "updated_at": branch_data.get("updated_at"),
                            "is_active": branch_data.get("is_active", False),
                            "change_count": len(branch_data.get("changes", []))
                        })
        except Exception as e:
            print(f"列出分支失败: {str(e)}")

        # 按更新时间排序
        branches.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return branches

    def add_change(self, branch_id: str, change_type: str, change_description: str,
                   change_data: Dict[str, Any]) -> bool:
        """
        添加分支变更

        Args:
            branch_id: 分支ID
            change_type: 变更类型 (chapter_created, chapter_modified, chapter_deleted, etc.)
            change_description: 变更描述
            change_data: 变更数据

        Returns:
            bool: 添加是否成功
        """
        branch_data = self.load_branch(branch_id)
        if not branch_data:
            return False

        change = {
            "change_id": str(uuid.uuid4()),
            "change_type": change_type,
            "change_description": change_description,
            "change_data": change_data,
            "timestamp": datetime.now().isoformat()
        }

        branch_data["changes"].append(change)
        return self.save_branch(branch_data)

    def get_branch_changes(self, branch_id: str) -> List[Dict[str, Any]]:
        """
        获取分支变更历史

        Args:
            branch_id: 分支ID

        Returns:
            List[Dict[str, Any]]: 变更历史
        """
        branch_data = self.load_branch(branch_id)
        if not branch_data:
            return []

        return branch_data.get("changes", [])

    def merge_branch(self, source_branch_id: str, target_branch_id: str) -> bool:
        """
        合并分支

        Args:
            source_branch_id: 源分支ID
            target_branch_id: 目标分支ID

        Returns:
            bool: 合并是否成功
        """
        source_branch = self.load_branch(source_branch_id)
        target_branch = self.load_branch(target_branch_id)

        if not source_branch or not target_branch:
            return False

        # 记录合并操作
        merge_change = {
            "change_id": str(uuid.uuid4()),
            "change_type": "branch_merged",
            "change_description": f"合并分支 '{source_branch['branch_name']}'",
            "change_data": {
                "source_branch_id": source_branch_id,
                "source_branch_name": source_branch["branch_name"],
                "merged_changes_count": len(source_branch.get("changes", []))
            },
            "timestamp": datetime.now().isoformat()
        }

        target_branch["changes"].append(merge_change)
        return self.save_branch(target_branch)

    def delete_branch(self, branch_id: str) -> bool:
        """
        删除分支

        Args:
            branch_id: 分支ID

        Returns:
            bool: 删除是否成功
        """
        try:
            branch_file = os.path.join(self.branches_dir, f"{branch_id}.json")

            if os.path.exists(branch_file):
                os.remove(branch_file)
                return True
            else:
                return False

        except Exception as e:
            print(f"删除分支失败: {str(e)}")
            return False

    def compare_branches(self, branch1_id: str, branch2_id: str) -> Dict[str, Any]:
        """
        比较两个分支

        Args:
            branch1_id: 分支1 ID
            branch2_id: 分支2 ID

        Returns:
            Dict[str, Any]: 比较结果
        """
        branch1 = self.load_branch(branch1_id)
        branch2 = self.load_branch(branch2_id)

        if not branch1 or not branch2:
            return {"error": "分支不存在"}

        project1 = branch1.get("base_project_data", {})
        project2 = branch2.get("base_project_data", {})

        # 比较章节
        chapters1 = {ch.get("chapter_num"): ch for ch in project1.get("chapters", [])}
        chapters2 = {ch.get("chapter_num"): ch for ch in project2.get("chapters", [])}

        all_chapter_nums = set(chapters1.keys()) | set(chapters2.keys())

        differences = {
            "branch1_info": {
                "branch_id": branch1_id,
                "branch_name": branch1.get("branch_name"),
                "updated_at": branch1.get("updated_at")
            },
            "branch2_info": {
                "branch_id": branch2_id,
                "branch_name": branch2.get("branch_name"),
                "updated_at": branch2.get("updated_at")
            },
            "chapter_differences": [],
            "summary": {}
        }

        for chapter_num in sorted(all_chapter_nums):
            ch1 = chapters1.get(chapter_num)
            ch2 = chapters2.get(chapter_num)

            if ch1 and ch2:
                # 比较内容
                content1 = ch1.get("content", "")
                content2 = ch2.get("content", "")

                if content1 != content2:
                    differences["chapter_differences"].append({
                        "chapter_num": chapter_num,
                        "status": "modified",
                        "branch1_title": ch1.get("title"),
                        "branch2_title": ch2.get("title"),
                        "word_count_diff": len(content2.split()) - len(content1.split())
                    })
            elif ch1 and not ch2:
                differences["chapter_differences"].append({
                    "chapter_num": chapter_num,
                    "status": "deleted_in_branch2",
                    "branch1_title": ch1.get("title"),
                    "branch2_title": None
                })
            elif not ch1 and ch2:
                differences["chapter_differences"].append({
                    "chapter_num": chapter_num,
                    "status": "added_in_branch2",
                    "branch1_title": None,
                    "branch2_title": ch2.get("title")
                })

        # 生成摘要
        differences["summary"] = {
            "total_differences": len(differences["chapter_differences"]),
            "added": len([d for d in differences["chapter_differences"] if d["status"] == "added_in_branch2"]),
            "deleted": len([d for d in differences["chapter_differences"] if d["status"] == "deleted_in_branch2"]),
            "modified": len([d for d in differences["chapter_differences"] if d["status"] == "modified"])
        }

        return differences

    def create_revision_branch(self, project_id: str, chapter_num: int, feedback: str, project_data: Dict[str, Any] = None) -> str:
        """
        创建修订分支

        Args:
            project_id: 项目ID
            chapter_num: 章节号
            feedback: 用户反馈
            project_data: 项目数据（可选，如果没有则创建空数据）

        Returns:
            str: 分支ID
        """
        # 生成分支名称
        branch_name = f"修订分支_第{chapter_num}章"
        branch_description = f"针对第{chapter_num}章的用户反馈修订: {feedback[:50]}..."
        
        # 创建一个基本的分支数据结构
        # 如果提供了完整的项目数据就使用它，否则创建一个基本结构
        if project_data is not None:
            branch_data = project_data.copy()
        else:
            branch_data = {
                "project_id": project_id,
                "chapters": [],
                "feedback": [],
                "title": f"修订项目_{project_id}_{chapter_num}",
                "genre": "修订类型",
                "current_chapter": chapter_num
            }
        
        # 添加修订相关信息
        branch_data["revision_info"] = {
            "chapter_num": chapter_num,
            "feedback": feedback,
            "revision_type": "user_feedback"
        }
        
        return self.create_branch(branch_data, branch_name, branch_description)

    def display_branch_tree(self, project_id: str):
        """
        显示分支树
        
        Args:
            project_id: 项目ID
        """
        branches = self.list_branches(project_id)
        
        if not branches:
            print("📂 暂无分支")
            return
        
        print("🌳 分支树:")
        for branch in branches:
            status_icon = "✅" if branch.get("status") == "merged" else "🔄"
            print(f"  {status_icon} {branch.get('branch_name', 'Unknown')} ({branch.get('branch_description', '')})")
            print(f"     创建时间: {branch.get('created_at', '')}")
            print(f"     更新时间: {branch.get('updated_at', '')}")
            print(f"     变更数: {branch.get('change_count', 0)}")

    def get_branch_statistics(self, project_id: str) -> Dict[str, Any]:
        """
        获取分支统计信息
        
        Args:
            project_id: 项目ID
            
        Returns:
            Dict[str, Any]: 统计信息
        """
        branches = self.list_branches(project_id)
        
        if not branches:
            return {
                "total_branches": 0,
                "active_branches": 0,
                "merged_branches": 0,
                "average_branch_length": 0
            }
        
        total_branches = len(branches)
        active_branches = len([b for b in branches if b.get("is_active", False)])
        merged_branches = len([b for b in branches if not b.get("is_active", True)])
        
        # 计算平均分支长度（基于变更数）
        total_changes = sum(b.get("change_count", 0) for b in branches)
        average_branch_length = total_changes // total_branches if total_branches > 0 else 0
        
        return {
            "total_branches": total_branches,
            "active_branches": active_branches,
            "merged_branches": merged_branches,
            "average_branch_length": average_branch_length
        }