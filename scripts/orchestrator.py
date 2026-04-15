#!/usr/bin/env python3
"""
双周报多Agent编排器 / Biweekly Report Multi-Agent Orchestrator

Orchestrates 6 agents to generate a complete biweekly report:
  1. HKPeersAgent   - 处理香港同业信息 (文字8)
  2. Table6Agent    - 处理表6信息
  3. ETFAgent       - 处理表4-5 ETF Excel数据
  4. ComparisonAgent- 与上期双周报对比分析
  5. CompilerAgent  - 汇总编撰完整报告
  6. ReviewerAgent  - 张总审查并修改

Usage:
  python -m scripts.orchestrator [--inputs-dir inputs/] [--output-dir reports/]

Inputs (placed in inputs/ directory before running):
  - hk_peers.txt       香港同业信息原始文字
  - table6.txt         表6原始数据
  - etf_data.xlsx      表4-5 ETF Excel文件
  - previous_report.md 上期双周报

Environment:
  - ANTHROPIC_API_KEY  (required) Anthropic API key
  - REPORT_PERIOD      (optional) e.g. "2025-03-31 ~ 2025-04-15"
"""

import argparse
import glob
import json
import os
import sys
import time
from datetime import datetime, timezone

from anthropic import Anthropic

from scripts.agents.hk_peers import HKPeersAgent
from scripts.agents.table6 import Table6Agent
from scripts.agents.etf_analysis import ETFAgent
from scripts.agents.comparison import ComparisonAgent
from scripts.agents.compiler import CompilerAgent
from scripts.agents.reviewer import ReviewerAgent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_file(path: str) -> str | None:
    """Read a text file, return None if not found."""
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def find_previous_report(reports_dir: str) -> str | None:
    """Find the most recent previous report in the reports directory."""
    pattern = os.path.join(reports_dir, "*.md")
    files = sorted(glob.glob(pattern), reverse=True)
    for f in files:
        # Skip any file we're about to create this run
        if "final" not in os.path.basename(f):
            content = read_file(f)
            if content:
                return content
    return None


def find_excel(inputs_dir: str) -> str | None:
    """Find the ETF Excel file in the inputs directory."""
    for ext in ("*.xlsx", "*.xls"):
        matches = glob.glob(os.path.join(inputs_dir, ext))
        if matches:
            return matches[0]
    return None


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(inputs_dir: str, output_dir: str, report_period: str | None = None):
    """Run the full 6-agent pipeline."""

    total_start = time.time()
    client = Anthropic()

    # ------------------------------------------------------------------
    # 1. Load inputs
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  双周报多Agent系统 / Biweekly Report Pipeline")
    print("=" * 60)

    hk_peers_text = read_file(os.path.join(inputs_dir, "hk_peers.txt"))
    table6_text = read_file(os.path.join(inputs_dir, "table6.txt"))
    excel_path = find_excel(inputs_dir)
    previous_report = read_file(os.path.join(inputs_dir, "previous_report.md"))

    # Also check reports/ for previous report if not in inputs/
    if not previous_report:
        previous_report = find_previous_report(output_dir)

    if not report_period:
        report_period = os.environ.get("REPORT_PERIOD", "")
    if not report_period:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        report_period = f"截至 {today}"

    print(f"\n📋 报告期间: {report_period}")
    print(f"📂 输入目录: {inputs_dir}")
    print(f"  - 香港同业信息: {'✅ 已找到' if hk_peers_text else '❌ 未找到 (hk_peers.txt)'}")
    print(f"  - 表6数据:      {'✅ 已找到' if table6_text else '❌ 未找到 (table6.txt)'}")
    print(f"  - ETF Excel:    {'✅ ' + excel_path if excel_path else '❌ 未找到 (*.xlsx)'}")
    print(f"  - 上期双周报:   {'✅ 已找到' if previous_report else '⚠️  未找到 (首期报告)'}")

    # Validate: at least one input must exist
    if not any([hk_peers_text, table6_text, excel_path]):
        print("\n❌ 错误: 至少需要一个输入文件。请将文件放入 inputs/ 目录。")
        print("  所需文件: hk_peers.txt, table6.txt, etf_data.xlsx")
        sys.exit(1)

    # ------------------------------------------------------------------
    # 2. Run Phase 1 agents in parallel (independent sections)
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  Phase 1: 各板块Agent并行处理")
    print("=" * 60)

    hk_peers_agent = HKPeersAgent(client)
    table6_agent = Table6Agent(client)
    etf_agent = ETFAgent(client)

    # Run agents (sequential in this implementation; can be parallelized
    # with threading/asyncio in production)
    hk_output = ""
    if hk_peers_text:
        hk_output = hk_peers_agent.run_with_raw_text(hk_peers_text)
    else:
        hk_output = "_（本期无香港同业信息更新）_"

    table6_output = ""
    if table6_text:
        table6_output = table6_agent.run_with_data(table6_text)
    else:
        table6_output = "_（本期无表6数据更新）_"

    etf_output = ""
    if excel_path:
        etf_output = etf_agent.run_with_excel(excel_path)
    else:
        etf_output = "_（本期无ETF数据更新）_"

    # ------------------------------------------------------------------
    # 3. Run Phase 2: Comparison agent (needs Phase 1 outputs)
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  Phase 2: 对比分析")
    print("=" * 60)

    comparison_output = ""
    if previous_report:
        comparison_agent = ComparisonAgent(client)
        current_sections = {
            "表4-5 ETF分析": etf_output,
            "表6": table6_output,
            "香港同业信息": hk_output,
        }
        comparison_output = comparison_agent.run_with_reports(
            previous_report, current_sections
        )
    else:
        comparison_output = "_（首期报告，无上期数据可对比）_"

    # ------------------------------------------------------------------
    # 4. Run Phase 3: Compiler agent (needs all outputs)
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  Phase 3: 汇总编撰")
    print("=" * 60)

    compiler_agent = CompilerAgent(client)
    full_report = compiler_agent.run_with_sections(
        report_period=report_period,
        etf_section=etf_output,
        table6_section=table6_output,
        hk_peers_section=hk_output,
        comparison_section=comparison_output,
    )

    # ------------------------------------------------------------------
    # 5. Run Phase 4: Reviewer agent (张总审查)
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  Phase 4: 张总审查")
    print("=" * 60)

    reviewer_agent = ReviewerAgent(client)
    review_output = reviewer_agent.review_report(full_report)

    # ------------------------------------------------------------------
    # 6. Save outputs
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  保存报告")
    print("=" * 60)

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

    # Save draft report (pre-review)
    draft_path = os.path.join(output_dir, f"draft_{timestamp}.md")
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(full_report)
    print(f"  📄 初稿已保存: {draft_path}")

    # Save reviewed report (post-review)
    final_path = os.path.join(output_dir, f"final_{timestamp}.md")
    with open(final_path, "w", encoding="utf-8") as f:
        f.write(review_output)
    print(f"  📄 终稿（含张总审查）已保存: {final_path}")

    # Save individual section outputs for reference
    sections_dir = os.path.join(output_dir, f"sections_{timestamp}")
    os.makedirs(sections_dir, exist_ok=True)
    section_files = {
        "01_hk_peers.md": hk_output,
        "02_table6.md": table6_output,
        "03_etf_tables4_5.md": etf_output,
        "04_comparison.md": comparison_output,
    }
    for fname, content in section_files.items():
        with open(os.path.join(sections_dir, fname), "w", encoding="utf-8") as f:
            f.write(content)
    print(f"  📁 各板块输出已保存: {sections_dir}/")

    elapsed = time.time() - total_start
    print(f"\n✅ 双周报生成完毕！总耗时: {elapsed:.1f}秒")
    print(f"  初稿: {draft_path}")
    print(f"  终稿: {final_path}")

    return final_path, draft_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="双周报多Agent编排器 / Biweekly Report Multi-Agent Orchestrator"
    )
    parser.add_argument(
        "--inputs-dir", default="inputs",
        help="输入文件目录 (default: inputs/)"
    )
    parser.add_argument(
        "--output-dir", default="reports",
        help="报告输出目录 (default: reports/)"
    )
    parser.add_argument(
        "--period", default=None,
        help="报告期间，如 '2025-03-31 ~ 2025-04-15'"
    )
    args = parser.parse_args()

    run_pipeline(
        inputs_dir=args.inputs_dir,
        output_dir=args.output_dir,
        report_period=args.period,
    )


if __name__ == "__main__":
    main()
