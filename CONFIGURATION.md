# 📋 AI小说创作引擎配置文档

## 📁 配置文件结构

```
config.yaml
├── models                  # AI模型配置
├── system                  # 系统配置
├── feedback                # 反馈系统配置
└── logging                 # 日志配置
```

## ⚙️ 详细配置说明

### AI模型配置 (models)

系统使用LazyLLM框架调用商汤大模型，模型配置如下：

```yaml
models:
  # 默认模型源设置
  default_source: "sensenova"
  
  # 是否启用备用模型
  fallback_enabled: true
  
  # 是否启用模型轮换
  model_rotation: false

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
```

### 向量模型配置 (embedding_api)

向量模型使用独立的API调用，不通过LazyLLM框架：

```yaml
# Embedding API配置（Embedding不走LazyLLM框架，需要配置API）
embedding_api:
  # 使用的embedding服务商
  provider: "siliconflow"
  
  # 硅基流动Embedding API
  siliconflow:
    api_url: "https://api.siliconflow.cn/v1/embeddings"
    api_key: "your_siliconflow_api_key_here"  # 通过环境变量配置
    model: "Pro/BAAI/bge-m3"
  
  # OpenAI Embedding API（备用）
  openai:
    api_url: "https://api.openai.com/v1/embeddings"
    api_key: ""  # 如需使用，填入OpenAI API密钥
    model: "text-embedding-3-small"
```

### 系统配置 (system)

```yaml
system:
  # 日志级别
  log_level: "INFO"
  
  # 最大重试次数
  max_retries: 3
  
  # 请求超时时间（秒）
  timeout: 30
  
  # 项目存储目录
  projects_dir: "projects"
  
  # 分支存储目录
  branches_dir: "branches"
  
  # 缓存配置
  cache:
    enabled: true
    max_size: 1000
    ttl: 86400  # 24小时
```

### 反馈系统配置 (feedback)

```yaml
feedback:
  # 启用情感反馈
  enable_emotion_feedback: true
  
  # 启用质量评估
  enable_quality_assessment: true
  
  # 反馈分析配置
  analysis:
    window_size: 5  # 分析最近5章的反馈
    min_feedbacks: 3  # 最少需要3个反馈才能进行分析
```

### 日志配置 (logging)

```yaml
logging:
  # 系统日志配置
  system:
    level: "INFO"
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: "logs/system.log"
  
  # 用户日志配置
  user:
    level: "INFO"
    format: "%(asctime)s - USER - %(message)s"
    file: "logs/user.log"
  
  # 错误日志配置
  error:
    level: "ERROR"
    format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(traceback)s"
    file: "logs/error.log"
```

## 🔐 环境变量配置

系统依赖以下环境变量进行认证：

| 环境变量 | 用途 | 说明 |
|---------|------|------|
| `SENSENOVA_API_KEY` | 商汤模型API密钥 | 用于LazyLLM框架调用商汤大模型 |
| `SILICONFLOW_API_KEY` | 硅基流动API密钥 | 用于向量模型API调用 |

设置环境变量的方法：

### Linux/Mac:
```bash
export SENSENOVA_API_KEY="your_sensenova_api_key_here"
export SILICONFLOW_API_KEY="your_siliconflow_api_key_here"
```

### Windows:
```cmd
set SENSENOVA_API_KEY=your_sensenova_api_key_here
set SILICONFLOW_API_KEY=your_siliconflow_api_key_here
```

## 🛠️ 配置修改指南

### 1. 修改AI模型配置

#### 更换默认模型源
```yaml
models:
  default_source: "sensenova"  # 保持商汤作为默认源
```

#### 调整智能体模型
```yaml
agent_models:
  story_architect:
    model_source: "sensenova"
    model_name: "Kimi-K2"  # 可以更换为其他商汤模型
```

### 2. 调整系统性能

#### 增加重试次数
```yaml
system:
  max_retries: 5  # 增加到5次重试
```

#### 调整超时时间
```yaml
system:
  timeout: 60  # 增加到60秒超时
```

### 3. 自定义日志级别

#### 开启调试模式
```yaml
logging:
  system:
    level: "DEBUG"  # 开启调试日志
```

## 📊 配置验证

系统启动时会自动验证配置文件的完整性：

1. 检查必需的配置项是否存在
2. 验证环境变量是否设置
3. 验证API密钥格式
4. 验证目录权限
5. 验证网络连接

## 🔄 配置热更新

系统支持运行时配置更新：

1. 修改 `config.yaml` 文件
2. 重启系统或发送重载信号
3. 系统将自动加载新配置

## 🚨 常见配置问题

### 1. API密钥错误
```
错误信息: Invalid API key
解决方案: 
1. 检查环境变量是否正确设置
2. 检查config.yaml中的api_key配置
3. 确认API密钥未过期
```

### 2. 网络连接超时
```
错误信息: Request timeout
解决方案: 
1. 增加system.timeout配置值
2. 检查网络连接
3. 检查防火墙设置
```

### 3. 目录权限问题
```
错误信息: Permission denied
解决方案: 
1. 检查projects_dir和branches_dir目录权限
2. 确保程序有读写权限
```

## 📈 性能调优建议

### 1. 缓存配置
```yaml
system:
  cache:
    enabled: true
    max_size: 2000  # 增加缓存大小
    ttl: 172800     # 延长缓存时间到48小时
```

### 2. 并发配置
```yaml
system:
  max_concurrent_requests: 10  # 增加并发请求数量
```

### 3. 模型参数调优
```yaml
models:
  agent_models:
    chapter_writer:
      temperature: 0.8  # 增加创造性
      max_tokens: 3000  # 增加输出长度
```