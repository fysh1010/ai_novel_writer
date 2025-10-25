#!/usr/bin/env python3
"""
用户意图聚焦模板 - 确保用户意图得到最高优先级处理
将用户的核心需求和约束条件贯穿整个创作过程
"""

from typing import Dict, Any, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class IntentFocusConfig:
    """意图聚焦配置"""
    priority_level: int  # 优先级 1-10
    strict_mode: bool    # 严格模式
    weight_multiplier: float  # 权重倍数

class UserIntentFocusedTemplate:
    """用户意图聚焦模板"""

    def __init__(self):
        # 意图类型配置
        self.intent_configs = {
            "core_elements": IntentFocusConfig(
                priority_level=10,
                strict_mode=True,
                weight_multiplier=2.0
            ),
            "constraints": IntentFocusConfig(
                priority_level=9,
                strict_mode=True,
                weight_multiplier=1.8
            ),
            "forbidden_elements": IntentFocusConfig(
                priority_level=8,
                strict_mode=True,
                weight_multiplier=1.5
            ),
            "preferences": IntentFocusConfig(
                priority_level=6,
                strict_mode=False,
                weight_multiplier=1.2
            )
        }

        # 意图强化策略
        self.reinforcement_strategies = {
            "title": {
                "insertion_points": ["开头", "章节标题", "关键对话"],
                "reinforcement_text": "体现《{title}》的主题"
            },
            "genre": {
                "insertion_points": ["背景描述", "情节设计", "氛围营造"],
                "reinforcement_text": "保持{genre}类型特色"
            },
            "custom_plot": {
                "insertion_points": ["主线推进", "关键转折", "结局安排"],
                "reinforcement_text": "围绕'{custom_plot}'展开"
            },
            "constraints": {
                "insertion_points": ["情节设计", "角色行为", "场景设置"],
                "reinforcement_text": "必须包含：{constraint}"
            },
            "forbidden_elements": {
                "insertion_points": ["内容审查", "情节检查", "角色设定"],
                "reinforcement_text": "避免出现：{forbidden}"
            }
        }

    def create_intent_focused_prompt(self, user_intent: Dict[str, Any],
                                   creation_stage: str, context: Dict[str, Any]) -> str:
        """
        创建聚焦用户意图的提示

        Args:
            user_intent: 用户意图
            creation_stage: 创作阶段
            context: 上下文信息

        Returns:
            str: 聚焦用户意图的提示
        """
        prompt = f"用户意图聚焦创作指南（{creation_stage}阶段）：\n\n"

        # 1. 核心要素强化
        core_elements = getattr(user_intent, "core_elements", {})
        if core_elements:
            prompt += "【核心要素 - 最高优先级】\n"
            for key, value in core_elements.items():
                if value:
                    config = self.intent_configs["core_elements"]
                    prompt += f"- {key}：{value} (优先级: {config.priority_level}, 权重: {config.weight_multiplier}x)\n"

            prompt += "\n核心要素强化策略：\n"
            for key, value in core_elements.items():
                if value and key in self.reinforcement_strategies:
                    strategy = self.reinforcement_strategies[key]
                    reinforcement = strategy["reinforcement_text"].format(**{key: value})
                    prompt += f"- {reinforcement}\n"

        # 2. 约束条件强化
        constraints = getattr(user_intent, "constraints", [])
        if constraints:
            prompt += "\n【约束条件 - 高优先级】\n"
            config = self.intent_configs["constraints"]
            for i, constraint in enumerate(constraints, 1):
                prompt += f"{i}. {constraint} (优先级: {config.priority_level}, 权重: {config.weight_multiplier}x)\n"

            prompt += "\n约束条件强化策略：\n"
            for constraint in constraints:
                reinforcement = self.reinforcement_strategies["constraints"]["reinforcement_text"].format(constraint=constraint)
                prompt += f"- {reinforcement}\n"

        # 3. 禁止元素强化
        forbidden_elements = getattr(user_intent, "forbidden_elements", [])
        if forbidden_elements:
            prompt += "\n【禁止元素 - 中高优先级】\n"
            config = self.intent_configs["forbidden_elements"]
            for i, forbidden in enumerate(forbidden_elements, 1):
                prompt += f"{i}. {forbidden} (优先级: {config.priority_level}, 权重: {config.weight_multiplier}x)\n"

            prompt += "\n禁止元素强化策略：\n"
            for forbidden in forbidden_elements:
                reinforcement = self.reinforcement_strategies["forbidden_elements"]["reinforcement_text"].format(forbidden=forbidden)
                prompt += f"- {reinforcement}\n"

        # 4. 偏好设置
        preferences = getattr(user_intent, "preferences", {})
        if preferences:
            prompt += "\n【偏好设置 - 中等优先级】\n"
            config = self.intent_configs["preferences"]
            for key, value in preferences.items():
                if value:
                    prompt += f"- {key}：{value} (优先级: {config.priority_level}, 权重: {config.weight_multiplier}x)\n"

        # 5. 创作执行原则
        prompt += "\n【创作执行原则】\n"
        prompt += "1. 用户意图优先级最高，任何创作决策都必须符合用户意图\n"
        prompt += "2. 核心要素必须在内容中得到明确体现\n"
        prompt += "3. 约束条件必须得到满足，严格模式下不得违反\n"
        prompt += "4. 禁止元素必须完全避免，一经发现立即修正\n"
        prompt += "5. 在满足上述条件的基础上，考虑偏好设置\n"

        # 6. 质量检查清单
        prompt += "\n【质量检查清单】\n"
        prompt += "□ 核心要素是否充分体现\n"
        prompt += "□ 约束条件是否全部满足\n"
        prompt += "□ 禁止元素是否完全避免\n"
        prompt += "□ 偏好设置是否适当考虑\n"
        prompt += "□ 整体质量是否达到预期\n"

        # 7. 阶段性指导
        prompt += f"\n【{creation_stage}阶段指导】\n"
        stage_guidance = self._get_stage_guidance(creation_stage, user_intent, context)
        prompt += stage_guidance

        return prompt

    def validate_intent_alignment(self, content: str, user_intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证内容与用户意图的对齐程度

        Args:
            content: 待验证内容
            user_intent: 用户意图

        Returns:
            Dict[str, Any]: 验证结果
        """
        validation_result = {
            "overall_alignment": 0.0,
            "detail_results": {},
            "issues": [],
            "suggestions": []
        }

        if not content or not user_intent:
            return validation_result

        total_score = 0.0
        total_weight = 0.0

        # 1. 检查核心要素
        core_elements = getattr(user_intent, "core_elements", {})
        if core_elements:
            core_score = 0.0
            core_weight = self.intent_configs["core_elements"].weight_multiplier

            for key, value in core_elements.items():
                if value and value in content:
                    core_score += 1.0
                elif value:
                    validation_result["issues"].append(f"核心要素 '{key}' 未在内容中体现")

            if core_elements:
                core_score = core_score / len(core_elements)
                total_score += core_score * core_weight
                total_weight += core_weight

                validation_result["detail_results"]["core_elements"] = core_score

        # 2. 检查约束条件
        constraints = getattr(user_intent, "constraints", [])
        if constraints:
            constraint_score = 0.0
            constraint_weight = self.intent_configs["constraints"].weight_multiplier

            for constraint in constraints:
                if constraint in content:
                    constraint_score += 1.0
                else:
                    validation_result["issues"].append(f"约束条件 '{constraint}' 未满足")

            if constraints:
                constraint_score = constraint_score / len(constraints)
                total_score += constraint_score * constraint_weight
                total_weight += constraint_weight

                validation_result["detail_results"]["constraints"] = constraint_score

        # 3. 检查禁止元素
        forbidden_elements = getattr(user_intent, "forbidden_elements", [])
        if forbidden_elements:
            forbidden_score = 1.0  # 默认满分
            forbidden_weight = self.intent_configs["forbidden_elements"].weight_multiplier

            for forbidden in forbidden_elements:
                if forbidden in content:
                    forbidden_score -= 0.5  # 每个禁止元素扣0.5分
                    validation_result["issues"].append(f"禁止元素 '{forbidden}' 出现在内容中")

            forbidden_score = max(0.0, forbidden_score)
            total_score += forbidden_score * forbidden_weight
            total_weight += forbidden_weight

            validation_result["detail_results"]["forbidden_elements"] = forbidden_score

        # 4. 检查偏好设置
        preferences = getattr(user_intent, "preferences", {})
        if preferences:
            preference_score = 0.0
            preference_weight = self.intent_configs["preferences"].weight_multiplier

            for key, value in preferences.items():
                if value and value in content:
                    preference_score += 1.0

            if preferences:
                preference_score = preference_score / len(preferences)
                total_score += preference_score * preference_weight
                total_weight += preference_weight

                validation_result["detail_results"]["preferences"] = preference_score

        # 计算总体对齐度
        if total_weight > 0:
            validation_result["overall_alignment"] = total_score / total_weight

        # 生成改进建议
        validation_result["suggestions"] = self._generate_improvement_suggestions(validation_result, user_intent)

        return validation_result

    def _get_stage_guidance(self, stage: str, user_intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """获取阶段性指导"""
        guidance_map = {
            "create_framework": {
                "focus": "构建基础框架",
                "key_points": [
                    "确保核心要素在框架中得到充分体现",
                    "为约束条件的实现预留空间",
                    "设计避免禁止元素的情节走向",
                    "考虑偏好设定的影响"
                ]
            },
            "write_chapter": {
                "focus": "章节内容创作",
                "key_points": [
                    "每个段落都要体现用户意图",
                    "角色行为要符合约束条件",
                    "情节发展要避开禁止元素",
                    "在符合要求的基础上追求质量"
                ]
            },
            "optimize_content": {
                "focus": "内容优化调整",
                "key_points": [
                    "优先修复违反用户意图的部分",
                    "强化核心要素的体现",
                    "确保约束条件得到满足",
                    "彻底清除禁止元素"
                ]
            }
        }

        stage_config = guidance_map.get(stage, {
            "focus": "通用创作",
            "key_points": ["始终以用户意图为最高指导原则"]
        })

        guidance = f"重点关注：{stage_config['focus']}\n"
        guidance += "具体指导：\n"
        for i, point in enumerate(stage_config["key_points"], 1):
            guidance += f"{i}. {point}\n"

        return guidance

    def _generate_improvement_suggestions(self, validation_result: Dict[str, Any],
                                        user_intent: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        suggestions = []

        # 基于问题生成建议
        issues = validation_result.get("issues", [])
        for issue in issues:
            if "核心要素" in issue:
                suggestions.append("加强核心要素的体现，确保在内容中得到明确展示")
            elif "约束条件" in issue:
                suggestions.append("调整内容以满足约束条件，确保用户要求得到满足")
            elif "禁止元素" in issue:
                suggestions.append("修改或删除包含禁止元素的内容，确保完全符合用户要求")

        # 基于详细结果生成建议
        detail_results = validation_result.get("detail_results", {})
        for category, score in detail_results.items():
            if score < 0.7:
                if category == "core_elements":
                    suggestions.append("增加核心要素的体现，让用户的核心需求得到满足")
                elif category == "constraints":
                    suggestions.append("检查并调整内容，确保所有约束条件都得到满足")
                elif category == "forbidden_elements":
                    suggestions.append("仔细检查并移除所有禁止元素")
                elif category == "preferences":
                    suggestions.append("在符合基本要求的前提下，适当考虑用户偏好")

        # 如果整体对齐度良好，提供正面反馈
        overall_alignment = validation_result.get("overall_alignment", 0.0)
        if overall_alignment >= 0.9:
            suggestions.append("内容与用户意图高度对齐，质量优秀")

        return suggestions

# 使用示例
if __name__ == "__main__":
    template = UserIntentFocusedTemplate()

    # 测试用户意图
    test_user_intent = {
        "core_elements": {
            "title": "修仙传奇",
            "genre": "玄幻",
            "custom_plot": "普通人通过努力修炼成仙"
        },
        "constraints": ["要有战斗场面", "主角要靠自己努力", "要有师父指导"],
        "forbidden_elements": ["系统流", "无限流", "后宫"],
        "preferences": {
            "节奏": "中等",
            "风格": "热血"
        }
    }

    # 生成聚焦提示
    prompt = template.create_intent_focused_prompt(test_user_intent, "write_chapter", {})

    print("用户意图聚焦提示：")
    print(prompt)

    # 测试验证
    test_content = """
    这是一个修仙的故事，主角张三通过自己的努力修炼，最终成为了仙人。
    他遇到了一位好师父，学习了很多功法。他经历了多次战斗，战胜了敌人。
    """

    validation = template.validate_intent_alignment(test_content, test_user_intent)
    print("\n验证结果：")
    print(f"总体对齐度: {validation['overall_alignment']:.2f}")
    print(f"问题: {validation['issues']}")
    print(f"建议: {validation['suggestions']}")