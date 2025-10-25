#!/usr/bin/env python3
"""
第五层：智囊体（Compliance Advisor）
负责内容审查、违禁词检测、同义词替换等合规性检查
"""

import json
import re
from typing import Dict, List, Any, Tuple
from .base_agent import BaseAgent

class ComplianceAdvisorAgent(BaseAgent):
    """智囊体 - 内容审查与修正智能体"""
    
    def __init__(self):
        super().__init__("智囊体")
        self.sensitive_dict = self._load_sensitive_dict()
        self.replacement_rules = self._load_replacement_rules()
    
    def _load_sensitive_dict(self) -> Dict[str, List[str]]:
        """加载敏感词词典"""
        import os
        sensitive_dict_file = os.path.join(os.path.dirname(__file__), "..", "data", "sensitive_dict.json")
        
        if os.path.exists(sensitive_dict_file):
            try:
                with open(sensitive_dict_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 如果文件不存在或加载失败，使用默认词典
        return {
            "brands": [
                "苹果公司", "Apple", "iPhone", "iPad", "MacBook",
                "华为", "Huawei", "小米", "Xiaomi", "OPPO", "VIVO",
                "腾讯", "Tencent", "阿里巴巴", "Alibaba", "百度", "Baidu",
                "字节跳动", "ByteDance", "美团", "Meituan", "滴滴", "Didi"
            ],
            "political": [
                "政府", "国家", "政治", "领导人", "主席", "总理",
                "共产党", "社会主义", "资本主义", "民主", "自由"
            ],
            "violence": [
                "暴力", "血腥", "杀戮", "屠杀", "死亡", "自杀",
                "恐怖", "恐怖主义", "爆炸", "枪击", "刀伤"
            ],
            "adult": [
                "色情", "性爱", "裸体", "淫秽", "黄色", "成人"
            ]
        }
    
    def _load_replacement_rules(self) -> Dict[str, str]:
        """加载替换规则"""
        import os
        replacement_rules_file = os.path.join(os.path.dirname(__file__), "..", "data", "replacement_rules.json")
        
        if os.path.exists(replacement_rules_file):
            try:
                with open(replacement_rules_file, 'r', encoding='utf-8') as f:
                    rules_data = json.load(f)
                    # 合并所有类别的替换规则
                    combined_rules = {}
                    for category, rules in rules_data.items():
                        combined_rules.update(rules)
                    return combined_rules
            except:
                pass
        
        # 如果文件不存在或加载失败，使用默认规则
        return {
            # 品牌替换
            "苹果公司": "水果科技",
            "Apple": "水果科技",
            "iPhone": "智能灵机",
            "iPad": "平板灵机",
            "MacBook": "笔记本灵机",
            "华为": "神威科技",
            "Huawei": "神威科技",
            "小米": "谷物科技",
            "Xiaomi": "谷物科技",
            "腾讯": "天讯科技",
            "Tencent": "天讯科技",
            "阿里巴巴": "天宝集团",
            "Alibaba": "天宝集团",
            "百度": "千度搜索",
            "Baidu": "千度搜索",
            "字节跳动": "字节科技",
            "ByteDance": "字节科技",
            "美团": "美食团",
            "Meituan": "美食团",
            "滴滴": "出行科技",
            "Didi": "出行科技",
            
            # 政治敏感词替换
            "政府": "管理机构",
            "国家": "地区",
            "政治": "管理",
            "领导人": "管理者",
            "主席": "负责人",
            "总理": "执行长",
            "共产党": "管理党",
            "社会主义": "集体主义",
            "资本主义": "市场主义",
            "民主": "民治",
            "自由": "自主",
            
            # 暴力词汇替换
            "暴力": "冲突",
            "血腥": "激烈",
            "杀戮": "战斗",
            "屠杀": "大规模战斗",
            "死亡": "离去",
            "自杀": "自我了断",
            "恐怖": "可怕",
            "恐怖主义": "极端主义",
            "爆炸": "巨响",
            "枪击": "射击",
            "刀伤": "刀伤",
            
            # 成人内容替换
            "色情": "情感",
            "性爱": "亲密",
            "裸体": "无衣",
            "淫秽": "不当",
            "黄色": "成人",
            "成人": "成熟"
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理内容审查请求 - 增强版"""
        content = input_data.get("content", "")
        content_type = input_data.get("type", "chapter")
        auto_replace = input_data.get("auto_replace", True)  # 新增：是否自动替换
        force_check = input_data.get("force_check", False)  # 新增：强制检查
        
        if not content:
            return {
                "content": "",
                "compliance_report": {
                    "status": "empty",
                    "message": "内容为空，无需审查"
                }
            }
        
        # 智能触发检查
        if not force_check and not self._should_trigger_compliance_check(content):
            return {
                "content": content,
                "compliance_report": {
                    "status": "skipped",
                    "message": "内容安全，跳过审查",
                    "risk_score": 0,
                    "corrections_applied": 0
                }
            }
        
        # 执行内容审查
        compliance_result = self._check_compliance(content)
        
        # 新增：替换确认机制
        if not auto_replace and compliance_result["issues"]:
            # 显示需要确认的替换项
            confirmed_issues = self._confirm_replacements(compliance_result["issues"])
            compliance_result["issues"] = confirmed_issues
        
        # 生成修正后的内容
        corrected_content = self._apply_corrections(content, compliance_result["issues"])
        
        # 生成审查报告
        compliance_report = self._generate_compliance_report(compliance_result, content, corrected_content)
        
        return {
            "content": corrected_content,
            "compliance_report": compliance_report,
            "original_content": content,
            "corrections_applied": len(compliance_result["issues"])
        }
    
    def _check_compliance(self, content: str) -> Dict[str, Any]:
        """检查内容合规性 - 五维审查"""
        issues = []
        sensitive_words_found = []
        
        # 1. 法律类审查 - 品牌名/真实机构
        legal_issues = self._check_legal_compliance(content)
        issues.extend(legal_issues)
        
        # 2. 社会类审查 - 政治敏感话题
        social_issues = self._check_social_compliance(content)
        issues.extend(social_issues)
        
        # 3. 道德类审查 - 性、暴力、侮辱
        moral_issues = self._check_moral_compliance(content)
        issues.extend(moral_issues)
        
        # 4. 逻辑类审查 - 设定矛盾、时序混乱
        logic_issues = self._check_logic_consistency(content)
        issues.extend(logic_issues)
        
        # 5. 审美类审查 - 文风突变、AI痕迹
        aesthetic_issues = self._check_aesthetic_compliance(content)
        issues.extend(aesthetic_issues)
        
        # 计算风险评分
        risk_score = self._calculate_risk_score(issues)
        
        # 新增：问题分级体系
        classified_issues = self._classify_issues_by_severity(issues)
        
        return {
            "issues": issues,
            "classified_issues": classified_issues,
            "sensitive_words": sensitive_words_found,
            "total_issues": len(issues),
            "high_severity": len([i for i in issues if i.get("severity") == "high"]),
            "medium_severity": len([i for i in issues if i.get("severity") == "medium"]),
            "low_severity": len([i for i in issues if i.get("severity") == "low"]),
            "risk_score": risk_score,
            "dimension_scores": {
                "legal": len(legal_issues),
                "social": len(social_issues),
                "moral": len(moral_issues),
                "logic": len(logic_issues),
                "aesthetic": len(aesthetic_issues)
            }
        }
    
    def _get_severity(self, category: str) -> str:
        """获取问题严重程度"""
        severity_map = {
            "political": "high",
            "violence": "high", 
            "adult": "high",
            "brands": "medium"
        }
        return severity_map.get(category, "low")
    
    def _classify_issues_by_severity(self, issues: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """问题分级体系 - 增强版"""
        classified = {
            "critical": [],  # 高危：政治、色情、仇恨、暴力
            "warning": [],   # 中危：商标、公司名、社会机构
            "suggestion": [] # 低危：敏感表达、隐喻、讽刺
        }
        
        for issue in issues:
            severity = issue.get("severity", "medium")
            category = issue.get("category", "")
            
            if severity == "high" or category in ["political", "violence", "adult", "hate"]:
                classified["critical"].append(issue)
            elif severity == "medium" or category in ["brands", "company", "institution"]:
                classified["warning"].append(issue)
            else:
                classified["suggestion"].append(issue)
        
        return classified
    
    def _confirm_replacements(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """替换确认机制"""
        confirmed_issues = []
        
        for issue in issues:
            if issue.get("type") == "sensitive_word" and issue.get("replacement"):
                original = issue.get("original", "")
                replacement = issue.get("replacement", "")
                category = issue.get("category", "")
                
                print(f"\n🔍 智囊体发现: \"{original}\" → \"{replacement}\"")
                print(f"   类别: {category}")
                
                # 高危问题自动替换，其他需要确认
                if issue.get("severity") == "high":
                    print("   ⚠️ 高危内容，自动替换")
                    confirmed_issues.append(issue)
                else:
                    confirm = input("   是否接受此替换？ (y/n): ").strip().lower()
                    if confirm == 'y':
                        confirmed_issues.append(issue)
                        print("   ✅ 已确认替换")
                    else:
                        print("   ❌ 跳过替换")
            else:
                confirmed_issues.append(issue)
        
        return confirmed_issues
    
    def _generate_summary_report(self, compliance_result: Dict[str, Any], content: str) -> str:
        """自动生成摘要报告"""
        # 安全获取内容文本
        content_text = content.get_content() if hasattr(content, 'get_content') else str(content)
        total_words = len(content_text)
        total_issues = compliance_result.get("total_issues", 0)
        risk_score = compliance_result.get("risk_score", 0)
        classified_issues = compliance_result.get("classified_issues", {})
        
        critical_count = len(classified_issues.get("critical", []))
        warning_count = len(classified_issues.get("warning", []))
        suggestion_count = len(classified_issues.get("suggestion", []))
        
        # 计算安全评分
        safety_score = max(0, 100 - risk_score)
        
        summary = f"""
📋 本章合规摘要:
   总词数: {total_words:,}
   发现问题: {total_issues} 个
   - ❌ 高危: {critical_count} 个
   - ⚠️ 中危: {warning_count} 个  
   - 📝 低危: {suggestion_count} 个
   安全评分: {safety_score}%
   审查状态: {'✅ 通过' if risk_score < 50 else '⚠️ 需注意' if risk_score < 80 else '❌ 高风险'}
"""
        return summary.strip()
    
    def _check_logic_consistency(self, content: str) -> List[Dict[str, Any]]:
        """检查逻辑一致性 - 增强版"""
        # 安全获取内容文本
        content_text = content.get_content() if hasattr(content, 'get_content') else str(content)

        issues = []

        # 1. 基础逻辑检查
        basic_logic_issues = self._check_basic_logic(content_text)
        issues.extend(basic_logic_issues)

        # 2. 权限逻辑检查（程序员视角）
        permission_issues = self._check_permission_logic(content_text)
        issues.extend(permission_issues)

        # 3. 系统逻辑检查（技术视角）
        system_issues = self._check_system_logic(content_text)
        issues.extend(system_issues)

        # 4. 读者视角逻辑检查
        reader_issues = self._check_reader_perspective(content_text)
        issues.extend(reader_issues)

        # 5. 文学质量检查
        literary_issues = self._check_literary_quality(content_text)
        issues.extend(literary_issues)

        return issues
    
    def _check_basic_logic(self, content: str) -> List[Dict[str, Any]]:
        """检查基础逻辑"""
        issues = []
        
        # 检查时间逻辑
        time_patterns = [
            r"(\d{4})年.*?(\d{4})年",
            r"昨天.*?明天",
            r"上周.*?下周"
        ]
        
        for pattern in time_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues.append({
                    "type": "logic_inconsistency",
                    "category": "time_logic",
                    "description": f"发现时间逻辑问题: {matches[0]}",
                    "severity": "medium"
                })
        
        # 检查人物逻辑
        character_patterns = [
            r"(\w+)死了.*?(\w+)还活着",
            r"(\w+)是(\w+)的儿子.*?(\w+)是(\w+)的父亲"
        ]
        
        for pattern in character_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues.append({
                    "type": "logic_inconsistency", 
                    "category": "character_logic",
                    "description": f"发现人物逻辑问题: {matches[0]}",
                    "severity": "medium"
                })
        
        return issues
    
    def _check_permission_logic(self, content: str) -> List[Dict[str, Any]]:
        """检查权限逻辑（程序员视角）"""
        issues = []
        
        # 检查权限矛盾
        if ("只读权限" in content or "只读访问" in content) and ("修改" in content or "写入" in content or "编辑" in content):
            issues.append({
                "type": "permission_contradiction",
                "description": "权限逻辑矛盾：只读权限无法进行修改操作",
                "severity": "high",
                "category": "logic",
                "suggestion": "需要解释权限来源，如'系统漏洞'、'特殊身份'或'临时权限'"
            })
        
        # 检查权限升级逻辑
        if "权限等级" in content and "提升" in content:
            if "原因" not in content and "为什么" not in content:
                issues.append({
                    "type": "permission_upgrade_unclear",
                    "description": "权限升级原因不明确",
                    "severity": "medium",
                    "category": "logic",
                    "suggestion": "需要解释权限升级的原因和过程"
                })
        
        return issues
    
    def _check_system_logic(self, content: str) -> List[Dict[str, Any]]:
        """检查系统逻辑（技术视角）"""
        issues = []
        
        # 检查系统bug逻辑
        if "未定义" in content and "系统" in content:
            if "完善" in content or "稳定" in content:
                issues.append({
                    "type": "system_logic_contradiction",
                    "description": "系统逻辑矛盾：完善系统不应有未定义值",
                    "severity": "high",
                    "category": "logic",
                    "suggestion": "需要解释为'系统升级中'、'权限变更'或'检测模块损坏'"
                })
        
        # 检查配置文件逻辑
        if "配置文件" in content and "修改" in content:
            if "权限" not in content and "授权" not in content:
                issues.append({
                    "type": "config_edit_permission_unclear",
                    "description": "配置文件修改权限不明确",
                    "severity": "medium",
                    "category": "logic",
                    "suggestion": "需要说明为什么能修改配置文件"
                })
        
        return issues
    
    def _check_reader_perspective(self, content: str) -> List[Dict[str, Any]]:
        """检查读者视角逻辑"""
        issues = []
        
        # 检查可能引起读者疑问的地方
        if "突然" in content or "忽然" in content:
            if "原因" not in content and "为什么" not in content:
                issues.append({
                    "type": "sudden_change_unexplained",
                    "description": "突然变化缺乏解释",
                    "severity": "medium",
                    "category": "logic",
                    "suggestion": "需要解释突然变化的原因"
                })
        
        # 检查因果关系
        if "因为" in content and "所以" in content:
            if "但是" in content or "然而" in content:
                issues.append({
                    "type": "causal_relationship_unclear",
                    "description": "因果关系可能不清晰",
                    "severity": "low",
                    "category": "logic",
                    "suggestion": "需要明确因果关系"
                })
        
        return issues
    
    def _check_literary_quality(self, content: str) -> List[Dict[str, Any]]:
        """检查文学质量"""
        issues = []

        # 检查文笔质量
        if "然后" in content and content.count("然后") > 3:
            issues.append({
                "type": "repetitive_language",
                "description": "语言重复，文笔单调",
                "severity": "medium",
                "category": "literary",
                "suggestion": "使用更多样化的连接词和表达方式"
            })

        # 检查情感深度
        if "很" in content and content.count("很") > 5:
            issues.append({
                "type": "shallow_emotion",
                "description": "情感表达过于浅显",
                "severity": "medium",
                "category": "literary",
                "suggestion": "使用更深刻的情感表达方式"
            })

        # 检查创意性
        if "突然" in content and "忽然" in content:
            issues.append({
                "type": "lack_creativity",
                "description": "表达方式缺乏创意",
                "severity": "low",
                "category": "literary",
                "suggestion": "使用更独特的表达方式"
            })

        # 检查文学价值
        if len(content) < 1000:
            issues.append({
                "type": "insufficient_content",
                "description": "内容过于简短，缺乏文学深度",
                "severity": "medium",
                "category": "literary",
                "suggestion": "增加内容深度和文学价值"
            })

        return issues
    
    def _check_semantic_ambiguity(self, content: str) -> List[Dict[str, Any]]:
        """检查语义歧义"""
        issues = []
        
        # 检查模糊表述
        ambiguous_patterns = [
            r"可能.*?可能",
            r"也许.*?也许", 
            r"大概.*?大概",
            r"似乎.*?似乎"
        ]
        
        for pattern in ambiguous_patterns:
            matches = re.findall(pattern, content)
            if matches:
                issues.append({
                    "type": "semantic_ambiguity",
                    "category": "ambiguous_expression",
                    "description": f"发现模糊表述: {matches[0]}",
                    "severity": "low"
                })
        
        return issues
    
    def _check_legal_compliance(self, content: str) -> List[Dict[str, Any]]:
        """法律类审查 - 品牌名/真实机构"""
        # 安全获取内容文本
        content_text = content.get_content() if hasattr(content, 'get_content') else str(content)
        
        issues = []
        for word in self.sensitive_dict["brands"]:
            if word in content_text:
                issues.append({
                    "type": "legal",
                    "category": "brand",
                    "original": word,
                    "replacement": self.replacement_rules.get(word, "虚构品牌"),
                    "position": content_text.find(word),
                    "severity": "medium"
                })
        return issues
    
    def _check_social_compliance(self, content: str) -> List[Dict[str, Any]]:
        """社会类审查 - 政治敏感话题"""
        # 安全获取内容文本
        content_text = content.get_content() if hasattr(content, 'get_content') else str(content)
        
        issues = []
        for word in self.sensitive_dict["political"]:
            if word in content_text:
                issues.append({
                    "type": "social",
                    "category": "political",
                    "original": word,
                    "replacement": self.replacement_rules.get(word, "相关机构"),
                    "position": content_text.find(word),
                    "severity": "high"
                })
        return issues
    
    def _check_moral_compliance(self, content: str) -> List[Dict[str, Any]]:
        """道德类审查 - 性、暴力、侮辱"""
        # 安全获取内容文本
        content_text = content.get_content() if hasattr(content, 'get_content') else str(content)
        
        issues = []
        for word in self.sensitive_dict["violence"] + self.sensitive_dict["adult"]:
            if word in content_text:
                issues.append({
                    "type": "moral",
                    "category": "violence" if word in self.sensitive_dict["violence"] else "adult",
                    "original": word,
                    "replacement": self.replacement_rules.get(word, "适当描述"),
                    "position": content_text.find(word),
                    "severity": "high"
                })
        return issues
    
    def _check_aesthetic_compliance(self, content: str) -> List[Dict[str, Any]]:
        """审美类审查 - 文风突变、AI痕迹"""
        # 安全获取内容文本
        content_text = content.get_content() if hasattr(content, 'get_content') else str(content)
        
        issues = []
        
        # 检测AI痕迹
        ai_patterns = [
            "根据我的理解", "作为一个AI", "我无法", "我不能",
            "请注意", "需要说明的是", "值得一提的是"
        ]
        
        for pattern in ai_patterns:
            if pattern in content_text:
                issues.append({
                    "type": "aesthetic",
                    "category": "ai_trace",
                    "original": pattern,
                    "replacement": "自然表达",
                    "position": content.find(pattern),
                    "severity": "low"
                })
        
        # 检测文风突变（简单检测）
        if len(content_text.split('。')) > 10:  # 长文本才检测
            sentences = content_text.split('。')
            for i, sentence in enumerate(sentences[:-1]):
                if len(sentence) > 50 and len(sentences[i+1]) > 50:
                    # 检测句子长度差异过大
                    if abs(len(sentence) - len(sentences[i+1])) > 30:
                        issues.append({
                            "type": "aesthetic",
                            "category": "style_inconsistency",
                            "original": f"句子长度差异: {len(sentence)} vs {len(sentences[i+1])}",
                            "replacement": "调整句子长度",
                            "position": content_text.find(sentence),
                            "severity": "low"
                        })
        
        return issues
    
    def _calculate_risk_score(self, issues: List[Dict[str, Any]]) -> int:
        """计算风险评分 (0-100)"""
        if not issues:
            return 0
        
        score = 0
        for issue in issues:
            severity = issue.get("severity", "low")
            if severity == "high":
                score += 20
            elif severity == "medium":
                score += 10
            else:
                score += 5
        
        return min(score, 100)
    
    def _apply_corrections(self, content: str, issues: List[Dict[str, Any]]) -> str:
        """应用修正 - 智能重写 + 词汇替换"""
        # 安全获取内容文本
        content_text = content.get_content() if hasattr(content, 'get_content') else str(content)
        corrected_content = content_text
        
        # 统计高危问题数量
        high_severity_issues = [i for i in issues if i.get("severity") == "high"]
        medium_severity_issues = [i for i in issues if i.get("severity") == "medium"]
        
        self.log(f"发现问题：高危 {len(high_severity_issues)} 个，中危 {len(medium_severity_issues)} 个")
        
        # 策略1：如果有高危问题或中危问题超过3个，智能重写有问题的段落
        if len(high_severity_issues) > 0 or len(medium_severity_issues) > 3:
            self.log("检测到严重问题，启动智能重写...")
            corrected_content = self._intelligent_rewrite(content_text, issues)
        else:
            # 策略2：低危问题，仅做词汇替换
            self.log("问题较轻，进行词汇替换...")
            for issue in issues:
                if issue["type"] in ["legal", "social", "moral", "aesthetic"]:
                    original = issue.get("original", "")
                    replacement = issue.get("replacement", "")
                    if original and replacement and original != replacement:
                        # 使用正则表达式进行精确替换，避免部分匹配
                        import re
                        corrected_content = re.sub(fr"\b{re.escape(original)}\b", replacement, corrected_content)
            
            # 上下文语义优化 - 如果内容有修改，进行语义润色
            if corrected_content != content_text:
                corrected_content = self._contextual_polish(corrected_content)
        
        return corrected_content
    
    def _intelligent_rewrite(self, content: str, issues: List[Dict[str, Any]]) -> str:
        """智能重写 - 针对有问题的段落进行完整重写"""
        self.log("正在使用LLM智能重写有问题的内容...")
        
        # 提取所有有问题的原文
        problem_words = [issue.get("original", "") for issue in issues if issue.get("original")]
        problem_descriptions = [f"{issue.get('original', '')}({issue.get('category', '')})" for issue in issues]
        
        rewrite_prompt = f"""
请重写以下内容，解决其中的合规问题：

【原文内容】
{content}

【发现的问题】
{chr(10).join([f"{i+1}. {desc}" for i, desc in enumerate(problem_descriptions)])}

【重写要求】
1. **保持原文的核心意思和情节发展**
2. **完全避免使用有问题的词汇和表述**
3. **使用合规、安全的替代表达**
4. **保持文学性和可读性**
5. **内容长度与原文相当**

【具体修改指引】
- 真实品牌名 → 改为虚构品牌或通用称呼
- 政治敏感词 → 改为中性表述
- 暴力/色情内容 → 改为暗示或淡化处理
- AI痕迹明显 → 改为更自然的人类表达

请直接返回重写后的内容，不要添加任何说明或注释。
"""
        
        try:
            rewrite_response = self.forward(rewrite_prompt)
            if rewrite_response.is_success():
                rewritten_content = rewrite_response.get_content()
                self.log("智能重写完成")
                return rewritten_content
            else:
                self.log("智能重写失败，返回原文")
                return content
        except Exception as e:
            self.log(f"智能重写出错：{e}，返回原文")
            return content
    
    def _contextual_polish(self, content: str) -> str:
        """上下文语义润色"""
        # 安全获取内容文本
        content_text = content.get_content() if hasattr(content, 'get_content') else str(content)
        
        try:
            # 分段处理，避免过长文本
            sentences = content_text.split('。')
            polished_sentences = []
            
            for sentence in sentences:
                if sentence.strip():
                    # 检查句子是否包含替换后的词汇
                    if any(replacement in sentence for replacement in self.replacement_rules.values()):
                        # 使用LLM进行语义润色
                        polish_prompt = f"""
请在不改变原意的情况下，让以下句子更自然流畅：
"{sentence.strip()}。"

要求：
1. 保持原意不变
2. 让语言更自然
3. 避免生硬的替换痕迹
4. 只返回润色后的句子，不要其他说明
"""
                        try:
                            polished_response = self.forward(polish_prompt, show_response=False)
                            if polished_response.is_success():
                                polished_sentence = polished_response.get_content()
                                if polished_sentence and len(polished_sentence.strip()) > 0:
                                    polished_sentences.append(polished_sentence.strip())
                                else:
                                    polished_sentences.append(sentence.strip())
                            else:
                                polished_sentences.append(sentence.strip())
                        except:
                            polished_sentences.append(sentence.strip())
                    else:
                        polished_sentences.append(sentence.strip())
            
            return '。'.join(polished_sentences) + ('。' if content.endswith('。') else '')
        except:
            return content
    
    def _generate_compliance_report(self, compliance_result: Dict[str, Any], 
                                  original_content: str, corrected_content: str) -> Dict[str, Any]:
        """生成标准化审查报告"""
        # 标准化问题列表
        standardized_issues = []
        for issue in compliance_result["issues"]:
            standardized_issue = {
                "type": issue.get("type", "unknown"),
                "original": issue.get("original", issue.get("word", "")),
                "replacement": issue.get("replacement", ""),
                "position": issue.get("position", -1),
                "severity": issue.get("severity", "low"),
                "category": issue.get("category", "unknown"),
                "description": issue.get("description", "")
            }
            standardized_issues.append(standardized_issue)
        
        # 生成摘要报告
        summary_report = self._generate_summary_report(compliance_result, original_content)
        
        return {
            "chapter": "unknown",  # 将在主控智能体中设置
            "timestamp": self._get_timestamp(),
            "content_length": len(original_content.get_content() if hasattr(original_content, 'get_content') else str(original_content)),
            "corrections_applied": compliance_result["total_issues"],
            "risk_score": compliance_result.get("risk_score", 0),
            "severity_breakdown": {
                "high": compliance_result["high_severity"],
                "medium": compliance_result["medium_severity"], 
                "low": compliance_result["low_severity"]
            },
            "classified_issues": compliance_result.get("classified_issues", {}),
            "summary_report": summary_report,
            "dimension_scores": compliance_result.get("dimension_scores", {}),
            "issues": standardized_issues,
            "content_changed": original_content != corrected_content,
            "compliance_status": self._determine_compliance_status(compliance_result),
            "recommendations": self._generate_recommendations(compliance_result)
        }
    
    def _determine_compliance_status(self, compliance_result: Dict[str, Any]) -> str:
        """确定合规状态"""
        risk_score = compliance_result.get("risk_score", 0)
        high_severity = compliance_result.get("high_severity", 0)
        
        if high_severity > 0 or risk_score > 50:
            return "needs_review"
        elif risk_score > 20:
            return "caution"
        else:
            return "passed"
    
    def _generate_recommendations(self, compliance_result: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        dimension_scores = compliance_result.get("dimension_scores", {})
        
        if dimension_scores.get("legal", 0) > 0:
            recommendations.append("建议减少真实品牌名称的使用，使用虚构品牌替代")
        
        if dimension_scores.get("social", 0) > 0:
            recommendations.append("建议避免涉及政治敏感话题，使用更中性的表述")
        
        if dimension_scores.get("moral", 0) > 0:
            recommendations.append("建议减少暴力或成人内容描述，使用更温和的表达")
        
        if dimension_scores.get("logic", 0) > 0:
            recommendations.append("建议检查情节逻辑一致性，避免时间线或人物设定矛盾")
        
        if dimension_scores.get("aesthetic", 0) > 0:
            recommendations.append("建议优化文风一致性，减少AI痕迹")
        
        if not recommendations:
            recommendations.append("内容质量良好，无需特别改进")
        
        return recommendations
    
    def _should_trigger_compliance_check(self, content: str) -> bool:
        """智能触发检查 - 基于命中词和内容特征"""
        # 高风险关键词列表
        high_risk_keywords = [
            "公司", "组织", "政府", "国家", "政治", "领导人", "主席", "总理",
            "暴力", "血腥", "杀戮", "死亡", "恐怖", "爆炸", "枪击",
            "色情", "性爱", "裸体", "淫秽", "黄色", "成人",
            "苹果", "华为", "小米", "腾讯", "阿里巴巴", "百度", "字节跳动"
        ]
        
        # 检查是否包含高风险关键词
        content_text = content.get_content() if hasattr(content, 'get_content') else str(content)
        content_lower = content_text.lower()
        for keyword in high_risk_keywords:
            if keyword in content_lower:
                return True
        
        # 检查内容长度（短内容可能不需要审查）
        if len(content_text) < 500:
            return False
        
        # 检查修改率（如果之前有大量修改，需要重新审查）
        # 这里可以结合历史数据，暂时返回True
        return True
    
    def _calculate_modification_rate(self, original_content: str, modified_content: str) -> float:
        """计算修改率"""
        if not original_content:
            return 0.0
        
        # 简单的字符差异计算
        diff_count = 0
        max_len = max(len(original_content), len(modified_content))
        
        for i in range(max_len):
            if i >= len(original_content) or i >= len(modified_content):
                diff_count += 1
            elif original_content[i] != modified_content[i]:
                diff_count += 1
        
        return diff_count / max_len if max_len > 0 else 0.0
    
    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
