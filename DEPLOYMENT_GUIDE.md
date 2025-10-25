# 🚀 AI小说创作引擎部署和使用指南

## 📋 目录结构说明

```
ai_novel_writer/
├── agents/                    # 智能体模块
│   ├── main_controller_agent.py         # 主控智能体
│   ├── story_architect_simplified.py    # 故事架构师
│   ├── character_manager_simplified.py  # 人物管理器
│   ├── plot_controller_simplified.py    # 情节控制器
│   └── optimizer_agent.py               # 网文优化师
├── core/                      # 核心组件
│   ├── branch_manager.py                # 分支管理器
│   ├── story_dashboard.py               # 故事仪表板
│   ├── config_manager.py                # 配置管理器
│   └── enhanced_logger.py               # 增强日志系统
├── data/                      # 数据资源
├── projects/                  # 项目存储目录
├── templates/                 # 模板文件
├── utils/                     # 工具模块
├── main.py                    # 主程序入口
├── project_manager.py         # 项目管理器
├── README.md                  # 使用说明
├── CONFIGURATION.md           # 详细配置文档
├── DEPLOYMENT_GUIDE.md        # 详细部署指南
└── requirements.txt           # 依赖包列表
```

## 🛠️ 部署步骤

### 1. 环境准备

#### Python环境
确保已安装Python 3.8或更高版本：
```bash
python --version
```

#### 创建虚拟环境（推荐）
```bash
python -m venv ai_novel_writer_env
source ai_novel_writer_env/bin/activate  # Linux/Mac
# 或
ai_novel_writer_env\Scripts\activate     # Windows
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

系统使用LazyLLM框架调用商汤大模型，需要配置以下环境变量：

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

### 4. 配置模型参数

编辑 `config.yaml` 文件，配置AI模型参数：

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

  # 章节创作 - 核心功能，需要顶尖的创意写作和情感表达能力
  chapter_writer:
    model_source: "sensenova"
    model_name: "Kimi-K2"
    reason: "创意写作顶尖，情感表达细腻，长文创作流畅自然"

# Embedding API配置（Embedding不走LazyLLM框架，需要配置API）
embedding_api:
  # 硅基流动Embedding API
  provider: "siliconflow"  # 使用的embedding服务商
  siliconflow:
    api_url: "https://api.siliconflow.cn/v1/embeddings"
    api_key: "your_siliconflow_api_key_here"  # 通过环境变量配置
    model: "Pro/BAAI/bge-m3"
```

### 5. 启动系统

```bash
python main.py
```

## 🎮 使用指南

### 主菜单选项

```
============================================================
AI写小说智能体 v5.0
============================================================
1. 创建新小说
2. 继续创作
3. 项目管理
4. 退出
============================================================
```

### 1. 创建新小说

选择选项 `1`：
1. 输入小说标题
2. 输入小说类型（如：玄幻、都市、历史等）
3. 输入主题关键词（如：穿越、重生、系统等）
4. 系统自动生成故事框架和角色设定

### 2. 继续创作

选择选项 `2`：
1. 从项目列表中选择已有项目
2. 系统会继续创作下一章

### 3. 项目管理

选择选项 `3`：
1. 查看项目详情
2. 进行分支管理
3. 查看故事脉络仪表盘

## 📊 功能详解

### 章节创作流程

1. **故事架构生成** - 系统根据用户输入生成完整故事框架
2. **角色设定** - 自动生成主要角色和配角设定
3. **情节规划** - 制定详细的情节发展时间线
4. **章节创作** - 创作具体章节内容
5. **内容优化** - 优化文风，去除AI痕迹
6. **合规检查** - 进行内容审查和合规检查

### 用户反馈系统

每章创作完成后，系统会提示用户评分和反馈：
- 1-5分评分系统
- 12种情感标签选择
- 可提出具体修改意见

### 分支管理系统

支持多版本创作和版本控制：
- 创建新分支
- 查看分支详情
- 合并分支
- 比较分支
- 删除分支

### 故事仪表盘

实时显示故事创作进度和统计信息：
- 故事基本信息
- 进度指标
- 写作统计
- 章节分析

## ⚙️ 模型配置详解

### LazyLLM框架配置

本项目使用LazyLLM框架来统一管理商汤大模型的调用。模型配置位于 `config.yaml` 的 `agent_models` 部分：

- **模型源**: `sensenova` (商汤)
- **模型名称**: `Kimi-K2` (或其他商汤模型)
- **API密钥**: 通过环境变量 `SENSENOVA_API_KEY` 配置

### 向量模型配置

向量模型使用独立的API调用，不通过LazyLLM框架：

- **服务提供商**: `siliconflow` (硅基流动)
- **API URL**: `https://api.siliconflow.cn/v1/embeddings`
- **模型**: `Pro/BAAI/bge-m3`
- **API密钥**: 通过环境变量 `SILICONFLOW_API_KEY` 配置

### 智能体差异化配置

系统为每个智能体配置了最适合的模型：

- **故事架构师**: 逻辑推理能力强，擅长复杂架构设计
- **角色管理器**: 人物理解深刻，情感分析细腻
- **情节控制器**: 逻辑严密，擅长因果关系分析
- **网文优化师**: 语言表达优美，文风掌控精准
- **章节创作**: 创意写作顶尖，情感表达细腻

## 🐛 故障排除

### 常见问题

#### 1. 模型调用失败
```
错误信息: Model call failed
解决方案: 
1. 检查环境变量SENSENOVA_API_KEY是否正确设置
2. 检查网络连接
3. 检查模型配置
4. 确认商汤账户有足够余额
```

#### 2. 向量模型调用失败
```
错误信息: Embedding call failed
解决方案:
1. 检查环境变量SILICONFLOW_API_KEY是否正确设置
2. 检查向量模型配置
3. 确认硅基流动账户有足够余额
```

#### 3. 项目加载失败
```
错误信息: Project load failed
解决方案:
1. 检查项目文件完整性
2. 检查目录权限
3. 查看日志文件获取详细信息
```

### 日志查看

系统日志文件位于 `logs/` 目录：
- `system.log` - 系统日志
- `user.log` - 用户操作日志
- `error.log` - 错误日志

## 🔒 安全说明

### 数据安全

- 项目数据本地存储
- 敏感信息通过环境变量配置
- 定期备份建议

### API密钥安全

- 不要在代码中硬编码密钥
- 使用环境变量配置API密钥
- 定期更换密钥

## 🔄 更新升级

### 版本升级步骤

1. 备份现有项目数据
2. 下载新版本代码
3. 迁移配置文件
4. 安装新依赖
5. 更新环境变量配置
6. 测试系统功能

### 兼容性说明

- 向后兼容项目数据格式
- 配置文件格式可能变化
- 智能体接口保持稳定