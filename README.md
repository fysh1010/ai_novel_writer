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

## 📁 项目结构

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
└── requirements.txt           # 依赖包列表
```

## ⚙️ 配置说明

### 模型配置
在 `config.yaml` 中配置AI模型参数：

```yaml
models:
  default: "deepseek-chat"
  api_key: "your-api-key-here"
  base_url: "https://api.deepseek.com"
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