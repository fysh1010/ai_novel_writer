#!/usr/bin/env python3
"""
基础智能体类 - 所有智能体的基类
"""

import lazyllm
import time
import sys
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from core.agent_response import AgentResponse, AgentStatus, safe_agent_call

class BaseAgent(ABC):
    """基础智能体类"""
    
    def __init__(self, name: str, model_source: str = 'sensenova', model_name: str = 'DeepSeek-V3-1'):
        """初始化智能体"""
        self.name = name
        self.model_source = model_source
        self.model_name = model_name
        self.knowledge_base = {}
        self.context = {}
        self.llm_ready = False
        self._init_llm()
    
    def _init_llm(self):
        """初始化LLM，带错误处理"""
        try:
            self.chat = lazyllm.OnlineChatModule(source=self.model_source, model=self.model_name)
            self.llm_ready = True
            print(f"[OK] {self.name} LLM初始化成功")
        except Exception as e:
            print(f"[ERROR] {self.name} LLM初始化失败: {e}")
            self.llm_ready = False
            self.chat = None
    
    def set_context(self, context: Dict[str, Any]):
        """设置上下文信息"""
        self.context.update(context)
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """获取上下文信息"""
        return self.context.get(key, default)
    
    def update_knowledge_base(self, knowledge: Dict[str, Any]):
        """更新知识库"""
        self.knowledge_base.update(knowledge)
    
    def get_knowledge(self, key: str, default: Any = None) -> Any:
        """获取知识库信息"""
        return self.knowledge_base.get(key, default)
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理输入数据，返回处理结果"""
        pass
    
    def forward(self, prompt: str, max_retries: int = 3, show_response: bool = True) -> AgentResponse:
        """转发请求到AI模型，带重试机制和打字机效果 - 统一返回格式"""
        if not self.llm_ready or not self.chat:
            return AgentResponse.error(
                error_message="LLM未初始化或不可用",
                text="智能体暂时不可用，请稍后重试"
            )
        
        for attempt in range(max_retries):
            try:
                self.log(f"调用LLM进行处理... (第{attempt + 1}次尝试)")
                
                # 移除思考动画提示，避免影响内容显示
                
                response = self.chat.forward(prompt)
                
                if response and len(response.strip()) > 10:  # 确保响应不为空且有意义
                    self.log(f"LLM处理完成，响应长度: {len(response)}")
                    
                    # 显示完整内容（使用打字机效果）
                    if show_response:
                        print(f"\n[{self.name}] 生成内容:")
                        print("-" * 50)
                        # 始终使用打字机效果显示完整内容
                        self.typewriter_effect(response, delay=0.001)
                        print("-" * 50)
                    
                    return AgentResponse.success(
                        text=response,
                        json_struct={"content": response, "length": len(response)}
                    )
                else:
                    self.log(f"响应为空或过短，重试中...")
                    
            except Exception as e:
                error_msg = str(e)
                self.log(f"第{attempt + 1}次尝试失败: {error_msg}")
                
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # 指数退避
                    self.log(f"等待{wait_time}秒后重试...")
                    time.sleep(wait_time)
                else:
                    self.log(f"经过{max_retries}次重试后仍然失败")
                    return AgentResponse.error(
                        error_message=f"LLM调用失败: {error_msg}",
                        text="智能体处理失败，请稍后重试"
                    )
        
        return AgentResponse.error(
            error_message="达到最大重试次数",
            text="智能体处理超时，请稍后重试"
        )
    
    
    def typewriter_effect(self, text: str, delay: float = 0.001):
        """打字机效果显示文本 - 优化显示速度"""
        # 对于长文本，使用更快的显示速度
        if len(text) > 1000:
            delay = 0.0001  # 长文本显示更快
        
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()  # 换行
    
    def log(self, message: str):
        """记录日志"""
        print(f"[{self.name}] {message}")
