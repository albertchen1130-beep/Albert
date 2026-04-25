# 双周报自动生成系统

在手机上一键生成双周报，无需电脑。多Agent协同工作，张总PR审核。

## 系统架构

```
用户输入 → 数据预处理 → 各板块Agent → 报告汇编 → 张总审核 → 对比分析
  │                                                    │
  ├─ ETF Excel (表4-5)     Agent 02: 市场概览           │
  ├─ 表6信息               Agent 03: ETF分析            ├─ Draft PR
  ├─ 香港同业信息(文字8)    Agent 04: 表6分析            ├─ PR评论修改
  └─ 上期双周报            Agent 05: 香港同业            └─ Approve合并
                           Agent 06: 报告汇编
                           Agent 07: 审核准备
```

## 使用方式

### 方式一：Claude Code Web（推荐）

1. 打开 [claude.ai/code](https://claude.ai/code)，连接本仓库
2. 上传输入文件到 `inputs/` 对应目录
3. 运行 `/project:run-all` 或说"生成双周报"
4. 系统自动运行所有Agent，生成报告并创建PR
5. 张总在GitHub上审核PR

### 方式二：GitHub Actions（手机触发）

1. 打开 GitHub App → 本仓库 → Actions
2. 选择 "双周报生成" workflow → Run workflow
3. 填写报告日期范围 → 运行
4. 查看生成的PR

### 方式三：GitHub Issue（文字数据提交）

1. 在本仓库创建新 Issue，选择"双周报数据提交"模板
2. 填入香港同业信息和表6文字数据
3. 系统自动提取数据到 `inputs/` 目录
4. 再通过方式一或二触发生成

## 用户需要提供的输入

| 输入项 | 存放目录 | 格式 | 说明 |
|--------|----------|------|------|
| 表4-5 ETF数据 | `inputs/etf_data/` | .xlsx/.csv | ETF持仓及交易Excel |
| 表6信息 | `inputs/table6/` | .txt/.xlsx | 表6相关数据 |
| 香港同业信息 | `inputs/hk_peer_info/` | .txt | 第8部分文字材料 |
| 上期双周报 | `inputs/previous_report/` | .md/.txt | 用于格式参考和对比 |

## Agent列表

| Agent | 功能 | Claude Code命令 |
|-------|------|----------------|
| 01 数据预处理 | 解析Excel、文本输入 | 自动（orchestrator） |
| 02 市场概览 | 撰写市场概览部分 | `/project:parse-etf-excel` |
| 03 ETF分析 | 生成表4-5 | `/project:parse-etf-excel` |
| 04 表6分析 | 处理表6数据 | `/project:parse-table6` |
| 05 香港同业 | 整理香港同业信息 | `/project:parse-hk-peers` |
| 06 报告汇编 | 汇总生成完整报告 | `/project:generate-report` |
| 07 审核准备 | 生成审核摘要和PR | `/project:zhang-review` |
| -- 对比分析 | 与上期对比 | `/project:compare-with-previous` |
| -- 全流程 | 运行所有Agent | `/project:run-all` |

## 项目结构

```
Albert/
├── CLAUDE.md                    # Claude Code 主指令
├── .claude/commands/            # Claude Code 项目命令（Agent）
│   ├── run-all.md              # 全流程编排
│   ├── parse-etf-excel.md      # ETF数据处理
│   ├── parse-table6.md         # 表6处理
│   ├── parse-hk-peers.md       # 香港同业信息
│   ├── compare-with-previous.md # 对比分析
│   ├── generate-report.md      # 报告汇编
│   └── zhang-review.md         # 张总审核
├── agents/                      # Agent详细指令
├── inputs/                      # 用户输入数据
├── outputs/                     # Agent中间输出
├── reports/                     # 最终双周报
├── templates/                   # 报告模板
├── scripts/                     # 数据处理脚本
│   ├── orchestrator.py         # Agent编排运行器
│   ├── validate_inputs.py      # 输入验证
│   └── utils/                  # 工具库
└── .github/
    ├── workflows/              # GitHub Actions
    └── ISSUE_TEMPLATE/         # Issue模板
```

## 审核流程

1. 系统生成双周报后自动创建 Draft PR
2. 张总在 GitHub 上审核（手机或电脑）
3. 在PR中直接对具体内容添加评论
4. Claude Code 监听评论，自动修改
5. 修改完成后张总 Approve → 合并
