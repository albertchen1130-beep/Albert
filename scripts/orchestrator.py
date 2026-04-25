#!/usr/bin/env python3
"""
Biweekly Report Orchestrator

Runs all agents in sequence to generate a complete biweekly report.
Can be triggered from CLI or GitHub Actions.

Usage:
    python scripts/orchestrator.py --run-all
    python scripts/orchestrator.py --agent 01_data_preprocessor
    python scripts/orchestrator.py --compile-only
    python scripts/orchestrator.py --preprocess-only
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUTS_DIR = BASE_DIR / "inputs"
OUTPUTS_DIR = BASE_DIR / "outputs"
REPORTS_DIR = BASE_DIR / "reports"
AGENTS_DIR = BASE_DIR / "agents"
TEMPLATES_DIR = BASE_DIR / "templates"
SCRIPTS_DIR = BASE_DIR / "scripts"


def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}", file=sys.stderr)


def ensure_dirs():
    """Create output directories if they don't exist."""
    OUTPUTS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)


def backup_previous_outputs():
    """Backup previous outputs before a new run."""
    if OUTPUTS_DIR.exists() and any(OUTPUTS_DIR.iterdir()):
        backup_name = f"outputs_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir = BASE_DIR / backup_name
        shutil.copytree(OUTPUTS_DIR, backup_dir)
        log(f"Previous outputs backed up to {backup_name}")


def check_inputs():
    """Check which inputs are available and report status."""
    status = {}
    input_checks = {
        "etf_data": {
            "dir": INPUTS_DIR / "etf_data",
            "extensions": [".xlsx", ".csv", ".xls"],
            "required": True,
            "description": "表4-5 ETF Excel数据",
        },
        "table6": {
            "dir": INPUTS_DIR / "table6",
            "extensions": [".txt", ".xlsx", ".csv", ".md"],
            "required": True,
            "description": "表6信息",
        },
        "hk_peer_info": {
            "dir": INPUTS_DIR / "hk_peer_info",
            "extensions": [".txt", ".md"],
            "required": True,
            "description": "香港同业信息文字",
        },
        "previous_report": {
            "dir": INPUTS_DIR / "previous_report",
            "extensions": [".txt", ".md"],
            "required": True,
            "description": "上期双周报",
        },
    }

    all_ok = True
    log("=" * 50)
    log("检查输入文件状态")
    log("=" * 50)

    for name, check in input_checks.items():
        input_dir = check["dir"]
        if not input_dir.exists():
            input_dir.mkdir(parents=True, exist_ok=True)

        files = []
        for ext in check["extensions"]:
            files.extend(input_dir.glob(f"*{ext}"))

        if files:
            status[name] = {
                "status": "ok",
                "files": [f.name for f in files],
            }
            log(f"  ✓ {check['description']}: {len(files)} 个文件")
            for f in files:
                log(f"    - {f.name}")
        else:
            status[name] = {"status": "missing", "files": []}
            if check["required"]:
                log(f"  ✗ {check['description']}: 未找到文件", "WARN")
                all_ok = False
            else:
                log(f"  - {check['description']}: 未找到（可选）")

    log("=" * 50)
    if not all_ok:
        log("部分必需输入缺失，Agent将使用占位符标记", "WARN")

    return status


def run_step_preprocess():
    """Step 1: Data preprocessing."""
    log("=" * 50)
    log("Agent 01: 数据预处理")
    log("=" * 50)

    sys.path.insert(0, str(SCRIPTS_DIR / "utils"))
    from excel_parser import parse_directory, validate_etf_data
    from text_processor import process_hk_peer_info, process_previous_report, process_table6_text

    # Parse ETF Excel data
    log("解析ETF数据...")
    etf_output = str(OUTPUTS_DIR / "etf_parsed.json")
    etf_data = parse_directory(str(INPUTS_DIR / "etf_data"), etf_output)
    validation = validate_etf_data(etf_data)
    log(f"ETF数据验证: valid={validation['valid']}, warnings={len(validation.get('warnings', []))}")

    # Parse Table 6 text/excel
    log("处理表6数据...")
    table6_text_output = str(OUTPUTS_DIR / "table6_parsed.json")
    process_table6_text(str(INPUTS_DIR / "table6"), table6_text_output)

    # Also check for table6 Excel files
    table6_excel_files = list((INPUTS_DIR / "table6").glob("*.xlsx")) + list(
        (INPUTS_DIR / "table6").glob("*.csv")
    )
    if table6_excel_files:
        log("发现表6 Excel文件，额外解析...")
        parse_directory(str(INPUTS_DIR / "table6"), str(OUTPUTS_DIR / "table6_excel_parsed.json"))

    # Process HK peer info
    log("处理香港同业信息...")
    process_hk_peer_info(str(INPUTS_DIR / "hk_peer_info"), str(OUTPUTS_DIR / "hk_peer_parsed.txt"))

    # Process previous report
    log("分析上期双周报...")
    process_previous_report(
        str(INPUTS_DIR / "previous_report"), str(OUTPUTS_DIR / "previous_report_summary.json")
    )

    # Write validation report
    validation_report = OUTPUTS_DIR / "data_validation_report.txt"
    with open(validation_report, "w", encoding="utf-8") as f:
        f.write("数据验证报告\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"ETF数据: {'通过' if validation['valid'] else '存在问题'}\n")
        if validation.get("issues"):
            for issue in validation["issues"]:
                f.write(f"  [错误] {issue}\n")
        if validation.get("warnings"):
            for warn in validation["warnings"]:
                f.write(f"  [警告] {warn}\n")

    log("数据预处理完成")
    return validation


def run_step_compile(period_start=None, period_end=None):
    """Step 6: Compile all agent outputs into final report."""
    log("=" * 50)
    log("Agent 06: 报告汇编")
    log("=" * 50)

    template_path = TEMPLATES_DIR / "biweekly_template.md"
    if not template_path.exists():
        log("报告模板不存在", "ERROR")
        return None

    template = template_path.read_text(encoding="utf-8")

    if not period_end:
        period_end = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if not period_start:
        end_dt = datetime.strptime(period_end, "%Y-%m-%d")
        period_start = (end_dt - timedelta(days=14)).strftime("%Y-%m-%d")

    generated_date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    def read_output(filename, default="[待补充]"):
        path = OUTPUTS_DIR / filename
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
        return default

    def read_json_content(filename, key="content", default="[待补充]"):
        path = OUTPUTS_DIR / filename
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, dict) and key in data:
                    return data[key]
                return json.dumps(data, ensure_ascii=False, indent=2)
            except json.JSONDecodeError:
                return path.read_text(encoding="utf-8").strip()
        return default

    replacements = {
        "{{period_start}}": period_start,
        "{{period_end}}": period_end,
        "{{generated_date}}": generated_date,
        "{{version}}": "v1.0-draft",
        "{{market_overview}}": read_output("02_market_overview.md"),
        "{{portfolio_overview}}": "[待补充 - 投资组合概况]",
        "{{fixed_income}}": "[待补充 - 固定收益分析]",
        "{{table4_etf_holdings}}": read_output("03_table4_etf_holdings.md"),
        "{{table5_etf_trades}}": read_output("03_table5_etf_trades.md"),
        "{{etf_summary}}": read_output("03_etf_summary.md"),
        "{{table6}}": read_output("04_table6.md"),
        "{{risk_monitoring}}": "[待补充 - 风险监控]",
        "{{hk_peer_info}}": read_output("05_hk_peer_info.md"),
    }

    report = template
    for placeholder, value in replacements.items():
        report = report.replace(placeholder, value)

    report_filename = f"biweekly-report-{period_start}-to-{period_end}.md"
    report_path = REPORTS_DIR / report_filename
    report_path.write_text(report, encoding="utf-8")

    # Write compilation log
    missing = [k for k, v in replacements.items() if "[待补充" in v]
    log_path = OUTPUTS_DIR / "06_compilation_log.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("汇编日志\n")
        f.write(f"生成时间: {generated_date}\n")
        f.write(f"报告文件: {report_filename}\n")
        f.write("=" * 40 + "\n\n")
        if missing:
            f.write(f"待补充项 ({len(missing)}):\n")
            for m in missing:
                f.write(f"  - {m}\n")
        else:
            f.write("所有板块已填充完成\n")

    log(f"报告已生成: {report_path}")
    log(f"待补充项: {len(missing)}")
    return str(report_path)


def generate_review_summary():
    """Step 7: Generate review summary for 张总."""
    log("=" * 50)
    log("Agent 07: 审核准备")
    log("=" * 50)

    summary_lines = []
    summary_lines.append("# 双周报审核摘要\n")
    summary_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # Check compilation log
    comp_log = OUTPUTS_DIR / "06_compilation_log.txt"
    if comp_log.exists():
        summary_lines.append("## 汇编状态\n")
        summary_lines.append(comp_log.read_text(encoding="utf-8"))
        summary_lines.append("")

    # Check validation report
    val_report = OUTPUTS_DIR / "data_validation_report.txt"
    if val_report.exists():
        summary_lines.append("## 数据验证\n")
        summary_lines.append(val_report.read_text(encoding="utf-8"))
        summary_lines.append("")

    # List all outputs
    summary_lines.append("## Agent输出文件\n")
    if OUTPUTS_DIR.exists():
        for f in sorted(OUTPUTS_DIR.iterdir()):
            if not f.name.startswith("."):
                size = f.stat().st_size
                summary_lines.append(f"- {f.name} ({size} bytes)")

    summary_text = "\n".join(summary_lines)
    summary_path = OUTPUTS_DIR / "07_review_summary.md"
    summary_path.write_text(summary_text, encoding="utf-8")

    log(f"审核摘要已生成: {summary_path}")
    return summary_text


def main():
    parser = argparse.ArgumentParser(description="双周报Agent编排运行器")
    parser.add_argument("--run-all", action="store_true", help="运行所有Agent")
    parser.add_argument("--agent", type=str, help="运行指定Agent (如: 01_data_preprocessor)")
    parser.add_argument("--preprocess-only", action="store_true", help="仅运行数据预处理")
    parser.add_argument("--compile-only", action="store_true", help="仅运行报告汇编")
    parser.add_argument("--period-start", type=str, help="报告起始日期 (YYYY-MM-DD)")
    parser.add_argument("--period-end", type=str, help="报告结束日期 (YYYY-MM-DD)")
    parser.add_argument("--no-backup", action="store_true", help="不备份上次输出")

    args = parser.parse_args()

    ensure_dirs()

    if args.run_all:
        log("=" * 60)
        log("双周报生成系统 - 全流程运行")
        log("=" * 60)

        # Check inputs
        input_status = check_inputs()

        # Backup previous outputs
        if not args.no_backup:
            backup_previous_outputs()

        # Step 1: Preprocess
        run_step_preprocess()

        # Steps 2-5: Agent content generation
        # These are handled by Claude Code agents reading from outputs/
        # The orchestrator prepares the data, agents generate content
        log("")
        log("=" * 50)
        log("数据预处理完成。以下步骤由Claude Code Agent执行：")
        log("  - Agent 02: 市场概览")
        log("  - Agent 03: ETF数据分析 (表4-5)")
        log("  - Agent 04: 表6分析")
        log("  - Agent 05: 香港同业信息")
        log("请在Claude Code中运行各Agent生成内容，")
        log("或等待Agent自动执行后运行 --compile-only 汇编报告。")
        log("=" * 50)

        # Step 6: Compile (if agent outputs exist)
        report_path = run_step_compile(args.period_start, args.period_end)

        # Step 7: Review preparation
        generate_review_summary()

        log("")
        log("=" * 60)
        log("全流程运行完成")
        if report_path:
            log(f"报告文件: {report_path}")
        log("下一步: 提交PR供张总审核")
        log("=" * 60)

    elif args.preprocess_only:
        input_status = check_inputs()
        run_step_preprocess()

    elif args.compile_only:
        report_path = run_step_compile(args.period_start, args.period_end)
        generate_review_summary()
        if report_path:
            log(f"报告已生成: {report_path}")

    elif args.agent:
        log(f"单独运行Agent: {args.agent}")
        if args.agent == "01_data_preprocessor":
            run_step_preprocess()
        elif args.agent in ("06_report_compiler", "compile"):
            run_step_compile(args.period_start, args.period_end)
        elif args.agent in ("07_review_prep", "review"):
            generate_review_summary()
        else:
            log(f"Agent {args.agent} 需要由Claude Code执行")
            log(f"请参阅 agents/{args.agent}.md 中的指令")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
