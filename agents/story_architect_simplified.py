#!/usr/bin/env python3
"""
简化故事架构师 - 专注于用户意图和核心创作
减少冗余的复杂性，提高生成效率和质量
"""

from .base_agent import BaseAgent
from .model_config import ModelConfig
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class StoryArchitectSimplified(BaseAgent):
    """简化故事架构师"""

    def __init__(self, model_source: str = None, model_name: str = None):
        # 使用模型配置
        config = ModelConfig.get_model_config("story_architect")
        if model_source is None:
            model_source = config["model_source"]
        if model_name is None:
            model_name = config["model_name"]

        super().__init__("故事架构师", model_source, model_name)
        
        # 简化的核心知识库
        self.core_knowledge = {
            "玄幻": {
                "elements": ["修炼体系", "境界划分", "法宝神器"],
                "conflicts": ["修炼竞争", "宗门恩怨"],
                "satisfaction": ["境界突破", "实力碾压"]
            },
            "都市": {
                "elements": ["现代生活", "商业竞争", "人际关系"],
                "conflicts": ["商业竞争", "感情纠葛"],
                "satisfaction": ["事业成功", "感情圆满"]
            },
            "历史": {
                "elements": ["历史背景", "政治斗争", "军事战争"],
                "conflicts": ["政治斗争", "军事冲突"],
                "satisfaction": ["政治成功", "军事胜利"]
            },
            "科幻": {
                "elements": ["科技设定", "未来世界", "外星文明"],
                "conflicts": ["科技竞争", "星际战争"],
                "satisfaction": ["科技突破", "文明胜利"]
            }
        }

    def _get_attr_or_key(self, obj, key, default=None):
        """获取对象属性或字典键，兼容字典和对象格式"""
        if hasattr(obj, key):
            return getattr(obj, key, default)
        elif isinstance(obj, dict):
            return obj.get(key, default)
        return default

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""
        try:
            operation_type = input_data.get("type", "")

            if operation_type == "create_framework":
                return self._create_framework(input_data)
            elif operation_type == "analyze_rhythm":
                return self._analyze_rhythm(input_data)
            elif operation_type == "design_conflict":
                return self._design_conflict(input_data)
            elif operation_type == "get_suggestions":
                return self._get_suggestions(input_data)
            else:
                return {"error": f"未知的操作类型: {operation_type}"}

        except Exception as e:
            self.log(f"处理请求时发生错误: {str(e)}")
            return {"error": f"处理请求时发生错误: {str(e)}"}

    def _create_framework(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建故事框架"""
        self.log("正在创建故事框架（简化版）...")

        # 获取用户意图
        user_intent = input_data.get("user_intent", {})
        title = input_data.get("title", "未命名小说")
        genre = input_data.get("genre", "其他")
        custom_plot = input_data.get("custom_plot", "")

        # 获取该类型的核心知识
        genre_knowledge = self.core_knowledge.get(genre, {})

        # 构建简化提示
        prompt = self._build_framework_prompt(title, genre, custom_plot, user_intent, genre_knowledge)

        # 生成框架
        response = self.chat.forward(prompt)

        return {
            "type": "framework_created",
            "content": response,
            "metadata": {
                "genre": genre,
                "user_intent": user_intent,
                "created_at": self._get_timestamp()
            }
        }

    def _analyze_rhythm(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析节奏（简化版）"""
        self.log("正在分析节奏（简化版）...")

        content = input_data.get("content", "")
        previous_chapters = input_data.get("previous_chapters", [])
        rhythm = input_data.get("rhythm", "3起2落1翻转")

        if not content and not previous_chapters:
            return {
                "type": "rhythm_analysis",
                "content": "保持当前的叙事节奏，确保情节自然发展"
            }

        # 简化的节奏分析
        analysis = self._simple_rhythm_analysis(content, previous_chapters, rhythm)

        return {
            "type": "rhythm_analysis",
            "content": analysis,
            "metadata": {
                "rhythm_pattern": rhythm,
                "analyzed_at": self._get_timestamp()
            }
        }

    def _design_conflict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """设计冲突（简化版）"""
        self.log("正在设计冲突（简化版）...")

        story_context = input_data.get("story_context", "")
        conflict_type = input_data.get("conflict_type", "个人冲突")
        user_intent = input_data.get("user_intent", {})
        chapter_num = input_data.get("chapter_num", 1)

        # 简化的冲突设计
        conflict_design = self._simple_conflict_design(
            story_context, conflict_type, user_intent, chapter_num
        )

        return {
            "type": "conflict_design",
            "content": conflict_design,
            "metadata": {
                "conflict_type": conflict_type,
                "chapter_num": chapter_num,
                "designed_at": self._get_timestamp()
            }
        }

    def _get_suggestions(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """获取建议（简化版）"""
        self.log("正在生成建议（简化版）...")

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

    def _build_framework_prompt(self, title: str, genre: str, custom_plot: str,
                               user_intent: Dict[str, Any], genre_knowledge: Dict[str, Any]) -> str:
        """构建框架生成提示"""

        # 获取核心要素
        elements = genre_knowledge.get("elements", [])
        conflicts = genre_knowledge.get("conflicts", [])
        satisfaction = genre_knowledge.get("satisfaction", [])

        prompt = f"""
请为小说《{title}》创建故事框架。

类型：{genre}
核心要素：{', '.join(elements)}
冲突类型：{', '.join(conflicts)}
爽点设计：{', '.join(satisfaction)}
"""

        if custom_plot:
            prompt += f"\n用户自定义剧情：{custom_plot}\n"

        # 添加用户约束和偏好 - 兼容字典和对象格式
        constraints = self._get_attr_or_key(user_intent, "constraints", [])
        forbidden_elements = self._get_attr_or_key(user_intent, "forbidden_elements", [])

        if constraints:
            prompt += f"\n必须包含的元素：{', '.join(constraints)}\n"

        if forbidden_elements:
            prompt += f"\n禁止出现的元素：{', '.join(forbidden_elements)}\n"

        prompt += """
请创建一个简洁的故事框架，包括：
1. 核心设定（1-2句话）
2. 主角背景（1-2句话）
3. 主要冲突（1-2句话）
4. 发展方向（1-2句话）

要求：简洁明了，不超过200字。
"""

        return prompt

    def _simple_rhythm_analysis(self, content: str, previous_chapters: List[Dict],
                               rhythm: str) -> str:
        """简化的节奏分析"""
        if not content and not previous_chapters:
            return "保持自然的叙事节奏，确保情节流畅发展"

        # 基于内容长度的简单分析
        if content:
            content_length = len(content)
            if content_length < 1000:
                return "当前章节较短，建议适度展开情节，增加细节描写"
            elif content_length > 3000:
                return "当前章节较长，建议精简部分内容，保持节奏紧凑"
            else:
                return "章节长度适中，节奏控制良好"

        # 基于章节数量的简单分析
        if previous_chapters:
            chapter_count = len(previous_chapters)
            if chapter_count < 5:
                return "故事初期，建议循序渐进，逐步展开世界观"
            elif chapter_count < 20:
                return "故事发展期，建议保持情节推进，适当增加冲突"
            else:
                return "故事后期，建议逐步收束情节，准备高潮"

        return "保持当前叙事节奏，确保情节自然发展"

    def _simple_conflict_design(self, story_context: str, conflict_type: str,
                               user_intent: Dict[str, Any], chapter_num: int) -> str:
        """简化的冲突设计"""

        # 基于章节号设计冲突强度
        if chapter_num <= 3:
            intensity = "轻微"
            suggestion = "引入小规模冲突，建立基本矛盾"
        elif chapter_num <= 10:
            intensity = "中等"
            suggestion = "升级冲突，增加情节张力"
        elif chapter_num <= 20:
            intensity = "激烈"
            suggestion = "设计关键冲突，推动情节高潮"
        else:
            intensity = "终极"
            suggestion = "设计最终冲突，完成故事主线"

        # 检查用户约束
        forbidden_elements = self._get_attr_or_key(user_intent, "forbidden_elements", [])
        if "暴力冲突" in forbidden_elements:
            suggestion = suggestion.replace("冲突", "矛盾")
            suggestion = suggestion.replace("激烈", "紧张")

        return f"""
第{chapter_num}章冲突设计：
冲突类型：{conflict_type}
冲突强度：{intensity}
设计建议：{suggestion}
请确保冲突与故事背景和角色设定保持一致。
"""

    def _simple_suggestions(self, context: str, user_intent: Dict[str, Any]) -> str:
        """简化的建议生成"""

        # 基于用户意图的核心要素生成建议
        core_elements = self._get_attr_or_key(user_intent, "core_elements", {})
        title = core_elements.get("title", "")
        genre = core_elements.get("genre", "")

        suggestions = []

        if genre:
            suggestions.append(f"保持{genre}类型的特色和风格")

        if title:
            suggestions.append(f"围绕《{title}》的主题展开创作")

        constraints = self._get_attr_or_key(user_intent, "constraints", [])
        if constraints:
            suggestions.append(f"注意包含：{', '.join(constraints)}")

        forbidden_elements = self._get_attr_or_key(user_intent, "forbidden_elements", [])
        if forbidden_elements:
            suggestions.append(f"避免出现：{', '.join(forbidden_elements)}")

        if not suggestions:
            suggestions.append("保持创作连贯性，确保情节自然发展")

        return "创作建议：\n" + "\n".join(f"- {s}" for s in suggestions)

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 工厂函数
def create_story_architect():
    """创建故事架构师实例"""
    return StoryArchitectSimplified()