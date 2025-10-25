#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
故事仪表板 - 提供故事进度和统计信息
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

class StoryDashboard:
    """故事仪表板类"""

    def __init__(self):
        """初始化故事仪表板"""
        self.current_story = None
        self.metrics = {}

    def set_story(self, story_data: Dict[str, Any]):
        """
        设置当前故事

        Args:
            story_data: 故事数据
        """
        self.current_story = story_data
        self._update_metrics()

    def _update_metrics(self):
        """更新故事指标"""
        if not self.current_story:
            return

        chapters = self.current_story.get("chapters", [])
        total_words = 0
        total_chars = 0

        for chapter in chapters:
            content = chapter.get("content", "")
            total_words += len(content.split())
            total_chars += len(content)

        self.metrics = {
            "title": self.current_story.get("title", "未命名故事"),
            "genre": self.current_story.get("genre", "未知"),
            "chapter_count": len(chapters),
            "total_words": total_words,
            "total_characters": total_chars,
            "average_chapter_length": total_words // len(chapters) if chapters else 0,
            "created_at": self.current_story.get("created_at"),
            "updated_at": self.current_story.get("updated_at"),
            "completion_percentage": self._calculate_completion(),
            "last_chapter_number": max([c.get("chapter_num", 0) for c in chapters]) if chapters else 0
        }

    def _calculate_completion(self) -> float:
        """计算完成度"""
        # 简单的完成度计算：基于章节数和平均长度
        target_chapters = 30  # 假设目标30章
        target_words_per_chapter = 2500  # 假设目标每章2500字

        current_chapters = self.metrics.get("chapter_count", 0)
        current_avg_length = self.metrics.get("average_chapter_length", 0)

        chapter_progress = min(100, (current_chapters / target_chapters) * 100)
        length_progress = min(100, (current_avg_length / target_words_per_chapter) * 100) if current_avg_length > 0 else 0

        return (chapter_progress + length_progress) / 2

    def display_dashboard(self, story_data: Dict[str, Any]):
        """
        显示故事仪表板

        Args:
            story_data: 故事数据
        """
        # 设置当前故事
        self.set_story(story_data)
        
        # 获取摘要信息
        summary = self.get_dashboard_summary()
        analysis = self.get_chapter_analysis()
        
        # 显示仪表板
        print("\n" + "="*60)
        print("📊 故事脉络仪表盘")
        print("="*60)
        
        # 故事基本信息
        print(f"\n📖 故事信息:")
        print(f"   标题: {summary['story_info']['title']}")
        print(f"   类型: {summary['story_info']['genre']}")
        print(f"   创建时间: {summary['story_info']['created_at']}")
        print(f"   最后更新: {summary['story_info']['updated_at']}")
        
        # 进度指标
        print(f"\n📈 进度指标:")
        print(f"   已写章节: {summary['progress_metrics']['chapters_written']} 章")
        print(f"   总字数: {summary['progress_metrics']['total_word_count']:,} 字")
        print(f"   平均章节长度: {summary['progress_metrics']['average_chapter_length']} 字")
        print(f"   完成度: {summary['progress_metrics']['completion_percentage']}%")
        
        # 写作统计
        print(f"\n✍️  写作统计:")
        print(f"   写作连续天数: {summary['writing_streak']} 天")
        
        # 章节长度分析
        print(f"\n📊 章节长度分析:")
        print(f"   最短章节: {analysis.get('length_statistics', {}).get('minimum', 0)} 字")
        print(f"   最长章节: {analysis.get('length_statistics', {}).get('maximum', 0)} 字")
        print(f"   平均长度: {analysis.get('length_statistics', {}).get('average', 0)} 字")
        
        # 长度分布
        print(f"\n📏 长度分布:")
        print(f"   短章节 (<1500字): {analysis.get('length_distribution', {}).get('short (<1500 words)', 0)} 章")
        print(f"   中等章节 (1500-3000字): {analysis.get('length_distribution', {}).get('medium (1500-3000 words)', 0)} 章")
        print(f"   长章节 (>3000字): {analysis.get('length_distribution', {}).get('long (>3000 words)', 0)} 章")
        
        # 最近活动
        print(f"\n🕒 最近活动:")
        for activity in summary['recent_activity'][:3]:  # 只显示最近3个活动
            print(f"   第{activity['chapter_num']}章: {activity['title']} ({activity['word_count']}字)")
        
        print("\n" + "="*60)

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """
        获取仪表板摘要

        Returns:
            Dict[str, Any]: 仪表板摘要
        """
        return {
            "story_info": {
                "title": self.metrics.get("title"),
                "genre": self.metrics.get("genre"),
                "created_at": self.metrics.get("created_at"),
                "updated_at": self.metrics.get("updated_at")
            },
            "progress_metrics": {
                "chapters_written": self.metrics.get("chapter_count", 0),
                "total_word_count": self.metrics.get("total_words", 0),
                "average_chapter_length": self.metrics.get("average_chapter_length", 0),
                "completion_percentage": round(self.metrics.get("completion_percentage", 0), 2)
            },
            "recent_activity": self._get_recent_activity(),
            "writing_streak": self._calculate_writing_streak()
        }

    def _get_recent_activity(self) -> List[Dict[str, Any]]:
        """获取最近活动"""
        chapters = self.current_story.get("chapters", [])

        # 按更新时间排序
        sorted_chapters = sorted(
            chapters,
            key=lambda x: x.get("updated_at", ""),
            reverse=True
        )

        recent_activity = []
        for chapter in sorted_chapters[:5]:  # 最近5个章节
            recent_activity.append({
                "type": "chapter_updated",
                "chapter_num": chapter.get("chapter_num"),
                "title": chapter.get("title", f"第{chapter.get('chapter_num')}章"),
                "timestamp": chapter.get("updated_at"),
                "word_count": len(chapter.get("content", "").split())
            })

        return recent_activity

    def _calculate_writing_streak(self) -> int:
        """计算写作连续天数"""
        chapters = self.current_story.get("chapters", [])
        if not chapters:
            return 0

        # 获取所有更新日期
        dates = set()
        for chapter in chapters:
            updated_at = chapter.get("updated_at")
            if updated_at:
                # 提取日期部分
                date_str = updated_at.split("T")[0] if "T" in updated_at else updated_at.split(" ")[0]
                dates.add(date_str)

        if not dates:
            return 0

        # 计算连续天数
        sorted_dates = sorted(dates, reverse=True)
        streak = 1

        for i in range(1, len(sorted_dates)):
            current_date = datetime.strptime(sorted_dates[i-1], "%Y-%m-%d")
            prev_date = datetime.strptime(sorted_dates[i], "%Y-%m-%d")

            # 检查是否是连续的日期
            if (current_date - prev_date).days == 1:
                streak += 1
            else:
                break

        return streak

    def get_chapter_analysis(self) -> Dict[str, Any]:
        """
        获取章节分析

        Returns:
            Dict[str, Any]: 章节分析
        """
        chapters = self.current_story.get("chapters", [])
        if not chapters:
            return {"error": "没有章节数据"}

        # 分析章节长度分布
        lengths = [len(ch.get("content", "").split()) for ch in chapters]

        # 计算统计信息
        min_length = min(lengths) if lengths else 0
        max_length = max(lengths) if lengths else 0
        avg_length = sum(lengths) / len(lengths) if lengths else 0

        # 长度分布
        short_chapters = sum(1 for l in lengths if l < 1500)
        medium_chapters = sum(1 for l in lengths if 1500 <= l < 3000)
        long_chapters = sum(1 for l in lengths if l >= 3000)

        return {
            "total_chapters": len(chapters),
            "length_statistics": {
                "minimum": min_length,
                "maximum": max_length,
                "average": round(avg_length, 1)
            },
            "length_distribution": {
                "short (<1500 words)": short_chapters,
                "medium (1500-3000 words)": medium_chapters,
                "long (>3000 words)": long_chapters
            },
            "chapter_details": [
                {
                    "chapter_num": ch.get("chapter_num"),
                    "title": ch.get("title", f"第{ch.get('chapter_num')}章"),
                    "word_count": len(ch.get("content", "").split()),
                    "created_at": ch.get("created_at"),
                    "updated_at": ch.get("updated_at")
                }
                for ch in chapters
            ]
        }

    def export_progress_report(self) -> str:
        """
        导出进度报告

        Returns:
            str: 进度报告文本
        """
        summary = self.get_dashboard_summary()
        analysis = self.get_chapter_analysis()

        report = f"""
=== 故事进度报告 ===

故事信息:
- 标题: {summary['story_info']['title']}
- 类型: {summary['story_info']['genre']}
- 创建时间: {summary['story_info']['created_at']}
- 最后更新: {summary['story_info']['updated_at']}

进度指标:
- 已写章节: {summary['progress_metrics']['chapters_written']} 章
- 总字数: {summary['progress_metrics']['total_word_count']} 字
- 平均章节长度: {summary['progress_metrics']['average_chapter_length']} 字
- 完成度: {summary['progress_metrics']['completion_percentage']}%

写作统计:
- 写作连续天数: {summary['writing_streak']} 天

章节长度分析:
- 最短章节: {analysis.get('length_statistics', {}).get('minimum', 0)} 字
- 最长章节: {analysis.get('length_statistics', {}).get('maximum', 0)} 字
- 平均长度: {analysis.get('length_statistics', {}).get('average', 0)} 字

长度分布:
- 短章节 (<1500字): {analysis.get('length_distribution', {}).get('short (<1500 words)', 0)} 章
- 中等章节 (1500-3000字): {analysis.get('length_distribution', {}).get('medium (1500-3000 words)', 0)} 章
- 长章节 (>3000字): {analysis.get('length_distribution', {}).get('long (>3000 words)', 0)} 章

最近活动:
"""

        for activity in summary['recent_activity']:
            report += f"- 第{activity['chapter_num']}章: {activity['title']} ({activity['word_count']}字)\n"

        report += f"\n报告生成时间: {datetime.now().isoformat()}\n"

        return report.strip()