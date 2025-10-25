"""
剧情意图分析器
用于分析用户输入的剧情简介，提取关键信息并分发给各智能体
"""

import json
import os
from typing import Dict, Any, List
from agents.base_agent import BaseAgent


class StoryIntentAnalyzer:
    """剧情意图分析器"""
    
    def __init__(self):
        self.intent_cache = {}
    
    def forward(self, prompt: str, show_response: bool = False) -> str:
        """调用LLM进行推理"""
        import lazyllm
        from agents.model_config import ModelConfig
        
        try:
            # 使用故事架构师模型
            model_config = ModelConfig.get_model_config("story_architect")
            model = lazyllm.OnlineChatModule(
                source=model_config["model_source"], 
                model=model_config["model_name"]
            )
            
            result = model.forward(prompt)
            if isinstance(result, dict):
                return result.get("content", "")
            else:
                return str(result)
        except Exception as e:
            print(f"⚠️ LLM调用失败: {e}")
            return ""
    
    def analyze_story_intent(self, custom_plot: str, genre: str = "", theme: str = "") -> Dict[str, Any]:
        """分析剧情意图"""
        if not custom_plot:
            return self._get_default_intent(genre, theme)
        
        # 检查缓存
        cache_key = f"{custom_plot}_{genre}_{theme}"
        if cache_key in self.intent_cache:
            return self.intent_cache[cache_key]
        
        # 使用LLM分析剧情意图
        analysis_prompt = f"""
请分析以下剧情简介，提取关键信息：

剧情简介：{custom_plot}
类型：{genre}
主题：{theme}

请提取以下信息并以JSON格式返回：
{{
    "worldview": "世界观设定（如：现代都市、古代修仙、未来科幻等）",
    "protagonist_motivation": "主角动机（如：复仇、成长、拯救、探索等）",
    "conflict_type": "主要冲突类型（如：个人成长、社会矛盾、种族战争等）",
    "rhythm_style": "节奏风格（如：爽文节奏、慢热节奏、悬疑节奏等）",
    "key_elements": ["关键元素1", "关键元素2", "关键元素3"],
    "target_audience": "目标读者群体",
    "emotional_tone": "情感基调（如：热血、温馨、黑暗、轻松等）",
    "special_requirements": "特殊要求或限制"
}}

要求：
1. 基于用户输入进行合理推断
2. 保持与类型和主题的一致性
3. 提取的信息要具体明确
4. 只返回JSON，不要其他说明
"""
        
        try:
            result = self.forward(analysis_prompt, show_response=False)
            if result:
                # 尝试解析JSON
                intent_data = json.loads(result)
                
                # 验证必要字段
                required_fields = ["worldview", "protagonist_motivation", "conflict_type", "rhythm_style"]
                for field in required_fields:
                    if field not in intent_data:
                        intent_data[field] = self._get_default_value(field, genre, theme)
                
                # 缓存结果
                self.intent_cache[cache_key] = intent_data
                return intent_data
        except:
            pass
        
        # 如果分析失败，返回默认意图
        return self._get_default_intent(genre, theme)
    
    def _get_default_intent(self, genre: str, theme: str) -> Dict[str, Any]:
        """获取默认剧情意图"""
        return {
            "worldview": self._get_default_worldview(genre),
            "protagonist_motivation": "成长与冒险",
            "conflict_type": "个人成长",
            "rhythm_style": "爽文节奏",
            "key_elements": ["主角", "系统", "成长"],
            "target_audience": "网文读者",
            "emotional_tone": "热血",
            "special_requirements": "无"
        }
    
    def _get_default_worldview(self, genre: str) -> str:
        """根据类型获取默认世界观"""
        worldview_map = {
            "玄幻": "修仙世界",
            "都市": "现代都市",
            "历史": "古代历史",
            "科幻": "未来世界",
            "武侠": "江湖武林",
            "洪荒": "洪荒世界",
            "仙侠": "仙界凡间",
            "军事": "现代军事",
            "悬疑": "现代都市",
            "言情": "现代都市"
        }
        return worldview_map.get(genre, "现代都市")
    
    def _get_default_value(self, field: str, genre: str, theme: str) -> str:
        """获取默认值"""
        defaults = {
            "worldview": self._get_default_worldview(genre),
            "protagonist_motivation": "成长与冒险",
            "conflict_type": "个人成长",
            "rhythm_style": "爽文节奏",
            "target_audience": "网文读者",
            "emotional_tone": "热血",
            "special_requirements": "无"
        }
        return defaults.get(field, "")
    
    def save_intent_analysis(self, project_id: str, intent_data: Dict[str, Any]):
        """保存剧情意图分析结果"""
        import os
        
        # 创建项目目录
        project_dir = os.path.join("projects", project_id)
        os.makedirs(project_dir, exist_ok=True)
        
        # 保存分析结果
        intent_file = os.path.join(project_dir, "story_intent.json")
        with open(intent_file, 'w', encoding='utf-8') as f:
            json.dump(intent_data, f, ensure_ascii=False, indent=2)
        
        self.log(f"剧情意图分析已保存到: {intent_file}")
    
    def load_intent_analysis(self, project_id: str) -> Dict[str, Any]:
        """加载剧情意图分析结果"""
        intent_file = os.path.join("projects", project_id, "story_intent.json")
        
        if os.path.exists(intent_file):
            try:
                with open(intent_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {}
    
    def create_story_lock_config(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建剧情锁定配置"""
        return {
            "worldview_locked": True,
            "protagonist_motivation_locked": True,
            "conflict_type_locked": True,
            "rhythm_style_locked": True,
            "key_elements_locked": intent_data.get("key_elements", []),
            "emotional_tone_locked": intent_data.get("emotional_tone", "热血"),
            "lock_strength": "medium",  # low, medium, high
            "deviation_threshold": 0.3,  # 允许偏离的程度
            "auto_correction": True
        }
    
    def check_story_deviation(self, current_content: str, intent_data: Dict[str, Any], 
                            lock_config: Dict[str, Any]) -> Dict[str, Any]:
        """检查剧情偏离度"""
        if lock_config.get("lock_strength") == "low":
            return {"deviated": False, "deviation_score": 0, "suggestions": []}
        
        # 简化的偏离检查
        worldview = intent_data.get("worldview", "")
        emotional_tone = intent_data.get("emotional_tone", "")
        
        deviation_indicators = []
        deviation_score = 0
        
        # 检查世界观一致性
        if worldview and worldview not in current_content:
            deviation_indicators.append(f"内容与世界观'{worldview}'不符")
            deviation_score += 0.3
        
        # 检查情感基调
        if emotional_tone == "热血" and "平淡" in current_content:
            deviation_indicators.append("情感基调偏离热血风格")
            deviation_score += 0.2
        
        # 判断是否偏离
        threshold = lock_config.get("deviation_threshold", 0.3)
        deviated = deviation_score > threshold
        
        return {
            "deviated": deviated,
            "deviation_score": deviation_score,
            "indicators": deviation_indicators,
            "suggestions": self._generate_correction_suggestions(deviation_indicators)
        }
    
    def _generate_correction_suggestions(self, indicators: List[str]) -> List[str]:
        """生成修正建议"""
        suggestions = []
        
        for indicator in indicators:
            if "世界观" in indicator:
                suggestions.append("请确保内容符合设定的世界观")
            elif "情感基调" in indicator:
                suggestions.append("请调整情感表达，保持热血风格")
            elif "节奏" in indicator:
                suggestions.append("请优化情节节奏，增加爽点")
        
        return suggestions
