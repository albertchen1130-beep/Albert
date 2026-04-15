# 双周报多Agent自动生成系统

**全程手机操作，电脑关机也能生成双周报。**

## 系统架构

```
┌─────────────────────────────────────────────────────┐
│                  手机触发 (GitHub App)                │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│              GitHub Actions Pipeline                 │
│                                                     │
│  Phase 1 (并行处理)                                   │
│  ┌─────────────┐ ┌──────────┐ ┌──────────────────┐  │
│  │ HKPeersAgent│ │Table6Agent│ │   ETFAgent       │  │
│  │ 香港同业信息  │ │ 表6信息   │ │ 表4-5 ETF分析    │  │
│  └──────┬──────┘ └────┬─────┘ └────────┬─────────┘  │
│         └──────────┬──┴────────────────┘             │
│                    ▼                                 │
│  Phase 2    ┌─────────────────┐                      │
│             │ComparisonAgent  │                      │
│             │ 与上期对比分析    │                      │
│             └────────┬────────┘                      │
│                      ▼                               │
│  Phase 3    ┌─────────────────┐                      │
│             │ CompilerAgent   │                      │
│             │ 汇总编撰完整报告  │                      │
│             └────────┬────────┘                      │
│                      ▼                               │
│  Phase 4    ┌─────────────────┐                      │
│             │ ReviewerAgent   │                      │
│             │ 张总审查修改      │                      │
│             └────────┬────────┘                      │
│                      ▼                               │
│             ┌─────────────────┐                      │
│             │ 创建PR待审阅     │                      │
│             └─────────────────┘                      │
└─────────────────────────────────────────────────────┘
```

## 6个Agent说明

| # | Agent | 功能 | 输入 | 输出 |
|---|-------|------|------|------|
| 1 | **HKPeersAgent** | 整理香港同业信息 | `hk_peers.txt` 原始文字 | 结构化的"八、香港同业信息"板块 |
| 2 | **Table6Agent** | 处理表6数据 | `table6.txt` 原始数据 | 格式化的表6（含分析说明） |
| 3 | **ETFAgent** | 分析ETF Excel | `etf_data.xlsx` | 表4和表5（含数据分析） |
| 4 | **ComparisonAgent** | 对比上期报告 | 上期双周报 + 本期各板块 | 变动分析（↑↓→标注） |
| 5 | **CompilerAgent** | 汇总编撰 | 所有板块输出 | 完整双周报 |
| 6 | **ReviewerAgent** | 张总审查 | 完整双周报 | 审查意见 + 修改后终稿 |

## 使用方法（手机操作）

### 方法一：直接上传文件 + 触发Workflow（推荐）

**Step 1: 上传输入文件**

1. 在手机上打开 GitHub App / 浏览器，进入本仓库
2. 进入 `inputs/` 目录
3. 上传以下文件：
   - `hk_peers.txt` — 香港同业信息原始文字
   - `table6.txt` — 表6原始数据
   - `etf_data.xlsx` — 表4-5 ETF Excel文件
   - `previous_report.md` — 上期双周报（可选，系统会自动查找历史报告）

**Step 2: 触发双周报生成**

1. 点击 **Actions** 标签
2. 选择 **"Biweekly Report / 双周报生成"**
3. 点击 **"Run workflow"**
4. 填写报告期间（如 `2025-04-01 ~ 2025-04-15`）
5. 确认运行

**Step 3: 查看结果**

- **在线查看**: Actions 运行完成后查看 Summary
- **下载文件**: 在 Artifacts 下载完整报告
- **审阅PR**: 系统自动创建PR，张总可直接在PR中审阅修改

### 方法二：通过Issue提交文字数据

1. 进入 **Issues** → **New Issue**
2. 选择 **"📊 双周报数据提交"** 模板
3. 在表单中填写香港同业信息和表6数据
4. 提交Issue后，系统自动提取数据到 `inputs/`
5. 手动上传ETF Excel到 `inputs/`
6. 触发 Actions workflow

### 方法三：自动定时运行

系统会在每月 **1日和15日** 的UTC 9:00（北京时间17:00）自动运行。
请确保在此之前已上传最新的输入文件。

## 项目结构

```
.
├── .github/
│   ├── workflows/
│   │   ├── biweekly-report.yml      # 主workflow（触发Agent流水线）
│   │   └── issue-to-inputs.yml      # Issue数据自动提取
│   └── ISSUE_TEMPLATE/
│       └── biweekly-input.yml       # 双周报数据提交模板
├── scripts/
│   ├── orchestrator.py              # 多Agent编排器（主入口）
│   ├── biweekly_report.py           # 基础报告生成（已废弃）
│   └── agents/
│       ├── __init__.py
│       ├── base.py                  # Agent基类（Anthropic API）
│       ├── hk_peers.py              # Agent 1: 香港同业信息
│       ├── table6.py                # Agent 2: 表6处理
│       ├── etf_analysis.py          # Agent 3: ETF分析
│       ├── comparison.py            # Agent 4: 对比分析
│       ├── compiler.py              # Agent 5: 汇总编撰
│       └── reviewer.py              # Agent 6: 张总审查
├── inputs/                          # 输入文件目录
│   └── README.md                    # 输入文件说明
├── reports/                         # 生成的报告（自动创建）
├── requirements.txt                 # Python依赖
└── README.md
```

## 配置要求

### GitHub Secrets

在仓库 Settings → Secrets and variables → Actions 中添加：

| Secret名称 | 说明 |
|------------|------|
| `ANTHROPIC_API_KEY` | Anthropic API密钥（用于Claude Agent） |

> `GITHUB_TOKEN` 由GitHub自动提供，无需手动配置。

### 本地运行（可选）

```bash
# 安装依赖
pip install -r requirements.txt

# 设置API密钥
export ANTHROPIC_API_KEY="your-key-here"

# 将输入文件放入 inputs/ 目录后运行
python -m scripts.orchestrator --period "2025-04-01 ~ 2025-04-15"
```

## 输出说明

每次运行生成以下文件：

| 文件 | 说明 |
|------|------|
| `reports/final_YYYYMMDD_HHMM.md` | **终稿** — 含张总审查修改 |
| `reports/draft_YYYYMMDD_HHMM.md` | 初稿 — 审查前版本 |
| `reports/sections_YYYYMMDD_HHMM/` | 各板块独立输出 |

## 张总审阅流程

1. 系统自动创建PR
2. 张总在PR中查看 `final_*.md` 终稿
3. 如需修改：直接在PR中编辑文件或留下评论
4. 确认无误后合并PR
5. 报告正式归档
