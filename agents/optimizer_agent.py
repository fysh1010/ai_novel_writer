#!/usr/bin/env python3
"""
优化师智能体 - 负责网文专业优化和质量提升
"""

from .base_agent import BaseAgent
from .model_config import ModelConfig
from typing import Dict, List, Any

class OptimizerAgent(BaseAgent):
    """优化师智能体"""
    
    def __init__(self, model_source: str = None, model_name: str = None):
        # 使用模型配置
        config = ModelConfig.get_model_config("optimizer")
        if model_source is None:
            model_source = config["model_source"]
        if model_name is None:
            model_name = config["model_name"]
        
        super().__init__("优化师", model_source, model_name)
        self._init_knowledge_base()
    
    def _init_knowledge_base(self):
        """初始化知识库"""
        self.knowledge_base = {
            "platform_standards": {
                "起点": {
                    "style": "传统网文风格，注重爽点",
                    "length": "每章2000-3000字",
                    "rhythm": "快节奏，多爽点",
                    "language": "通俗易懂，有代入感"
                },
                "晋江": {
                    "style": "文艺风格，注重情感",
                    "length": "每章1500-2500字",
                    "rhythm": "慢节奏，重情感",
                    "language": "优美流畅，有文学性"
                },
                "番茄": {
                    "style": "轻松风格，注重娱乐",
                    "length": "每章1000-2000字",
                    "rhythm": "快节奏，多反转",
                    "language": "简单直接，有吸引力"
                }
            },
            "quality_metrics": {
                "readability": "语言流畅，易于理解",
                "engagement": "情节吸引，有代入感",
                "consistency": "逻辑一致，前后连贯",
                "originality": "有创新，避免套路"
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理优化请求"""
        request_type = input_data.get("type", "optimize_content")
        
        if request_type == "optimize_content":
            return self._optimize_content(input_data)
        elif request_type == "assess_quality":
            return self._assess_quality(input_data)
        elif request_type == "eliminate_ai_traces":
            return self._eliminate_ai_traces(input_data)
        elif request_type == "platform_adaptation":
            return self._platform_adaptation(input_data)
        else:
            return {"error": f"未知请求类型: {request_type}"}
    
    def _optimize_content(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """优化内容 - 作为最后一道防线纠正偏离"""
        chapter_content = input_data.get("content", "")
        genre = input_data.get("genre", "")
        platform = input_data.get("platform", "起点")
        optimization_goals = input_data.get("optimization_goals", [])
        user_custom_plot = input_data.get("user_custom_plot", "")
        strict_user_input = input_data.get("strict_user_input", True)
        chapter_num = input_data.get("chapter_num", 0)
        
        # 获取平台标准
        platform_standards = self.knowledge_base["platform_standards"].get(platform, {})
        
        # 内容审核机制
        content_audit = self._audit_content_against_user_background(chapter_content, user_custom_plot, strict_user_input)
        
        # 第一章特殊提示
        first_chapter_note = ""
        if chapter_num == 1:
            first_chapter_note = """
【第一章特别注意】：
- 如果内容写的是"穿越过程"但用户背景没提穿越，必须删除
- 如果主角名字不对，必须改正
- 如果主角身份不对（如用户说河神，但写的是书生），必须改正
- 如果添加了用户未提及的元素（系统、金手指等），必须删除
"""
        
        optimization_prompt = f"""
你是最后一道防线，负责优化内容，同时纠正所有偏离用户背景的错误。

【最高优先级】用户背景设定（必须严格遵循）：
{user_custom_plot if user_custom_plot else '无特殊要求'}

{'【严格模式】如果内容偏离用户背景，必须强制拉回。不得改变用户设定的核心元素。' if strict_user_input else ''}

【内容审核和修正要求】：
- 检查生成内容是否严格符合用户背景设定
- 如果发现偏离用户背景，必须立即修正
- 确保生成内容完全符合用户需求
- 不得添加用户未提及的元素
- 不得改变用户设定的核心内容

【文学性和艺术性要求】：
- 文笔要优美流畅，有诗意表达
- 语言要有美感，追求文学价值
- 情感要深刻动人，触动读者内心
- 创意要独特新颖，避免模板化
- 整体要有艺术美感，追求文学深度

【情感渲染和人性挖掘】：
- 人物要有丰富的情感层次
- 对话要有情感色彩和温度
- 情节要有人性深度和真实感
- 冲突要有人性基础，不能只是技术问题
- 追求读者情感共鸣和内心触动

{first_chapter_note}

章节内容：
{chapter_content}

小说类型：{genre}
目标平台：{platform}
优化目标：{optimization_goals}

平台标准：
{platform_standards}

## 【最重要】偏离检查与纠正：

请先检查内容是否偏离用户背景：
1. 主角名字是否正确？
2. 主角身份是否符合用户背景？（如用户说河神，不能写成书生）
3. 是否添加了用户未提及的元素？（如系统、穿越、金手指）
4. 世界观是否符合？（如用户说洪荒，不能写成古代）
5. 主角能力是否符合？（用户设定的主能力和辅助能力）

**如果发现偏离，必须在优化时强制拉回，改正所有错误！**

## 优化要求：

### 1. 语言优化
- 提升语言流畅性
- 增强代入感
- 符合{genre}类型风格

### 2. 节奏优化
- 调整节奏快慢
- 增加爽点密度
- 优化情绪起伏

### 3. 结构优化
- 优化章节结构
- 调整段落安排
- 增强逻辑连贯性

### 4. 内容优化
- 增强情节吸引力
- 提升人物魅力
- 优化对话质量

### 5. 消除AI痕迹
- 避免机械化表达
- 增加人性化元素
- 提升自然度

## 核心原则（绝对不能违反）：

- 【最高优先】必须符合用户背景设定，这是不可动摇的原则
- 【纠偏职责】如果内容偏离，必须强制拉回
- 【不得改变】用户设定的主角名字、身份、能力、背景
- 【不得添加】用户未提及的元素（系统、穿越等）
- 【不得删除】用户明确提及的元素

## 格式要求（重要）：
- **禁止使用"一、二、三、四..."等数字分段**
- **禁止使用"第一章"、"第二节"等标题分段**
- **使用自然段落过渡，不要人为分段**
- **保持小说章节的自然流畅性**

请直接返回优化后的章节内容（如果有偏离，必须纠正后再返回）。
"""
        
        self.log("正在优化章节内容...")
        optimized_response = self.forward(optimization_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if optimized_response.is_success():
            optimized_content = optimized_response.get_content()
        else:
            optimized_content = chapter_content  # 如果优化失败，返回原内容
        
        return {
            "type": "optimized_content",
            "content": optimized_content,
            "metadata": {
                "genre": genre,
                "platform": platform,
                "optimization_goals": optimization_goals,
                "optimized_at": self._get_timestamp()
            }
        }
    
    def _assess_quality(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """评估质量"""
        chapter_content = input_data.get("content", "")
        genre = input_data.get("genre", "")
        platform = input_data.get("platform", "起点")
        
        assessment_prompt = f"""
请评估以下章节的质量：

章节内容：
{chapter_content}

小说类型：{genre}
目标平台：{platform}

请从以下维度评估：

## 1. 可读性评估
- 语言流畅度
- 表达清晰度
- 理解难度
- 阅读体验

## 2. 吸引力评估
- 情节吸引力
- 人物魅力
- 悬念设置
- 代入感

## 3. 一致性评估
- 逻辑一致性
- 人物一致性
- 风格一致性
- 前后连贯性

## 4. 创新性评估
- 情节创新
- 人物创新
- 表达创新
- 整体创新

## 5. 平台适配性
- 是否符合{platform}标准
- 是否符合{genre}类型
- 是否符合读者期待
- 是否符合商业价值

请给出：
- 各维度评分（1-10分）
- 具体问题分析
- 改进建议
- 优化方向

请以结构化的方式返回质量评估结果。
"""
        
        self.log("正在评估章节质量...")
        quality_response = self.forward(assessment_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if quality_response.is_success():
            quality_assessment = quality_response.get_content()
        else:
            quality_assessment = "质量评估失败"  # 如果评估失败，返回默认内容
        
        return {
            "type": "quality_assessment",
            "content": quality_assessment,
            "metadata": {
                "genre": genre,
                "platform": platform,
                "assessed_at": self._get_timestamp()
            }
        }
    
    def _eliminate_ai_traces(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """消除AI痕迹"""
        chapter_content = input_data.get("content", "")
        genre = input_data.get("genre", "")
        
        elimination_prompt = f"""
请消除以下章节中的AI痕迹：

章节内容：
{chapter_content}

小说类型：{genre}

请消除以下AI痕迹：

## 1. 语言痕迹
- 避免过于正式的表达
- 增加口语化元素
- 提升自然度
- 符合网文习惯

## 2. 结构痕迹
- 避免过于规整的结构
- 增加变化和起伏
- 提升自然感
- 符合阅读习惯

## 3. 内容痕迹
- 避免过于完美的情节
- 增加人性化元素
- 提升真实感
- 符合生活逻辑

## 4. 表达痕迹
- 避免机械化描述
- 增加情感色彩
- 提升生动性
- 符合{genre}类型

要求：
- 保持原有情节
- 提升自然度
- 消除AI痕迹
- 增强人性化

请直接返回消除AI痕迹后的章节内容。
"""
        
        self.log("正在消除AI痕迹...")
        natural_response = self.forward(elimination_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if natural_response.is_success():
            natural_content = natural_response.get_content()
        else:
            natural_content = content  # 如果处理失败，返回原内容
        
        return {
            "type": "natural_content",
            "content": natural_content,
            "metadata": {
                "genre": genre,
                "processed_at": self._get_timestamp()
            }
        }
    
    def _platform_adaptation(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """平台适配"""
        chapter_content = input_data.get("content", "")
        source_platform = input_data.get("source_platform", "起点")
        target_platform = input_data.get("target_platform", "晋江")
        genre = input_data.get("genre", "")
        
        # 获取平台标准
        source_standards = self.knowledge_base["platform_standards"].get(source_platform, {})
        target_standards = self.knowledge_base["platform_standards"].get(target_platform, {})
        
        adaptation_prompt = f"""
请将以下章节从{source_platform}适配到{target_platform}：

章节内容：
{chapter_content}

源平台标准：
{source_standards}

目标平台标准：
{target_standards}

小说类型：{genre}

请进行以下适配：

## 1. 风格适配
- 调整语言风格
- 改变表达方式
- 适配平台特色
- 符合读者习惯

## 2. 节奏适配
- 调整节奏快慢
- 改变爽点密度
- 适配平台偏好
- 符合阅读习惯

## 3. 内容适配
- 调整内容重点
- 改变表达角度
- 适配平台特色
- 符合读者期待

## 4. 长度适配
- 调整章节长度
- 改变段落安排
- 适配平台标准
- 符合阅读习惯

要求：
- 保持原有情节
- 适配平台特色
- 符合读者习惯
- 提升平台适配性

请直接返回适配后的章节内容。
"""
        
        self.log(f"正在从{source_platform}适配到{target_platform}...")
        adapted_response = self.forward(adaptation_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if adapted_response.is_success():
            adapted_content = adapted_response.get_content()
        else:
            adapted_content = content  # 如果处理失败，返回原内容
        
        return {
            "type": "adapted_content",
            "content": adapted_content,
            "metadata": {
                "source_platform": source_platform,
                "target_platform": target_platform,
                "genre": genre,
                "adapted_at": self._get_timestamp()
            }
        }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _audit_content_against_user_background(self, content: str, user_background: str, strict_mode: bool) -> Dict[str, Any]:
        """审核内容是否符合用户背景设定"""
        if not user_background:
            return {"status": "no_background", "issues": []}
        
        issues = []
        
        # 检查是否偏离用户背景
        if "穿越" in content and "穿越" not in user_background:
            issues.append("内容包含穿越元素，但用户背景未提及")
        
        if "古代" in content and "古代" not in user_background:
            issues.append("内容涉及古代，但用户背景未提及")
        
        if "洪荒" in user_background and "洪荒" not in content:
            issues.append("用户背景是洪荒，但内容未体现洪荒元素")
        
        if "代码" in user_background and "代码" not in content:
            issues.append("用户背景涉及代码，但内容未体现代码元素")
        
        # 检查是否添加了用户未提及的元素
        if "系统" in content and "系统" not in user_background:
            issues.append("内容添加了系统元素，但用户背景未提及")
        
        if "金手指" in content and "金手指" not in user_background:
            issues.append("内容添加了金手指元素，但用户背景未提及")
        
        return {
            "status": "audit_complete",
            "issues": issues,
            "needs_correction": len(issues) > 0
        }
