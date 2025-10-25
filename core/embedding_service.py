#!/usr/bin/env python3
"""
嵌入服务模块 - 提供文本向量化和相似度计算功能
"""

import numpy as np
from typing import List, Dict, Any, Optional
import hashlib

class EmbeddingService:
    """简化的嵌入服务实现"""

    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
        self.cache = {}

    def get_embedding(self, text: str) -> List[float]:
        """
        获取文本的向量表示

        Args:
            text: 输入文本

        Returns:
            List[float]: 向量表示
        """
        # 简单的哈希向量实现（实际项目中应使用真正的嵌入模型）
        if text in self.cache:
            return self.cache[text]

        # 使用文本哈希生成固定长度向量
        hash_obj = hashlib.md5(text.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()

        # 将哈希值转换为向量
        vector = []
        for i in range(0, len(hash_hex), 2):
            hex_pair = hash_hex[i:i+2]
            value = int(hex_pair, 16) / 255.0 - 0.5  # 归一化到 [-0.5, 0.5]
            vector.append(value)

        # 确保向量长度为64
        while len(vector) < 64:
            vector.append(0.0)
        vector = vector[:64]

        self.cache[text] = vector
        return vector

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        计算两个文本的相似度

        Args:
            text1: 文本1
            text2: 文本2

        Returns:
            float: 相似度分数 [0, 1]
        """
        vec1 = np.array(self.get_embedding(text1))
        vec2 = np.array(self.get_embedding(text2))

        # 计算余弦相似度
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = dot_product / (norm1 * norm2)
        return float((similarity + 1) / 2)  # 归一化到 [0, 1]

# 全局实例
_embedding_service = None

def get_embedding_service(model_name: str = "default") -> EmbeddingService:
    """
    获取嵌入服务实例

    Args:
        model_name: 模型名称

    Returns:
        EmbeddingService: 嵌入服务实例
    """
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService(model_name)
    return _embedding_service