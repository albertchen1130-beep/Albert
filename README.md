# 双周报自动生成系统

在手机上一键生成双周报，全程无需电脑。基于 Claude Code + GitHub Actions 构建。

---

## 工作原理

```
手机上传输入文件 → 触发 GitHub Actions → Claude Code Agents 处理 → 生成双周报 → 张总 PR 审查
```

### Agent 流水线

| 步骤 | Agent | 输入 | 输出 |
|------|-------|------|------|
| 1 | parse-etf-excel | `inputs/表4-5-ETF/` 中的 Excel/CSV | `outputs/sections/表4-5-ETF数据.md` |
| 2 | parse-table6 | `inputs/表6/` 中的数据文件 | `outputs/sections/表6信息.md` |
| 3 | parse-hk-peers | `inputs/香港同业信息/` 中的文字 | `outputs/sections/8-香港同业信息.md` |
| 4 | generate-report | 所有章节 + 上期双周报 + 模板 | `outputs/双周报-{日期}.md` |
| 5 | zhang-review | 生成的双周报 + 上期双周报 | `outputs/审查意见.md` + 修正后的报告 |

---

## 使用步骤

### Step 1: 上传输入文件

通过 GitHub App 或浏览器，将以下文件上传到对应目录：

| 输入内容 | 上传目录 | 支持格式 |
|----------|----------|----------|
| 表4-5 ETF 数据 | `inputs/表4-5-ETF/` | `.xlsx`, `.csv`, `.md`, `.txt` |
| 表6 信息 | `inputs/表6/` | `.xlsx`, `.csv`, `.md`, `.txt` |
| 香港同业信息 | `inputs/香港同业信息/` | `.md`, `.txt` |
| 上期双周报 | `inputs/上期双周报/` | `.md`, `.docx` |

### Step 2: 触发双周报生成

1. 打开 GitHub App → Actions 标签
2. 选择 **"双周报生成 (Claude Code)"** workflow
3. 点击 **"Run workflow"**
4. 可选：填写报告周期起止日期
5. 确认运行

### Step 3: 等待生成完成

- 预计耗时 5-15 分钟
- 5 个 Agent 依次运行：数据处理 → 报告汇编 → 审查
- 运行完成后会收到通知

### Step 4: 张总审查

- 系统自动创建 PR（Pull Request）
- 张总在 PR 中审阅报告内容
- 可直接在 PR 中修改或 comment 反馈
- 确认无误后 Approve 并 Merge

### Step 5: 获取最终报告

- **在线查看**: PR 中直接查看 Markdown 报告
- **下载文件**: Actions 运行页面的 Artifacts 区域下载
- **仓库浏览**: `reports/` 和 `outputs/` 目录

---

## 本地运行（Claude Code CLI）

如果在电脑上使用 Claude Code，可以直接运行各 agent：

```bash
# 一键运行所有 agent
claude /project:run-all

# 或分步运行
claude /project:parse-etf-excel      # 处理表4-5 ETF数据
claude /project:parse-table6          # 处理表6信息
claude /project:parse-hk-peers       # 处理香港同业信息
claude /project:generate-report      # 汇编完整双周报
claude /project:zhang-review          # 张总审查
```

---

## 首次设置

### 1. 配置 API Key

在仓库 Settings → Secrets and variables → Actions 中添加：

| Secret 名称 | 说明 |
|-------------|------|
| `ANTHROPIC_API_KEY` | Claude API 密钥 |

### 2. 配置权限

确保仓库 Settings → Actions → General → Workflow permissions 设置为 "Read and write permissions"。

---

## 项目结构

```
.
├── .claude/
│   └── commands/                    # Claude Code Agent 定义
│       ├── parse-etf-excel.md       # Agent 1: ETF数据处理
│       ├── parse-table6.md          # Agent 2: 表6处理
│       ├── parse-hk-peers.md        # Agent 3: 香港同业信息
│       ├── generate-report.md       # Agent 4: 报告汇编
│       ├── zhang-review.md          # Agent 5: 张总审查
│       └── run-all.md               # 一键运行所有Agent
├── .github/workflows/
│   ├── biweekly-report.yml          # 基础双周报 (Git历史)
│   └── biweekly-report-claude.yml   # Claude Code 双周报
├── inputs/                          # 📥 输入文件目录
│   ├── 表4-5-ETF/                   # ETF Excel/CSV 文件
│   ├── 表6/                         # 表6数据文件
│   ├── 香港同业信息/                 # HK同业信息文字
│   └── 上期双周报/                   # 上一期双周报
├── outputs/                         # 📤 输出文件目录
│   └── sections/                    # 各章节中间输出
├── reports/                         # 📊 历史报告存档
├── scripts/
│   ├── biweekly_report.py           # 基础报告生成脚本
│   └── excel_to_markdown.py         # Excel转Markdown工具
├── templates/
│   └── report-template.md           # 报告模板
├── CLAUDE.md                        # Claude Code 项目说明
└── README.md
```

---

## FAQ

**Q: 可以只更新部分章节吗？**
A: 可以。只上传需要更新的输入文件，未提供输入的章节会标注"本期暂无更新"。

**Q: 张总如何修改报告？**
A: 在自动创建的 PR 中直接编辑文件或留下 comment，修改后 Merge 即可。

**Q: 支持哪些 Excel 格式？**
A: 支持 `.xlsx` 和 `.csv` 格式。多 Sheet 的 Excel 文件会自动处理所有 Sheet。

**Q: 如何查看历史报告？**
A: 所有报告都存档在 `reports/` 目录中，可随时查看。
