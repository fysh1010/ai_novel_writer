#!/usr/bin/env python3
"""
情节控制师智能体 - 负责情节一致性和逻辑控制
"""

from .base_agent import BaseAgent
from .model_config import ModelConfig
from typing import Dict, List, Any

class PlotControllerAgent(BaseAgent):
    """情节控制师智能体"""
    
    def __init__(self, model_source: str = None, model_name: str = None):
        # 使用模型配置
        config = ModelConfig.get_model_config("plot_controller")
        if model_source is None:
            model_source = config["model_source"]
        if model_name is None:
            model_name = config["model_name"]
        
        super().__init__("情节控制师", model_source, model_name)
        self._init_knowledge_base()
    
    def _init_knowledge_base(self):
        """初始化知识库"""
        self.knowledge_base = {
            "plot_patterns": {
                "英雄之旅": ["启程", "启蒙", "回归"],
                "三幕结构": ["建置", "对抗", "解决"],
                "五幕结构": ["开端", "发展", "高潮", "结局", "尾声"]
            },
            "logic_rules": {
                "因果关系": "每个事件都要有合理的原因和结果",
                "时间逻辑": "时间顺序要合理，不能前后矛盾",
                "空间逻辑": "空间位置要合理，不能违反物理规律",
                "人物逻辑": "人物行为要符合其性格和动机"
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理情节控制请求"""
        try:
            request_type = input_data.get("type", "check_consistency")
            
            if request_type == "check_consistency":
                return self._check_plot_consistency(input_data)
            elif request_type == "manage_timeline":
                return self._manage_timeline(input_data)
            elif request_type == "check_logic":
                return self._check_logic(input_data)
            elif request_type == "plan_foreshadowing":
                return self._plan_foreshadowing(input_data)
            else:
                return {"error": f"未知请求类型: {request_type}"}
        except Exception as e:
            self.log(f"处理请求时发生异常: {str(e)}")
            return {
                "type": "error",
                "content": f"处理失败: {str(e)}",
                "error": str(e)
            }
    
    def _check_plot_consistency(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查情节一致性"""
        chapter_content = input_data.get("content", "")
        previous_chapters = input_data.get("previous_chapters", [])
        plot_timeline = input_data.get("plot_timeline", {})
        chapter_num = input_data.get("chapter_num", 1)
        custom_plot = input_data.get("custom_plot", "")
        
        consistency_prompt = f"""
请检查以下章节的情节一致性：

{'【用户背景设定】（检查是否符合）：' if custom_plot else ''}
{custom_plot if custom_plot else ''}

章节内容：
{chapter_content}

前面章节：
{previous_chapters}

情节时间线：
{plot_timeline}

章节号：第{chapter_num}章

请检查：
1. 【最重要】与用户背景设定的一致性：是否符合用户设定
2. 时间逻辑：时间顺序是否合理
3. 空间逻辑：空间位置是否合理
4. 因果关系：事件的前因后果是否合理
5. 人物逻辑：人物行为是否符合其设定
6. 情节连贯性：与前面章节是否连贯
7. 伏笔一致性：伏笔是否与设定一致

请指出：
- 与用户背景不符的地方（最重要）
- 一致性问题
- 逻辑漏洞
- 具体修改建议
- 优化方案

请以结构化的方式返回一致性检查结果。
"""
        
        self.log("正在检查情节一致性...")
        consistency_response = self.forward(consistency_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if consistency_response.is_success():
            consistency_check = consistency_response.get_content()
        else:
            consistency_check = "情节一致性检查失败"  # 如果检查失败，返回默认内容
        
        return {
            "type": "plot_consistency_check",
            "content": consistency_check,
            "chapter_num": chapter_num
        }
    
    def _manage_timeline(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """管理情节时间线"""
        current_timeline = input_data.get("current_timeline", {})
        new_events = input_data.get("new_events", [])
        chapter_num = input_data.get("chapter_num", 1)
        
        # 🎯 简化版情节时间线管理提示词
        timeline_prompt = f"""
请管理第{chapter_num}章的情节时间线。

📋 当前信息：
- 当前时间线：{current_timeline}
- 新事件：{new_events}

✨ 核心任务：
1️⃣ **时间轴更新** - 整合新事件
2️⃣ **逻辑检查** - 确保时间顺序合理
3️⃣ **事件关联** - 分析事件间关联
4️⃣ **冲突解决** - 处理时间冲突
5️⃣ **预留空间** - 为后续发展做准备

🎯 管理原则：
• 时间线清晰易懂
• 逻辑严密无矛盾
• 事件关联合理
• 保持发展空间

请用结构化方式返回管理结果。
"""
        
        self.log("正在管理情节时间线...")
        timeline_response = self.forward(timeline_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if timeline_response.is_success():
            timeline_management = timeline_response.get_content()
        else:
            timeline_management = "时间线管理失败"  # 如果管理失败，返回默认内容
        
        return {
            "type": "timeline_management",
            "content": timeline_management,
            "chapter_num": chapter_num
        }
    
    def _check_logic(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查逻辑"""
        chapter_content = input_data.get("content", "")
        world_rules = input_data.get("world_rules", {})
        character_profiles = input_data.get("character_profiles", {})
        chapter_num = input_data.get("chapter_num", 1)
        
        logic_prompt = f"""
请检查以下章节的逻辑：

章节内容：
{chapter_content}

世界观规则：
{world_rules}

角色档案：
{character_profiles}

章节号：第{chapter_num}章

请检查：
1. 世界观逻辑：是否符合世界观设定
2. 人物逻辑：人物行为是否合理
3. 事件逻辑：事件发展是否合理
4. 因果关系：因果关系是否明确
5. 逻辑漏洞：是否存在逻辑漏洞

请指出：
- 逻辑问题
- 不合理之处
- 修改建议
- 优化方案

请以结构化的方式返回逻辑检查结果。
"""
        
        self.log("正在检查逻辑...")
        logic_response = self.forward(logic_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if logic_response.is_success():
            logic_check = logic_response.get_content()
        else:
            logic_check = "逻辑检查失败"  # 如果检查失败，返回默认内容
        
        return {
            "type": "logic_check",
            "content": logic_check,
            "chapter_num": chapter_num
        }
    
    def _plan_foreshadowing(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """规划伏笔"""
        existing_foreshadowing = input_data.get("existing_foreshadowing", [])
        chapter_events = input_data.get("chapter_events", [])
        future_plans = input_data.get("future_plans", [])
        chapter_num = input_data.get("chapter_num", 1)
        
        foreshadowing_prompt = f"""
请规划伏笔：

现有伏笔：
{existing_foreshadowing}

章节事件：
{chapter_events}

未来计划：
{future_plans}

章节号：第{chapter_num}章

请规划：
1. 新伏笔的埋设：为未来事件埋下伏笔
2. 现有伏笔的推进：推进现有伏笔的发展
3. 伏笔的回收：回收到期的伏笔
4. 误导性伏笔：设置误导性伏笔
5. 伏笔网络：构建伏笔网络

要求：
- 伏笔要有层次感
- 设置误导性伏笔
- 为后续章节铺垫
- 确保逻辑连贯

请以结构化的方式返回伏笔规划结果。
"""
        
        self.log("正在规划伏笔...")
        foreshadowing_response = self.forward(foreshadowing_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if foreshadowing_response.is_success():
            foreshadowing_plan = foreshadowing_response.get_content()
        else:
            foreshadowing_plan = "伏笔规划失败"  # 如果规划失败，返回默认内容
        
        return {
            "type": "foreshadowing_plan",
            "content": foreshadowing_plan,
            "chapter_num": chapter_num
        }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
