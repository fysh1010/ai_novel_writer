#!/usr/bin/env python3
"""
主控智能体 - 协调所有智能体，控制整体创作流程
"""

import lazyllm
from .base_agent import BaseAgent
from .story_architect_simplified import StoryArchitectSimplified
from .character_manager_simplified import CharacterManagerSimplified
from .plot_controller_simplified import PlotControllerSimplified
from .optimizer_agent import OptimizerAgent
from .knowledge_base_agent import KnowledgeBaseAgent
from .compliance_advisor_agent import ComplianceAdvisorAgent
from core.story_intent_analyzer import StoryIntentAnalyzer
from core.smart_chapter_analyzer import get_chapter_analyzer
from .model_config import ModelConfig
from typing import Dict, List, Any

class MainControllerAgent(BaseAgent):
    """主控智能体"""

    def __init__(self, model_source: str = 'sensenova', model_name: str = 'DeepSeek-V3-1'):
        super().__init__("主控智能体", model_source, model_name)

        # 初始化子智能体 - 使用简化版本
        self.knowledge_base = KnowledgeBaseAgent()
        self.story_architect = StoryArchitectSimplified()
        self.character_manager = CharacterManagerSimplified()
        self.plot_controller = PlotControllerSimplified()
        self.optimizer = OptimizerAgent()
        self.compliance_advisor = ComplianceAdvisorAgent()

        # 初始化剧情意图分析器
        self.story_intent_analyzer = StoryIntentAnalyzer()

        # 初始化智能章节分析器（向量模型）
        self.chapter_analyzer = get_chapter_analyzer()

        # 智能体列表
        self.agents = {
            "knowledge_base": self.knowledge_base,
            "story_architect": self.story_architect,
            "character_manager": self.character_manager,
            "plot_controller": self.plot_controller,
            "optimizer": self.optimizer,
            "compliance_advisor": self.compliance_advisor
        }

    def _show_progress(self, stage: str, current: int, total: int, message: str = ""):
        """显示进度"""
        progress = f"[{current}/{total}]"
        self.log(f"📊 {stage} {progress} {message}")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理用户请求"""
        try:
            # 获取操作类型
            operation_type = input_data.get("type", "")

            if operation_type == "create_novel":
                return self._create_novel(input_data)
            elif operation_type == "write_chapter":
                return self._write_chapter(input_data)
            elif operation_type == "modify_chapter":
                return self._modify_chapter(input_data)
            elif operation_type == "continue_novel":
                return self._continue_novel(input_data)
            else:
                return {"error": f"未知的操作类型: {operation_type}"}

        except Exception as e:
            self.log(f"处理请求时发生错误: {str(e)}")
            return {"error": f"处理请求时发生错误: {str(e)}"}

    def _create_novel(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建新的小说"""
        self.log("开始创建小说...")

        # 引入用户意图解析器
        from core.intent_parser import IntentParser
        intent_parser = IntentParser()

        # 解析用户意图
        user_intent = intent_parser.parse_user_intent(input_data)
        self.log(f"用户意图解析完成: {intent_parser.get_intent_summary(user_intent)}")

        # 验证用户意图一致性
        consistency_issues = intent_parser.validate_intent_consistency(user_intent)
        if consistency_issues:
            self.log(f"⚠️ 用户意图存在一致性 issues: {consistency_issues}")

        # 引入权重管理器
        from core.weight_manager import WeightManager
        weight_manager = WeightManager()

        # 构建智能体建议
        agent_outputs = [
            {"agent_name": "user_background", "output": f"用户背景: {user_intent.core_elements}"}
        ]

        # 计算权重
        weights = weight_manager.calculate_weights(agent_outputs, user_intent)
        self.log(f"权重分配: {weight_manager.get_weight_summary(weights)}")

        # 应用过滤器
        filtered_suggestions = weight_manager.apply_priority_filter(
            {"user_background": agent_outputs[0]["output"]},
            weights
        )

        # 提取核心要素
        title = user_intent.core_elements.get('title', '未命名小说')
        genre = user_intent.core_elements.get('genre', '其他')
        custom_plot = user_intent.core_elements.get('custom_plot', '')

        # 生成故事框架
        self.log("故事架构师正在构建故事框架...")
        story_framework_result = self.story_architect.process({
            "type": "create_framework",
            "title": title,
            "genre": genre,
            "custom_plot": custom_plot,
            "user_intent": user_intent
        })

        if "error" in story_framework_result:
            return story_framework_result

        story_framework = story_framework_result["content"]

        # 生成角色系统
        self.log("角色管理师正在构建角色系统...")
        character_system_result = self.character_manager.process({
            "type": "create_system",
            "story_framework": story_framework,
            "user_intent": user_intent
        })

        if "error" in character_system_result:
            return character_system_result

        character_system = character_system_result["content"]

        # 生成情节时间线
        self.log("情节控制师正在构建情节时间线...")
        plot_timeline_result = self.plot_controller.process({
            "type": "create_timeline",
            "story_framework": story_framework,
            "character_system": character_system,
            "user_intent": user_intent
        })

        if "error" in plot_timeline_result:
            return plot_timeline_result

        plot_timeline = plot_timeline_result["content"]

        # 整合结果
        novel_data = {
            "title": title,
            "genre": genre,
            "story_framework": story_framework,
            "character_system": character_system,
            "plot_timeline": plot_timeline,
            "user_intent": user_intent,
            "metadata": {
                "agent_weights": weights,
                "filtered_suggestions": filtered_suggestions,
                "created_at": self._get_timestamp()
            }
        }

        self.log("✅ 小说创建完成！")
        return {
            "type": "novel_created",
            "data": novel_data
        }

    def _write_chapter(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """创作章节 - 使用简化生成器"""
        self.log("开始创作章节（使用简化生成器）...")

        # 引入简化章节生成器
        from simplified_chapter_writer import SimplifiedChapterWriter
        simplified_writer = SimplifiedChapterWriter(self)

        # 使用简化生成器创建章节
        result = simplified_writer.write_chapter_simplified(input_data)

        return result

    def _modify_chapter(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """修改章节"""
        self.log("开始修改章节...")

        chapter_num = input_data.get("chapter_num", 1)
        current_content = input_data.get("current_content", "")
        modification_suggestions = input_data.get("modification_suggestions", "")
        story_framework = input_data.get("story_framework", "")
        character_system = input_data.get("character_system", "")
        plot_timeline = input_data.get("plot_timeline", {})

        # 设置上下文
        context = {
            "chapter_num": chapter_num,
            "current_content": current_content,
            "story_framework": story_framework,
            "character_system": character_system,
            "plot_timeline": plot_timeline
        }

        for agent in self.agents.values():
            agent.set_context(context)

        # 生成修改后的章节内容
        modified_content = self._generate_chapter_content({
            "chapter_num": chapter_num,
            "story_framework": story_framework,
            "character_system": character_system,
            "plot_timeline": plot_timeline,
            "current_content": current_content,
            "modification_suggestions": modification_suggestions,
            "is_modification": True
        })

        # 提取章节标题和正文
        chapter_title, chapter_content = self._extract_title_and_content(modified_content)

        # 生成章节摘要
        chapter_summary = self._generate_chapter_summary(chapter_content)

        # 整合结果
        chapter_data = {
            "chapter_num": chapter_num,
            "title": chapter_title,
            "content": chapter_content,
            "summary": chapter_summary,
            "modification_suggestions": modification_suggestions,
            "metadata": {
                "modified_at": self._get_timestamp()
            }
        }

        self.log("✅ 章节修改完成！")
        return {
            "type": "chapter_modified",
            "data": chapter_data
        }

    def _continue_novel(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """继续小说创作"""
        self.log("开始继续小说创作...")

        # 获取小说信息
        novel_data = input_data.get("novel_data", {})
        target_chapter = input_data.get("target_chapter", 1)

        # 检查是否需要创作新章节
        existing_chapters = novel_data.get("chapters", [])

        if len(existing_chapters) >= target_chapter:
            return {"error": f"目标章节 {target_chapter} 已存在"}

        # 创作新章节
        chapter_input = {
            "type": "write_chapter",
            "chapter_num": target_chapter,
            "story_framework": novel_data.get("story_framework", ""),
            "character_system": novel_data.get("character_system", ""),
            "plot_timeline": novel_data.get("plot_timeline", ""),
            "previous_chapters": existing_chapters,
            "user_intent": novel_data.get("user_intent", {})
        }

        return self._write_chapter(chapter_input)

    def _generate_chapter_content(self, params: Dict[str, Any]) -> str:
        """生成章节内容"""
        # 构建生成提示
        prompt = self._build_chapter_prompt(params)

        # 调用模型生成内容
        response = self.chat.forward(prompt)

        return response

    def _build_chapter_prompt(self, params: Dict[str, Any]) -> str:
        """构建章节生成提示"""
        chapter_num = params.get("chapter_num", 1)
        story_framework = params.get("story_framework", "")
        character_system = params.get("character_system", "")
        plot_timeline = params.get("plot_timeline", "")
        previous_chapters = params.get("previous_chapters", [])
        custom_prompt = params.get("custom_prompt", "")

        prompt = f"""
请创作第{chapter_num}章的内容。

故事框架：
{story_framework}

角色系统：
{character_system}

情节时间线：
{plot_timeline}

"""

        if previous_chapters:
            prompt += "前面章节摘要：\n"
            for ch in previous_chapters[-3:]:  # 只显示最近3章
                prompt += f"第{ch['chapter_num']}章：{ch.get('summary', '')}\n"
            prompt += "\n"

        if custom_prompt:
            prompt += f"特殊要求：\n{custom_prompt}\n"

        prompt += """
请创作完整的章节内容，要求：
1. 保持与前面章节的连贯性
2. 符合故事框架和角色设定
3. 情节发展自然流畅
4. 字数控制在2000-3000字
5. **禁止使用"一、二、三、四..."等数字分段**
6. **禁止使用"第一章"、"第二节"等标题分段**
7. **使用自然段落过渡，保持小说章节的自然流畅性**

请直接输出章节内容，不需要其他说明。
"""

        return prompt

    def _generate_chapter_summary(self, chapter_content: str) -> str:
        """生成章节摘要"""
        prompt = f"""
请为以下章节内容生成一个简短的摘要（100字以内）：

{chapter_content[:1000]}

摘要要求：
1. 概括主要情节
2. 语言简洁明了
3. 不超过100字

请直接输出摘要内容：
"""

        response = self.chat.forward(prompt)
        return response.strip()

    def _extract_title_and_content(self, content: str) -> tuple:
        """提取章节标题和内容"""
        lines = content.strip().split('\n')
        title = ""
        content_lines = []
        title_found = False

        # 查找标题模式
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # 如果已经找到标题，后面的都是内容
            if title_found:
                content_lines.append(line)
                continue
            
            # 跳过空行
            if not line_stripped:
                continue
                    
            # 检查是否是标题（短行，可能是标题）
            if len(line_stripped) <= 50:
                # 检查是否包含章节标识
                if any(keyword in line_stripped for keyword in ['第', '章', '节', '回', '集']):
                    title = line_stripped
                    title_found = True
                    continue
                # 如果第一行很短，也可能是标题
                elif i == 0 and len(line_stripped) <= 30:
                    title = line_stripped
                    title_found = True
                    continue
            
            # 如果不是标题，就是内容
            content_lines.append(line)

        # 如果没有找到合适的标题，使用AI生成一个
        if not title:
            title = self._generate_chapter_title(content_lines)

        content = '\n'.join(content_lines)

        return title, content

    def _generate_chapter_title(self, content_lines: List[str]) -> str:
        """使用AI生成章节标题"""
        # 取内容的前200字作为生成依据
        content_sample = '\n'.join(content_lines[:5])[:200]
        
        prompt = f"""
请根据以下小说内容，生成一个简洁有力的章节标题（不超过15字）：

内容：
{content_sample}

要求：
1. 标题要简洁有力，体现章节核心内容
2. 符合网文风格，有吸引力
3. 不超过15个字符
4. 不要包含"第X章"等字样

请直接输出标题：
"""
        
        try:
            response = self.chat.forward(prompt)
            title = response.strip()
            # 清理标题，移除可能的引号等
            title = title.strip('"\'""\'\'')
            if len(title) > 15:
                title = title[:15]
            return title or "未命名章节"
        except Exception:
            # 如果AI生成失败，使用内容前几个字
            first_line = content_lines[0] if content_lines else ""
            if len(first_line) > 15:
                return first_line[:15] + "..."
            return first_line or "未命名章节"

    def optimize_chapter(self, project_data: Dict[str, Any], chapter_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        优化章节内容

        Args:
            project_data: 项目数据，包含故事框架、角色系统等
            chapter_data: 章节数据，包含标题、内容等

        Returns:
            Dict[str, Any]: 优化后的章节数据
        """
        self.log("正在优化章节内容...")

        chapter_content = chapter_data.get("content", "")
        if not chapter_content:
            return {
                "success": False,
                "error": "章节内容为空",
                "content": "",
                "data": chapter_data
            }

        # 使用优化师进行内容优化
        try:
            optimization_result = self.optimizer.process({
                "type": "optimize_content",
                "content": chapter_content,
                "optimization_goals": ["提升文笔", "增强情感", "改善节奏", "消除AI痕迹"]
            })

            if "error" in optimization_result:
                self.log(f"⚠️ 优化师处理失败: {optimization_result['error']}")
                return {
                    "success": False,
                    "error": f"优化师处理失败: {optimization_result['error']}",
                    "content": chapter_content,
                    "data": chapter_data
                }

            optimized_content = optimization_result.get("content", chapter_content)

            # 提取新的标题和内容
            new_title, new_content = self._extract_title_and_content(optimized_content)

            # 生成新的摘要
            new_summary = self._generate_chapter_summary(new_content)

            optimized_chapter = chapter_data.copy()
            optimized_chapter.update({
                "title": new_title,
                "content": new_content,
                "summary": new_summary,
                "metadata": {
                    **optimized_chapter.get("metadata", {}),
                    "optimized_at": self._get_timestamp(),
                    "optimization_applied": True
                }
            })

            self.log("✅ 章节优化完成")
            return {
                "success": True,
                "content": new_content,
                "title": new_title,
                "summary": new_summary,
                "data": optimized_chapter
            }

        except Exception as e:
            self.log(f"⚠️ 章节优化异常: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "content": chapter_data.get("content", ""),
                "data": chapter_data
            }

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _safe_agent_call(self, agent, input_data: Dict[str, Any], agent_name: str = "智能体") -> Dict[str, Any]:
        """安全的智能体调用包装器"""
        try:
            result = agent.process(input_data)
            if "error" in result:
                self.log(f"⚠️ {agent_name}处理失败: {result['error']}")
                return {"error": result["error"]}
            return result
        except Exception as e:
            self.log(f"⚠️ {agent_name}调用异常: {str(e)}")
            return {"error": f"{agent_name}调用异常: {str(e)}"}

# 工厂函数
def create_main_controller():
    """创建主控智能体实例"""
    return MainControllerAgent()