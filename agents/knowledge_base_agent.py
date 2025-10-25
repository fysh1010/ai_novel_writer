#!/usr/bin/env python3
"""
知识库智能体 - 负责题材识别、信息搜索、真实性验证
解决AI创作中随意编造人物和情节的问题
"""

from .base_agent import BaseAgent
from .model_config import ModelConfig
from typing import Dict, List, Any

class KnowledgeBaseAgent(BaseAgent):
    """知识库智能体"""
    
    def __init__(self, model_source: str = None, model_name: str = None):
        # 使用模型配置
        config = ModelConfig.get_model_config("knowledge_base")
        if model_source is None:
            model_source = config["model_source"]
        if model_name is None:
            model_name = config["model_name"]
        
        super().__init__("知识库智能体", model_source, model_name)
        self._init_knowledge_base()
    
    def _init_knowledge_base(self):
        """初始化知识库"""
        self.knowledge_base = {
            "genre_classification": {
                "洪荒": {
                    "description": "基于中国神话的洪荒世界设定，以神话传说为主，技术元素为辅",
                    "requires_real_info": True,
                    "key_elements": ["神话人物", "修炼体系", "世界观设定", "重要事件", "天道法则"],
                    "search_keywords": ["洪荒神话", "封神演义", "中国神话", "道教神仙", "鸿钧道祖", "三清", "女娲", "盘古开天", "女娲造人"]
                },
                "历史": {
                    "description": "基于真实历史背景的创作",
                    "requires_real_info": True,
                    "key_elements": ["历史人物", "历史事件", "时代背景", "社会制度"],
                    "search_keywords": ["历史人物", "历史事件", "朝代背景", "历史资料"]
                },
                "都市": {
                    "description": "现代都市背景的创作",
                    "requires_real_info": False,
                    "key_elements": ["现代生活", "社会现实", "人际关系", "商业环境"],
                    "search_keywords": ["都市生活", "现代商业", "社会现实"]
                },
                "玄幻": {
                    "description": "玄幻修仙背景的创作",
                    "requires_real_info": False,
                    "key_elements": ["修炼体系", "境界划分", "法宝神器", "宗门势力"],
                    "search_keywords": ["修仙体系", "玄幻设定", "修炼境界"]
                },
                "科幻": {
                    "description": "科幻背景的创作",
                    "requires_real_info": False,
                    "key_elements": ["科技设定", "未来世界", "外星文明", "时空概念"],
                    "search_keywords": ["科幻设定", "未来科技", "太空探索"]
                },
                "武侠": {
                    "description": "武侠背景的创作",
                    "requires_real_info": False,
                    "key_elements": ["武功秘籍", "江湖门派", "武林高手", "侠义精神"],
                    "search_keywords": ["武侠设定", "江湖门派", "武功秘籍"]
                },
                "军事": {
                    "description": "军事背景的创作",
                    "requires_real_info": True,
                    "key_elements": ["军事装备", "战术战略", "历史战役", "军事制度"],
                    "search_keywords": ["军事装备", "战术战略", "历史战役"]
                },
                "悬疑": {
                    "description": "悬疑推理背景的创作",
                    "requires_real_info": False,
                    "key_elements": ["推理逻辑", "犯罪手法", "心理分析", "线索推理"],
                    "search_keywords": ["悬疑推理", "犯罪心理", "推理逻辑"]
                }
            },
            "real_info_cache": {},
            "verification_rules": {
                "人物关系": "确保人物关系符合原著/历史",
                "世界观设定": "确保世界观设定合理一致",
                "重要事件": "确保重要事件符合原著/历史",
                "时间线": "确保时间线逻辑合理"
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理知识库请求"""
        request_type = input_data.get("type", "identify_genre")
        
        if request_type == "identify_genre":
            return self._identify_genre(input_data)
        elif request_type == "search_real_info":
            return self._search_real_info(input_data)
        elif request_type == "verify_authenticity":
            return self._verify_authenticity(input_data)
        elif request_type == "build_knowledge_base":
            return self._build_knowledge_base(input_data)
        else:
            return {"error": f"未知请求类型: {request_type}"}
    
    def _identify_genre(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """识别题材类型 - 完全动态，不限制固定类型"""
        title = input_data.get("title", "")
        genre = input_data.get("genre", "")
        theme = input_data.get("theme", "")
        custom_plot = input_data.get("custom_plot", "")
        
        identification_prompt = f"""
请深度分析以下小说信息，识别其真实题材类型和创作需求：

小说标题：{title}
用户输入类型：{genre}
主题关键词：{theme}
剧情简介：{custom_plot if custom_plot else "（用户未提供）"}

请你作为专业的小说策划，综合分析以上信息，识别出最准确的题材类型。
不要局限于传统分类（如玄幻、都市、历史等），要根据实际内容判断。

示例题材参考（仅供参考，不限于此）：
- 现代都市、科普教学、情感励志、职场商战
- 历史架空、古代言情、历史军事
- 玄幻修仙、洪荒神话、异界大陆
- 科幻未来、末日求生、星际探索
- 武侠江湖、仙侠修真
- 悬疑推理、恐怖灵异
- 游戏竞技、电子竞技
- 军事战争、谍战特工
- 二次元、轻小说、同人
等等...

请以JSON格式返回分析结果：
{{
  "题材类型": "具体的题材类型名称",
  "题材描述": "简要描述这个题材的特点",
  "是否需要真实信息": "是/否",
  "需要真实信息的原因": "如果需要，说明原因；如果不需要，可为空",
  "关键创作要素": ["要素1", "要素2", "要素3"],
  "建议搜索关键词": ["关键词1", "关键词2", "关键词3"],
  "创作建议": "针对这个题材的创作建议"
}}

注意：
1. 题材类型要准确反映小说的实际内容，不要套用常见模板
2. "是否需要真实信息"的判断标准：
   - 如果涉及真实历史、真实地理、真实科学知识、真实社会现象等需要严谨考证的内容，则需要
   - 如果是纯虚构、幻想、架空世界，则不需要
3. 教学类、科普类小说通常需要真实信息支撑
"""
        
        self.log("正在智能识别题材类型...")
        identification_response = self.forward(identification_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if identification_response.is_success():
            identification_result = identification_response.get_content()
        else:
            identification_result = genre  # 如果识别失败，使用原题材
        
        # 解析识别结果，提取题材类型和是否需要真实信息
        parsed_result = self._parse_genre_identification_dynamic(identification_result, genre)
        
        return {
            "type": "genre_identified",
            "genre": parsed_result["genre"],
            "requires_real_info": parsed_result["requires_real_info"],
            "analysis": identification_result,
            "genre_description": parsed_result.get("genre_description", ""),
            "search_keywords": parsed_result.get("search_keywords", [])
        }
    
    def _search_real_info(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """动态搜索真实信息 - 根据题材智能生成搜索关键词"""
        genre = input_data.get("genre", "")
        search_keywords = input_data.get("search_keywords", [])
        title = input_data.get("title", "")
        theme = input_data.get("theme", "")
        custom_plot = input_data.get("custom_plot", "")
        
        # 如果没有提供搜索关键词，动态生成
        if not search_keywords:
            self.log(f"正在为《{title}》({genre})动态生成搜索关键词...")
            
            keyword_generation_prompt = f"""
请为以下小说生成精准的搜索关键词，用于搜索创作所需的真实信息：

小说标题：{title}
题材类型：{genre}
主题关键词：{theme}
剧情简介：{custom_plot if custom_plot else "（未提供）"}

请分析这部小说需要哪些真实信息支撑，生成3-5个精准的搜索关键词。

要求：
1. 关键词要具体、精准，便于搜索到相关资料
2. 针对小说的核心内容，不要泛泛而谈
3. 如果是教学类，关键词应该是具体的知识领域
4. 如果是历史类，关键词应该是具体的历史时期或事件
5. 如果是科技类，关键词应该是具体的科技概念

请以JSON格式返回：
{{
  "搜索关键词": ["关键词1", "关键词2", "关键词3"],
  "搜索目的": "简要说明这些关键词用于搜索什么信息"
}}
"""
            
            keyword_response = self.forward(keyword_generation_prompt)
            if keyword_response.is_success():
                keyword_result = keyword_response.get_content()
                try:
                    import json
                    if '{' in keyword_result:
                        json_start = keyword_result.index('{')
                        json_end = keyword_result.rindex('}') + 1
                        json_str = keyword_result[json_start:json_end]
                        keyword_data = json.loads(json_str)
                        search_keywords = keyword_data.get("搜索关键词", [])
                        self.log(f"动态生成的搜索关键词：{search_keywords}")
                except Exception as e:
                    self.log(f"解析搜索关键词失败：{e}")
                    # 如果解析失败，使用默认关键词
                    search_keywords = [genre, theme, title]
        
        if not search_keywords:
            self.log(f"未生成搜索关键词，使用题材名称作为关键词")
            search_keywords = [genre]
        
        self.log(f"正在搜索{genre}题材的真实信息...")
        
        search_results = {}
        
        for keyword in search_keywords:
            self.log(f"搜索关键词：{keyword}")
            
            try:
                # 使用内置搜索功能搜索信息
                search_result = self._search_information(keyword)
                
                if search_result:
                    search_results[keyword] = search_result
                    self.log(f"找到{keyword}相关信息")
                else:
                    self.log(f"未找到{keyword}相关信息")
                    
            except Exception as e:
                self.log(f"搜索{keyword}时出错：{e}")
                search_results[keyword] = f"搜索出错：{e}"
        
        # 整理搜索结果
        organized_info = self._organize_search_results(search_results, genre)
        
        return {
            "type": "real_info_searched",
            "genre": genre,
            "search_results": search_results,
            "organized_info": organized_info,
            "search_keywords": search_keywords
        }
    
    def _verify_authenticity(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """验证真实性"""
        content = input_data.get("content", "")
        genre = input_data.get("genre", "")
        real_info = input_data.get("real_info", {})
        
        verification_prompt = f"""
请验证以下内容的真实性：

创作内容：
{content}

题材类型：{genre}

真实信息参考：
{real_info}

请验证：
1. 人物设定是否符合真实信息
2. 人物关系是否符合原著/历史
3. 世界观设定是否合理
4. 重要事件是否符合真实信息
5. 是否存在随意编造的问题

请指出：
- 真实性问题
- 不符合真实信息的地方
- 需要修正的内容
- 修改建议

请以结构化的方式返回验证结果。
"""
        
        self.log("正在验证内容真实性...")
        verification_response = self.forward(verification_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if verification_response.is_success():
            verification_result = verification_response.get_content()
        else:
            verification_result = "真实性验证失败"  # 如果验证失败，返回默认内容
        
        return {
            "type": "authenticity_verified",
            "content": verification_result,
            "genre": genre,
            "verified_at": self._get_timestamp()
        }
    
    def _build_knowledge_base(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """构建知识库"""
        genre = input_data.get("genre", "")
        real_info = input_data.get("real_info", {})
        
        knowledge_base_prompt = f"""
请基于以下信息构建{genre}题材的知识库：

真实信息：
{real_info}

请构建包含以下内容的知识库：

## 1. 主要人物
- 人物姓名、身份、关系
- 人物性格、能力、背景
- 人物在故事中的作用

## 2. 世界观设定
- 世界背景、时代设定
- 社会制度、文化背景
- 修炼体系、境界划分（如适用）

## 3. 重要事件
- 历史事件、神话传说
- 事件时间线、因果关系
- 事件对故事的影响

## 4. 势力关系
- 各方势力的立场
- 势力间的冲突和合作
- 权力结构和等级关系

## 5. 创作约束
- 不能随意编造的人物
- 不能随意改变的关系
- 必须遵循的设定
- 创作注意事项

要求：
- 确保信息准确可靠
- 结构清晰便于使用
- 为创作提供明确指导
- 避免随意编造重要信息

请以结构化的方式返回知识库内容。
"""
        
        self.log(f"正在构建{genre}题材的知识库...")
        knowledge_base_response = self.forward(knowledge_base_prompt)
        
        # 提取内容，确保返回可序列化的数据
        if knowledge_base_response.is_success():
            knowledge_base_content = knowledge_base_response.get_content()
        else:
            knowledge_base_content = f"{genre}题材知识库构建失败"  # 如果构建失败，返回默认内容
        
        # 缓存知识库
        self.knowledge_base["real_info_cache"][genre] = {
            "content": knowledge_base_content,
            "real_info": real_info,
            "created_at": self._get_timestamp()
        }
        
        return {
            "type": "knowledge_base_built",
            "genre": genre,
            "content": knowledge_base_content,
            "metadata": {
                "created_at": self._get_timestamp(),
                "cache_key": genre
            }
        }
    
    def _parse_genre_identification_dynamic(self, identification_result: str, default_genre: str) -> Dict[str, Any]:
        """动态解析题材识别结果 - 不依赖固定分类"""
        import json
        
        result = {
            "genre": default_genre or "现代都市",
            "requires_real_info": False,
            "genre_description": "",
            "search_keywords": []
        }
        
        try:
            # 尝试解析JSON格式的返回结果
            if '{' in identification_result:
                # 提取JSON部分
                json_start = identification_result.index('{')
                json_end = identification_result.rindex('}') + 1
                json_str = identification_result[json_start:json_end]
                result_data = json.loads(json_str)
                
                # 提取题材类型
                if "题材类型" in result_data:
                    result["genre"] = result_data["题材类型"]
                elif "genre" in result_data:
                    result["genre"] = result_data["genre"]
                
                # 提取题材描述
                if "题材描述" in result_data:
                    result["genre_description"] = result_data["题材描述"]
                elif "description" in result_data:
                    result["genre_description"] = result_data["description"]
                
                # 判断是否需要真实信息
                if "是否需要真实信息" in result_data:
                    needs_info = result_data["是否需要真实信息"]
                    result["requires_real_info"] = needs_info in ["是", "需要", "true", "True", True]
                elif "requires_real_info" in result_data:
                    result["requires_real_info"] = result_data["requires_real_info"]
                
                # 提取搜索关键词
                if "建议搜索关键词" in result_data:
                    result["search_keywords"] = result_data["建议搜索关键词"]
                elif "search_keywords" in result_data:
                    result["search_keywords"] = result_data["search_keywords"]
                
                self.log(f"动态解析成功 - 题材：{result['genre']}，需要真实信息：{result['requires_real_info']}")
                return result
                
        except Exception as e:
            self.log(f"JSON解析失败，使用文本分析：{e}")
        
        # 如果JSON解析失败，使用智能文本分析
        text_lower = identification_result.lower()
        
        # 判断是否需要真实信息（关键词判断）
        if any(keyword in text_lower for keyword in ["需要真实信息", "需要", "是", "真实", "考证", "历史", "科普", "教学"]):
            result["requires_real_info"] = True
        
        if any(keyword in text_lower for keyword in ["不需要", "否", "虚构", "幻想", "架空"]):
            result["requires_real_info"] = False
        
        self.log(f"文本分析结果 - 题材：{result['genre']}，需要真实信息：{result['requires_real_info']}")
        return result
    
    def _parse_genre_identification(self, identification_result: str, default_genre: str) -> str:
        """解析题材识别结果"""
        import json
        import re
        
        try:
            # 尝试解析JSON格式的返回结果
            if identification_result.strip().startswith('{'):
                result_data = json.loads(identification_result)
                # 从JSON中提取题材类型
                genre_value = None
                if "题材类型识别" in result_data:
                    genre_value = result_data["题材类型识别"]
                elif "genre" in result_data:
                    genre_value = result_data["genre"]
                elif "type" in result_data:
                    genre_value = result_data["type"]
                
                # 如果成功提取到题材类型，直接返回（不再进行关键词匹配）
                if genre_value:
                    self.log(f"JSON解析成功，提取题材类型：{genre_value}")
                    return genre_value
        except Exception as e:
            self.log(f"JSON解析失败：{e}")
        
        # 如果JSON解析失败，使用关键词匹配（只在第一句话中匹配，避免误判）
        # 优先从第一句话或第一行中提取题材
        first_line = identification_result.split('\n')[0].lower()
        
        # 按优先级检查关键词（注意：科普/教学优先级最高）
        if "科普" in first_line or "教学" in first_line:
            self.log("关键词匹配：科普/教学 -> 都市")
            return "都市"
        elif "洪荒" in first_line:
            return "洪荒"
        elif "都市" in first_line:
            return "都市"
        elif "历史" in first_line:
            return "历史"
        elif "玄幻" in first_line:
            return "玄幻"
        elif "科幻" in first_line:
            return "科幻"
        elif "武侠" in first_line:
            return "武侠"
        elif "仙侠" in first_line:
            return "仙侠"
        elif "军事" in first_line:
            return "军事"
        elif "悬疑" in first_line:
            return "悬疑"
        elif "言情" in first_line:
            return "言情"
        else:
            self.log(f"未匹配到关键词，使用默认题材：{default_genre or '都市'}")
            return default_genre or "都市"
    
    def _organize_search_results(self, search_results: Dict[str, Any], genre: str) -> Dict[str, Any]:
        """整理搜索结果"""
        organized_info = {
            "genre": genre,
            "characters": {},
            "worldview": {},
            "events": {},
            "relationships": {},
            "constraints": {}
        }
        
        # 基于搜索结果整理信息
        for keyword, result in search_results.items():
            if isinstance(result, str) and len(result) > 100:
                # 简单的信息提取（实际应用中需要更复杂的NLP处理）
                if "人物" in keyword or "角色" in keyword:
                    organized_info["characters"][keyword] = result
                elif "世界" in keyword or "设定" in keyword:
                    organized_info["worldview"][keyword] = result
                elif "事件" in keyword or "历史" in keyword:
                    organized_info["events"][keyword] = result
                elif "关系" in keyword or "势力" in keyword:
                    organized_info["relationships"][keyword] = result
                else:
                    organized_info["constraints"][keyword] = result
        
        return organized_info
    
    def get_cached_knowledge(self, genre: str) -> Dict[str, Any]:
        """获取缓存的知识库"""
        return self.knowledge_base["real_info_cache"].get(genre, {})
    
    def _search_information(self, keyword: str) -> str:
        """内置信息搜索功能"""
        # 基于关键词搜索相关信息
        search_prompt = f"""
请搜索并整理关于"{keyword}"的相关信息：

请提供：
1. 基本定义和概念
2. 重要人物和角色
3. 关键事件和情节
4. 世界观设定
5. 关系网络
6. 重要细节

要求：
- 信息要准确可靠
- 结构清晰便于使用
- 为小说创作提供参考

请以结构化的方式返回搜索结果。
"""
        
        try:
            search_result = self.forward(search_prompt)
            return search_result
        except Exception as e:
            return f"搜索失败：{e}"
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
