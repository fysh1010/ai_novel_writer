#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的章节生成器 - 专注于用户意图和核心创作
减少冗余的智能体调用，提高生成效率和质量
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class SimplifiedChapterWriter:
    """简化章节生成器"""

    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.log = main_controller.log

    def write_chapter_simplified(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        简化的章节创作方法

        Args:
            input_data: 章节创作输入数据

        Returns:
            Dict: 章节创作结果
        """
        self.log("开始创作章节（简化版本）...")

        # 引入权重管理器
        from core.weight_manager import WeightManager
        weight_manager = WeightManager()

        chapter_num = input_data.get("chapter_num", 1)
        previous_chapters = input_data.get("previous_chapters", [])
        story_framework = input_data.get("story_framework", "")
        character_system = input_data.get("character_system", "")
        plot_timeline = input_data.get("plot_timeline", "")
        custom_prompt = input_data.get("custom_prompt", "")
        is_revision = input_data.get("is_revision", False)

        # 获取用户意图（从小说数据中）
        user_intent = input_data.get("user_intent", {})
        if not user_intent:
            # 如果没有用户意图，从背景中提取
            user_intent = {
                "core_elements": {
                    "title": input_data.get("title", ""),
                    "genre": input_data.get("genre", ""),
                    "custom_plot": input_data.get("custom_plot", "")
                },
                "constraints": [],
                "forbidden_elements": []
            }

        # 确保用户意图是字典格式（兼容字典和对象）
        if hasattr(user_intent, 'core_elements'):
            # 如果是UserIntent对象，转换为字典
            user_intent_dict = {
                "core_elements": user_intent.core_elements,
                "constraints": user_intent.constraints,
                "forbidden_elements": user_intent.forbidden_elements,
                "preferences": getattr(user_intent, 'preferences', {}),
                "priority_weights": getattr(user_intent, 'priority_weights', {})
            }
        else:
            # 如果已经是字典，直接使用
            user_intent_dict = user_intent

        # 构建智能体建议（简化版）
        agent_suggestions = {}

        # 1. 基础节奏分析（可选）
        if previous_chapters:
            self.log("分析前面章节的节奏...")
            previous_content = "\n".join([
                ch.get('content', '')[:300] for ch in previous_chapters[-3:]  # 只取最近3章
            ])
            agent_suggestions["rhythm"] = f"前面章节节奏：{len(previous_content)}字，建议保持连贯性"

        # 2. 角色一致性检查（简化）
        if character_system and previous_chapters:
            self.log("检查角色一致性...")
            agent_suggestions["character"] = "根据已有角色设定保持一致性"

        # 3. 情节连贯性检查（简化）
        if plot_timeline and previous_chapters:
            self.log("检查情节连贯性...")
            agent_suggestions["plot"] = "根据时间线保持情节连贯"

        # 计算权重
        agent_outputs = [
            {"agent_name": "rhythm_analyzer", "output": agent_suggestions.get("rhythm", "")},
            {"agent_name": "character_consistency", "output": agent_suggestions.get("character", "")},
            {"agent_name": "plot_coherence", "output": agent_suggestions.get("plot", "")}
        ]

        weights = weight_manager.calculate_weights(agent_outputs, user_intent_dict)
        self.log(f"智能体建议权重: {weight_manager.get_weight_summary(weights)}")

        # 应用过滤器
        filtered_suggestions = weight_manager.apply_priority_filter(agent_suggestions, weights)

        # 构建简化的生成参数
        generation_params = {
            "chapter_num": chapter_num,
            "story_framework": story_framework,
            "character_system": character_system,
            "plot_timeline": plot_timeline,
            "previous_chapters": previous_chapters,
            "custom_prompt": custom_prompt,
            "rhythm_analysis": filtered_suggestions.get("rhythm", "保持节奏连贯"),
            "character_analysis": filtered_suggestions.get("character", "保持角色一致"),
            "plot_analysis": filtered_suggestions.get("plot", "保持情节连贯"),
            "user_custom_plot": user_intent_dict["core_elements"].get("custom_plot", ""),
            "strict_user_input": True,
            "is_revision": is_revision
        }

        # 生成章节内容
        self.log("正在生成章节内容...")
        chapter_content = self._generate_chapter_content(generation_params)

        # 简化的优化和审查
        self.log("进行内容优化和审查...")

        # 优化（简化版）
        try:
            optimization_result = self.main_controller.optimizer.process({
                "type": "optimize_content",
                "content": chapter_content,
                "genre": user_intent_dict["core_elements"].get("genre", ""),
                "optimization_goals": ["消除AI痕迹", "提升质量"]
            })
            if "error" not in optimization_result:
                chapter_content = optimization_result.get("content", chapter_content)
        except Exception as e:
            self.log(f"优化跳过: {e}")

        # 合规审查（简化版）
        try:
            compliance_result = self.main_controller.compliance_advisor.process({
                "type": "chapter",
                "content": chapter_content
            })
            if "error" not in compliance_result:
                chapter_content = compliance_result.get("content", chapter_content)
        except Exception as e:
            self.log(f"合规审查跳过: {e}")

        # 提取标题和内容
        self.log(f"📊 优化和审查后内容长度: {len(chapter_content)} 字符")
        chapter_title, chapter_content = self.main_controller._extract_title_and_content(chapter_content)
        self.log(f"📊 提取后 - 标题: {chapter_title[:50] if len(chapter_title) > 50 else chapter_title}")
        self.log(f"📊 提取后 - 内容长度: {len(chapter_content)} 字符")

        # 生成摘要
        chapter_summary = self._generate_chapter_summary(chapter_content)

        # 简化的质量检查
        quality_score = 1.0
        if previous_chapters:
            # 简单的重复检查
            for prev_ch in previous_chapters[-3:]:  # 只检查最近3章
                prev_content = prev_ch.get("content", "")
                if len(prev_content) > 100:
                    # 简单的相似度检查
                    common_words = set(chapter_content[:100]) & set(prev_content[:100])
                    similarity = len(common_words) / 100
                    quality_score = min(quality_score, 1.0 - similarity * 0.5)

        # 整合结果
        chapter_data = {
            "chapter_num": chapter_num,
            "title": chapter_title,
            "content": chapter_content,
            "summary": chapter_summary,
            "metadata": {
                "agent_weights": weights,
                "quality_score": quality_score,
                "user_intent": user_intent_dict,
                "created_at": self.main_controller._get_timestamp(),
                "optimization": "simplified",
                "agent_suggestions": filtered_suggestions
            }
        }

        self.log(f"✅ 章节创作完成！质量评分: {quality_score:.2f}")
        return {
            "type": "chapter_created",
            "data": chapter_data
        }

    def _generate_chapter_content(self, params: Dict[str, Any]) -> str:
        """生成章节内容"""
        return self.main_controller._generate_chapter_content(params)

    def _generate_chapter_summary(self, chapter_content: str) -> str:
        """生成章节摘要"""
        return self.main_controller._generate_chapter_summary(chapter_content)

# 使用示例
if __name__ == "__main__":
    # 这里只是示例，实际使用时需要传入main_controller实例
    pass