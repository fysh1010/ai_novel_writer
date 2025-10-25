"""
智能章节分析器 - 使用Embedding提升章节分析能力
解决：长文本记忆、语义连贯性、关键章节识别等问题
"""

from typing import List, Dict, Any, Optional
from core.embedding_service import get_embedding_service


class SmartChapterAnalyzer:
    """智能章节分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.embedding_service = get_embedding_service()
    
    def smart_chapter_sampling(self, chapters: List[Dict[str, Any]], 
                              target_count: int = 15) -> List[Dict[str, Any]]:
        """
        智能章节取样 - 解决"只取最近10章"的问题
        
        策略：
        1. 最近5章（保证连贯性）
        2. 关键章节（高潮、转折点）
        3. 高评分章节
        
        Args:
            chapters: 所有章节列表
            target_count: 目标取样数量
            
        Returns:
            采样后的章节列表
        """
        if len(chapters) <= target_count:
            return chapters
        
        sampled_chapters = []
        sampled_indices = set()
        
        # 1. 最近5章（必须包含）
        recent_count = min(5, len(chapters))
        recent_chapters = chapters[-recent_count:]
        sampled_chapters.extend(recent_chapters)
        sampled_indices.update(range(len(chapters) - recent_count, len(chapters)))
        
        remaining_slots = target_count - len(sampled_chapters)
        if remaining_slots <= 0:
            return sampled_chapters
        
        # 2. 识别关键章节（使用embedding）
        chapter_summaries = [ch.get('summary', '') for ch in chapters[:-recent_count]]
        if chapter_summaries:
            key_chapter_indices = self.embedding_service.find_key_chapters(
                chapter_summaries, 
                top_k=min(remaining_slots, len(chapter_summaries))
            )
            
            for idx in key_chapter_indices:
                if idx not in sampled_indices:
                    sampled_chapters.append(chapters[idx])
                    sampled_indices.add(idx)
                    remaining_slots -= 1
                    if remaining_slots <= 0:
                        break
        
        # 3. 如果还有空位，按评分选择
        if remaining_slots > 0:
            rated_chapters = []
            for i, ch in enumerate(chapters):
                if i not in sampled_indices:
                    rating = ch.get('rating', 0)
                    rated_chapters.append((i, rating, ch))
            
            # 按评分排序
            rated_chapters.sort(key=lambda x: x[1], reverse=True)
            
            for i, rating, ch in rated_chapters[:remaining_slots]:
                sampled_chapters.append(ch)
                sampled_indices.add(i)
        
        # 按章节序号排序
        sampled_chapters.sort(key=lambda x: x.get('chapter_num', 0))
        
        return sampled_chapters
    
    def check_coherence(self, new_chapter_summary: str, 
                       previous_chapters: List[Dict[str, Any]],
                       threshold: float = 0.3) -> Dict[str, Any]:
        """
        检查新章节与前面章节的连贯性
        
        Args:
            new_chapter_summary: 新章节摘要
            previous_chapters: 前面的章节列表
            threshold: 最低相似度阈值
            
        Returns:
            连贯性检查结果
        """
        if not previous_chapters:
            return {"coherent": True, "similarity": 1.0}
        
        # 获取新章节的embedding
        new_embedding = self.embedding_service.get_embedding(new_chapter_summary)
        if not new_embedding:
            return {"coherent": True, "similarity": 1.0, "error": "无法获取embedding"}
        
        # 计算与最近几章的相似度
        recent_chapters = previous_chapters[-5:]
        similarities = []
        
        for ch in recent_chapters:
            summary = ch.get('summary', '')
            if summary:
                ch_embedding = self.embedding_service.get_embedding(summary)
                if ch_embedding:
                    sim = self.embedding_service.cosine_similarity(new_embedding, ch_embedding)
                    similarities.append(sim)
        
        if not similarities:
            return {"coherent": True, "similarity": 1.0, "error": "无法计算相似度"}
        
        max_similarity = max(similarities)
        avg_similarity = sum(similarities) / len(similarities)
        
        return {
            "coherent": max_similarity >= threshold,
            "max_similarity": max_similarity,
            "avg_similarity": avg_similarity,
            "warning": "新章节与前面内容关联度较低" if max_similarity < threshold else None
        }
    
    def detect_duplicate_content(self, new_chapter_content: str, 
                                 existing_chapters: List[Dict[str, Any]],
                                 threshold: float = 0.85) -> Optional[Dict[str, Any]]:
        """
        检测重复内容 - 优化版，区分术语重复和内容重复
        
        Args:
            new_chapter_content: 新章节内容
            existing_chapters: 已有章节列表
            threshold: 重复检测阈值
            
        Returns:
            如果检测到重复，返回重复信息
        """
        # 1. 先检测术语重复（科学概念、专业词汇）
        technical_terms = self._extract_technical_terms(new_chapter_content)
        if technical_terms:
            # 如果主要是术语重复，降低阈值
            adjusted_threshold = min(threshold, 0.95)  # 提高阈值，减少误报
        else:
            adjusted_threshold = threshold
        
        existing_contents = [ch.get('content', '') for ch in existing_chapters]
        duplicate = self.embedding_service.detect_duplicate(
            new_chapter_content, 
            existing_contents,
            adjusted_threshold
        )
        
        if duplicate:
            chapter_num = existing_chapters[duplicate['index']].get('chapter_num', 0)
            return {
                "is_duplicate": True,
                "duplicate_chapter": chapter_num,
                "similarity": duplicate['similarity'],
                "warning": f"内容与第{chapter_num}章高度相似（{duplicate['similarity']:.2%}）"
            }
        
        return None
    
    def check_character_consistency(self, character_name: str,
                                   chapters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        检查角色一致性
        
        Args:
            character_name: 角色名称
            chapters: 章节列表
            
        Returns:
            一致性检查结果
        """
        # 提取角色在各章节的描述
        character_descriptions = []
        chapter_nums = []
        
        for ch in chapters:
            content = ch.get('content', '')
            # 简单提取：查找角色名称附近的句子
            if character_name in content:
                # 这里可以更智能地提取角色描述
                # 暂时简化处理
                character_descriptions.append(content[:500])
                chapter_nums.append(ch.get('chapter_num', 0))
        
        if len(character_descriptions) < 2:
            return {
                "consistent": True,
                "score": 1.0,
                "note": "角色出现次数不足，无法检查一致性"
            }
        
        # 计算一致性
        consistency_score = self.embedding_service.calculate_consistency(
            character_descriptions
        )
        
        return {
            "consistent": consistency_score >= 0.7,
            "score": consistency_score,
            "appearance_chapters": chapter_nums,
            "warning": f"角色'{character_name}'性格描述前后不太一致" if consistency_score < 0.7 else None
        }
    
    def find_similar_chapters(self, query_chapter: Dict[str, Any],
                             all_chapters: List[Dict[str, Any]],
                             top_k: int = 3) -> List[Dict[str, Any]]:
        """
        找到与指定章节最相似的章节
        
        Args:
            query_chapter: 查询章节
            all_chapters: 所有章节
            top_k: 返回前k个
            
        Returns:
            相似章节列表
        """
        query_summary = query_chapter.get('summary', '')
        if not query_summary:
            return []
        
        candidate_summaries = [ch.get('summary', '') for ch in all_chapters]
        results = self.embedding_service.find_most_similar(
            query_summary,
            candidate_summaries,
            top_k
        )
        
        similar_chapters = []
        for result in results:
            idx = result['index']
            if idx < len(all_chapters):
                similar_chapters.append({
                    "chapter": all_chapters[idx],
                    "similarity": result['similarity']
                })
        
        return similar_chapters
    
    def _extract_technical_terms(self, content: str) -> List[str]:
        """
        提取技术术语，用于区分术语重复和内容重复
        
        Args:
            content: 文本内容
            
        Returns:
            技术术语列表
        """
        import re
        
        # 科幻/技术术语模式
        technical_patterns = [
            r'能源[脉冲|阵列|系统|设备]',
            r'电磁[防护|脉冲|感应|线圈]',
            r'轨道[修正|转移|机动|参数]',
            r'推进[剂|系统|器|装置]',
            r'导航[算法|系统|数据|仪]',
            r'脉冲[追踪|单元|检测|分析]',
            r'伽马[射线|暴|检测]',
            r'太阳[风|通量|帆|压]',
            r'空间[站|站|碎片|残骸]',
            r'量子[加密|纠缠|通讯]',
            r'等离子[体|帆|推进]',
            r'光帆[阵列|推进|系统]',
            r'奥米克戎[舰队|武器|信号]',
            r'深空[广播|通讯|测控]',
            r'射电[望远镜|阵列|信号]',
            r'莫尔斯[电码|信号|通讯]',
            r'LoRa[电台|通讯|网络]',
            r'树莓派[系统|设备|模拟]',
            r'Python[代码|程序|模拟]',
            r'开普勒[定律|轨道|参数]',
            r'傅里叶[变换|分析|算法]',
            r'三体[问题|轨道|计算]',
            r'六分仪[坐标|测量|导航]',
            r'半人马座[α星|坐标|位置]',
            r'赤经[坐标|测量|导航]',
            r'赤纬[坐标|测量|导航]'
        ]
        
        technical_terms = []
        for pattern in technical_patterns:
            matches = re.findall(pattern, content)
            technical_terms.extend(matches)
        
        return list(set(technical_terms))  # 去重
    
    def analyze_plot_development(self, chapters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析剧情发展趋势
        
        Args:
            chapters: 章节列表
            
        Returns:
            剧情发展分析结果
        """
        if len(chapters) < 5:
            return {
                "trend": "初期",
                "key_turning_points": [],
                "note": "章节数量不足，无法分析趋势"
            }
        
        # 识别关键章节（转折点）
        summaries = [ch.get('summary', '') for ch in chapters]
        key_indices = self.embedding_service.find_key_chapters(summaries, top_k=5)
        
        key_chapters = []
        for idx in key_indices:
            key_chapters.append({
                "chapter_num": chapters[idx].get('chapter_num', 0),
                "title": chapters[idx].get('title', ''),
                "summary": chapters[idx].get('summary', '')[:100]
            })
        
        return {
            "total_chapters": len(chapters),
            "key_turning_points": key_chapters,
            "note": "这些章节可能是剧情的关键转折点"
        }


# 全局单例
_analyzer = None

def get_chapter_analyzer() -> SmartChapterAnalyzer:
    """获取章节分析器单例"""
    global _analyzer
    if _analyzer is None:
        _analyzer = SmartChapterAnalyzer()
    return _analyzer


if __name__ == "__main__":
    # 测试代码
    analyzer = SmartChapterAnalyzer()
    
    # 模拟章节数据
    test_chapters = [
        {"chapter_num": i, "summary": f"第{i}章的内容摘要", "content": f"第{i}章的详细内容", "rating": i % 5}
        for i in range(1, 21)
    ]
    
    print("测试1：智能章节取样")
    sampled = analyzer.smart_chapter_sampling(test_chapters, target_count=10)
    print(f"从20章中采样10章：{[ch['chapter_num'] for ch in sampled]}")
    
    print("\n测试2：连贯性检查")
    new_summary = "主角突破到圣人境界"
    result = analyzer.check_coherence(new_summary, test_chapters[:10])
    print(f"连贯性：{result}")
