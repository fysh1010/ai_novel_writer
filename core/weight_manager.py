#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
权重管理器 - 统一管理智能体输出的权重和优先级
确保用户意图得到最高优先级处理
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class WeightConfig:
    """权重配置"""
    element_type: str
    base_weight: float
    max_weight: float
    priority_level: int  # 1-10, 10为最高优先级

class WeightManager:
    """权重管理器"""

    def __init__(self):
        # 基础权重配置
        self.base_weights = {
            'user_background': WeightConfig('user_background', 100.0, 100.0, 10),
            'story_architect': WeightConfig('story_architect', 30.0, 50.0, 6),
            'character_manager': WeightConfig('character_manager', 30.0, 50.0, 6),
            'plot_controller': WeightConfig('plot_controller', 30.0, 50.0, 6),
            'optimizer': WeightConfig('optimizer', 20.0, 40.0, 4),
            'compliance_advisor': WeightConfig('compliance_advisor', 40.0, 60.0, 7),
            'knowledge_base': WeightConfig('knowledge_base', 25.0, 45.0, 5),
        }

        # 动态权重调整因子
        self.adjustment_factors = {
            'user_explicit': 1.2,      # 用户明确提及
            'repeated_mention': 1.1,   # 多次提及
            'detailed_description': 1.15, # 详细描述
            'constraint_violation': 0.5, # 违反约束
            'consistency_bonus': 1.1,   # 一致性奖励
        }

        # 权重阈值
        self.weight_thresholds = {
            'critical': 80.0,    # 关键权重，必须考虑
            'important': 60.0,   # 重要权重，应该考虑
            'normal': 40.0,      # 正常权重，可以参考
            'low': 20.0,         # 低权重，较少考虑
        }

    def calculate_weights(self, agent_outputs: List[Dict[str, Any]],
                         user_intent) -> Dict[str, float]:
        """
        计算各智能体输出的权重

        Args:
            agent_outputs: 智能体输出列表
            user_intent: 用户意图信息

        Returns:
            Dict[str, float]: 权重字典
        """
        logger.info("开始计算智能体输出权重...")

        weights = {}

        # 用户背景始终为最高权重
        weights['user_background'] = self.base_weights['user_background'].base_weight

        # 计算其他智能体权重
        for output in agent_outputs:
            agent_name = output.get('agent_name', '')
            content = output.get('output', '')

            if agent_name in self.base_weights:
                base_config = self.base_weights[agent_name]
                weight = self._calculate_agent_weight(
                    agent_name, content, user_intent, base_config
                )
                weights[agent_name] = weight

        # 归一化权重
        normalized_weights = self._normalize_weights(weights)

        logger.info(f"权重计算完成: {normalized_weights}")
        return normalized_weights

    def _calculate_agent_weight(self, agent_name: str, content: str,
                               user_intent: Dict[str, Any],
                               base_config: WeightConfig) -> float:
        """计算单个智能体的权重"""
        weight = base_config.base_weight

        # 根据内容质量调整权重
        quality_score = self._assess_content_quality(content)
        weight *= quality_score

        # 根据与用户意图的一致性调整权重
        consistency_score = self._assess_intent_consistency(
            content, user_intent, agent_name
        )
        weight *= consistency_score

        # 根据约束违反情况调整权重
        constraint_penalty = self._assess_constraint_violation(
            content, user_intent
        )
        weight *= constraint_penalty

        # 确保权重在合理范围内
        weight = max(0.0, min(weight, base_config.max_weight))

        return weight

    def _assess_content_quality(self, content: str) -> float:
        """评估内容质量"""
        if not content:
            return 0.5

        quality_score = 1.0

        # 长度合理性
        content_length = len(content)
        if content_length < 100:
            quality_score *= 0.7  # 内容过短
        elif content_length > 5000:
            quality_score *= 0.8  # 内容过长

        # 结构完整性
        if '结构' in content or '框架' in content:
            quality_score *= 1.1

        # 逻辑连贯性
        if '逻辑' in content or '连贯' in content:
            quality_score *= 1.05

        # 创新性
        if '创新' in content or '独特' in content:
            quality_score *= 1.05

        return quality_score

    def _assess_intent_consistency(self, content: str, user_intent: Dict[str, Any],
                                  agent_name: str) -> float:
        """评估与用户意图的一致性"""
        consistency_score = 1.0

        # 检查关键词匹配
        user_keywords = self._extract_keywords_from_intent(user_intent)
        content_keywords = self._extract_keywords_from_content(content)

        # 计算关键词重叠度
        if user_keywords:
            overlap_ratio = len(set(user_keywords) & set(content_keywords)) / len(user_keywords)
            consistency_score = 0.5 + overlap_ratio * 0.5

        # 根据智能体类型调整一致性权重
        if agent_name == 'story_architect':
            # 故事架构师与世界观一致性更重要
            if any(keyword in content for keyword in ['世界观', '背景', '设定']):
                consistency_score *= 1.2

        elif agent_name == 'character_manager':
            # 角色管理师与角色设定一致性更重要
            if any(keyword in content for keyword in ['角色', '人物', '主角']):
                consistency_score *= 1.2

        elif agent_name == 'plot_controller':
            # 情节控制师与情节设定一致性更重要
            if any(keyword in content for keyword in ['情节', '剧情', '发展']):
                consistency_score *= 1.2

        return consistency_score

    def _assess_constraint_violation(self, content: str, user_intent: Dict[str, Any]) -> float:
        """评估约束违反情况"""
        penalty_score = 1.0

        # 兼容性函数：获取属性或字典值
        def _get_attr_or_key(obj, key, default=None):
            if hasattr(obj, key):
                return getattr(obj, key, default)
            elif isinstance(obj, dict):
                return obj.get(key, default)
            return default

        # 获取禁止元素
        forbidden_elements = _get_attr_or_key(user_intent, 'forbidden_elements', [])

        # 检查是否包含禁止元素
        for forbidden in forbidden_elements:
            if forbidden in content:
                penalty_score *= 0.7  # 违反约束降低权重

        # 检查约束条件
        constraints = _get_attr_or_key(user_intent, 'constraints', [])
        for constraint in constraints:
            if '必须' in constraint and constraint.replace('必须', '') not in content:
                penalty_score *= 0.9  # 未满足必须条件降低权重

        return penalty_score

    def _extract_keywords_from_intent(self, user_intent) -> List[str]:
        """从用户意图中提取关键词"""
        keywords = []

        # 兼容性函数
        def _get_attr_or_key(obj, key, default=None):
            if hasattr(obj, key):
                return getattr(obj, key, default)
            elif isinstance(obj, dict):
                return obj.get(key, default)
            return default

        # 从核心要素提取
        core_elements = _get_attr_or_key(user_intent, 'core_elements', {})
        for key, value in core_elements.items():
            if isinstance(value, str) and value:
                keywords.extend(self._extract_words(value))

        # 从约束条件提取
        constraints = _get_attr_or_key(user_intent, 'constraints', [])
        for constraint in constraints:
            keywords.extend(self._extract_words(constraint))

        return list(set(keywords))

    def _extract_keywords_from_content(self, content: str) -> List[str]:
        """从内容中提取关键词"""
        return self._extract_words(content)

    def _extract_words(self, text: str) -> List[str]:
        """提取词汇"""
        # 简单的词汇提取，可以根据需要优化
        import re
        words = re.findall(r'[\u4e00-\u9fff]+', text)  # 提取中文词汇
        return [word for word in words if len(word) >= 2]  # 过滤单字

    def _normalize_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        """归一化权重"""
        if not weights:
            return weights

        # 找到最大权重
        max_weight = max(weights.values())
        if max_weight == 0:
            return weights

        # 归一化到0-100范围
        normalized = {}
        for key, weight in weights.items():
            normalized[key] = (weight / max_weight) * 100

        return normalized

    def apply_priority_filter(self, content_dict: Dict[str, Any],
                            weights: Dict[str, float]) -> Dict[str, Any]:
        """
        应用优先级过滤器，根据权重筛选内容

        Args:
            content_dict: 内容字典
            weights: 权重字典

        Returns:
            Dict[str, Any]: 过滤后的内容
        """
        filtered_content = {}

        # 按权重排序
        sorted_items = sorted(
            content_dict.items(),
            key=lambda x: weights.get(x[0], 0),
            reverse=True
        )

        # 筛选高权重内容
        for key, content in sorted_items:
            weight = weights.get(key, 0)
            if weight >= self.weight_thresholds['important']:
                filtered_content[key] = content
            elif weight >= self.weight_thresholds['normal']:
                # 对于正常权重的内容，进行简化处理
                if isinstance(content, str):
                    # 简化长文本
                    if len(content) > 1000:
                        filtered_content[key] = content[:1000] + "...[内容已简化]"
                    else:
                        filtered_content[key] = content
                else:
                    filtered_content[key] = content

        return filtered_content

    def get_weight_summary(self, weights: Dict[str, float]) -> str:
        """
        获取权重摘要

        Args:
            weights: 权重字典

        Returns:
            str: 权重摘要
        """
        summary_parts = []

        for key, weight in sorted(weights.items(), key=lambda x: x[1], reverse=True):
            level = self._get_weight_level(weight)
            summary_parts.append(f"{key}: {weight:.1f} ({level})")

        return " | ".join(summary_parts)

    def _get_weight_level(self, weight: float) -> str:
        """获取权重等级"""
        if weight >= self.weight_thresholds['critical']:
            return "关键"
        elif weight >= self.weight_thresholds['important']:
            return "重要"
        elif weight >= self.weight_thresholds['normal']:
            return "正常"
        else:
            return "低"

    def adjust_weights_by_context(self, weights: Dict[str, float],
                                 context: Dict[str, Any]) -> Dict[str, float]:
        """
        根据上下文调整权重

        Args:
            weights: 原始权重
            context: 上下文信息

        Returns:
            Dict[str, float]: 调整后的权重
        """
        adjusted_weights = weights.copy()

        # 根据创作阶段调整权重
        creation_stage = context.get('creation_stage', 'normal')
        if creation_stage == 'character_development':
            adjusted_weights['character_manager'] *= 1.3
        elif creation_stage == 'plot_development':
            adjusted_weights['plot_controller'] *= 1.3
        elif creation_stage == 'world_building':
            adjusted_weights['story_architect'] *= 1.3

        # 根据用户反馈调整权重
        user_feedback = context.get('user_feedback', {})
        if user_feedback.get('character_issues'):
            adjusted_weights['character_manager'] *= 1.2
        if user_feedback.get('plot_issues'):
            adjusted_weights['plot_controller'] *= 1.2

        # 重新归一化
        return self._normalize_weights(adjusted_weights)

# 使用示例
if __name__ == "__main__":
    weight_manager = WeightManager()

    # 测试智能体输出
    agent_outputs = [
        {'agent_name': 'story_architect', 'output': '故事框架设定...'},
        {'agent_name': 'character_manager', 'output': '角色体系设计...'},
        {'agent_name': 'plot_controller', 'output': '情节发展设计...'},
    ]

    # 测试用户意图
    user_intent = {
        'core_elements': {
            'title': '测试小说',
            'genre': '玄幻',
            'custom_plot': '主角是程序员'
        },
        'constraints': ['不要后宫情节'],
        'forbidden_elements': ['系统流', '无限流']
    }

    weights = weight_manager.calculate_weights(agent_outputs, user_intent)
    print("权重计算结果:", weights)

    summary = weight_manager.get_weight_summary(weights)
    print("权重摘要:", summary)