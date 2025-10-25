#!/usr/bin/env python3
"""
智能体响应模块 - 提供统一的响应格式和状态枚举
"""

from enum import Enum
from typing import Dict, List, Any, Optional
import traceback

class AgentStatus(Enum):
    """智能体状态枚举"""
    SUCCESS = "success"
    ERROR = "error"
    PROCESSING = "processing"
    TIMEOUT = "timeout"

class AgentResponse:
    """智能体响应类"""

    def __init__(self, status: AgentStatus, content: str = "", metadata: Optional[Dict[str, Any]] = None):
        self.status = status
        self.content = content
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "status": self.status.value,
            "content": self.content,
            "metadata": self.metadata
        }

    @classmethod
    def success(cls, content: str = "", metadata: Optional[Dict[str, Any]] = None, text: Optional[str] = None, **kwargs) -> 'AgentResponse':
        """创建成功响应"""
        # 支持多种参数格式：content 或 text 或其他关键字参数
        final_content = content or text or kwargs.get('message', "") or ""
        return cls(AgentStatus.SUCCESS, final_content, metadata)

    @classmethod
    def error(cls, error_msg: str = "", metadata: Optional[Dict[str, Any]] = None, error_message: Optional[str] = None, text: Optional[str] = None, **kwargs) -> 'AgentResponse':
        """创建错误响应"""
        # 支持多种参数格式：error_msg 或 error_message 或 text 或其他关键字参数
        final_content = error_msg or error_message or text or kwargs.get('message', "") or ""
        return cls(AgentStatus.ERROR, final_content, metadata)

    def is_success(self) -> bool:
        """检查是否成功"""
        return self.status == AgentStatus.SUCCESS

    def get_content(self) -> str:
        """获取内容"""
        return self.content

    def get_status(self) -> AgentStatus:
        """获取状态"""
        return self.status

def safe_agent_call(func, *args, **kwargs) -> Dict[str, Any]:
    """
    安全的智能体调用包装器

    Args:
        func: 要调用的函数
        *args: 位置参数
        **kwargs: 关键字参数

    Returns:
        Dict[str, Any]: 标准化的响应格式
    """
    try:
        result = func(*args, **kwargs)

        # 如果结果已经是标准格式
        if isinstance(result, dict) and "status" in result:
            return result

        # 如果结果是 AgentResponse 对象
        if isinstance(result, AgentResponse):
            return result.to_dict()

        # 包装为成功响应
        return {
            "status": AgentStatus.SUCCESS.value,
            "content": result if isinstance(result, str) else str(result),
            "data": result,
            "metadata": {}
        }

    except Exception as e:
        error_msg = f"调用异常: {str(e)}"
        traceback.print_exc()

        return {
            "status": AgentStatus.ERROR.value,
            "error": error_msg,
            "content": "",
            "metadata": {
                "exception_type": type(e).__name__,
                "exception_message": str(e)
            }
        }