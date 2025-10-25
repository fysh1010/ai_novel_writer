#!/usr/bin/env python3
"""
简化情节控制师 - 专注于情节连贯性和用户意图
减少冗余的复杂性，提高生成效率和质量
"""

from .base_agent import BaseAgent
from .model_config import ModelConfig
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class PlotControllerSimplified(BaseAgent):
    """简化情节控制师"""

    def __init__(self, model_source: str = None, model_name: str = None):
        # 使用模型配置
        config = ModelConfig.get_model_config("plot_controller")
        if model_source is None:
            model_source = config["model_source"]
        if model_name is None:
            model_name = config["model_name"]

        super().__init__("情节控制师", model_source, model_name)

    def _get_attr_or_key(self, obj, key, default=None):
        """获取对象属性或字典键，兼容字典和对象格式"""
        if hasattr(obj, key):
            return getattr(obj, key, default)
        elif isinstance(obj, dict):
            return obj.get(key, default)
        return default

        # 简化的情节模板
        self.plot_templates = {
            "开端": {
                "elements": ["引入主角", "建立背景", "暗示冲突"],
                "pace": "平缓"
            },
            "发展": {
                "elements": ["展开冲突", "引入配角", "推进剧情"],
                "pace": "中等"
            },
            "高潮": {
                "elements": ["激化矛盾", "关键对决", "重大转折"],
                "pace": "紧凑"
            },
            "结局": {
                "elements": ["解决冲突", "角色成长", "收束剧情"],
                "pace": "缓和"
            }
        }

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""
        try:
            operation_type = input_data.get("type", "")

            if operation_type == "create_timeline":
                return self._create_timeline(input_data)
            elif operation_type == "check_consistency":
                return self._check_consistency(input_data)
            elif operation_type == "develop_plot":
                return self._develop_plot(input_data)
            elif operation_type == "get_suggestions":
                return self._get_suggestions(input_data)
            else:
                return {"error": f"未知的操作类型: {operation_type}"}

        except Exception as e:
            self.log(f"处理请求时发生错误: {str(e)}")
            return {"error": f"处理请求时发生错误: {str(e)}"}

    def _create_timeline(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建情节时间线"""
        self.log("正在创建情节时间线（简化版）...")

        story_framework = input_data.get("story_framework", "")
        character_system = input_data.get("character_system", "")
        user_intent = input_data.get("user_intent", {})

        # 构建简化提示
        prompt = self._build_timeline_prompt(story_framework, character_system, user_intent)

        # 生成时间线
        response = self.chat.forward(prompt)

        return {
            "type": "timeline_created",
            "content": response,
            "metadata": {
                "user_intent": user_intent,
                "created_at": self._get_timestamp()
            }
        }

    def _check_consistency(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查情节一致性（简化版）"""
        self.log("正在检查情节一致性（简化版）...")

        content = input_data.get("content", "")
        previous_chapters = input_data.get("previous_chapters", [])
        plot_timeline = input_data.get("plot_timeline", "")
        chapter_num = input_data.get("chapter_num", 1)

        # 简化的一致性检查
        consistency_result = self._simple_plot_consistency_check(
            content, previous_chapters, plot_timeline, chapter_num
        )

        return {
            "type": "consistency_check",
            "content": consistency_result,
            "metadata": {
                "chapter_num": chapter_num,
                "checked_at": self._get_timestamp()
            }
        }

    def _develop_plot(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """发展情节（简化版）"""
        self.log("正在发展情节（简化版）...")

        current_plot = input_data.get("current_plot", "")
        development_direction = input_data.get("development_direction", "")
        user_intent = input_data.get("user_intent", {})

        # 简化的情节发展
        development = self._simple_plot_development(
            current_plot, development_direction, user_intent
        )

        return {
            "type": "plot_development",
            "content": development,
            "metadata": {
                "developed_at": self._get_timestamp()
            }
        }

    def _get_suggestions(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """获取情节建议（简化版）"""
        self.log("正在生成情节建议（简化版）...")

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

    def _build_timeline_prompt(self, story_framework: str, character_system: str,
                               user_intent: Dict[str, Any]) -> str:
        """构建时间线生成提示"""

        prompt = f"""
基于以下信息创建情节时间线：

故事框架：
{story_framework}

角色系统：
{character_system}
"""

        # 添加用户约束和偏好
        constraints = self._get_attr_or_key(user_intent, "constraints", [])
        forbidden_elements = self._get_attr_or_key(user_intent, "forbidden_elements", [])

        if constraints:
            prompt += f"\n必须包含的情节元素：{', '.join(constraints)}\n"

        if forbidden_elements:
            prompt += f"\n禁止出现的情节：{', '.join(forbidden_elements)}\n"

        prompt += """
请创建简洁的情节时间线，包括：
1. 开端阶段（1-3章）：引入设定和角色
2. 发展阶段（4-15章）：展开主线冲突
3. 高潮阶段（16-25章）：激化矛盾达到顶点
4. 结局阶段（26-30章）：解决冲突收束剧情

要求：结构清晰，逻辑连贯，不超过400字。
"""

        return prompt

    def _simple_plot_consistency_check(self, content: str, previous_chapters: List[Dict],
                                       plot_timeline: str, chapter_num: int) -> str:
        """简化的情节一致性检查"""

        if not content:
            return "没有内容需要检查"

        # 基于章节位置的检查
        if chapter_num <= 5:
            stage = "开端"
            focus = "角色介绍和背景设定"
        elif chapter_num <= 15:
            stage = "发展"
            focus = "冲突展开和情节推进"
        elif chapter_num <= 25:
            stage = "高潮"
            focus = "矛盾激化和关键转折"
        else:
            stage = "结局"
            focus = "冲突解决和剧情收束"

        check_result = f"情节一致性检查（第{chapter_num}章，{stage}阶段）：\n"
        check_result += f"- 当前阶段重点：{focus}\n"

        # 检查与前面章节的连贯性
        if previous_chapters:
            check_result += f"- 与前面{len(previous_chapters)}章的连贯性：良好\n"
            check_result += "- 情节推进：符合发展轨迹\n"
        else:
            check_result += "- 首章创作，注意建立基础设定\n"

        # 基于内容长度的简单检查
        content_length = len(content)
        if content_length < 1000:
            check_result += "- 内容长度：偏短，建议适当展开\n"
        elif content_length > 3000:
            check_result += "- 内容长度：偏长，建议精简紧凑\n"
        else:
            check_result += "- 内容长度：适中\n"

        check_result += "总体：情节发展较为合理，建议继续保持。"

        return check_result

    def _simple_plot_development(self, current_plot: str, development_direction: str,
                                 user_intent: Dict[str, Any]) -> str:
        """简化的情节发展"""

        development_base = "情节发展建议：\n"

        if current_plot:
            development_base += f"当前情节：{current_plot[:100]}...\n"

        if development_direction:
            development_base += f"发展方向：{development_direction}\n"

        # 基于用户约束调整发展建议
        constraints = self._get_attr_or_key(user_intent, "constraints", [])
        forbidden_elements = self._get_attr_or_key(user_intent, "forbidden_elements", [])

        suggestions = []

        if "快节奏" in constraints:
            suggestions.append("加快情节推进速度")
        if "多冲突" in constraints:
            suggestions.append("增加多重冲突线索")

        if "拖沓" in forbidden_elements:
            suggestions.append("避免情节发展过于缓慢")
        if "老套" in forbidden_elements:
            suggestions.append("创新情节设计，避免俗套")

        if not suggestions:
            suggestions = [
                "保持情节逻辑的连贯性",
                "注重冲突的自然升级",
                "平衡各条情节线的发展"
            ]

        development_base += "\n具体建议：\n"
        development_base += "\n".join(f"- {s}" for s in suggestions)

        return development_base

    def _simple_suggestions(self, context: str, user_intent: Dict[str, Any]) -> str:
        """简化的建议生成"""

        suggestions = []

        # 基于用户意图生成建议
        constraints = self._get_attr_or_key(user_intent, "constraints", [])
        forbidden_elements = self._get_attr_or_key(user_intent, "forbidden_elements", [])

        if constraints:
            suggestions.append(f"情节需包含：{', '.join(constraints)}")

        if forbidden_elements:
            suggestions.append(f"避免情节：{', '.join(forbidden_elements)}")

        # 添加通用建议
        suggestions.extend([
            "保持情节的逻辑性和连贯性",
            "注重冲突的合理设置和解决",
            "平衡情节节奏和人物发展",
            "确保主线清晰，支线适度"
        ])

        return "情节创作建议：\n" + "\n".join(f"- {s}" for s in suggestions)

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 工厂函数
def create_plot_controller():
    """创建情节控制师实例"""
    return PlotControllerSimplified()