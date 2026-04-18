# 双周报生成系统 / Biweekly Report Generator

## 项目概述

本项目是一个基于 Claude Code 的双周报自动生成系统，可在手机上通过 GitHub Actions 触发，全程无需电脑。

## 核心工作流

1. 用户上传 4 类输入文件到 `inputs/` 目录
2. GitHub Actions 触发 Claude Code agents 依次处理
3. 最终生成完整双周报到 `outputs/` 目录
4. 自动创建 PR 供张总审查修改

## 输入文件说明

| 输入 | 目录 | 格式 | 说明 |
|------|------|------|------|
| 表4-5 ETF数据 | `inputs/表4-5-ETF/` | `.xlsx` / `.csv` | ETF相关数据表格 |
| 表6信息 | `inputs/表6/` | `.md` / `.txt` / `.xlsx` | 表6相关数据 |
| 香港同业信息 | `inputs/香港同业信息/` | `.md` / `.txt` | 第8部分文字内容 |
| 上期双周报 | `inputs/上期双周报/` | `.md` / `.docx` | 上一期双周报供参考格式和延续性 |

## Agent 列表

所有 agent 定义在 `.claude/commands/` 目录：

| Agent | 命令 | 功能 |
|-------|------|------|
| parse-etf-excel | `/project:parse-etf-excel` | 解析表4-5 ETF Excel，生成格式化表格 |
| parse-table6 | `/project:parse-table6` | 解析表6信息，生成对应章节 |
| parse-hk-peers | `/project:parse-hk-peers` | 处理香港同业信息文字，生成第8部分 |
| generate-report | `/project:generate-report` | 汇编所有章节，生成完整双周报 |
| zhang-review | `/project:zhang-review` | 张总审查视角，检查报告质量 |
| run-all | `/project:run-all` | 一键顺序运行所有agent |

## 输出文件

- 各agent中间输出: `outputs/sections/`
- 最终双周报: `outputs/双周报-{日期}.md`

## 技术栈

- Python 3.x + openpyxl (Excel解析)
- Claude Code CLI (agent执行)
- GitHub Actions (自动化调度)

## 关键约定

- 所有报告使用中文
- 表格数据保持原始精度，不做四舍五入
- 参考上期双周报的格式和结构
- 张总审查后的修改通过 PR review 完成
