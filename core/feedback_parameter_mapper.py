#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反馈参数映射器 - 处理用户反馈并映射为系统参数
"""

from typing import Dict, Any, List, Tuple, Optional
import re

class FeedbackParameterMapper:
    """反馈参数映射器类"""

    def __init__(self):
        """初始化反馈参数映射器"""
        self.emotion_keywords = {
            "positive": ["好", "棒", "优秀", "满意", "喜欢", "很好", "不错", "完美", "精彩"],
            "negative": ["差", "糟糕", "不满意", "讨厌", "不好", "垃圾", "失败", "无聊"],
            "neutral": ["还行", "一般", "普通", "可以", "接受"]
        }

        self.aspect_keywords = {
            "plot": ["情节", "剧情", "故事", "发展", "冲突", "转折"],
            "character": ["角色", "人物", "性格", "对话", "行为", "心理"],
            "writing": ["文笔", "语言", "描述", "表达", "修辞", "流畅"],
            "pacing": ["节奏", "速度", "紧张", "拖沓", "紧凑", "缓慢"],
            "emotion": ["情感", "感情", "情绪", "感动", "激动", "平淡"]
        }

        self.suggestion_patterns = [
            "希望.*更.*",
            "建议.*",
            "可以.*",
            "应该.*",
            "需要.*"
        ]

    def analyze_feedback(self, feedback_text: str) -> Dict[str, Any]:
        """
        分析用户反馈

        Args:
            feedback_text: 用户反馈文本

        Returns:
            Dict[str, Any]: 分析结果
        """
        feedback_text = feedback_text.strip().lower()

        # 分析情感倾向
        emotion = self._analyze_emotion(feedback_text)

        # 分析涉及方面
        aspects = self._analyze_aspects(feedback_text)

        # 提取评分
        rating = self._extract_rating(feedback_text)

        # 提取建议
        suggestions = self._extract_suggestions(feedback_text)

        return {
            "emotion": emotion,
            "aspects": aspects,
            "rating": rating,
            "suggestions": suggestions,
            "original_text": feedback_text,
            "analysis_time": self._get_timestamp()
        }

    def _analyze_emotion(self, text: str) -> str:
        """分析情感倾向"""
        positive_count = sum(1 for keyword in self.emotion_keywords["positive"] if keyword in text)
        negative_count = sum(1 for keyword in self.emotion_keywords["negative"] if keyword in text)
        neutral_count = sum(1 for keyword in self.emotion_keywords["neutral"] if keyword in text)

        if positive_count > negative_count and positive_count > neutral_count:
            return "positive"
        elif negative_count > positive_count and negative_count > neutral_count:
            return "negative"
        else:
            return "neutral"

    def _analyze_aspects(self, text: str) -> List[str]:
        """分析涉及方面"""
        aspects = []
        for aspect, keywords in self.aspect_keywords.items():
            if any(keyword in text for keyword in keywords):
                aspects.append(aspect)
        return aspects

    def _extract_rating(self, text: str) -> Optional[int]:
        """提取评分"""
        # 查找数字评分模式
        rating_patterns = [
            r"(\d+)分",
            r"评分[：:]\s*(\d+)",
            r"给.*?(\d+)分",
            r"(\d+)\/10",
            r"(\d+)\/5"
        ]

        for pattern in rating_patterns:
            match = re.search(pattern, text)
            if match:
                rating = int(match.group(1))
                # 标准化到1-5分
                if rating > 5:
                    rating = int(rating / 2)
                return min(5, max(1, rating))

        return None

    def _extract_suggestions(self, text: str) -> List[str]:
        """提取建议"""
        suggestions = []
        for pattern in self.suggestion_patterns:
            matches = re.findall(pattern, text)
            suggestions.extend(matches)
        return suggestions

    def map_to_parameters(self, feedback_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        将反馈分析结果映射为系统参数

        Args:
            feedback_analysis: 反馈分析结果

        Returns:
            Dict[str, Any]: 系统参数
        """
        emotion = feedback_analysis.get("emotion", "neutral")
        aspects = feedback_analysis.get("aspects", [])
        rating = feedback_analysis.get("rating")
        suggestions = feedback_analysis.get("suggestions", [])

        parameters = {
            "emotion_weight": self._get_emotion_weight(emotion),
            "aspect_priorities": self._get_aspect_priorities(aspects),
            "quality_boost": self._get_quality_boost(rating),
            "suggestion_hints": suggestions,
            "adjustment_factors": {}
        }

        # 根据具体方面调整参数
        for aspect in aspects:
            if aspect == "plot":
                parameters["adjustment_factors"]["plot_complexity"] = 0.1
            elif aspect == "character":
                parameters["adjustment_factors"]["character_depth"] = 0.1
            elif aspect == "writing":
                parameters["adjustment_factors"]["language_quality"] = 0.1
            elif aspect == "pacing":
                parameters["adjustment_factors"]["narrative_pace"] = 0.1
            elif aspect == "emotion":
                parameters["adjustment_factors"]["emotional_impact"] = 0.1

        return parameters

    def _get_emotion_weight(self, emotion: str) -> float:
        """获取情感权重"""
        weights = {
            "positive": 1.2,
            "neutral": 1.0,
            "negative": 0.8
        }
        return weights.get(emotion, 1.0)

    def _get_aspect_priorities(self, aspects: List[str]) -> Dict[str, float]:
        """获取方面优先级"""
        priorities = {}
        for aspect in aspects:
            priorities[aspect] = 1.0
        return priorities

    def _get_quality_boost(self, rating: Optional[int]) -> float:
        """获取质量提升系数"""
        if rating is None:
            return 0.0
        return (rating - 3) * 0.1  # 将1-5分映射到-0.2到0.2

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()

    def batch_analyze(self, feedback_list: List[str]) -> Dict[str, Any]:
        """
        批量分析反馈

        Args:
            feedback_list: 反馈列表

        Returns:
            Dict[str, Any]: 批量分析结果
        """
        analyses = [self.analyze_feedback(feedback) for feedback in feedback_list]

        # 统计分析
        emotions = [a["emotion"] for a in analyses]
        ratings = [a["rating"] for a in analyses if a["rating"] is not None]
        all_aspects = []
        for a in analyses:
            all_aspects.extend(a["aspects"])

        emotion_distribution = {
            "positive": emotions.count("positive"),
            "neutral": emotions.count("neutral"),
            "negative": emotions.count("negative")
        }

        aspect_frequency = {}
        for aspect in all_aspects:
            aspect_frequency[aspect] = aspect_frequency.get(aspect, 0) + 1

        average_rating = sum(ratings) / len(ratings) if ratings else None

        return {
            "total_feedbacks": len(analyses),
            "emotion_distribution": emotion_distribution,
            "aspect_frequency": aspect_frequency,
            "average_rating": average_rating,
            "detailed_analyses": analyses
        }