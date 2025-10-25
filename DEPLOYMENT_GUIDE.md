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

### 3. 配置AI模型

编辑 `config.yaml` 文件，配置AI模型参数：

```yaml
models:
  default: "deepseek-chat"
  api_key: "your-api-key-here"
  base_url: "https://api.deepseek.com"
```

### 4. 启动系统

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

## ⚙️ 高级配置

### 模型配置

支持多种AI模型：
- DeepSeek系列
- Qwen系列
- 其他兼容OpenAI API的模型

### 系统性能调优

```yaml
system:
  max_retries: 3      # 最大重试次数
  timeout: 30         # 请求超时时间
  cache:
    enabled: true     # 启用缓存
    max_size: 1000    # 缓存最大大小
    ttl: 86400        # 缓存过期时间（秒）
```

### 日志配置

```yaml
logging:
  system:
    level: "INFO"     # 日志级别
    file: "logs/system.log"  # 日志文件路径
```

## 🐛 故障排除

### 常见问题

#### 1. 模型调用失败
```
错误信息: Model call failed
解决方案: 
1. 检查API密钥是否正确
2. 检查网络连接
3. 检查模型配置
```

#### 2. 项目加载失败
```
错误信息: Project load failed
解决方案:
1. 检查项目文件完整性
2. 检查目录权限
3. 查看日志文件获取详细信息
```

#### 3. 缓存问题
```
错误信息: Cache error
解决方案:
1. 清理缓存文件
2. 重启系统
3. 检查磁盘空间
```

### 日志查看

系统日志文件位于 `logs/` 目录：
- `system.log` - 系统日志
- `user.log` - 用户操作日志
- `error.log` - 错误日志

## 📈 性能监控

### 系统指标

- **缓存命中率**: 80%+
- **响应时间**: <30秒（平均）
- **系统健康度**: 实时监控
- **Token节约**: 50%+

### 监控日志

系统运行时会显示实时性能指标：
- 各智能体处理进度
- 缓存命中情况
- 性能指标统计

## 🔒 安全说明

### 数据安全

- 项目数据本地存储
- 敏感信息加密处理
- 定期备份建议

### API密钥安全

- 不要在代码中硬编码密钥
- 使用环境变量或配置文件
- 定期更换密钥

## 🔄 更新升级

### 版本升级步骤

1. 备份现有项目数据
2. 下载新版本代码
3. 迁移配置文件
4. 安装新依赖
5. 测试系统功能

### 兼容性说明

- 向后兼容项目数据格式
- 配置文件格式可能变化
- 智能体接口保持稳定

## 📞 技术支持

### 社区支持

- 提交Issue到GitHub仓库
- 参与讨论区交流

### 商业支持

- 企业定制开发
- 技术咨询服务
- 培训支持服务

## 📄 附录

### 项目数据结构

```
projects/
└── {project_id}/
    ├── project.json            # 项目元数据
    ├── story_framework.json    # 故事框架
    ├── characters.json         # 角色设定
    ├── plot_timeline.json      # 情节时间线
    ├── chapters.json           # 章节数据
    ├── {project_name}.txt      # 完整小说内容
    ├── txt/                   # 分章节TXT文件
    └── feedback/              # 用户反馈数据
```

### 分支数据结构

```
branches/
└── {branch_id}.json           # 分支数据文件
```

### 配置文件结构

```yaml
models:
  default: "deepseek-chat"
  api_key: "your-api-key-here"
  base_url: "https://api.deepseek.com"

system:
  log_level: "INFO"
  max_retries: 3
  timeout: 30

feedback:
  enable_emotion_feedback: true

logging:
  system:
    level: "INFO"
    file: "logs/system.log"
```