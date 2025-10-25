# 🚀 AI小说创作引擎 v5.0

一个基于五层智能体架构的AI小说创作系统，支持从故事构思到最终成品的全流程自动化创作。

## 🌟 核心特性

### 🧠 五层智能体架构
- **故事架构师** - 构建完整故事框架和世界观
- **人物管理器** - 智能角色设定和一致性管理
- **情节控制器** - 确保情节逻辑连贯和时序正确
- **网文优化师** - 优化文风，去除AI痕迹
- **智囊体** - 内容审查和合规检查

### 🔧 核心功能
- **智能创作** - 全流程自动化小说创作
- **分支管理** - 多版本创作和版本控制
- **用户反馈** - 实时反馈和内容调整
- **质量监控** - 多维度质量评估和监控
- **配置管理** - 灵活的YAML配置系统

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 网络连接（用于调用AI模型）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置环境变量
在使用系统之前，需要配置以下环境变量：

```bash
# 商汤模型API密钥（用于LazyLLM框架调用商汤大模型）
export SENSENOVA_API_KEY="your_sensenova_api_key_here"

# 向量模型API密钥（用于语义向量化和相似度计算）
export SILICONFLOW_API_KEY="your_siliconflow_api_key_here"
```

Windows用户可以使用：
```cmd
set SENSENOVA_API_KEY=your_sensenova_api_key_here
set SILICONFLOW_API_KEY=your_siliconflow_api_key_here
```

### 启动系统
```bash
python main.py
```

## 📖 使用指南

### 1. 创建新小说
1. 运行 `python main.py`
2. 选择菜单选项 `1` 创建新小说
3. 输入小说标题、类型和主题关键词
4. 系统自动生成故事框架和角色设定

### 2. 继续创作
1. 运行 `python main.py`
2. 选择菜单选项 `2` 继续创作
3. 从已有项目列表中选择项目
4. 继续创作新章节

### 3. 项目管理
1. 运行 `python main.py`
2. 选择菜单选项 `3` 项目管理
3. 查看项目详情和分支管理

## ⚙️ 配置说明

### 模型配置
在 `config.yaml` 中配置AI模型参数：

```yaml
# 模型设置
models:
  default_source: "sensenova"   # 默认模型源（商汤）
  fallback_enabled: true        # 是否启用备用模型
  model_rotation: false         # 是否启用模型轮换

# 智能体模型配置 - 差异化策略（发挥各模型优势）
agent_models:
  # 故事架构师 - 需要强大的逻辑规划和全局思维能力
  story_architect:
    model_source: "sensenova"
    model_name: "Kimi-K2"
    reason: "逻辑推理能力强，擅长复杂架构设计和系统性思维"

  # 角色管理师 - 需要强大的人物理解和性格分析能力
  character_manager:
    model_source: "sensenova"
    model_name: "Kimi-K2"
    reason: "人物理解深刻，情感分析细腻，擅长角色塑造"

  # 情节控制师 - 需要强大的逻辑推理和因果关系分析
  plot_controller:
    model_source: "sensenova"
    model_name: "Kimi-K2"
    reason: "逻辑严密，擅长因果关系分析和情节连贯性把控"

  # 优化师 - 需要强大的语言润色和文风掌控能力
  optimizer:
    model_source: "sensenova"
    model_name: "Kimi-K2"
    reason: "语言表达优美，文风掌控精准，润色效果出色"

  # 知识库智能体 - 需要强大的信息检索和知识整合能力
  knowledge_base:
    model_source: "sensenova"
    model_name: "Kimi-K2"
    reason: "知识面广，信息整合能力强，适合知识管理"

  # 章节创作 - 核心功能，需要顶尖的创意写作和情感表达能力
  chapter_writer:
    model_source: "sensenova"
    model_name: "Kimi-K2"
    reason: "创意写作顶尖，情感表达细腻，长文创作流畅自然"

  # 章节修改 - 需要精准理解修改意图和高效执行
  chapter_modifier:
    model_source: "sensenova"
    model_name: "Kimi-K2"
    reason: "理解准确，执行精准，能准确把握修改需求"

  # 合规顾问 - 需要敏感词检测和合规审查能力
  compliance_advisor:
    model_source: "sensenova"
    model_name: "Kimi-K2"
    reason: "理解能力强，审查严谨，适合合规检查"

# Embedding API配置（Embedding不走LazyLLM框架，需要配置API）
embedding_api:
  # 硅基流动Embedding API
  provider: "siliconflow"  # 使用的embedding服务商
  siliconflow:
    api_url: "https://api.siliconflow.cn/v1/embeddings"
    api_key: "sk-kdumbjnbygltcxncprqaiezhbrdhakpuyhjopiosnbpmtcru"
    model: "Pro/BAAI/bge-m3"
  
  # OpenAI Embedding API（备用）
  openai:
    api_url: "https://api.openai.com/v1/embeddings"
    api_key: ""  # 如需使用，填入OpenAI API密钥
    model: "text-embedding-3-small"
```

### 系统配置
```yaml
system:
  log_level: "INFO"
  max_retries: 3
  timeout: 30
```

## 📤 输出格式

### 项目文件结构
```
projects/
└── {project_id}/
    ├── {project_name}.txt          # 完整小说内容
    ├── chapters.json               # 章节数据
    ├── txt/                       # 分章节TXT文件
    └── feedback/                  # 用户反馈数据
```

## 🔧 开发指南

### 添加新功能
1. 在 `agents/` 目录中创建新的智能体
2. 在 `core/` 目录中添加核心功能模块
3. 更新 `main.py` 中的主控制器逻辑

### 扩展智能体
智能体遵循统一接口，可通过继承 `BaseAgent` 类来创建新智能体。

## 📞 技术支持

如有问题，请提交Issue或联系项目维护者。