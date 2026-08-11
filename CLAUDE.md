# 双周报自动生成系统 / Biweekly Report System

## 项目简介

本项目通过 Claude Code 多 Agent 协作，在手机端全程完成金融双周报的生成与审核。用户只需上传必要输入文件，系统自动完成报告撰写、编译和审核。

## 工作流程

当用户说 **"生成双周报"** 或 **"运行双周报"** 时，执行以下流程：

### 第一步：检查输入文件

在 `inputs/` 目录中确认以下文件存在：

| 文件 | 说明 | 格式 |
|------|------|------|
| `inputs/上期双周报.md` | 上一期双周报，用于保持格式一致性和对比 | Markdown |
| `inputs/香港同业信息.md` | 第8节：香港同业市场信息（文字） | Markdown/纯文本 |
| `inputs/表6信息.md` | 第6表相关数据和信息 | Markdown/纯文本 |
| `inputs/ETF数据.xlsx` 或 `inputs/ETF数据.csv` | 表4-5所需的ETF数据 | Excel/CSV |

如果文件缺失，提示用户通过 GitHub 手机 App 上传，或直接在对话中粘贴内容。

### 第二步：运行各 Agent（按顺序）

依次运行以下 Agent，每个 Agent 的 prompt 文件在 `agents/` 目录下：

1. **Agent 1 - 输入解析** (`agents/01_输入解析.md`)
   - 读取所有输入文件，解析 ETF Excel 数据
   - 输出结构化数据到 `outputs/parsed_data.json`

2. **Agent 2 - 上期回顾分析** (`agents/02_上期回顾.md`)
   - 分析上期双周报，提取格式、结构和关键数据点
   - 确保新报告与上期风格一致

3. **Agent 3 - ETF分析（表4-5）** (`agents/03_ETF分析.md`)
   - 基于 ETF Excel 数据生成表4和表5
   - 包含 ETF 规模、净值变化、申赎情况等分析

4. **Agent 4 - 表6生成** (`agents/04_表6生成.md`)
   - 基于用户提供的表6信息生成规范的表6内容

5. **Agent 5 - 香港同业信息（第8节）** (`agents/05_香港同业.md`)
   - 基于用户提供的香港同业信息文字生成第8节内容
   - 整理、润色、结构化

6. **Agent 6 - 报告编译** (`agents/06_报告编译.md`)
   - 汇总所有 Agent 输出，参照上期格式编译完整双周报
   - 输出到 `outputs/双周报_YYYY-MM-DD.md`

7. **Agent 7 - 张总审核** (`agents/07_张总审核.md`)
   - 以张总的视角审核报告：数据准确性、表述规范性、逻辑连贯性
   - 生成审核意见到 `outputs/审核意见.md`
   - 自动修改报告中的问题

### 第三步：输出结果

- 最终报告保存在 `outputs/双周报_YYYY-MM-DD.md`
- 审核意见保存在 `outputs/审核意见.md`
- 创建 PR 供团队查看

## 输入文件上传方式（手机端）

1. 打开 GitHub 手机 App
2. 进入本仓库 → `inputs/` 目录
3. 点击 "+" 添加文件，上传所需文件
4. 提交到当前分支
5. 在 Claude Code 会话中说 "生成双周报"

## 目录结构

```
Albert/
├── CLAUDE.md                    # 本文件 - 工作流编排
├── agents/                      # Agent 提示词定义
│   ├── 01_输入解析.md
│   ├── 02_上期回顾.md
│   ├── 03_ETF分析.md
│   ├── 04_表6生成.md
│   ├── 05_香港同业.md
│   ├── 06_报告编译.md
│   └── 07_张总审核.md
├── inputs/                      # 用户输入文件
│   └── README.md
├── outputs/                     # 生成的报告
├── templates/                   # 报告模板
│   └── 双周报模板.md
├── scripts/                     # 工具脚本
│   └── biweekly_report.py
└── reports/                     # 历史报告存档
```
