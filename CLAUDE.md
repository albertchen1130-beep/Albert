# 双周报生成系统 / Biweekly Report System

## 项目概述

这是一个多Agent双周报自动生成系统。用户可以在手机上（电脑关机状态下）通过 Claude Code Web 触发运行，系统会通过多个专业Agent协同工作，自动生成结构化的双周报，最终由张总审核修改。

## 工作流程

### 第一步：确认用户输入

运行前需要确认以下输入文件已放置在 `inputs/` 目录中：

| 输入项 | 目录 | 格式 | 说明 |
|--------|------|------|------|
| 上期双周报 | `inputs/previous_report/` | `.md` 或 `.txt` | 用于参考上期内容和格式 |
| 表4-5 ETF数据 | `inputs/etf_data/` | `.xlsx` 或 `.csv` | ETF持仓及交易数据 |
| 表6信息 | `inputs/table6/` | `.txt` 或 `.xlsx` | 表6相关数据 |
| 香港同业信息 | `inputs/hk_peer_info/` | `.txt` | 第8部分文字材料 |

### 第二步：运行所有Agent

使用 `/generate-report` 或直接告诉 Claude "生成双周报"，系统将按以下顺序运行Agent：

1. **数据预处理Agent** (`agents/01_data_preprocessor.md`) - 解析Excel和文本输入
2. **市场概览Agent** (`agents/02_market_overview.md`) - 生成市场概览部分
3. **ETF数据分析Agent** (`agents/03_etf_analysis.md`) - 处理表4-5的ETF数据
4. **表6分析Agent** (`agents/04_table6_analysis.md`) - 处理表6数据
5. **香港同业Agent** (`agents/05_hk_peer_info.md`) - 整理香港同业信息
6. **报告汇编Agent** (`agents/06_report_compiler.md`) - 汇总所有部分，生成完整双周报
7. **审核准备Agent** (`agents/07_review_prep.md`) - 格式检查，生成审核摘要供张总审阅

### 第三步：张总审核

- 生成的报告会自动提交为 Draft PR
- 张总可在 GitHub 上直接审核和评论
- Claude Code 会监听PR评论，根据反馈自动修改

## Agent运行命令

```
# 完整运行（推荐）
python scripts/orchestrator.py --run-all

# 单独运行某个Agent
python scripts/orchestrator.py --agent 03_etf_analysis

# 仅汇编（所有中间结果已就绪时）
python scripts/orchestrator.py --compile-only
```

## 报告结构

最终双周报包含以下板块：

1. **封面信息** - 报告期间、生成日期、版本号
2. **市场概览** - 本双周市场整体情况
3. **投资组合概况** - 组合表现总结
4. **表4: ETF持仓明细** - ETF持仓详情
5. **表5: ETF交易记录** - ETF交易明细
6. **表6: 专项数据** - 表6相关信息
7. **风险监控** - 风险指标和预警
8. **香港同业信息** - 香港同业市场动态

## 目录结构

```
Albert/
├── CLAUDE.md                    # 本文件 - Agent指令
├── agents/                      # Agent提示词文件
│   ├── 01_data_preprocessor.md
│   ├── 02_market_overview.md
│   ├── 03_etf_analysis.md
│   ├── 04_table6_analysis.md
│   ├── 05_hk_peer_info.md
│   ├── 06_report_compiler.md
│   └── 07_review_prep.md
├── inputs/                      # 用户输入数据
│   ├── etf_data/               # 表4-5 ETF Excel
│   ├── table6/                 # 表6信息
│   ├── hk_peer_info/           # 香港同业信息文字
│   └── previous_report/        # 上期双周报
├── templates/                   # 报告模板
│   └── biweekly_template.md
├── scripts/
│   ├── orchestrator.py          # Agent编排运行器
│   ├── biweekly_report.py       # 原有报告脚本（保留）
│   └── utils/
│       ├── excel_parser.py      # Excel数据解析
│       └── text_processor.py    # 文本预处理
├── outputs/                     # Agent中间输出（自动生成）
├── reports/                     # 最终报告
└── .github/workflows/
    └── biweekly-report.yml      # GitHub Actions
```

## 注意事项

- 所有Agent输出保存在 `outputs/` 目录，最终报告在 `reports/`
- 每次生成报告前会自动备份上次的输出
- 如果某个Agent失败，可以单独重跑该Agent
- 张总的修改意见通过PR评论提交，系统自动响应
