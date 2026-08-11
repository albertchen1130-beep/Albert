#!/usr/bin/env python3
"""
双周报 Agent 编排脚本

用于检查输入文件就绪状态和展示运行流程。
实际的 agent 运行通过 Claude Code 完成。
"""

import os
import sys
from datetime import datetime, timedelta, timezone


INPUT_DIR = os.path.join(os.path.dirname(__file__), "inputs")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
AGENTS_DIR = os.path.join(os.path.dirname(__file__), "agents")

REQUIRED_INPUTS = {
    "上期双周报": os.path.join(INPUT_DIR, "上期双周报"),
    "表4-5 ETF": os.path.join(INPUT_DIR, "表4-5_ETF"),
    "表6": os.path.join(INPUT_DIR, "表6"),
    "文字8 香港同业": os.path.join(INPUT_DIR, "文字8_香港同业"),
}

AGENTS = [
    ("01", "数据读取", "01_数据读取.md"),
    ("02", "市场回顾", "02_市场回顾.md"),
    ("03", "ETF分析", "03_ETF分析.md"),
    ("04", "表6整理", "04_表6整理.md"),
    ("05", "香港同业", "05_香港同业.md"),
    ("06", "报告编译", "06_报告编译.md"),
    ("07", "张总审查", "07_张总审查.md"),
]


def check_inputs():
    """检查输入文件是否就绪"""
    print("=" * 50)
    print("📋 检查输入文件")
    print("=" * 50)

    all_ready = True
    for name, path in REQUIRED_INPUTS.items():
        if not os.path.exists(path):
            print(f"  ❌ {name}: 文件夹不存在")
            all_ready = False
            continue

        files = [f for f in os.listdir(path) if not f.startswith(".") and f != "README.md"]
        if files:
            print(f"  ✅ {name}: {', '.join(files)}")
        else:
            print(f"  ⚠️  {name}: 文件夹为空（需要上传文件）")
            all_ready = False

    return all_ready


def list_agents():
    """列出所有 agents"""
    print("\n" + "=" * 50)
    print("🤖 Agent 运行顺序")
    print("=" * 50)

    for num, name, filename in AGENTS:
        agent_path = os.path.join(AGENTS_DIR, filename)
        exists = "✅" if os.path.exists(agent_path) else "❌"
        print(f"  {exists} Agent {num}: {name}")


def check_outputs():
    """检查已有输出"""
    print("\n" + "=" * 50)
    print("📄 已有输出文件")
    print("=" * 50)

    if not os.path.exists(OUTPUT_DIR):
        print("  （无输出文件）")
        return

    files = sorted([f for f in os.listdir(OUTPUT_DIR) if not f.startswith(".")])
    if files:
        for f in files:
            print(f"  📝 {f}")
    else:
        print("  （无输出文件）")


def main():
    now = datetime.now(timezone(timedelta(hours=8)))
    print(f"\n🕐 当前时间: {now.strftime('%Y-%m-%d %H:%M')} (北京时间)")

    two_weeks_ago = now - timedelta(days=14)
    print(f"📅 双周报周期: {two_weeks_ago.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')}")

    ready = check_inputs()
    list_agents()
    check_outputs()

    print("\n" + "=" * 50)
    if ready:
        print("✅ 所有输入文件已就绪，可以运行双周报生成！")
        print("\n在 Claude Code 中输入：")
        print('  「请按顺序运行双周报所有agent，生成完整双周报」')
    else:
        print("⚠️  部分输入文件缺失，请先上传文件到对应文件夹")
        print("\n需要的文件：")
        print("  1. 上期双周报 → 双周报/inputs/上期双周报/")
        print("  2. ETF Excel  → 双周报/inputs/表4-5_ETF/")
        print("  3. 表6信息    → 双周报/inputs/表6/")
        print("  4. 香港同业   → 双周报/inputs/文字8_香港同业/")
    print("=" * 50)


if __name__ == "__main__":
    main()
