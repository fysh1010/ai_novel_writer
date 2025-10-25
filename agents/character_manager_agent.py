#!/usr/bin/env python3
"""
角色管理师智能体 - 负责角色管理和一致性控制
"""

from .base_agent import BaseAgent
from .model_config import ModelConfig
from typing import Dict, List, Any

class CharacterManagerAgent(BaseAgent):
    """角色管理师智能体"""
    
    def __init__(self, model_source: str = None, model_name: str = None):
        # 使用模型配置
        config = ModelConfig.get_model_config("character_manager")
        if model_source is None:
            model_source = config["model_source"]
        if model_name is None:
            model_name = config["model_name"]
        
        super().__init__("角色管理师", model_source, model_name)
        self._init_knowledge_base()
    
    def _init_knowledge_base(self):
        """初始化知识库"""
        self.knowledge_base = {
            "character_types": {
                "主角": {
                    "traits": ["现代思维", "独特认知", "成长潜力", "冲突性"],
                    "development": ["认知颠覆", "能力提升", "关系变化", "理念转变"],
                    "dialogue_style": "符合现代人思维，有独特见解"
                },
                "反派": {
                    "traits": ["复杂动机", "立体性格", "合理行为", "成长性"],
                    "development": ["动机揭示", "关系变化", "理念冲突", "最终对决"],
                    "dialogue_style": "符合身份地位，有独特个性"
                },
                "配角": {
                    "traits": ["功能明确", "性格鲜明", "关系复杂", "成长空间"],
                    "development": ["功能发挥", "关系发展", "性格展现", "作用变化"],
                    "dialogue_style": "符合身份性格，有个人特色"
                }
            },
            "relationship_types": {
                "师徒": ["传承", "成长", "冲突", "和解"],
                "朋友": ["信任", "背叛", "支持", "竞争"],
                "恋人": ["吸引", "冲突", "成长", "圆满"],
                "敌人": ["对立", "理解", "转化", "决战"]
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理角色管理请求"""
        try:
            request_type = input_data.get("type", "manage_characters")
            
            if request_type == "create_characters":
                return self._create_characters(input_data)
            elif request_type == "check_consistency":
                return self._check_consistency(input_data)
            elif request_type == "develop_character":
                return self._develop_character(input_data)
            elif request_type == "manage_relationships":
                return self._manage_relationships(input_data)
            else:
                return {"error": f"未知请求类型: {request_type}"}
        except Exception as e:
            self.log(f"处理请求时发生异常: {str(e)}")
            return {
                "type": "error",
                "content": f"处理失败: {str(e)}",
                "error": str(e)
            }
    
    def _create_characters(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建角色"""
        story_framework = input_data.get("story_framework", "")
        genre = input_data.get("genre", "")
        theme = input_data.get("theme", "")
        knowledge_base = input_data.get("knowledge_base", "")
        real_info = input_data.get("real_info", {})
        requires_real_info = input_data.get("requires_real_info", False)
        custom_plot = input_data.get("custom_plot", "")
        strict_mode = input_data.get("strict_user_input", True)
        
        # 🎯 简化版角色创建提示词
        character_prompt = f"""
请为小说《{input_data.get('title', '')}》创建角色体系。

📋 基础信息：
- 类型：{genre}
- 主题：{theme}

{f'🔥 用户设定（必须遵循）：\n{custom_plot}\n' if custom_plot else ''}

✨ 核心任务：
创建立体、丰富的角色体系：

1️⃣ **主角设定**
2️⃣ **主要配角**
3️⃣ **反派角色**
4️⃣ **角色关系网络**
5️⃣ **对话风格特色**

🎯 创作原则：
• 严格遵循用户设定，不随意添加角色
• 角色要有立体感，避免脸谱化
• 关系要复杂但不混乱
• 符合{genre}类型的角色特色
• 为后续发展留下空间

请用结构化方式返回角色体系。
"""
        
        self.log("正在创建角色体系...")
        character_response = self.forward(character_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if character_response.is_success():
            character_system = character_response.get_content()
        else:
            character_system = "角色体系创建失败"  # 如果创建失败，返回默认内容
        
        return {
            "type": "character_system",
            "content": character_system,
            "metadata": {
                "genre": genre,
                "theme": theme,
                "created_at": self._get_timestamp()
            }
        }
    
    def _check_consistency(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """检查角色一致性"""
        chapter_content = input_data.get("content", "")
        character_profiles = input_data.get("character_profiles", {})
        chapter_num = input_data.get("chapter_num", 1)
        
        consistency_prompt = f"""
请检查以下章节内容的角色一致性：

章节内容：
{chapter_content}

角色档案：
{character_profiles}

章节号：第{chapter_num}章

请检查：
1. 角色行为是否符合其性格设定
2. 角色对话是否符合其说话风格
3. 角色关系是否与设定一致
4. 角色成长是否符合逻辑
5. 角色动机是否合理

请指出：
- 一致性问题
- 具体修改建议
- 角色发展建议

请以结构化的方式返回一致性检查结果。
"""
        
        self.log("正在检查角色一致性...")
        consistency_response = self.forward(consistency_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if consistency_response.is_success():
            consistency_check = consistency_response.get_content()
        else:
            consistency_check = "角色一致性检查失败"  # 如果检查失败，返回默认内容
        
        return {
            "type": "consistency_check",
            "content": consistency_check,
            "chapter_num": chapter_num
        }
    
    def _develop_character(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """发展角色"""
        character_name = input_data.get("character_name", "")
        current_state = input_data.get("current_state", {})
        development_goal = input_data.get("development_goal", "")
        chapter_num = input_data.get("chapter_num", 1)
        
        development_prompt = f"""
请为角色{character_name}设计发展：

当前状态：
{current_state}

发展目标：
{development_goal}

章节号：第{chapter_num}章

请设计：
1. 性格发展：性格如何变化
2. 能力发展：能力如何提升
3. 关系发展：关系如何变化
4. 理念发展：理念如何转变
5. 具体表现：在章节中的具体表现

要求：
- 发展要符合逻辑
- 变化要有渐进性
- 体现角色的成长
- 为后续发展铺垫

请以结构化的方式返回角色发展设计。
"""
        
        self.log(f"正在设计角色{character_name}的发展...")
        development_response = self.forward(development_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if development_response.is_success():
            character_development = development_response.get_content()
        else:
            character_development = "角色发展设计失败"  # 如果设计失败，返回默认内容
        
        return {
            "type": "character_development",
            "content": character_development,
            "character_name": character_name,
            "chapter_num": chapter_num
        }
    
    def _manage_relationships(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """管理角色关系"""
        current_relationships = input_data.get("current_relationships", {})
        chapter_events = input_data.get("chapter_events", [])
        chapter_num = input_data.get("chapter_num", 1)
        
        relationship_prompt = f"""
请管理角色关系的发展：

当前关系：
{current_relationships}

章节事件：
{chapter_events}

章节号：第{chapter_num}章

请分析：
1. 事件对关系的影响
2. 关系的变化趋势
3. 新的关系可能性
4. 关系冲突的解决
5. 为后续关系发展铺垫

要求：
- 关系变化要合理
- 体现关系的复杂性
- 为故事发展服务
- 增加戏剧张力

请以结构化的方式返回关系管理结果。
"""
        
        self.log("正在管理角色关系...")
        relationship_response = self.forward(relationship_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if relationship_response.is_success():
            relationship_management = relationship_response.get_content()
        else:
            relationship_management = "角色关系管理失败"  # 如果管理失败，返回默认内容
        
        return {
            "type": "relationship_management",
            "content": relationship_management,
            "chapter_num": chapter_num
        }
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
