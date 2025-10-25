#!/usr/bin/env python3
"""
内容过滤器 - 过滤和优化生成的内容
基于用户意图和质量标准对内容进行精细化处理
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
import logging
import re

logger = logging.getLogger(__name__)

@dataclass
class FilterResult:
    """过滤结果"""
    filtered_content: str
    removed_sections: List[str]
    modifications: List[str]
    quality_improvement: float

class ContentFilter:
    """内容过滤器"""

    def __init__(self):
        # 过滤规则配置
        self.filter_rules = {
            "repetition": {
                "enabled": True,
                "threshold": 0.3,  # 重复度阈值
                "min_length": 10    # 最小重复长度
            },
            "ai_traces": {
                "enabled": True,
                "patterns": [
                    r"在这个.*的时代",
                    r"随着时间的推移",
                    r"然而，命运却",
                    r"就在这时",
                    r"令人惊讶的是",
                    r"不容忽视的是",
                    r"总而言之",
                    r"综上所述",
                    r"众所周知",
                    r"显而易见"
                ]
            },
            "quality": {
                "enabled": True,
                "min_paragraph_length": 20,  # 最小段落长度
                "max_paragraph_length": 500, # 最大段落长度
                "max_sentence_length": 50     # 最大句子长度
            },
            "user_intent": {
                "enabled": True,
                "strict_mode": True
            }
        }

    def filter_content(self, content: str, context: Dict[str, Any]) -> FilterResult:
        """
        过滤内容

        Args:
            content: 原始内容
            context: 上下文信息（用户意图、质量要求等）

        Returns:
            FilterResult: 过滤结果
        """
        logger.info("开始内容过滤...")

        filtered_content = content
        removed_sections = []
        modifications = []

        # 1. 重复内容过滤
        if self.filter_rules["repetition"]["enabled"]:
            filtered_content, repetition_removed = self._filter_repetition(filtered_content)
            removed_sections.extend(repetition_removed)
            if repetition_removed:
                modifications.append("移除重复内容")

        # 2. AI痕迹过滤
        if self.filter_rules["ai_traces"]["enabled"]:
            filtered_content, ai_traces_removed = self._filter_ai_traces(filtered_content)
            removed_sections.extend(ai_traces_removed)
            if ai_traces_removed:
                modifications.append("优化AI痕迹表达")

        # 3. 质量优化
        if self.filter_rules["quality"]["enabled"]:
            filtered_content, quality_improvements = self._improve_quality(filtered_content)
            modifications.extend(quality_improvements)

        # 4. 用户意图对齐
        if self.filter_rules["user_intent"]["enabled"]:
            filtered_content, intent_adjustments = self._align_user_intent(filtered_content, context)
            modifications.extend(intent_adjustments)

        # 计算质量改进程度
        quality_improvement = self._calculate_quality_improvement(content, filtered_content)

        result = FilterResult(
            filtered_content=filtered_content,
            removed_sections=removed_sections,
            modifications=modifications,
            quality_improvement=quality_improvement
        )

        logger.info(f"内容过滤完成，改进度: {quality_improvement:.2f}")
        return result

    def _filter_repetition(self, content: str) -> Tuple[str, List[str]]:
        """过滤重复内容"""
        if not content:
            return content, []

        removed_sections = []
        filtered_content = content

        # 按段落分割
        paragraphs = content.split('\n\n')
        unique_paragraphs = []
        seen_paragraphs = set()

        for paragraph in paragraphs:
            # 标准化段落用于比较
            normalized = paragraph.strip().lower()

            # 如果段落太短，跳过重复检查
            if len(normalized) < self.filter_rules["repetition"]["min_length"]:
                unique_paragraphs.append(paragraph)
                continue

            # 检查是否已出现过相似内容
            if normalized not in seen_paragraphs:
                unique_paragraphs.append(paragraph)
                seen_paragraphs.add(normalized)
            else:
                removed_sections.append(paragraph[:50] + "..." if len(paragraph) > 50 else paragraph)

        # 检查段落内部的重复句子
        final_paragraphs = []
        for paragraph in unique_paragraphs:
            sentences = re.split(r'[。！？]', paragraph)
            unique_sentences = []
            seen_sentences = set()

            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue

                normalized_sentence = sentence.lower()
                if normalized_sentence not in seen_sentences:
                    unique_sentences.append(sentence)
                    seen_sentences.add(normalized_sentence)
                else:
                    removed_sections.append(sentence[:30] + "..." if len(sentence) > 30 else sentence)

            final_paragraphs.append('。'.join(unique_sentences))

        filtered_content = '\n\n'.join(final_paragraphs)
        return filtered_content, removed_sections

    def _filter_ai_traces(self, content: str) -> Tuple[str, List[str]]:
        """过滤AI痕迹"""
        if not content:
            return content, []

        removed_sections = []
        filtered_content = content

        # 替换常见的AI模板化表达
        replacements = {
            "在这个.*的时代": "当时",
            "随着时间的推移": "后来",
            "然而，命运却": "但是",
            "就在这时": "这时",
            "令人惊讶的是": "没想到",
            "不容忽视的是": "值得注意的是",
            "总而言之": "总之",
            "综上所述": "综上",
            "众所周知": "大家都知道",
            "显而易见": "很明显"
        }

        for pattern, replacement in replacements.items():
            matches = re.findall(pattern, filtered_content)
            if matches:
                filtered_content = re.sub(pattern, replacement, filtered_content)
                removed_sections.extend(matches)

        # 优化过度修饰
        excessive_adverbs = ["非常", "极其", "十分", "特别", "格外", "相当"]
        for adverb in excessive_adverbs:
            # 如果同一个副词出现超过3次，进行优化
            count = filtered_content.count(adverb)
            if count > 3:
                # 保留前2次，后面的替换为更简单的表达
                filtered_content = re.sub(adverb, "很", filtered_content, count=count - 2)

        return filtered_content, removed_sections

    def _improve_quality(self, content: str) -> Tuple[str, List[str]]:
        """改进内容质量"""
        if not content:
            return content, []

        improvements = []
        filtered_content = content

        # 1. 优化段落长度
        paragraphs = filtered_content.split('\n\n')
        optimized_paragraphs = []

        for paragraph in paragraphs:
            # 如果段落太长，尝试合理分割
            if len(paragraph) > self.filter_rules["quality"]["max_paragraph_length"]:
                # 按句子分割并重新组合
                sentences = re.split(r'[。！？]', paragraph)
                current_group = []
                current_length = 0

                for sentence in sentences:
                    if not sentence.strip():
                        continue

                    sentence_length = len(sentence)
                    if current_length + sentence_length > self.filter_rules["quality"]["max_paragraph_length"] and current_group:
                        optimized_paragraphs.append('。'.join(current_group) + '。')
                        current_group = [sentence]
                        current_length = sentence_length
                    else:
                        current_group.append(sentence)
                        current_length += sentence_length

                if current_group:
                    optimized_paragraphs.append('。'.join(current_group) + '。')

                improvements.append("优化过长的段落")
            else:
                optimized_paragraphs.append(paragraph)

        filtered_content = '\n\n'.join(optimized_paragraphs)

        # 2. 优化句子长度
        sentences = re.split(r'[。！？]', filtered_content)
        optimized_sentences = []

        for sentence in sentences:
            if len(sentence) > self.filter_rules["quality"]["max_sentence_length"]:
                # 尝试在逗号、分号处分割长句
                parts = re.split(r'[，；]', sentence)
                if len(parts) > 1:
                    optimized_sentences.extend(parts)
                    improvements.append("优化过长的句子")
                else:
                    optimized_sentences.append(sentence)
            else:
                optimized_sentences.append(sentence)

        filtered_content = '。'.join(optimized_sentences)

        # 3. 确保段落最小长度
        paragraphs = filtered_content.split('\n\n')
        final_paragraphs = []

        for paragraph in paragraphs:
            if len(paragraph) < self.filter_rules["quality"]["min_paragraph_length"]:
                # 如果段落太短，尝试与前一段合并
                if final_paragraphs:
                    final_paragraphs[-1] += '\n\n' + paragraph
                    improvements.append("合并过短的段落")
                else:
                    final_paragraphs.append(paragraph)
            else:
                final_paragraphs.append(paragraph)

        filtered_content = '\n\n'.join(final_paragraphs)

        return filtered_content, improvements

    def _align_user_intent(self, content: str, context: Dict[str, Any]) -> Tuple[str, List[str]]:
        """对齐用户意图"""
        if not content:
            return content, []

        adjustments = []
        filtered_content = content

        user_intent = context.get("user_intent", {})
        if not user_intent:
            return filtered_content, adjustments

        # 1. 检查并移除禁止元素
        forbidden_elements = getattr(user_intent, "forbidden_elements", [])
        for forbidden in forbidden_elements:
            if forbidden in filtered_content:
                # 简单的移除操作（实际应用中可能需要更复杂的处理）
                filtered_content = filtered_content.replace(forbidden, "")
                adjustments.append(f"移除禁止元素: {forbidden}")

        # 2. 确保约束条件得到满足
        constraints = getattr(user_intent, "constraints", [])
        for constraint in constraints:
            if constraint not in filtered_content and self.filter_rules["user_intent"]["strict_mode"]:
                # 在内容末尾添加约束相关的提示（简化处理）
                if filtered_content and not filtered_content.endswith('\n\n'):
                    filtered_content += '\n\n'
                filtered_content += f"（注：需体现{constraint}）"
                adjustments.append(f"添加约束元素: {constraint}")

        # 3. 确保核心要素得到体现
        core_elements = getattr(user_intent, "core_elements", {})
        genre = core_elements.get("genre", "")
        custom_plot = core_elements.get("custom_plot", "")

        if genre and self.filter_rules["user_intent"]["strict_mode"]:
            # 确保类型特色得到体现
            genre_keywords = {
                "玄幻": ["修炼", "境界", "灵气", "法宝"],
                "都市": ["现代", "城市", "职场", "生活"],
                "历史": ["古代", "朝代", "历史", "传统"],
                "科幻": ["科技", "未来", "太空", "机器"]
            }

            keywords = genre_keywords.get(genre, [])
            keyword_found = any(keyword in filtered_content for keyword in keywords)

            if not keyword_found and keywords:
                # 选择一个关键词自然地融入内容
                keyword = keywords[0]
                if filtered_content and not filtered_content.endswith('\n\n'):
                    filtered_content += '\n\n'
                filtered_content += f"（注：需体现{genre}特色，如{keyword}相关内容）"
                adjustments.append(f"强化类型特色: {genre}")

        return filtered_content, adjustments

    def _calculate_quality_improvement(self, original: str, filtered: str) -> float:
        """计算质量改进程度"""
        if not original:
            return 0.0

        # 基于长度变化和内容变化的简单计算
        length_ratio = len(filtered) / len(original) if len(original) > 0 else 1.0

        # 计算内容差异度
        original_words = set(original.split())
        filtered_words = set(filtered.split())

        if original_words:
            overlap = len(original_words & filtered_words) / len(original_words)
            difference = 1.0 - overlap
        else:
            difference = 0.0

        # 综合评分
        improvement = (difference * 0.7) + (abs(1.0 - length_ratio) * 0.3)

        return min(improvement, 1.0)

# 使用示例
if __name__ == "__main__":
    filter = ContentFilter()

    # 测试内容
    test_content = """
    在这个玄幻的时代，主角开始了修炼之旅。
    随着时间的推移，他的实力不断增强。
    随着时间的推移，他遇到了很多挑战。
    令人惊讶的是，他克服了所有困难。
    """

    test_context = {
        "user_intent": {
            "core_elements": {"genre": "玄幻"},
            "constraints": ["要有战斗场面"],
            "forbidden_elements": ["系统流"]
        }
    }

    result = filter.filter_content(test_content, test_context)
    print("过滤后内容:", result.filtered_content)
    print("修改项目:", result.modifications)
    print("质量改进:", result.quality_improvement)