#!/usr/bin/env python3
"""
精简章节模板 - 高效的章节生成模板体系
专注于用户意图和核心创作，减少冗余复杂性
"""

from typing import Dict, Any, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ChapterTemplate:
    """章节模板"""
    name: str
    structure: List[str]
    key_elements: List[str]
    tips: List[str]

class SimplifiedChapterTemplate:
    """精简章节模板管理器"""

    def __init__(self):
        # 基础模板配置
        self.templates = {
            "开端": ChapterTemplate(
                name="开端章节",
                structure=[
                    "场景引入（1-2段）：建立时间和地点",
                    "主角登场（1-2段）：介绍主角状态",
                    "初始事件（1-2段）：触发故事的事件",
                    "悬念设置（1段）：为后续发展埋下伏笔"
                ],
                key_elements=[
                    "世界观基础设定",
                    "主角基本形象",
                    "故事起点",
                    "读者兴趣点"
                ],
                tips=[
                    "控制信息量，避免设定堆砌",
                    "聚焦主角，建立情感连接",
                    "设置合理的悬念，激发阅读兴趣",
                    "语言简洁，节奏明快"
                ]
            ),
            "发展": ChapterTemplate(
                name="发展章节",
                structure=[
                    "承接上文（1段）：连接前章情节",
                    "冲突展开（2-3段）：主要矛盾的发展",
                    "角色互动（2-3段）：人物关系推进",
                    "情节推进（1-2段）：向目标发展"
                ],
                key_elements=[
                    "情节连贯性",
                    "冲突升级",
                    "角色发展",
                    "节奏控制"
                ],
                tips=[
                    "保持与前文的逻辑连接",
                    "逐步提升冲突强度",
                    "通过行动展现角色性格",
                    "控制节奏，张弛有度"
                ]
            ),
            "高潮": ChapterTemplate(
                name="高潮章节",
                structure=[
                    "紧张铺垫（1-2段）：营造紧张氛围",
                    "关键对抗（3-4段）：核心冲突爆发",
                    "转折变化（1-2段）：重要情节转折",
                    "结果呈现（1段）：对抗的直接结果"
                ],
                key_elements=[
                    "情绪张力",
                    "冲突顶点",
                    "关键转折",
                    "冲击力营造"
                ],
                tips=[
                    "充分调动读者情绪",
                    "确保冲突的合理性和必然性",
                    "转折要有说服力",
                    "注重画面感和冲击力"
                ]
            ),
            "结局": ChapterTemplate(
                name="结局章节",
                structure=[
                    "余波处理（1-2段）：高潮后的直接后果",
                    "问题解决（2-3段）：主要矛盾的解决",
                    "角色归宿（1-2段）：人物的最终状态",
                    "主题升华（1段）：故事意义的总结"
                ],
                key_elements=[
                    "收束完整性",
                    "情感满足",
                    "主题表达",
                    "余韵回味"
                ],
                tips=[
                    "确保主要问题得到合理解决",
                    "给予读者情感满足",
                    "自然表达主题思想",
                    "留下适当的回味空间"
                ]
            )
        }

        # 类型特色配置
        self.genre_features = {
            "玄幻": {
                "elements": ["修炼体系", "境界划分", "法宝神器", "宗门势力"],
                "conflicts": ["修炼竞争", "宗门恩怨", "正邪对立", "天劫考验"],
                "satisfaction": ["境界突破", "实力碾压", "宝物获得", "打脸反转"]
            },
            "都市": {
                "elements": ["现代生活", "商业竞争", "人际关系", "社会现实"],
                "conflicts": ["商业竞争", "感情纠葛", "社会矛盾", "个人成长"],
                "satisfaction": ["事业成功", "感情圆满", "社会认可", "人生逆袭"]
            },
            "历史": {
                "elements": ["历史背景", "政治斗争", "军事战争", "文化传承"],
                "conflicts": ["政治斗争", "军事冲突", "文化冲突", "个人命运"],
                "satisfaction": ["政治成功", "军事胜利", "文化影响", "历史留名"]
            },
            "科幻": {
                "elements": ["科技设定", "未来世界", "外星文明", "时空概念"],
                "conflicts": ["科技竞争", "星际战争", "时空危机", "文明冲突"],
                "satisfaction": ["科技突破", "文明胜利", "探索发现", "问题解决"]
            }
        }

    def get_template(self, stage: str, chapter_num: int = 1) -> ChapterTemplate:
        """
        获取章节模板

        Args:
            stage: 章节阶段（开端/发展/高潮/结局）
            chapter_num: 章节号

        Returns:
            ChapterTemplate: 章节模板
        """
        # 根据章节号自动判断阶段
        if stage not in self.templates:
            stage = self._determine_stage(chapter_num)

        template = self.templates[stage]

        # 根据章节号微调模板
        return self._adjust_template_by_chapter(template, chapter_num)

    def generate_chapter_outline(self, stage: str, chapter_num: int,
                                user_intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        生成章节大纲

        Args:
            stage: 章节阶段
            chapter_num: 章节号
            user_intent: 用户意图
            context: 上下文信息

        Returns:
            str: 章节大纲
        """
        template = self.get_template(stage, chapter_num)

        # 获取类型特色
        core_elements = getattr(user_intent, "core_elements", {})
        genre = core_elements.get("genre", "")
        genre_features = self.genre_features.get(genre, {})

        # 构建大纲
        outline = f"第{chapter_num}章大纲（{template.name}）：\n\n"

        for i, structure_item in enumerate(template.structure, 1):
            outline += f"{i}. {structure_item}\n"

        # 添加类型特色要求
        if genre_features:
            outline += f"\n类型特色要求（{genre}）：\n"
            elements = genre_features.get("elements", [])
            if elements:
                outline += f"- 体现元素：{', '.join(elements[:3])}\n"

            conflicts = genre_features.get("conflicts", [])
            if conflicts:
                outline += f"- 冲突类型：{', '.join(conflicts[:2])}\n"

            satisfaction = genre_features.get("satisfaction", [])
            if satisfaction:
                outline += f"- 爽点设计：{', '.join(satisfaction[:2])}\n"

        # 添加用户约束
        constraints = getattr(user_intent, "constraints", [])
        if constraints:
            outline += f"\n用户约束：{', '.join(constraints)}\n"

        # 添加禁止元素
        forbidden_elements = getattr(user_intent, "forbidden_elements", [])
        if forbidden_elements:
            outline += f"\n禁止元素：{', '.join(forbidden_elements)}\n"

        # 添加创作建议
        outline += "\n创作建议：\n"
        for tip in template.tips:
            outline += f"- {tip}\n"

        return outline

    def build_generation_prompt(self, stage: str, chapter_num: int,
                              user_intent: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        构建生成提示

        Args:
            stage: 章节阶段
            chapter_num: 章节号
            user_intent: 用户意图
            context: 上下文信息

        Returns:
            str: 生成提示
        """
        # 获取大纲
        outline = self.generate_chapter_outline(stage, chapter_num, user_intent, context)

        # 构建完整提示
        prompt = f"""请根据以下大纲创作第{chapter_num}章：

{outline}

上下文信息：
"""

        # 添加故事框架
        story_framework = context.get("story_framework", "")
        if story_framework:
            prompt += f"故事框架：{story_framework[:200]}...\n"

        # 添加角色系统
        character_system = context.get("character_system", "")
        if character_system:
            prompt += f"角色系统：{character_system[:200]}...\n"

        # 添加前面章节摘要
        previous_chapters = context.get("previous_chapters", [])
        if previous_chapters:
            prompt += "前面章节摘要：\n"
            for ch in previous_chapters[-3:]:  # 最近3章
                prompt += f"第{ch['chapter_num']}章：{ch.get('summary', '')}\n"

        # 添加自定义提示
        custom_prompt = context.get("custom_prompt", "")
        if custom_prompt:
            prompt += f"\n特殊要求：{custom_prompt}\n"

        prompt += """
创作要求：
1. 严格按照大纲结构进行创作
2. 确保情节连贯，逻辑清晰
3. 人物性格保持一致
4. 语言生动自然，避免AI痕迹
5. 控制字数在2000-3000字之间

请直接创作章节内容，不需要其他说明：
"""

        return prompt

    def _determine_stage(self, chapter_num: int) -> str:
        """根据章节号判断阶段"""
        if chapter_num <= 3:
            return "开端"
        elif chapter_num <= 15:
            return "发展"
        elif chapter_num <= 25:
            return "高潮"
        else:
            return "结局"

    def _adjust_template_by_chapter(self, template: ChapterTemplate, chapter_num: int) -> ChapterTemplate:
        """根据章节号微调模板"""
        adjusted_template = ChapterTemplate(
            name=template.name,
            structure=template.structure.copy(),
            key_elements=template.key_elements.copy(),
            tips=template.tips.copy()
        )

        # 根据具体章节号添加特殊提示
        if chapter_num == 1:
            adjusted_template.tips.append("首章特别注意事项：开篇要吸引人，快速建立读者兴趣")
        elif chapter_num % 10 == 0:  # 每10章的节点
            adjusted_template.tips.append(f"第{chapter_num}章节点：适合设置小高潮或重要转折")

        return adjusted_template

# 使用示例
if __name__ == "__main__":
    template_manager = SimplifiedChapterTemplate()

    # 测试用户意图
    test_user_intent = {
        "core_elements": {
            "title": "测试小说",
            "genre": "玄幻",
            "custom_plot": "普通人修炼成神"
        },
        "constraints": ["要有战斗场面", "主角要成长"],
        "forbidden_elements": ["系统流", "无限流"]
    }

    # 测试上下文
    test_context = {
        "story_framework": "玄幻世界，修炼为尊",
        "character_system": "主角：张三，性格坚毅",
        "previous_chapters": [],
        "custom_prompt": "注重战斗描写"
    }

    # 生成第1章的大纲和提示
    outline = template_manager.generate_chapter_outline("开端", 1, test_user_intent, test_context)
    prompt = template_manager.build_generation_prompt("开端", 1, test_user_intent, test_context)

    print("章节大纲：")
    print(outline)
    print("\n生成提示：")
    print(prompt)