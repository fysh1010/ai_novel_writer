#!/usr/bin/env python3
"""
模型配置管理 - 为不同智能体配置最适合的模型
"""

import yaml
import os

class ModelConfig:
    """模型配置类"""
    
    # 默认模型配置（兜底配置，当config.yaml读取失败时使用）
    # 已开通模型: Kimi-K2, DeepSeek-V3-1, Qwen3-235B (均限时免费)
    _DEFAULT_CONFIGS = {
        # 故事架构师 - 需要复杂的世界观构建和长文本规划能力
        # 使用Kimi-K2: 长文本处理能力强，擅长构建复杂架构和全局规划
        "story_architect": {
            "model_source": "sensenova",
            "model_name": "Kimi-K2"
        },
        
        # 角色管理师 - 需要深度的人物理解和性格分析
        # 使用Qwen3-235B: 参数量大(235B)，人物理解和性格分析能力强
        "character_manager": {
            "model_source": "sensenova",
            "model_name": "Qwen3-235B"
        },
        
        # 情节控制师 - 需要强大的逻辑推理和情节连贯性
        # 使用Qwen3-235B: 逻辑能力强，擅长保持情节连贯性
        "plot_controller": {
            "model_source": "sensenova", 
            "model_name": "Qwen3-235B"
        },
        
        # 优化师 - 需要文本润色和语言优化，对创意要求不高
        # 使用DeepSeek-V3-1: 写作能力强，文本润色效果好，且速度快
        "optimizer": {
            "model_source": "sensenova",
            "model_name": "DeepSeek-V3-1"
        },
        
        # 知识库智能体 - 需要信息整理和知识验证
        # 使用DeepSeek-V3-1: 知识整理能力好，适合信息检索和验证
        "knowledge_base": {
            "model_source": "sensenova",
            "model_name": "DeepSeek-V3-1"
        },
        
        # 章节创作 - 核心功能，需要最强的创意写作和情感表达能力
        # 使用Kimi-K2: 写作能力顶尖，长文本创作流畅，情感表达细腻
        "chapter_writer": {
            "model_source": "sensenova",
            "model_name": "Kimi-K2"
        },
        
        # 章节修改 - 需要理解用户修改意图并精准执行
        # 使用Qwen3-235B: 理解能力强，能准确把握修改需求
        "chapter_modifier": {
            "model_source": "sensenova",
            "model_name": "Qwen3-235B"
        },
        
        # 合规顾问 - 负责敏感词检测和合规审查
        # 使用DeepSeek-V3-1: 敏感检测和中文理解能力强
        "compliance_advisor": {
            "model_source": "sensenova",
            "model_name": "DeepSeek-V3-1"
        }
    }
    
    # 实际使用的配置（从config.yaml加载，如果失败则使用默认配置）
    MODEL_CONFIGS = None
    
    @classmethod
    def _load_configs_from_yaml(cls) -> dict:
        """从config.yaml加载配置"""
        try:
            # 获取config.yaml的路径
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config.yaml'
            )
            
            # 读取配置文件
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 获取agent_models配置
            agent_models = config.get('agent_models', {})
            
            if agent_models:
                print("从config.yaml加载智能体模型配置")
                return agent_models
            else:
                print("config.yaml中未找到agent_models，使用默认配置")
                return cls._DEFAULT_CONFIGS.copy()

        except Exception as e:
            print(f"加载config.yaml失败: {e}，使用默认配置")
            return cls._DEFAULT_CONFIGS.copy()
    
    @classmethod
    def _get_configs(cls) -> dict:
        """获取配置（懒加载）"""
        if cls.MODEL_CONFIGS is None:
            cls.MODEL_CONFIGS = cls._load_configs_from_yaml()
        return cls.MODEL_CONFIGS
    
    @classmethod
    def get_model_config(cls, agent_type: str) -> dict:
        """获取指定智能体的模型配置"""
        configs = cls._get_configs()
        return configs.get(agent_type, {
            "model_source": "sensenova",
            "model_name": "DeepSeek-V3-1"
        })
    
    @classmethod
    def get_all_configs(cls) -> dict:
        """获取所有模型配置"""
        return cls._get_configs().copy()
    
    @classmethod
    def update_config(cls, agent_type: str, model_source: str, model_name: str):
        """更新模型配置"""
        configs = cls._get_configs()
        configs[agent_type] = {
            "model_source": model_source,
            "model_name": model_name
        }
        cls.MODEL_CONFIGS = configs
    
    @classmethod
    def get_model_info(cls, agent_type: str) -> str:
        """获取模型信息字符串"""
        config = cls.get_model_config(agent_type)
        return f"{config['model_source']}:{config['model_name']}"
