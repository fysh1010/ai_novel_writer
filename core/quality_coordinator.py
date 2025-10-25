#!/usr/bin/env python3
"""
质量协调器 - 统一管理内容质量和用户意图一致性
协调各个智能体的输出，确保最终质量符合用户期望
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
import logging
import re

logger = logging.getLogger(__name__)

@dataclass
class QualityMetrics:
    """质量指标"""
    coherence_score: float  # 连贯性评分
    consistency_score: float  # 一致性评分
    engagement_score: float  # 吸引力评分
    ai_trace_score: float  # AI痕迹评分（越低越好）
    user_intent_alignment: float  # 用户意图对齐度

class QualityCoordinator:
    """质量协调器"""

    def __init__(self):
        # 质量阈值
        self.quality_thresholds = {
            "excellent": 0.9,    # 优秀
            "good": 0.75,        # 良好
            "acceptable": 0.6,   # 可接受
            "poor": 0.4          # 差
        }

        # 权重配置
        self.metric_weights = {
            "coherence": 0.25,      # 连贯性权重
            "consistency": 0.25,    # 一致性权重
            "engagement": 0.2,      # 吸引力权重
            "ai_trace": 0.15,       # AI痕迹权重
            "user_intent": 0.15     # 用户意图权重
        }

    def evaluate_quality(self, content: str, context: Dict[str, Any]) -> QualityMetrics:
        """
        评估内容质量

        Args:
            content: 待评估内容
            context: 上下文信息（用户意图、前面章节等）

        Returns:
            QualityMetrics: 质量指标
        """
        logger.info("开始评估内容质量...")

        # 评估各项指标
        coherence_score = self._evaluate_coherence(content, context)
        consistency_score = self._evaluate_consistency(content, context)
        engagement_score = self._evaluate_engagement(content, context)
        ai_trace_score = self._evaluate_ai_traces(content)
        user_intent_alignment = self._evaluate_user_intent_alignment(content, context)

        metrics = QualityMetrics(
            coherence_score=coherence_score,
            consistency_score=consistency_score,
            engagement_score=engagement_score,
            ai_trace_score=ai_trace_score,
            user_intent_alignment=user_intent_alignment
        )

        logger.info(f"质量评估完成: {self._get_quality_summary(metrics)}")
        return metrics

    def get_improvement_suggestions(self, metrics: QualityMetrics,
                                   content: str, context: Dict[str, Any]) -> List[str]:
        """
        获取改进建议

        Args:
            metrics: 质量指标
            content: 内容
            context: 上下文

        Returns:
            List[str]: 改进建议列表
        """
        suggestions = []

        # 基于各项指标生成建议
        if metrics.coherence_score < 0.7:
            suggestions.append("提高内容连贯性：加强段落间的逻辑连接，确保情节发展自然")

        if metrics.consistency_score < 0.7:
            suggestions.append("改善一致性：检查角色性格、设定是否前后一致")

        if metrics.engagement_score < 0.7:
            suggestions.append("增强吸引力：增加冲突张力，改进对话质量，提升情节紧凑度")

        if metrics.ai_trace_score > 0.7:  # AI痕迹太高
            suggestions.append("减少AI痕迹：使用更自然的表达，避免模板化语言")

        if metrics.user_intent_alignment < 0.7:
            suggestions.append("对齐用户意图：确保内容符合用户的核心要求和约束条件")

        # 如果整体质量良好，提供正面反馈
        overall_score = self._calculate_overall_score(metrics)
        if overall_score >= 0.8:
            suggestions.append("内容质量优秀，继续保持当前水准")

        return suggestions

    def should_optimize(self, metrics: QualityMetrics) -> bool:
        """
        判断是否需要优化

        Args:
            metrics: 质量指标

        Returns:
            bool: 是否需要优化
        """
        overall_score = self._calculate_overall_score(metrics)

        # 如果任何关键指标过低，需要优化
        critical_issues = (
            metrics.coherence_score < 0.5 or
            metrics.consistency_score < 0.5 or
            metrics.ai_trace_score > 0.8
        )

        return overall_score < 0.7 or critical_issues

    def _evaluate_coherence(self, content: str, context: Dict[str, Any]) -> float:
        """评估连贯性"""
        if not content:
            return 0.0

        score = 0.5  # 基础分

        # 检查段落连接
        paragraphs = content.split('\n\n')
        if len(paragraphs) > 1:
            # 检查是否有逻辑连接词
            connection_words = ['然而', '因此', '接着', '然后', '同时', '另外']
            connection_count = sum(1 for p in paragraphs if any(word in p for word in connection_words))
            connection_ratio = connection_count / len(paragraphs)
            score += connection_ratio * 0.3

        # 检查时间线连贯性
        time_markers = ['首先', '接着', '随后', '最后', '然后', '于是']
        time_count = sum(1 for marker in time_markers if marker in content)
        if time_count > 0:
            score += min(time_count * 0.05, 0.2)

        return min(score, 1.0)

    def _evaluate_consistency(self, content: str, context: Dict[str, Any]) -> float:
        """评估一致性"""
        if not content:
            return 0.0

        score = 0.5  # 基础分

        # 检查角色名称一致性（简化版）
        previous_chapters = context.get("previous_chapters", [])
        if previous_chapters:
            # 提取当前内容的角色名称
            current_names = set(re.findall(r'[A-Za-z\u4e00-\u9fff]{2,4}(?=说|道|想|看)', content))

            # 提取前面章节的角色名称
            previous_content = '\n'.join([ch.get('content', '') for ch in previous_chapters[-3:]])
            previous_names = set(re.findall(r'[A-Za-z\u4e00-\u9fff]{2,4}(?=说|道|想|看)', previous_content))

            # 计算重叠度
            if previous_names:
                overlap = len(current_names & previous_names) / len(previous_names)
                score += overlap * 0.3

        # 检查设定一致性
        story_framework = context.get("story_framework", "")
        if story_framework:
            # 简单的关键词匹配
            framework_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,}', story_framework)[:10])
            content_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,}', content)[:20])

            if framework_keywords:
                keyword_match = len(framework_keywords & content_keywords) / len(framework_keywords)
                score += keyword_match * 0.2

        return min(score, 1.0)

    def _evaluate_engagement(self, content: str, context: Dict[str, Any]) -> float:
        """评估吸引力"""
        if not content:
            return 0.0

        score = 0.5  # 基础分

        # 检查对话比例
        dialogue_pattern = r'["「『].*?["」』]|说.*?["「『]|道.*?["」』]'
        dialogue_matches = re.findall(dialogue_pattern, content)
        dialogue_ratio = len(dialogue_matches) / max(len(content) / 100, 1)
        if 0.1 <= dialogue_ratio <= 0.3:  # 适度的对话比例
            score += 0.2

        # 检查动作描写
        action_words = ['跑', '跳', '打', '杀', '追', '逃', '冲', '撞', '抓', '推']
        action_count = sum(1 for word in action_words if word in content)
        if action_count > 0:
            score += min(action_count * 0.03, 0.15)

        # 检查情感词汇
        emotion_words = ['愤怒', '高兴', '悲伤', '惊讶', '恐惧', '兴奋', '紧张', '放松']
        emotion_count = sum(1 for word in emotion_words if word in content)
        if emotion_count > 0:
            score += min(emotion_count * 0.03, 0.15)

        return min(score, 1.0)

    def _evaluate_ai_traces(self, content: str) -> float:
        """评估AI痕迹（分数越高表示痕迹越明显）"""
        if not content:
            return 0.0

        trace_score = 0.0

        # 检查常见AI模板化表达
        ai_patterns = [
            r'在这个.*的时代',
            r'随着时间的推移',
            r'然而，命运却',
            r'就在这时',
            r'令人惊讶的是',
            r'不容忽视的是',
            r'总而言之',
            r'综上所述'
        ]

        for pattern in ai_patterns:
            matches = re.findall(pattern, content)
            trace_score += len(matches) * 0.1

        # 检查过度修饰
        excessive_adverbs = ['非常', '极其', '十分', '特别', '格外', '相当']
        adverb_count = sum(1 for adverb in excessive_adverbs if content.count(adverb) > 3)
        trace_score += adverb_count * 0.1

        # 检查句式单一性
        sentences = re.split(r'[。！？]', content)
        if len(sentences) > 10:
            # 计算平均句长
            avg_length = sum(len(s) for s in sentences) / len(sentences)
            if 15 <= avg_length <= 25:  # 适中的句长
                trace_score -= 0.1  # 减少AI痕迹评分

        return max(0.0, min(trace_score, 1.0))

    def _evaluate_user_intent_alignment(self, content: str, context: Dict[str, Any]) -> float:
        """评估用户意图对齐度"""
        if not content:
            return 0.0

        score = 0.5  # 基础分

        user_intent = context.get("user_intent", {})
        if not user_intent:
            return score

        # 检查核心要素匹配
        core_elements = getattr(user_intent, "core_elements", {})
        genre = core_elements.get("genre", "")
        custom_plot = core_elements.get("custom_plot", "")

        if genre and genre in content:
            score += 0.2

        if custom_plot:
            # 简单的关键词匹配
            plot_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,}', custom_plot)[:5])
            content_keywords = set(re.findall(r'[\u4e00-\u9fff]{2,}', content)[:30])

            if plot_keywords:
                keyword_match = len(plot_keywords & content_keywords) / len(plot_keywords)
                score += keyword_match * 0.2

        # 检查约束条件
        constraints = getattr(user_intent, "constraints", [])
        if constraints:
            constraint_matches = sum(1 for constraint in constraints if constraint in content)
            constraint_ratio = constraint_matches / len(constraints)
            score += constraint_ratio * 0.1

        # 检查禁止元素
        forbidden_elements = getattr(user_intent, "forbidden_elements", [])
        if forbidden_elements:
            forbidden_violations = sum(1 for forbidden in forbidden_elements if forbidden in content)
            if forbidden_violations > 0:
                score -= forbidden_violations * 0.2

        return max(0.0, min(score, 1.0))

    def _calculate_overall_score(self, metrics: QualityMetrics) -> float:
        """计算总体评分"""
        return (
            metrics.coherence_score * self.metric_weights["coherence"] +
            metrics.consistency_score * self.metric_weights["consistency"] +
            metrics.engagement_score * self.metric_weights["engagement"] +
            (1.0 - metrics.ai_trace_score) * self.metric_weights["ai_trace"] +  # AI痕迹越低越好
            metrics.user_intent_alignment * self.metric_weights["user_intent"]
        )

    def _get_quality_summary(self, metrics: QualityMetrics) -> str:
        """获取质量摘要"""
        overall = self._calculate_overall_score(metrics)

        if overall >= self.quality_thresholds["excellent"]:
            level = "优秀"
        elif overall >= self.quality_thresholds["good"]:
            level = "良好"
        elif overall >= self.quality_thresholds["acceptable"]:
            level = "可接受"
        else:
            level = "需改进"

        return f"{level} (总体:{overall:.2f}, 连贯:{metrics.coherence_score:.2f}, 一致:{metrics.consistency_score:.2f}, 吸引:{metrics.engagement_score:.2f}, AI痕迹:{metrics.ai_trace_score:.2f}, 意图:{metrics.user_intent_alignment:.2f})"

# 使用示例
if __name__ == "__main__":
    coordinator = QualityCoordinator()

    # 测试内容
    test_content = "这是一个测试章节内容..."
    test_context = {
        "user_intent": {
            "core_elements": {"genre": "玄幻", "custom_plot": "主角修炼成神"},
            "constraints": ["要有打斗场面"],
            "forbidden_elements": ["后宫"]
        },
        "previous_chapters": []
    }

    metrics = coordinator.evaluate_quality(test_content, test_context)
    suggestions = coordinator.get_improvement_suggestions(metrics, test_content, test_context)

    print("质量评估结果:", coordinator._get_quality_summary(metrics))
    print("改进建议:", suggestions)