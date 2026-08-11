#!/usr/bin/env python3
"""
Text processor for biweekly report inputs.
Handles reading and normalizing text inputs (HK peer info, Table 6 text, previous report).
"""

import json
import os
import sys
from pathlib import Path


def read_text_files(input_dir):
    """Read all text files from a directory and concatenate."""
    input_path = Path(input_dir)
    if not input_path.exists():
        return ""

    texts = []
    for ext in (".txt", ".md"):
        for f in sorted(input_path.glob(f"*{ext}")):
            content = f.read_text(encoding="utf-8").strip()
            if content:
                texts.append(f"--- {f.name} ---\n{content}")

    return "\n\n".join(texts)


def extract_previous_report_sections(report_text):
    """Extract sections from a previous biweekly report."""
    sections = {}
    current_section = None
    current_lines = []

    for line in report_text.split("\n"):
        if line.startswith("## "):
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = line.strip("# ").strip()
            current_lines = []
        elif current_section:
            current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


def process_hk_peer_info(input_dir, output_file):
    """Process Hong Kong peer information text."""
    text = read_text_files(input_dir)
    if not text:
        text = "[香港同业信息：未提供输入数据]"

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    print(f"HK peer info written to: {output_file}", file=sys.stderr)
    return text


def process_previous_report(input_dir, output_file):
    """Process previous biweekly report for reference."""
    text = read_text_files(input_dir)
    if not text:
        summary = {"_status": "no_previous_report", "sections": {}}
    else:
        sections = extract_previous_report_sections(text)
        summary = {
            "_status": "ok",
            "sections": sections,
            "section_names": list(sections.keys()),
        }

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Previous report summary written to: {output_file}", file=sys.stderr)
    return summary


def process_table6_text(input_dir, output_file):
    """Process Table 6 text data."""
    text = read_text_files(input_dir)

    if not text:
        data = {"_status": "no_data", "content": ""}
    else:
        data = {"_status": "ok", "content": text}

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Table 6 text data written to: {output_file}", file=sys.stderr)
    return data


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python text_processor.py <command> <input_dir> <output_file>",
            file=sys.stderr,
        )
        print("Commands: hk_peer | previous_report | table6", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    input_dir = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "output.json"

    if command == "hk_peer":
        process_hk_peer_info(input_dir, output_file)
    elif command == "previous_report":
        process_previous_report(input_dir, output_file)
    elif command == "table6":
        process_table6_text(input_dir, output_file)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)
