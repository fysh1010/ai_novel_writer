#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户意图解析器 - 提取和结构化用户的核心创作意图
确保智能体系统准确理解和遵循用户需求
"""

import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class UserIntent:
    """用户意图数据结构"""
    core_elements: Dict[str, Any]  # 核心要素
    constraints: List[str]          # 约束条件
    preferences: Dict[str, Any]     # 偏好设置
    forbidden_elements: List[str]   # 禁止元素
    priority_weights: Dict[str, float]  # 优先级权重

class IntentParser:
    """用户意图解析器"""

    def __init__(self):
        self.intent_patterns = {
            # 题材识别模式
            'genre_patterns': [
                r'(玄幻|修真|仙侠|洪荒|神话)',
                r'(都市|现代|现实|职场)',
                r'(科幻|未来|太空|机甲)',
                r'(历史|古代|武侠|江湖)',
                r'(言情|爱情|情感|恋爱)',
                r'(悬疑|推理|侦探|犯罪)',
                r'(恐怖|惊悚|灵异|鬼怪)'
            ],

            # 主角特征模式
            'protagonist_patterns': [
                r'主角.*?(是|为).*?([^\s，。！？]+)',
                r'(男主|女主|主人公).*?([^\s，。！？]+)',
                r'身份.*?(是|为).*?([^\s，。！？]+)',
                r'能力.*?(有|具备).*?([^\s，。！？]+)'
            ],

            # 世界观模式
            'worldview_patterns': [
                r'世界观.*?([^\s，。！？]+)',
                r'背景.*?(设定|是).*?([^\s，。！？]+)',
                r'时代.*?(背景|设定).*?([^\s，。！？]+)'
            ],

            # 约束条件模式
            'constraint_patterns': [
                r'(不要|避免|禁止).*?([^\s，。！？]+)',
                r'(不能|不可|不许).*?([^\s，。！？]+)',
                r'(必须|一定|务必).*?([^\s，。！？]+)',
                r'(限制|要求).*?([^\s，。！？]+)'
            ]
        }

    def parse_user_intent(self, user_input: Dict[str, Any]) -> UserIntent:
        """
        解析用户输入，提取核心意图

        Args:
            user_input: 用户输入的原始数据

        Returns:
            UserIntent: 结构化的用户意图
        """
        logger.info("开始解析用户意图...")

        # 提取核心要素
        core_elements = self._extract_core_elements(user_input)

        # 提取约束条件
        constraints = self._extract_constraints(user_input)

        # 提取偏好设置
        preferences = self._extract_preferences(user_input)

        # 提取禁止元素
        forbidden_elements = self._extract_forbidden_elements(user_input)

        # 计算优先级权重
        priority_weights = self._calculate_priority_weights(core_elements)

        intent = UserIntent(
            core_elements=core_elements,
            constraints=constraints,
            preferences=preferences,
            forbidden_elements=forbidden_elements,
            priority_weights=priority_weights
        )

        logger.info(f"用户意图解析完成，核心要素: {len(core_elements)}个，约束条件: {len(constraints)}个")
        return intent

    def _extract_core_elements(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """提取核心要素"""
        core_elements = {}

        # 基础信息
        core_elements['title'] = user_input.get('title', '')
        core_elements['genre'] = self._identify_genre(user_input.get('genre', ''))
        core_elements['theme'] = user_input.get('theme', '')
        core_elements['custom_plot'] = user_input.get('custom_plot', '')

        # 从详细描述中提取要素
        detailed_description = user_input.get('detailed_description', '')
        if detailed_description:
            # 提取主角信息
            protagonist_info = self._extract_protagonist_info(detailed_description)
            core_elements['protagonist'] = protagonist_info

            # 提取世界观信息
            worldview_info = self._extract_worldview_info(detailed_description)
            core_elements['worldview'] = worldview_info

            # 提取核心设定
            core_settings = self._extract_core_settings(detailed_description)
            core_elements['core_settings'] = core_settings

        return core_elements

    def _identify_genre(self, genre_text: str) -> str:
        """识别题材类型"""
        for pattern_group in self.intent_patterns['genre_patterns']:
            matches = re.findall(pattern_group, genre_text)
            if matches:
                return matches[0]
        return genre_text or "通用"

    def _extract_protagonist_info(self, text: str) -> Dict[str, Any]:
        """提取主角信息"""
        protagonist_info = {
            'identity': '',
            'abilities': [],
            'personality': '',
            'background': ''
        }

        for pattern in self.intent_patterns['protagonist_patterns']:
            matches = re.findall(pattern, text)
            for match in matches:
                if '身份' in pattern:
                    protagonist_info['identity'] = match
                elif '能力' in pattern:
                    protagonist_info['abilities'].append(match)
                else:
                    protagonist_info['background'] = match

        return protagonist_info

    def _extract_worldview_info(self, text: str) -> Dict[str, Any]:
        """提取世界观信息"""
        worldview_info = {
            'setting': '',
            'era': '',
            'rules': []
        }

        for pattern in self.intent_patterns['worldview_patterns']:
            matches = re.findall(pattern, text)
            if matches:
                worldview_info['setting'] = matches[0]

        return worldview_info

    def _extract_core_settings(self, text: str) -> List[str]:
        """提取核心设定"""
        settings = []

        # 查找关键设定词
        setting_keywords = [
            '系统', '金手指', '异能', '法宝', '功法',
            '组织', '势力', '门派', '家族', '公司',
            '特殊规则', '独特机制'
        ]

        for keyword in setting_keywords:
            if keyword in text:
                # 提取包含关键词的句子
                sentences = re.split(r'[。！？]', text)
                for sentence in sentences:
                    if keyword in sentence and len(sentence.strip()) > 5:
                        settings.append(sentence.strip())

        return settings

    def _extract_constraints(self, user_input: Dict[str, Any]) -> List[str]:
        """提取约束条件"""
        constraints = []

        # 从各个字段中提取约束
        all_text = " ".join([
            user_input.get('custom_plot', ''),
            user_input.get('detailed_description', ''),
            user_input.get('special_requirements', '')
        ])

        for pattern in self.intent_patterns['constraint_patterns']:
            matches = re.findall(pattern, all_text)
            constraints.extend(matches)

        return list(set(constraints))  # 去重

    def _extract_preferences(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """提取偏好设置"""
        preferences = {}

        # 风格偏好
        style_keywords = {
            '轻松': 'light',
            '严肃': 'serious',
            '幽默': 'humorous',
            '深刻': 'profound',
            '热血': 'passionate',
            '温馨': 'warm'
        }

        all_text = " ".join([
            user_input.get('custom_plot', ''),
            user_input.get('detailed_description', '')
        ])

        for keyword, style in style_keywords.items():
            if keyword in all_text:
                preferences['style'] = style
                break

        # 长度偏好
        target_length = user_input.get('target_length', 50)
        preferences['target_length'] = target_length

        # 更新频率偏好
        preferences['update_frequency'] = user_input.get('update_frequency', 'daily')

        return preferences

    def _extract_forbidden_elements(self, user_input: Dict[str, Any]) -> List[str]:
        """提取禁止元素"""
        forbidden = []

        all_text = " ".join([
            user_input.get('custom_plot', ''),
            user_input.get('detailed_description', ''),
            user_input.get('special_requirements', '')
        ])

        # 查找明确的禁止词
        forbid_patterns = [
            r'不要.*?([^\s，。！？]+)',
            r'避免.*?([^\s，。！？]+)',
            r'禁止.*?([^\s，。！？]+)',
            r'不能.*?([^\s，。！？]+)'
        ]

        for pattern in forbid_patterns:
            matches = re.findall(pattern, all_text)
            forbidden.extend(matches)

        return list(set(forbidden))

    def _calculate_priority_weights(self, core_elements: Dict[str, Any]) -> Dict[str, float]:
        """计算优先级权重"""
        weights = {
            'user_background': 100.0,      # 用户背景设定最高权重
            'protagonist_setting': 90.0,   # 主角设定
            'worldview_setting': 80.0,     # 世界观设定
            'core_plot': 85.0,            # 核心情节
            'style_preference': 70.0,      # 风格偏好
            'constraints': 95.0,          # 约束条件
        }

        # 根据内容丰富度调整权重
        if core_elements.get('custom_plot'):
            weights['user_background'] += 10

        if core_elements.get('protagonist'):
            weights['protagonist_setting'] += 5

        if core_elements.get('worldview'):
            weights['worldview_setting'] += 5

        return weights

    def validate_intent_consistency(self, intent: UserIntent) -> Dict[str, Any]:
        """
        验证用户意图的一致性

        Args:
            intent: 用户意图对象

        Returns:
            Dict: 验证结果
        """
        validation_result = {
            'is_consistent': True,
            'conflicts': [],
            'suggestions': []
        }

        # 检查约束条件与核心要素的冲突
        for constraint in intent.constraints:
            for element_type, elements in intent.core_elements.items():
                if isinstance(elements, str) and constraint in elements:
                    validation_result['conflicts'].append(
                        f"约束条件'{constraint}'与核心要素'{element_type}'存在冲突"
                    )
                    validation_result['is_consistent'] = False

        # 检查禁止元素与核心要素的冲突
        for forbidden in intent.forbidden_elements:
            for element_type, elements in intent.core_elements.items():
                if isinstance(elements, str) and forbidden in elements:
                    validation_result['conflicts'].append(
                        f"禁止元素'{forbidden}'与核心要素'{element_type}'存在冲突"
                    )
                    validation_result['is_consistent'] = False

        # 生成建议
        if not validation_result['is_consistent']:
            validation_result['suggestions'].append(
                "建议修改约束条件或核心要素以确保一致性"
            )

        return validation_result

    def get_intent_summary(self, intent: UserIntent) -> str:
        """
        获取用户意图摘要

        Args:
            intent: 用户意图对象

        Returns:
            str: 意图摘要
        """
        summary_parts = []

        if intent.core_elements.get('title'):
            summary_parts.append(f"标题: {intent.core_elements['title']}")

        if intent.core_elements.get('genre'):
            summary_parts.append(f"题材: {intent.core_elements['genre']}")

        if intent.core_elements.get('protagonist', {}).get('identity'):
            summary_parts.append(f"主角: {intent.core_elements['protagonist']['identity']}")

        if intent.core_elements.get('worldview', {}).get('setting'):
            summary_parts.append(f"世界观: {intent.core_elements['worldview']['setting']}")

        if intent.constraints:
            summary_parts.append(f"约束: {', '.join(intent.constraints[:3])}")

        return " | ".join(summary_parts)

# 使用示例
if __name__ == "__main__":
    parser = IntentParser()

    # 测试用户输入
    test_input = {
        'title': '天道有Bug我来修',
        'genre': '玄幻洪荒',
        'theme': '程序员穿越修仙',
        'custom_plot': '现代程序员林渊穿越洪荒，发现天道是源代码，用编程知识修补漏洞',
        'detailed_description': '主角是程序员，拥有调试器能力，不要写得太夸张，必须有技术细节',
        'special_requirements': '避免后宫情节，必须保持逻辑严谨'
    }

    intent = parser.parse_user_intent(test_input)
    print("用户意图解析结果:")
    print(f"核心要素: {intent.core_elements}")
    print(f"约束条件: {intent.constraints}")
    print(f"禁止元素: {intent.forbidden_elements}")
    print(f"优先级权重: {intent.priority_weights}")

    validation = parser.validate_intent_consistency(intent)
    print(f"一致性验证: {validation}")

    summary = parser.get_intent_summary(intent)
    print(f"意图摘要: {summary}")