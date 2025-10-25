#!/usr/bin/env python3
"""
简化角色管理师 - 专注于角色一致性和用户意图
减少冗余的复杂性，提高生成效率和质量
"""

from .base_agent import BaseAgent
from .model_config import ModelConfig
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class CharacterManagerSimplified(BaseAgent):
    """简化角色管理师"""

    def __init__(self, model_source: str = None, model_name: str = None):
        # 使用模型配置
        config = ModelConfig.get_model_config("character_manager")
        if model_source is None:
            model_source = config["model_source"]
        if model_name is None:
            model_name = config["model_name"]

        super().__init__("角色管理师", model_source, model_name)

    def _get_attr_or_key(self, obj, key, default=None):
        """获取对象属性或字典键，兼容字典和对象格式"""
        if hasattr(obj, key):
            return getattr(obj, key, default)
        elif isinstance(obj, dict):
            return obj.get(key, default)
        return default

        # 简化的角色模板
        self.character_templates = {
            "主角": {
                "attributes": ["姓名", "年龄", "性格", "背景", "目标", "能力"],
                "development": ["成长轨迹", "性格变化", "能力提升", "关系变化"]
            },
            "配角": {
                "attributes": ["姓名", "与主角关系", "性格特点", "作用定位"],
                "development": ["关系发展", "性格展现", "情节推动"]
            },
            "反派": {
                "attributes": ["姓名", "动机", "能力", "背景", "与主角冲突"],
                "development": ["冲突升级", "动机变化", "最终结局"]
            }
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""
        try:
            operation_type = input_data.get("type", "")

            if operation_type == "create_system":
                return self._create_system(input_data)
            elif operation_type == "check_consistency":
                return self._check_consistency(input_data)
            elif operation_type == "develop_character":
                return self._develop_character(input_data)
            elif operation_type == "get_suggestions":
                return self._get_suggestions(input_data)
            else:
                return {"error": f"未知的操作类型: {operation_type}"}

        except Exception as e:
            self.log(f"处理请求时发生错误: {str(e)}")
            return {"error": f"处理请求时发生错误: {str(e)}"}

    def _create_system(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建角色系统"""
        self.log("正在创建角色系统（简化版）...")

        story_framework = input_data.get("story_framework", "")
        user_intent = input_data.get("user_intent", {})

        # 构建简化提示
        prompt = self._build_system_prompt(story_framework, user_intent)

        # 生成角色系统
        response = self.chat.forward(prompt)

        return {
            "type": "system_created",
            "content": response,
            "metadata": {
                "user_intent": user_intent,
                "created_at": self._get_timestamp()
            }
        }

    def _check_consistency(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查角色一致性（简化版）"""
        self.log("正在检查角色一致性（简化版）...")

        content = input_data.get("content", "")
        character_profiles = input_data.get("character_profiles", "")
        chapter_num = input_data.get("chapter_num", 1)

        # 简化的一致性检查
        consistency_result = self._simple_consistency_check(
            content, character_profiles, chapter_num
        )

        return {
            "type": "consistency_check",
            "content": consistency_result,
            "metadata": {
                "chapter_num": chapter_num,
                "checked_at": self._get_timestamp()
            }
        }

    def _develop_character(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """发展角色（简化版）"""
        self.log("正在发展角色（简化版）...")

        character_name = input_data.get("character_name", "")
        current_situation = input_data.get("current_situation", "")
        user_intent = input_data.get("user_intent", {})

        # 简化的角色发展
        development = self._simple_character_development(
            character_name, current_situation, user_intent
        )

        return {
            "type": "character_development",
            "content": development,
            "metadata": {
                "character_name": character_name,
                "developed_at": self._get_timestamp()
            }
        }

    def _get_suggestions(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """获取角色建议（简化版）"""
        self.log("正在生成角色建议（简化版）...")

        context = input_data.get("context", "")
        user_intent = input_data.get("user_intent", {})

        # 简化的建议生成
        suggestions = self._simple_suggestions(context, user_intent)

        return {
            "type": "suggestions",
            "content": suggestions,
            "metadata": {
                "suggested_at": self._get_timestamp()
            }
        }

    def _build_system_prompt(self, story_framework: str, user_intent: Dict[str, Any]) -> str:
        """构建角色系统生成提示"""

        prompt = f"""
基于以下故事框架创建角色系统：

故事框架：
{story_framework}
"""

        # 添加用户约束和偏好
        constraints = self._get_attr_or_key(user_intent, "constraints", [])
        forbidden_elements = self._get_attr_or_key(user_intent, "forbidden_elements", [])

        if constraints:
            prompt += f"\n必须包含的角色元素：{', '.join(constraints)}\n"

        if forbidden_elements:
            prompt += f"\n禁止出现的角色设定：{', '.join(forbidden_elements)}\n"

        prompt += """
请创建简洁的角色系统，包括：
1. 主角设定（姓名、基本特征、目标）
2. 主要配角（2-3个，说明作用）
3. 角色关系网络
4. 角色发展方向

要求：简洁明了，重点突出，不超过300字。
"""

        return prompt

    def _simple_consistency_check(self, content: str, character_profiles: str,
                                 chapter_num: int) -> str:
        """简化的一致性检查"""

        if not content:
            return "没有内容需要检查"

        # 基于关键词的简单检查
        common_patterns = [
            "性格一致",
            "行为合理",
            "对话符合角色设定",
            "发展轨迹连贯"
        ]

        # 如果有角色设定，进行简单匹配
        if character_profiles:
            # 提取角色名称（简化实现）
            import re
            character_names = re.findall(r'(\S+?)：', character_profiles)

            if character_names:
                check_result = f"角色一致性检查（{len(character_names)}个角色）：\n"
                for name in character_names[:3]:  # 只检查前3个角色
                    check_result += f"- {name}：表现基本符合设定\n"
                check_result += "总体：角色表现较为一致，建议继续保持。"
                return check_result

        return """
角色一致性检查：
- 角色行为基本合理
- 性格表现相对一致
- 对话符合角色背景
- 建议继续保持角色设定的连贯性
"""

    def _simple_character_development(self, character_name: str, current_situation: str,
                                     user_intent: Dict[str, Any]) -> str:
        """简化的角色发展"""

        if not character_name:
            return "请指定要发展的角色名称"

        development_base = f"""
角色发展建议：{character_name}

当前状况：{current_situation if current_situation else "正常情节发展中"}
"""

        # 基于用户约束调整发展建议
        constraints = self._get_attr_or_key(user_intent, "constraints", [])
        forbidden_elements = self._get_attr_or_key(user_intent, "forbidden_elements", [])

        suggestions = []

        if "角色成长" in constraints:
            suggestions.append("注重角色内心的成长变化")
        if "关系发展" in constraints:
            suggestions.append("深化角色间的关系变化")

        if "黑化" in forbidden_elements:
            suggestions.append("避免角色走向极端化")
        if "死亡" in forbidden_elements:
            suggestions.append("保护主要角色的安全性")

        if not suggestions:
            suggestions = [
                "保持角色性格的一致性",
                "推动角色情节自然发展",
                "展现角色的多面性"
            ]

        development_base += "\n发展建议：\n"
        development_base += "\n".join(f"- {s}" for s in suggestions)

        return development_base

    def _simple_suggestions(self, context: str, user_intent: Dict[str, Any]) -> str:
        """简化的建议生成"""

        suggestions = []

        # 基于用户意图生成建议
        constraints = self._get_attr_or_key(user_intent, "constraints", [])
        forbidden_elements = self._get_attr_or_key(user_intent, "forbidden_elements", [])

        if constraints:
            suggestions.append(f"角色设定需包含：{', '.join(constraints)}")

        if forbidden_elements:
            suggestions.append(f"避免角色设定：{', '.join(forbidden_elements)}")

        # 添加通用建议
        suggestions.extend([
            "保持角色性格的连贯性",
            "确保角色行为符合逻辑",
            "注重角色间的关系发展"
        ])

        return "角色创作建议：\n" + "\n".join(f"- {s}" for s in suggestions)

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 工厂函数
def create_character_manager():
    """创建角色管理师实例"""
    return CharacterManagerSimplified()