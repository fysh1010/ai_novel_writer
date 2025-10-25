#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI写小说智能体 - 主程序
使用最新的智能体架构
"""

import sys
import os
from typing import Dict, Any, List

# 设置控制台编码为 UTF-8，避免 emoji 显示错误
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass  # 如果设置失败，继续运行

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from project_manager import ProjectManager
from agents.main_controller_agent import MainControllerAgent
from core.config_manager import config_manager
from core.enhanced_logger import enhanced_logger
from core.feedback_parameter_mapper import FeedbackParameterMapper
from core.story_dashboard import StoryDashboard
from core.branch_manager import BranchManager
# 移除动画相关导入

class NovelWriterApp:
    """AI写小说应用"""
    
    def __init__(self):
        """初始化应用"""
        self.project_manager = ProjectManager()
        self.main_controller = MainControllerAgent()
        self.running = True
        
        # 初始化配置和日志
        self.config = config_manager
        self.logger = enhanced_logger
        self.feedback_mapper = FeedbackParameterMapper()
        self.story_dashboard = StoryDashboard()
        self.branch_manager = BranchManager()
        
        # 记录系统启动
        self.logger.log_system_event("AI小说创作系统启动", "INFO")
    
    def _get_timestamp(self):
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _analyze_feedback_patterns(self, project_data: Dict[str, Any]):
        """多轮反馈聚合分析 - 增强版"""
        feedbacks = project_data.get("feedback", [])
        if len(feedbacks) < 2:
            return
        
        # 使用反馈参数映射器分析
        from core.data_schemas import UserFeedback
        
        # 转换反馈数据格式
        user_feedbacks = []
        for feedback in feedbacks:
            try:
                user_feedback = UserFeedback(**feedback)
                user_feedbacks.append(user_feedback)
            except:
                continue
        
        if not user_feedbacks:
            return
        
        # 分析反馈模式
        analysis = self.feedback_mapper.analyze_feedback_patterns(user_feedbacks)
        
        # 显示分析结果
        print(f"\n📊 反馈分析报告:")
        print(f"   平均评分: {analysis['average_rating']}/5")
        print(f"   总反馈数: {analysis['total_feedbacks']}")
        
        if analysis['frequent_issues']:
            print(f"   重复问题:")
            for issue in analysis['frequent_issues']:
                count = analysis['emotion_distribution'].get(issue, 0)
                print(f"     - {issue} (出现{count}次)")
        
        # 显示参数调整
        adjustments = analysis.get('adjustments', {})
        if adjustments.get('style_adjustments'):
            print(f"   系统调整:")
            for adjustment in adjustments['style_adjustments']:
                print(f"     ✅ {adjustment}")
        
        # 保存分析结果
        self.feedback_mapper.save_feedback_analysis(project_data.get("id", "unknown"), analysis)
    
    def _generate_feedback_summary(self, project_data: Dict[str, Any]):
        """生成反馈摘要报告"""
        feedbacks = project_data.get("feedback", [])
        if not feedbacks:
            return
        
        # 计算平均评分
        ratings = [f.get("rating", 3) for f in feedbacks if f.get("rating")]
        avg_rating = sum(ratings) / len(ratings) if ratings else 3
        
        # 统计情感标签
        all_emotions = []
        for feedback in feedbacks:
            all_emotions.extend(feedback.get("emotion_tags", []))
        
        emotion_counts = {}
        for emotion in all_emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # 生成摘要报告
        summary = {
            "project_id": project_data.get("id", "unknown"),
            "total_feedbacks": len(feedbacks),
            "average_rating": round(avg_rating, 2),
            "emotion_analysis": emotion_counts,
            "most_common_issues": sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True)[:5],
            "generated_at": self._get_timestamp()
        }
        
        # 保存到feedback目录
        import os
        import json
        
        feedback_dir = os.path.join("projects", project_data.get("id", "unknown"), "feedback")
        os.makedirs(feedback_dir, exist_ok=True)
        
        summary_file = os.path.join(feedback_dir, "feedback_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n📋 反馈摘要已保存到: {summary_file}")
        print(f"   平均评分: {avg_rating:.1f}/5")
        print(f"   总反馈数: {len(feedbacks)}")
        
        if emotion_counts:
            print(f"   主要问题: {', '.join([f'{k}({v}次)' for k, v in list(emotion_counts.items())[:3]])}")
    
    def show_menu(self):
        """显示主菜单"""
        print("\n" + "="*60)
        print("AI写小说智能体 v5.0")
        print("="*60)
        print("1. 创建新小说")
        print("2. 继续创作")
        print("3. 项目管理")
        print("4. 退出")
        print("="*60)
    
    def create_novel(self):
        """创建新小说"""
        print("\n📝 创建新小说")
        print("-" * 40)
        
        # 获取小说信息
        title = input("小说标题: ").strip()
        if not title:
            print("❌ 标题不能为空")
            return
        
        print("\n常见类型示例:")
        print("玄幻、都市、历史、科幻、武侠、洪荒、仙侠、军事、悬疑、言情等")
        
        genre = input("请输入小说类型: ").strip()
        if not genre:
            genre = "都市"
        
        theme = input("主题关键词 (如: 穿越、重生、系统): ").strip()
        if not theme:
            theme = "穿越"
        
        # 新增：用户自定义剧情简介
        print("\n💡 你可以输入自己的剧情想法，系统会据此进行创作")
        print("   如果不输入，系统将自动生成剧情简介")
        custom_plot = input("请输入剧情简介 (可选): ").strip()
        
        # 新增：剧情锁定参数
        story_lock = False
        if custom_plot:
            print("\n🔒 剧情锁定选项：")
            print("   开启后，系统会严格遵循你的剧情设定，防止AI偏题")
            lock_choice = input("是否锁定剧情主线？ (y/n): ").strip().lower()
            story_lock = lock_choice == 'y'
        
        print("\n📝 章节规划：")
        print("   提示：章节数仅作为参考，实际可根据创作情况灵活调整")
        print("   - 试写模式：建议先写3-5章看效果")
        print("   - 自由模式：边写边看，随时可完结")
        
        try:
            target_input = input("建议章节数 (默认50，输入0为自由模式): ").strip()
            if target_input == "0":
                target_length = 9999  # 自由模式，无限制
                print("✅ 已选择自由模式，无章节数限制")
            else:
                target_length = int(target_input or "50")
                print(f"✅ 建议章节数设为 {target_length} 章（可随时调整）")
        except ValueError:
            target_length = 50
            print(f"✅ 使用默认建议章节数 {target_length} 章")
        
        # 询问是否需要联网搜索
        print("\n" + "="*60)
        print("📡 是否需要联网搜索相关资料？")
        print("   适用于：历史题材、洪荒神话、真实人物背景等")
        print("   说明：系统会根据您的背景描述，搜索相关的真实信息")
        print("="*60)
        enable_web_search_input = input("是否启用联网搜索？(y/n，默认n): ").strip().lower()
        enable_web_search = enable_web_search_input in ['y', 'yes', '是']
        
        if enable_web_search:
            print("✅ 已启用联网搜索，将根据背景搜索相关资料")
        else:
            print("✅ 不启用联网搜索，完全基于您的背景描述创作")
        
        print(f"\n🚀 开始创建小说《{title}》...")
        
        try:
            # 创建项目
            project_data = {
                "title": title,
                "genre": genre,
                "theme": theme,
                "target_length": target_length,
                "author_style": "AI智能体创作",
                "current_chapter": 0,
                "chapters": [],
                "feedback": [],
                "custom_plot": custom_plot,  # 新增自定义剧情
                "story_lock": story_lock,  # 新增剧情锁定参数
                "enable_web_search": enable_web_search  # 新增：用户选择的联网搜索开关
            }
            
            project_id = self.project_manager.create_project(project_data)
            loaded_project = self.project_manager.load_project(project_id)
            
            if not loaded_project:
                print("❌ 项目创建失败")
                return
            
            print("✅ 项目创建成功")
            
            # 创建故事架构
            print("🏗️ 正在创建故事架构...")
            result = self.main_controller.process({
                    "type": "create_novel",
                    "title": title,
                    "genre": genre,
                    "theme": theme,
                    "target_length": target_length,
                    "custom_plot": custom_plot,  # 传递自定义剧情
                    "story_lock": story_lock,  # 传递剧情锁定参数
                    "enable_web_search": enable_web_search  # 传递用户选择的搜索开关
                })
            
            if result["type"] == "novel_created":
                novel_data = result["data"]
                
                # 更新项目数据
                loaded_project.update({
                    "story_framework": novel_data["story_framework"],
                    "character_system": novel_data["character_system"],
                    "plot_timeline": novel_data["plot_timeline"],
                    "knowledge_base": novel_data.get("knowledge_base", ""),
                    "real_info": novel_data.get("real_info", {}),
                    "requires_real_info": novel_data.get("requires_real_info", False)
                })
                
                # 保存项目
                self.project_manager.save_project(loaded_project)
                
                print("✅ 故事架构创建成功")
                print(f"📖 项目ID: {project_id}")
                print(f"🎯 题材: {novel_data.get('identified_genre', genre)}")
                print(f"📚 需要真实信息: {'是' if novel_data.get('requires_real_info', False) else '否'}")
                
                # 询问是否开始创作
                if input("\n是否开始创作第一章? (y/n): ").lower() == 'y':
                    self.write_chapter(loaded_project, 1)
            else:
                print(f"❌ 故事架构创建失败: {result.get('error', '未知错误')}")
                
        except Exception as e:
            print(f"❌ 创建小说时发生错误: {e}")
    
    def write_chapter(self, project_data: Dict[str, Any], chapter_num: int, ending_info: Dict[str, Any] = None):
        """创作章节
        
        Args:
            project_data: 项目数据
            chapter_num: 章节编号
            ending_info: 完结规划信息（可选），包含章节任务、关键点等
        """
        # 显示章节信息
        if ending_info:
            chapter_title = ending_info.get('章节标题建议', '')
            print(f"\n✍️ 正在创作第{chapter_num}章：{chapter_title}（完结篇）...")
        else:
            print(f"\n✍️ 正在创作第{chapter_num}章...")
        
        try:
            # 获取前面章节内容
            previous_chapters = []
            for chapter in project_data.get("chapters", []):
                previous_chapters.append({
                    "chapter_num": chapter["chapter_num"],
                    "content": chapter["content"],
                    "summary": chapter["summary"]
                })
            
            # 创作章节
            result = self.main_controller.process({
                    "type": "write_chapter",
                    "chapter_num": chapter_num,
                    "previous_chapters": previous_chapters,
                    "story_framework": project_data.get("story_framework", ""),
                    "character_system": project_data.get("character_system", ""),
                    "plot_timeline": project_data.get("plot_timeline", {}),
                    "knowledge_base": project_data.get("knowledge_base", ""),
                    "real_info": project_data.get("real_info", {}),
                    "requires_real_info": project_data.get("requires_real_info", False),
                    "ending_info": ending_info,  # 传入完结规划信息
                    "custom_prompt": ""
                })
            
            if result["type"] == "chapter_created":
                chapter_data = result["data"]
                
                # 添加到项目
                project_data["chapters"].append(chapter_data)
                project_data["current_chapter"] = chapter_num
                
                # 保存章节（包含TXT导出）
                self.project_manager.save_chapter(project_data, chapter_num, chapter_data)
                
                print("✅ 章节创作成功")
                print(f"📝 内容长度: {len(chapter_data['content'])} 字符")
                print(f"📋 摘要: {chapter_data['summary']}")
                
                # 记录章节创作成功
                self.logger.log_agent_activity("主控智能体", f"第{chapter_num}章创作完成", "INFO")
                
                # 显示章节内容预览
                content_preview = chapter_data['content'][:200] + "..." if len(chapter_data['content']) > 200 else chapter_data['content']
                print(f"\n📖 内容预览:\n{content_preview}")

                # 🎯 新增：用户质量评估和选择机制
                self._show_quality_assessment_menu(project_data, chapter_num, chapter_data)

                # 每个章节都显示用户反馈环节 - 使用统一菜单
                self._show_post_chapter_menu(project_data, chapter_num, chapter_data)
            else:
                print(f"❌ 章节创作失败: {result.get('error', '未知错误')}")
                
        except Exception as e:
            print(f"❌ 创作章节时发生错误: {e}")

    def _show_quality_assessment_menu(self, project_data: Dict[str, Any], chapter_num: int, chapter_data: Dict[str, Any]):
        """
        🎯 显示质量评估菜单 - 让用户参与质量控制
        """
        print("\n" + "="*50)
        print("📊 章节质量评估")
        print("="*50)

        # 获取质量检查结果（如果有的话）
        quality_info = chapter_data.get('quality_info', {})
        quality_score = quality_info.get('quality_score', 0)
        quality_report = quality_info.get('quality_report', '')

        if quality_score > 0:
            print(f"🤖 AI质量评分: {quality_score:.1f}/10")
            if quality_report:
                print(f"📋 质量报告: {quality_report[:100]}...")

        print("\n🎯 您对这个章节满意吗？")
        print("1. ✅ 很满意，继续下一章")
        print("2. 👍 基本满意，小幅优化")
        print("3. ⚠️  一般，需要重写")
        print("4. 💡 有想法，提供修改建议")
        print("5. 📊 查看详细质量分析")

        while True:
            try:
                choice = input("\n请选择 (1-5): ").strip()
                if choice == '1':
                    print("✅ 太棒了！继续创作下一章...")
                    break
                elif choice == '2':
                    print("🔧 正在进行小幅优化...")
                    self._optimize_chapter(project_data, chapter_num, chapter_data)
                    break
                elif choice == '3':
                    print("🔄 正在重新创作本章...")
                    self._rewrite_chapter(project_data, chapter_num, chapter_data)
                    break
                elif choice == '4':
                    self._collect_user_suggestions(project_data, chapter_num, chapter_data)
                    break
                elif choice == '5':
                    self._show_detailed_quality_analysis(quality_info)
                else:
                    print("❌ 请输入1-5之间的数字")
            except KeyboardInterrupt:
                print("\n⚠️ 用户取消操作")
                break

    def _optimize_chapter(self, project_data: Dict[str, Any], chapter_num: int, chapter_data: Dict[str, Any]):
        """小幅优化章节"""
        print("🔧 正在调用优化师进行润色...")

        # 调用优化师进行润色
        result = self.main_controller.optimize_chapter(project_data, chapter_data)
        if result.get("success"):
            optimized_content = result.get("content", chapter_data['content'])
            print("✅ 优化完成！")
            print("📝 优化后内容预览:")
            print(optimized_content[:200] + "...")

            # 更新章节数据
            chapter_data['content'] = optimized_content
            chapter_data['optimized'] = True

            # 保存优化后的章节（会覆盖原文件）
            self.project_manager.save_chapter(project_data, chapter_num, chapter_data)
            
            # 更新项目数据中的章节
            for i, ch in enumerate(project_data.get("chapters", [])):
                if ch.get("chapter_num") == chapter_num:
                    project_data["chapters"][i] = chapter_data
                    break
            
            print("💾 优化后的章节已保存并替换原文件！")
            print(f"📄 TXT文件已更新: projects/{project_data.get('title', '')}/txt/{chapter_num:02d}.*.txt")
        else:
            print("❌ 优化失败，保留原内容")

    def _rewrite_chapter(self, project_data: Dict[str, Any], chapter_num: int, chapter_data: Dict[str, Any]):
        """重新创作章节"""
        print("🔄 正在重新创作本章...")

        # 重新调用章节创作
        result = self.main_controller.process({
            "type": "write_chapter",
            "chapter_num": chapter_num,
            "previous_chapters": project_data.get("chapters", []),
            "story_framework": project_data.get("story_framework", ""),
            "character_system": project_data.get("character_system", ""),
            "plot_timeline": project_data.get("plot_timeline", {}),
            "knowledge_base": project_data.get("knowledge_base", ""),
            "real_info": project_data.get("real_info", {}),
            "requires_real_info": project_data.get("requires_real_info", False),
            "custom_prompt": "",
            "is_revision": True
        })
        
        if result["type"] == "chapter_created":
            new_chapter_data = result["data"]
            print("✅ 重写完成！")
            print("📝 新内容预览:")
            print(new_chapter_data.get('content', '')[:200] + "...")

            # 保存新章节（会覆盖原文件）
            self.project_manager.save_chapter(project_data, chapter_num, new_chapter_data)
            
            # 更新项目数据中的章节
            for i, ch in enumerate(project_data.get("chapters", [])):
                if ch.get("chapter_num") == chapter_num:
                    project_data["chapters"][i] = new_chapter_data
                    break
            
            print("💾 章节已保存并替换原文件！")
            print(f"📄 TXT文件已更新: projects/{project_data.get('title', '')}/txt/{chapter_num:02d}.*.txt")
        else:
            print("❌ 重写失败，保留原内容")

    def _collect_user_suggestions(self, project_data: Dict[str, Any], chapter_num: int, chapter_data: Dict[str, Any]):
        """收集用户修改建议"""
        print("\n💡 请详细描述您的修改建议：")
        print("   - 不满意的地方")
        print("   - 希望改进的方向")
        print("   - 具体的修改要求")

        suggestions = input("\n请输入您的建议: ").strip()
        if suggestions:
            # 保存用户建议
            feedback_data = {
                "type": "user_suggestion",
                "chapter": chapter_num,
                "suggestions": suggestions,
                "timestamp": self._get_timestamp()
            }

            # 保存到feedback目录
            import os
            import json
            feedback_dir = os.path.join("projects", project_data.get("id", ""), "feedback")
            os.makedirs(feedback_dir, exist_ok=True)

            feedback_file = os.path.join(feedback_dir, f"chapter_{chapter_num}_suggestions.json")
            with open(feedback_file, 'w', encoding='utf-8') as f:
                json.dump(feedback_data, f, ensure_ascii=False, indent=2)

            print(f"✅ 您的建议已保存，将在后续创作中参考")

            # 询问是否基于建议重写
            rewrite = input("是否基于您的建议重新创作本章？(y/n): ").strip().lower()
            if rewrite == 'y':
                self._rewrite_chapter(project_data, chapter_num, chapter_data)

    def _show_detailed_quality_analysis(self, quality_info: Dict[str, Any]):
        """显示详细质量分析"""
        print("\n📊 详细质量分析报告")
        print("="*40)

        if not quality_info:
            print("📋 暂无详细质量分析数据")
            return

        quality_report = quality_info.get('quality_report', '质量报告生成中...')
        print(quality_report)

        print("\n💡 质量提升建议：")
        print("• 关注角色一致性，确保行为符合性格设定")
        print("• 保持情节逻辑连贯，避免突兀转折")
        print("• 提升文学性，增强语言表达美感")
        print("• 增加创意元素，避免模板化叙事")

    def continue_writing(self):
        """继续创作"""
        print("\n📚 继续创作")
        print("-" * 40)
        
        # 获取项目列表
        projects = self.project_manager.list_projects()
        if not projects:
            print("❌ 没有找到项目")
            return
        
        print("现有项目:")
        for i, project in enumerate(projects, 1):
            status_icon = "✅" if project.get('status') == 'completed' else "📝"
            target = project.get('target_length', 50)
            mode_text = "(自由)" if target == 9999 else f"/{target}"
            print(f"{i}. {status_icon} {project['title']} ({project['genre']}) - {project.get('current_chapter', 0)}{mode_text}章")
        
        try:
            choice = int(input("选择项目 (输入序号): ").strip())
            if 1 <= choice <= len(projects):
                selected_project = projects[choice - 1]
                project_id = selected_project['project_id']
                
                # 加载项目
                project_data = self.project_manager.load_project(project_id)
                if not project_data:
                    print("❌ 项目加载失败")
                    return
                
                # 检查是否已完结
                if project_data.get("status") == "completed":
                    print("📚 该小说已完结")
                    reopen = input("是否重新开启创作？(y/n): ").strip().lower()
                    if reopen == "y":
                        project_data["status"] = "active"
                        self.project_manager.save_project(project_data)
                        print("✅ 已重新开启创作")
                    else:
                        return
                
                current_chapter = project_data.get("current_chapter", 0)
                next_chapter = current_chapter + 1
                target_length = project_data.get("target_length", 9999)
                
                # 显示进度提示
                if target_length == 9999:
                    print(f"📝 准备创作第 {next_chapter} 章（自由模式，无限制）")
                elif next_chapter > target_length:
                    print(f"📝 准备创作第 {next_chapter} 章")
                    print(f"⚠️ 已超过建议章节数({target_length}章)，可随时完结")
                else:
                    print(f"📝 准备创作第 {next_chapter} 章（进度：{next_chapter}/{target_length}）")
                
                # 允许创作，无硬性限制
                self.write_chapter(project_data, next_chapter)
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效数字")
        except Exception as e:
            print(f"❌ 继续创作时发生错误: {e}")
    
    def manage_projects(self):
        """项目管理 - 增强版"""
        print("\n📊 项目管理")
        print("-" * 40)
        
        projects = self.project_manager.list_projects()
        if not projects:
            print("❌ 没有找到项目")
            return
        
        print("项目列表:")
        for i, project in enumerate(projects, 1):
            status_icon = "✅" if project.get('status') == 'completed' else "📝"
            target = project.get('target_length', 50)
            mode_text = "(自由)" if target == 9999 else f"/{target}"
            print(f"{i}. {status_icon} {project['title']} ({project['genre']}) - {project.get('current_chapter', 0)}{mode_text}章")
        
        try:
            choice = int(input("选择项目 (输入序号): ").strip())
            if 1 <= choice <= len(projects):
                selected_project = projects[choice - 1]
                project_id = selected_project['project_id']
                
                # 加载项目
                project_data = self.project_manager.load_project(project_id)
                if not project_data:
                    print("❌ 项目加载失败")
                    return
                
                # 显示项目详情
                self._show_project_details(project_data)
                
                # 提供操作选项
                print("\n🔧 操作选项:")
                print("1. 查看故事脉络仪表盘")
                print("2. 继续创作")
                print("3. 分支管理")
                print("4. 返回主菜单")
                
                action = input("请选择操作 (1-4): ").strip()
                
                if action == "1":
                    # 显示仪表盘
                    self.story_dashboard.display_dashboard(project_data)
                elif action == "2":
                    # 继续创作
                    # 检查是否已完结
                    should_continue = True
                    if project_data.get("status") == "completed":
                        print("📚 该小说已完结")
                        reopen = input("是否重新开启创作？(y/n): ").strip().lower()
                        if reopen == "y":
                            project_data["status"] = "active"
                            self.project_manager.save_project(project_data)
                            print("✅ 已重新开启创作")
                        else:
                            should_continue = False
                            print("❌ 已取消")
                    
                    if should_continue:
                        current_chapter = project_data.get("current_chapter", 0)
                        next_chapter = current_chapter + 1
                        target_length = project_data.get("target_length", 9999)
                        
                        # 显示进度提示
                        if target_length == 9999:
                            print(f"📝 准备创作第 {next_chapter} 章（自由模式）")
                        elif next_chapter > target_length:
                            print(f"📝 准备创作第 {next_chapter} 章")
                            print(f"⚠️ 已超过建议章节数({target_length}章)，可随时完结")
                        else:
                            print(f"📝 准备创作第 {next_chapter} 章（进度：{next_chapter}/{target_length}）")
                        
                        # 允许创作，无硬性限制
                        self.write_chapter(project_data, next_chapter)
                elif action == "3":
                    # 分支管理
                    self._manage_branches(project_data)
                elif action == "4":
                    return
                else:
                    print("❌ 无效选择")
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效数字")
        except Exception as e:
            print(f"❌ 项目管理时发生错误: {e}")
    
    def _show_project_details(self, project_data: Dict[str, Any]):
        """显示项目详情"""
        print(f"\n📖 项目详情: {project_data['title']}")
        print(f"类型: {project_data['genre']}")
        print(f"主题: {project_data['theme']}")
        print(f"当前章节: {project_data.get('current_chapter', 0)}")
        
        # 显示目标章节或模式
        target_length = project_data.get('target_length', 50)
        if target_length == 9999:
            print(f"创作模式: 自由模式（无限制）")
        else:
            print(f"建议章节: {target_length}")
        
        # 显示完结状态
        status = project_data.get('status', 'active')
        if status == 'completed':
            print(f"状态: ✅ 已完结")
            completed_at = project_data.get('completed_at', '')
            if completed_at:
                from datetime import datetime
                try:
                    dt = datetime.fromisoformat(completed_at)
                    print(f"完结时间: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                except:
                    pass
        else:
            print(f"状态: 📝 创作中")
        
        # 显示章节列表
        chapters = project_data.get("chapters", [])
        if chapters:
            print(f"\n📚 章节列表:")
            for chapter in chapters:
                chapter_title = chapter.get('title', f'第{chapter.get("chapter_num", "?")}章')
                print(f"  第{chapter.get('chapter_num', '?')}章: {chapter_title}")
        
        # 显示反馈
        feedbacks = project_data.get("feedback", [])
        if feedbacks:
            print(f"\n💬 用户反馈:")
            for feedback in feedbacks:
                print(f"  第{feedback['chapter_num']}章: 评分{feedback.get('rating', 'N/A')} - {feedback.get('feedback', '无')}")
    
    def _manage_branches(self, project_data: Dict[str, Any]):
        """分支管理"""
        project_id = project_data.get("id", "unknown")
        
        print("\n🌳 分支管理")
        print("-" * 40)
        
        # 显示分支树
        self.branch_manager.display_branch_tree(project_id)
        
        # 显示分支统计
        stats = self.branch_manager.get_branch_statistics(project_id)
        if stats.get("total_branches", 0) > 0:
            print(f"\n📊 分支统计:")
            print(f"   总分支数: {stats['total_branches']}")
            print(f"   活跃分支: {stats['active_branches']}")
            print(f"   已合并分支: {stats['merged_branches']}")
            print(f"   平均分支长度: {stats['average_branch_length']} 章")
        
        # 分支操作选项
        print(f"\n🔧 分支操作:")
        print("1. 创建新分支")
        print("2. 查看分支详情")
        print("3. 合并分支")
        print("4. 比较分支")
        print("5. 删除分支")
        print("6. 返回项目管理")
        
        try:
            action = input("请选择操作 (1-6): ").strip()
            
            if action == "1":
                self._create_new_branch(project_data)
            elif action == "2":
                self._view_branch_details(project_id)
            elif action == "3":
                self._merge_branch(project_id)
            elif action == "4":
                self._compare_branches(project_id)
            elif action == "5":
                self._delete_branch(project_id)
            elif action == "6":
                return
            else:
                print("❌ 无效选择")
        except Exception as e:
            print(f"❌ 分支管理时发生错误: {e}")
    
    def _create_new_branch(self, project_data: Dict[str, Any]):
        """创建新分支"""
        project_id = project_data.get("id", "unknown")
        
        print("\n📂 创建新分支")
        print("-" * 30)
        
        branch_name = input("分支名称: ").strip()
        if not branch_name:
            print("❌ 分支名称不能为空")
            return
        
        description = input("分支描述 (可选): ").strip()
        
        # 选择分叉点
        chapters = project_data.get("chapters", [])
        if chapters:
            print(f"\n选择分叉点 (从第几章开始分叉):")
            for chapter in chapters:
                print(f"  {chapter['chapter_num']}. {chapter['title']}")
            
            try:
                fork_chapter = int(input("输入章节号: ").strip())
                if 1 <= fork_chapter <= len(chapters):
                    branch_id = self.branch_manager.fork_from_chapter(
                        project_id, fork_chapter, branch_name, description
                    )
                    print(f"✅ 分支创建成功: {branch_id}")
                else:
                    print("❌ 无效的章节号")
            except ValueError:
                print("❌ 请输入有效数字")
        else:
            print("❌ 项目暂无章节，无法创建分支")
    
    def _view_branch_details(self, project_id: str):
        """查看分支详情"""
        branches = self.branch_manager.list_branches(project_id)
        
        if not branches:
            print("❌ 暂无分支")
            return
        
        print(f"\n📋 选择要查看的分支:")
        for i, branch in enumerate(branches, 1):
            status_icon = "✅" if branch.get("status") == "merged" else "🔄"
            print(f"{i}. {status_icon} {branch.get('branch_name', 'Unknown')}")
        
        try:
            choice = int(input("输入分支序号: ").strip())
            if 1 <= choice <= len(branches):
                selected_branch = branches[choice - 1]
                branch_id = selected_branch.get("branch_id", "")
                
                # 加载分支数据
                branch_data = self.branch_manager.load_branch(branch_id)
                if branch_data:
                    print(f"\n📖 分支详情: {selected_branch.get('branch_name', '')}")
                    print(f"描述: {selected_branch.get('description', '无')}")
                    print(f"创建时间: {selected_branch.get('created_at', '')}")
                    print(f"状态: {selected_branch.get('status', 'unknown')}")
                    
                    chapters = branch_data.get("chapters", [])
                    print(f"章节数: {len(chapters)}")
                    
                    if chapters:
                        print(f"\n📚 章节列表:")
                        for chapter in chapters:
                            print(f"  第{chapter['chapter_num']}章: {chapter['title']}")
                else:
                    print("❌ 分支数据加载失败")
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效数字")
    
    def _merge_branch(self, project_id: str):
        """合并分支"""
        branches = self.branch_manager.list_branches(project_id)
        active_branches = [b for b in branches if b.get("status") == "active"]
        
        if not active_branches:
            print("❌ 暂无可合并的活跃分支")
            return
        
        print(f"\n🔄 选择要合并的分支:")
        for i, branch in enumerate(active_branches, 1):
            print(f"{i}. {branch.get('branch_name', 'Unknown')}")
        
        try:
            choice = int(input("输入分支序号: ").strip())
            if 1 <= choice <= len(active_branches):
                selected_branch = active_branches[choice - 1]
                branch_id = selected_branch.get("branch_id", "")
                
                # 确认合并
                confirm = input(f"确认合并分支 '{selected_branch.get('branch_name', '')}' 到主项目? (y/n): ").strip().lower()
                if confirm == 'y':
                    success = self.branch_manager.merge_branch(branch_id, project_id)
                    if success:
                        print("✅ 分支合并成功")
                    else:
                        print("❌ 分支合并失败")
                else:
                    print("❌ 取消合并")
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效数字")
    
    def _compare_branches(self, project_id: str):
        """比较分支"""
        branches = self.branch_manager.list_branches(project_id)
        
        if len(branches) < 2:
            print("❌ 需要至少2个分支才能比较")
            return
        
        print(f"\n⚖️ 选择要比较的分支:")
        for i, branch in enumerate(branches, 1):
            print(f"{i}. {branch.get('branch_name', 'Unknown')}")
        
        try:
            choice1 = int(input("选择第一个分支 (序号): ").strip())
            choice2 = int(input("选择第二个分支 (序号): ").strip())
            
            if 1 <= choice1 <= len(branches) and 1 <= choice2 <= len(branches) and choice1 != choice2:
                branch1_id = branches[choice1 - 1].get("branch_id", "")
                branch2_id = branches[choice2 - 1].get("branch_id", "")
                
                comparison = self.branch_manager.compare_branches(branch1_id, branch2_id)
                
                print(f"\n📊 分支比较结果:")
                print(f"分支1: {comparison['branch1']['name']} ({comparison['branch1']['chapters_count']}章, {comparison['branch1']['total_words']}字)")
                print(f"分支2: {comparison['branch2']['name']} ({comparison['branch2']['chapters_count']}章, {comparison['branch2']['total_words']}字)")
                
                differences = comparison.get("differences", [])
                if differences:
                    print(f"\n🔍 差异分析:")
                    for diff in differences:
                        print(f"  • {diff['description']}")
                else:
                    print(f"\n✅ 两个分支内容相同")
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效数字")
    
    def _delete_branch(self, project_id: str):
        """删除分支"""
        branches = self.branch_manager.list_branches(project_id)
        
        if not branches:
            print("❌ 暂无分支")
            return
        
        print(f"\n🗑️ 选择要删除的分支:")
        for i, branch in enumerate(branches, 1):
            status_icon = "✅" if branch.get("status") == "merged" else "🔄"
            print(f"{i}. {status_icon} {branch.get('branch_name', 'Unknown')}")
        
        try:
            choice = int(input("输入分支序号: ").strip())
            if 1 <= choice <= len(branches):
                selected_branch = branches[choice - 1]
                branch_id = selected_branch.get("branch_id", "")
                
                # 确认删除
                confirm = input(f"确认删除分支 '{selected_branch.get('branch_name', '')}'? (y/n): ").strip().lower()
                if confirm == 'y':
                    success = self.branch_manager.delete_branch(branch_id)
                    if success:
                        print("✅ 分支删除成功")
                    else:
                        print("❌ 分支删除失败")
                else:
                    print("❌ 取消删除")
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入有效数字")
    
    def _show_post_chapter_menu(self, project_data: Dict[str, Any], chapter_num: int, chapter_data: Dict[str, Any]):
        """统一章节后菜单 - 每个章节都有评分和反馈"""
        print(f"\n📝 第{chapter_num}章创作完成！")
        print("=" * 50)
        
        # 评分和反馈
        print("\n💬 请为本章评分并提供反馈:")
        print("😡 1分 - 无聊  😕 2分 - 一般  😌 3分 - 不错  🤩 4分 - 很好  🔥 5分 - 爽爆了")
        
        # 评分
        try:
            rating = int(input("请评分 (1-5): ").strip())
            if not 1 <= rating <= 5:
                rating = 3
        except:
            rating = 3
        
        # 情感标签
        emotion_tags = []
        if self.config.get("feedback", {}).get("enable_emotion_feedback", True):
            print("\n😊 情感标签 (可多选，用空格分隔):")
            print("1. 节奏太慢  2. 节奏太快  3. 冲突不够  4. 冲突太强")
            print("5. 角色有趣  6. 角色无聊  7. 文笔好  8. 文笔差")
            print("9. 剧情合理  10. 剧情不合理  11. 爽点不够  12. 爽点太多")
            
            emotion_input = input("请输入数字 (如: 1 3 11): ").strip()
            if emotion_input:
                try:
                    emotion_numbers = [int(x) for x in emotion_input.split()]
                    emotion_map = {
                        1: "节奏太慢", 2: "节奏太快", 3: "冲突不够", 4: "冲突太强",
                        5: "角色有趣", 6: "角色无聊", 7: "文笔好", 8: "文笔差",
                        9: "剧情合理", 10: "剧情不合理", 11: "爽点不够", 12: "爽点太多"
                    }
                    emotion_tags = [emotion_map.get(num, "") for num in emotion_numbers if emotion_map.get(num)]
                except:
                    pass
        
        # 操作选项
        print(f"\n🔧 操作选项:")
        print("1. 提出修改意见")
        print("2. 继续创作下一章")
        print("3. 完结小说")
        print("4. 查看故事脉络仪表盘")
        print("5. 分支管理")
        print("6. 返回主菜单")
        print("7. 退出系统")
        print("\n快捷键: e=完结, b=返回, m=主菜单, q=退出")
        
        while True:
            choice = input("请选择 (1-7): ").strip().lower()
            
            if choice in ['1', '修改', 'revision']:
                self._handle_revision_request(project_data, chapter_num, rating, emotion_tags)
                break
            elif choice in ['2', '继续', 'continue']:
                self._handle_continue_writing(project_data, chapter_num, rating, emotion_tags)
                break
            elif choice in ['3', 'e', '完结', 'finish', 'end']:
                self._handle_finish_novel(project_data)
                break
            elif choice in ['4', '仪表盘', 'dashboard']:
                self.story_dashboard.display_dashboard(project_data)
                # 继续显示菜单
                continue
            elif choice in ['5', '分支', 'branch']:
                self._manage_branches(project_data)
                # 继续显示菜单
                continue
            elif choice in ['6', 'b', '返回', 'back', 'm', '主菜单', 'main']:
                return
            elif choice in ['7', 'q', '退出', 'quit', 'exit']:
                print("👋 再见！")
                self.running = False
                return
            else:
                print("❌ 无效选择，请重新输入")
    
    def _handle_revision_request(self, project_data: Dict[str, Any], chapter_num: int, rating: int, emotion_tags: List[str]):
        """处理修改请求"""
        feedback = input("请提出你的修改意见: ").strip()
        if feedback:
            print(f"\n🔄 根据你的意见重新创作第{chapter_num}章...")
            
            # 创建修订分支
            branch_id = self.branch_manager.create_revision_branch(
                project_data.get("id", "unknown"), 
                chapter_num, 
                feedback,
                project_data  # 传递完整的项目数据
            )
            print(f"📂 已创建修订分支: {branch_id}")
            
            # 添加反馈到项目
            feedback_data = {
                "chapter_num": chapter_num,
                "rating": rating,
                "emotion_tags": emotion_tags,
                "feedback": feedback,
                "timestamp": self._get_timestamp(),
                "feedback_type": "revision_request",
                "branch_id": branch_id
            }
            project_data["feedback"].append(feedback_data)
            
            # 重新创作章节
            result = self.main_controller.process({
                "type": "write_chapter",
                "chapter_num": chapter_num,
                "previous_chapters": project_data.get("chapters", []),
                "story_framework": project_data.get("story_framework", ""),
                "character_system": project_data.get("character_system", ""),
                "plot_timeline": project_data.get("plot_timeline", {}),
                "knowledge_base": project_data.get("knowledge_base", ""),
                "real_info": project_data.get("real_info", {}),
                "requires_real_info": project_data.get("requires_real_info", False),
                "custom_prompt": f"用户反馈: {feedback}",
                "is_revision": True
            })
            
            if result["type"] == "chapter_created":
                # 替换章节内容
                project_data["chapters"][-1] = result["data"]
                self.project_manager.save_project(project_data)
                print("✅ 章节已根据你的意见重新创作")
                # 递归调用，重新显示结果
                self.write_chapter(project_data, chapter_num)
            else:
                print(f"❌ 重新创作失败: {result.get('error', '未知错误')}")
        else:
            print("❌ 请输入修改意见")
    
    def _analyze_feedback_patterns(self, project_data: Dict[str, Any]) -> List[str]:
        """分析反馈模式并生成调整建议"""
        feedbacks = project_data.get("feedback", [])
        if len(feedbacks) < 2:
            return []
        
        # 分析最近的反馈
        recent_feedbacks = feedbacks[-3:]  # 最近3章
        
        suggestions = []
        
        # 分析评分趋势
        ratings = [f.get("rating", 3) for f in recent_feedbacks if f.get("rating")]
        if ratings:
            avg_rating = sum(ratings) / len(ratings)
            if avg_rating < 3:
                suggestions.append("评分偏低，建议增加冲突强度和爽点密度")
            elif avg_rating > 4:
                suggestions.append("评分很高，保持当前创作风格")
        
        # 分析情感标签
        all_emotion_tags = []
        for f in recent_feedbacks:
            all_emotion_tags.extend(f.get("emotion_tags", []))
        
        if all_emotion_tags:
            # 统计标签频率
            tag_counts = {}
            for tag in all_emotion_tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            # 根据标签生成建议
            if "节奏太慢" in tag_counts and tag_counts["节奏太慢"] >= 2:
                suggestions.append("多次反馈节奏太慢，建议加快剧情推进速度")
            if "冲突不够" in tag_counts and tag_counts["冲突不够"] >= 2:
                suggestions.append("多次反馈冲突不够，建议增加矛盾冲突")
            if "爽点不够" in tag_counts and tag_counts["爽点不够"] >= 2:
                suggestions.append("多次反馈爽点不够，建议增加爽点密度")
            if "角色无聊" in tag_counts and tag_counts["角色无聊"] >= 2:
                suggestions.append("多次反馈角色无聊，建议增加角色互动和个性")
        
        return suggestions
    
    def _handle_continue_writing(self, project_data: Dict[str, Any], chapter_num: int, rating: int, emotion_tags: List[str]):
        """处理继续创作 - 根据反馈实时调整"""
        # 保存评分和情感反馈
        feedback_data = {
            "chapter_num": chapter_num,
            "rating": rating,
            "emotion_tags": emotion_tags,
            "feedback": "",
            "timestamp": self._get_timestamp(),
            "feedback_type": "continuation"
        }
        project_data["feedback"].append(feedback_data)
        
        # 保存项目
        self.project_manager.save_project(project_data)
        
        # 分析反馈模式并生成调整建议
        adjustment_suggestions = self._analyze_feedback_patterns(project_data)
        
        # 显示反馈分析结果
        if adjustment_suggestions:
            print(f"\n📊 反馈分析结果:")
            for suggestion in adjustment_suggestions:
                print(f"  💡 {suggestion}")
        
        # 继续下一章（移除章节数限制）
        next_chapter = chapter_num + 1
        target_length = project_data.get("target_length", 9999)
        
        if next_chapter > target_length and target_length != 9999:
            print(f"\n⚠️ 已超过建议章节数({target_length}章)，当前第{next_chapter}章")
            print("   (建议章节数仅供参考，可以继续创作)")
        
        print(f"\n🔄 根据你的反馈调整创作参数，开始第{next_chapter}章...")
        self.write_chapter(project_data, next_chapter)
    
    def _handle_finish_novel(self, project_data: Dict[str, Any]):
        """处理完结小说 - 智能规划完结方案"""
        title = project_data.get("title", "未命名")
        current_chapter = project_data.get("current_chapter", 0)
        target_length = project_data.get("target_length", 0)
        
        print(f"\n📚 规划小说完结《{title}》")
        print("=" * 60)
        print(f"当前进度: 已完成 {current_chapter} 章")
        if target_length and target_length != 9999:
            print(f"建议章节: {target_length} 章")
        print("=" * 60)
        
        # 选择完结方式
        print("\n完结方式：")
        print("1. 智能规划完结（推荐）- 系统分析剧情，规划完整收尾")
        print("2. 立即完结 - 在当前章节直接标记完结")
        print("3. 取消")
        
        choice = input("\n请选择 (1/2/3): ").strip()
        
        if choice == "1":
            # 智能规划完结
            self._plan_and_finish_novel(project_data)
        elif choice == "2":
            # 立即完结
            self._immediate_finish_novel(project_data)
        else:
            print("❌ 取消完结")
    
    def _plan_and_finish_novel(self, project_data: Dict[str, Any]):
        """智能规划并执行完结"""
        title = project_data.get("title", "未命名")
        current_chapter = project_data.get("current_chapter", 0)
        
        print(f"\n正在分析《{title}》的剧情...")
        
        # 生成完结规划
        ending_plan = self._generate_ending_plan(project_data)
        
        if not ending_plan:
            print("❌ 无法生成完结规划，请重试或选择立即完结")
            return
        
        # 展示规划方案
        self._display_ending_plan(ending_plan, current_chapter)
        
        # 用户确认
        confirm = input("\n确认执行此完结方案？(y/n/e=编辑调整): ").strip().lower()
        
        if confirm == "y":
            # 执行完结方案
            self._execute_ending_plan(project_data, ending_plan)
        elif confirm == "e":
            # 编辑调整
            print("编辑功能开发中...")
            return
        else:
            print("❌ 取消完结")
    
    def _immediate_finish_novel(self, project_data: Dict[str, Any]):
        """立即完结小说（原有逻辑）"""
        title = project_data.get("title", "未命名")
        current_chapter = project_data.get("current_chapter", 0)
        
        confirm = input(f"\n⚠️ 将在第{current_chapter}章直接完结，确认？(y/n): ").strip().lower()
        if confirm != 'y':
            print("❌ 取消完结")
            return
        
        # 标记为完结
        project_data["status"] = "completed"
        from datetime import datetime
        project_data["completed_at"] = datetime.now().isoformat()
        project_data["ending_type"] = "immediate"
        
        # 统计信息
        chapters = project_data.get("chapters", [])
        total_words = sum(len(ch.get("content", "")) for ch in chapters)
        
        # 保存项目
        self.project_manager.save_project(project_data)
        
        print(f"\n✅ 《{title}》已完结！")
        print("=" * 60)
        print(f"📊 完结统计:")
        print(f"   总章节数: {current_chapter} 章")
        print(f"   总字数: {total_words:,} 字")
        print(f"   完结方式: 立即完结")
        print(f"   完结时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        self.logger.log_system_event(f"小说《{title}》完结，共{current_chapter}章", "INFO")
    
    def _generate_ending_plan(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """生成完结规划方案"""
        import json
        
        title = project_data.get("title", "")
        genre = project_data.get("genre", "")
        theme = project_data.get("theme", "")
        current_chapter = project_data.get("current_chapter", 0)
        chapters = project_data.get("chapters", [])
        
        # 提取最近章节摘要
        recent_chapters = chapters[-10:] if len(chapters) > 10 else chapters
        chapter_summaries = "\n".join([
            f"第{ch['chapter_num']}章 {ch.get('title', '')}：{ch.get('summary', '')}"
            for ch in recent_chapters
        ])
        
        # 生成规划提示词
        prompt = f"""
你是专业的小说编辑和策划，请分析这部小说并规划一个完整的收尾方案。

小说信息：
- 标题：{title}
- 题材：{genre}
- 主题：{theme}
- 当前进度：已完成 {current_chapter} 章

最近章节内容：
{chapter_summaries}

请深度分析并规划：

1. 当前剧情发展阶段（开端/发展/高潮/收尾）
2. 还有哪些主要矛盾、伏笔、悬念未解决
3. 需要多少章节来完整收尾（建议2-5章，根据复杂度调整）
4. 每一章的具体任务和关键剧情点

要求：
- 必须给出完整、合理的结局，不能戛然而止
- 要解决所有主要矛盾和伏笔
- 要给主要角色一个明确的结局
- 收尾章节数要合理（不要太多也不要太少）

请以JSON格式返回（严格遵守格式）：
{{
  "当前剧情阶段": "高潮期/发展期/收尾期",
  "未解决的主要问题": ["问题1", "问题2", "问题3"],
  "建议完结章节数": 3,
  "整体情感氛围": "悲壮/圆满/开放式/温馨/激昂",
  "完结章节规划": [
    {{
      "章节序号": {current_chapter + 1},
      "章节标题建议": "标题",
      "章节任务": "本章要完成的任务",
      "关键剧情点": ["要点1", "要点2", "要点3"],
      "情感基调": "紧张/温馨/激昂/悲伤/喜悦等",
      "预计字数": "3000-5000字"
    }}
  ],
  "完结说明": "整体完结方案的说明",
  "结局类型": "圆满结局/开放式结局/悲剧结局/留白结局"
}}

注意：
1. 必须返回有效的JSON格式
2. 章节序号要从{current_chapter + 1}开始递增
3. 每章都要有明确的任务和剧情点
4. 最后一章要有明确的结局感
"""
        
        try:
            response = self.main_controller.forward(prompt)
            if response.is_success():
                result_text = response.get_content()
                
                # 解析JSON
                if '{' in result_text:
                    json_start = result_text.index('{')
                    json_end = result_text.rindex('}') + 1
                    json_str = result_text[json_start:json_end]
                    ending_plan = json.loads(json_str)
                    return ending_plan
            
            return None
        except Exception as e:
            print(f"❌ 生成完结规划失败：{e}")
            return None
    
    def _display_ending_plan(self, ending_plan: Dict[str, Any], current_chapter: int):
        """展示完结规划方案"""
        print("\n" + "=" * 60)
        print("📖 完结规划方案")
        print("=" * 60)
        
        # 显示剧情阶段和情感氛围
        print(f"\n📊 当前状态：")
        print(f"   剧情阶段：{ending_plan.get('当前剧情阶段', '未知')}")
        print(f"   整体情感：{ending_plan.get('整体情感氛围', '未设定')}")
        print(f"   结局类型：{ending_plan.get('结局类型', '未设定')}")
        
        problems = ending_plan.get('未解决的主要问题', [])
        if problems:
            print(f"\n⚠️ 待解决的问题：")
            for i, problem in enumerate(problems, 1):
                print(f"  {i}. {problem}")
        
        chapter_count = ending_plan.get('建议完结章节数', 0)
        print(f"\n📝 建议再写 {chapter_count} 章完整收尾")
        print("=" * 60)
        
        # 使用表格化显示章节规划
        chapters_plan = ending_plan.get('完结章节规划', [])
        for i, chapter_plan in enumerate(chapters_plan, 1):
            chapter_num = chapter_plan.get('章节序号', current_chapter + i)
            chapter_title = chapter_plan.get('章节标题建议', '未命名')
            emotion = chapter_plan.get('情感基调', '')
            word_count = chapter_plan.get('预计字数', '')
            
            print(f"\n第{chapter_num}章：{chapter_title}")
            if emotion:
                print(f"   情感基调：{emotion}")
            if word_count:
                print(f"   预计字数：{word_count}")
            print(f"   任务：{chapter_plan.get('章节任务', '')}")
            
            key_points = chapter_plan.get('关键剧情点', [])
            if key_points:
                print(f"   关键点：")
                for point in key_points:
                    print(f"     - {point}")
        
        print("\n" + "=" * 60)
        explanation = ending_plan.get('完结说明', '')
        if explanation:
            print(f"💡 方案说明：\n{explanation}")
            print("=" * 60)
    
    def _execute_ending_plan(self, project_data: Dict[str, Any], ending_plan: Dict[str, Any]):
        """执行完结规划方案 - 逐章创作，每章后用户确认"""
        from datetime import datetime
        import uuid
        
        title = project_data.get("title", "未命名")
        chapters_plan = ending_plan.get('完结章节规划', [])
        
        if not chapters_plan:
            print("❌ 完结规划为空，无法执行")
            return
        
        # 生成唯一的规划ID（版本追踪）
        plan_id = str(uuid.uuid4())[:8]
        ending_plan['plan_id'] = plan_id
        ending_plan['created_at'] = datetime.now().isoformat()
        
        print(f"\n🚀 开始创作完结篇（共{len(chapters_plan)}章）")
        print(f"📋 规划ID: {plan_id}")
        print("=" * 60)
        
        # 逐章创作，每章后用户确认
        total_chapters = len(chapters_plan)
        completed_chapters = 0
        
        for i, chapter_plan in enumerate(chapters_plan, 1):
            chapter_num = chapter_plan.get('章节序号')
            chapter_title = chapter_plan.get('章节标题建议', '')
            
            # 显示进度
            progress = int((i - 1) / total_chapters * 100)
            progress_bar = self._create_progress_bar(progress, 20)
            print(f"\n进度: {progress_bar} {progress}% ({i-1}/{total_chapters})")
            
            print(f"\n📝 准备创作第{chapter_num}章：{chapter_title}")
            print(f"任务：{chapter_plan.get('章节任务', '')}")
            
            # 创作章节（传入完结规划信息）
            try:
                self.write_chapter(project_data, chapter_num, ending_info=chapter_plan)
                completed_chapters += 1
                
                # 显示完成进度
                progress = int(i / total_chapters * 100)
                progress_bar = self._create_progress_bar(progress, 20)
                print(f"\n✅ 第{chapter_num}章完成")
                print(f"进度: {progress_bar} {progress}% ({i}/{total_chapters})")
                
                # 如果不是最后一章，询问是否继续
                if i < total_chapters:
                    print("\n" + "-" * 60)
                    print(f"下一章：第{chapters_plan[i]['章节序号']}章 - {chapters_plan[i]['章节标题建议']}")
                    choice = input("是否继续创作下一章？(y=继续, n=暂停, s=跳过后续全部自动完成): ").strip().lower()
                    
                    if choice == 'n':
                        print("⏸️ 已暂停完结篇创作")
                        print(f"当前进度: {completed_chapters}/{total_chapters} 章")
                        print("提示: 可以稍后继续，或在当前基础上调整")
                        return
                    elif choice == 's':
                        print("⚡ 跳过确认，自动完成剩余章节...")
                        # 自动完成剩余章节
                        for remaining_plan in chapters_plan[i:]:
                            remaining_num = remaining_plan.get('章节序号')
                            remaining_title = remaining_plan.get('章节标题建议', '')
                            print(f"\n📝 正在创作第{remaining_num}章：{remaining_title}...")
                            try:
                                self.write_chapter(project_data, remaining_num, ending_info=remaining_plan)
                                completed_chapters += 1
                                progress = int((completed_chapters) / total_chapters * 100)
                                progress_bar = self._create_progress_bar(progress, 20)
                                print(f"✅ 第{remaining_num}章完成 {progress_bar} {progress}%")
                            except Exception as e:
                                print(f"❌ 第{remaining_num}章创作失败：{e}")
                                return
                        break
                    # else: choice == 'y' 继续下一章
                    
            except Exception as e:
                print(f"❌ 第{chapter_num}章创作失败：{e}")
                print("可以选择：")
                print("1. 修复问题后重试")
                print("2. 暂停并手动调整")
                return
        
        # 标记为完结
        project_data["status"] = "completed"
        project_data["completed_at"] = datetime.now().isoformat()
        project_data["ending_type"] = "planned"
        project_data["ending_plan"] = ending_plan
        
        # 保存项目
        self.project_manager.save_project(project_data)
        
        # 统计信息
        current_chapter = project_data.get("current_chapter", 0)
        chapters = project_data.get("chapters", [])
        total_words = sum(len(ch.get("content", "")) for ch in chapters)
        
        print("\n" + "=" * 60)
        print(f"✅ 《{title}》已完结！")
        print("=" * 60)
        print(f"📊 完结统计:")
        print(f"   总章节数: {current_chapter} 章")
        print(f"   总字数: {total_words:,} 字")
        print(f"   完结方式: 智能规划完结")
        print(f"   完结章节: {len(chapters_plan)} 章")
        print(f"   完结时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print(f"\n📂 完整小说已保存:")
        print(f"   位置: projects/{title}/")
        print(f"   - {title}.txt (完整版)")
        print(f"   - txt/ (各章单独文件)")
        print(f"   - chapters.json (章节数据)")
        print("=" * 60)
        
        self.logger.log_system_event(f"小说《{title}》智能规划完结，共{current_chapter}章", "INFO")
    
    def _create_progress_bar(self, percentage: int, width: int = 20) -> str:
        """创建进度条
        
        Args:
            percentage: 完成百分比 (0-100)
            width: 进度条宽度
            
        Returns:
            进度条字符串，例如：[###########---------]
        """
        filled = int(width * percentage / 100)
        empty = width - filled
        return f"[{'#' * filled}{'-' * empty}]"
    
    def run(self):
        """运行应用"""
        print("🚀 AI写小说智能体启动中...")
        
        while self.running:
            try:
                self.show_menu()
                choice = input("请选择操作 (1-4): ").strip()
                
                if choice == "1":
                    self.create_novel()
                elif choice == "2":
                    self.continue_writing()
                elif choice == "3":
                    self.manage_projects()
                elif choice == "4":
                    print("👋 再见！")
                    self.running = False
                else:
                    print("❌ 无效选择，请重新输入")
                    
            except KeyboardInterrupt:
                print("\n👋 再见！")
                self.running = False
            except Exception as e:
                print(f"❌ 发生错误: {e}")

def main():
    """主函数"""
    app = NovelWriterApp()
    app.run()

if __name__ == "__main__":
    main()
