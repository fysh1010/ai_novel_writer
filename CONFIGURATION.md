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

```yaml
models:
  # 默认模型
  default: "deepseek-chat"
  
  # DeepSeek模型配置
  deepseek-chat:
    api_key: "your-api-key-here"
    base_url: "https://api.deepseek.com"
    model: "deepseek-chat"
    temperature: 0.7
    max_tokens: 2000
    timeout: 30
  
  # Qwen模型配置
  qwen-chat:
    api_key: "your-api-key-here"
    base_url: "https://dashscope.aliyuncs.com/api/v1"
    model: "qwen-plus"
    temperature: 0.7
    max_tokens: 2000
    timeout: 30
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

## 🛠️ 配置修改指南

### 1. 修改AI模型配置

#### 更换默认模型
```yaml
models:
  default: "qwen-chat"  # 将默认模型改为Qwen
```

#### 添加新模型
```yaml
models:
  # 添加Claude模型
  claude-chat:
    api_key: "your-claude-api-key"
    base_url: "https://api.anthropic.com"
    model: "claude-3-haiku"
    temperature: 0.7
    max_tokens: 2000
    timeout: 30
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

## 🔧 环境变量配置

除了配置文件，还可以通过环境变量来配置系统：

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `AI_MODEL_API_KEY` | AI模型API密钥 | 无 |
| `AI_MODEL_BASE_URL` | AI模型基础URL | 无 |
| `LOG_LEVEL` | 日志级别 | INFO |
| `PROJECTS_DIR` | 项目存储目录 | projects |
| `BRANCHES_DIR` | 分支存储目录 | branches |

## 📊 配置验证

系统启动时会自动验证配置文件的完整性：

1. 检查必需的配置项是否存在
2. 验证API密钥格式
3. 验证目录权限
4. 验证网络连接

## 🔄 配置热更新

系统支持运行时配置更新：

1. 修改 `config.yaml` 文件
2. 重启系统或发送重载信号
3. 系统将自动加载新配置

## 🚨 常见配置问题

### 1. API密钥错误
```
错误信息: Invalid API key
解决方案: 检查config.yaml中的api_key配置
```

### 2. 网络连接超时
```
错误信息: Request timeout
解决方案: 增加system.timeout配置值
```

### 3. 目录权限问题
```
错误信息: Permission denied
解决方案: 检查projects_dir和branches_dir目录权限
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
  deepseek-chat:
    temperature: 0.8  # 增加创造性
    max_tokens: 3000  # 增加输出长度
```