#!/usr/bin/env python3
"""
Input validation for biweekly report generation.
Checks all required input directories and files, reports status.
"""

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INPUTS_DIR = BASE_DIR / "inputs"

INPUT_SPECS = {
    "etf_data": {
        "dir": "etf_data",
        "extensions": [".xlsx", ".csv", ".xls"],
        "required": True,
        "label": "表4-5 ETF Excel数据",
    },
    "table6": {
        "dir": "table6",
        "extensions": [".txt", ".xlsx", ".csv", ".md"],
        "required": True,
        "label": "表6信息",
    },
    "hk_peer_info": {
        "dir": "hk_peer_info",
        "extensions": [".txt", ".md"],
        "required": True,
        "label": "香港同业信息",
    },
    "previous_report": {
        "dir": "previous_report",
        "extensions": [".txt", ".md"],
        "required": True,
        "label": "上期双周报",
    },
}


def validate_file_readable(file_path):
    """Check if a file is readable and try to detect encoding issues."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            f.read(100)
        return {"readable": True, "encoding": "utf-8"}
    except UnicodeDecodeError:
        for enc in ["gbk", "gb2312", "gb18030", "latin-1"]:
            try:
                with open(file_path, "r", encoding=enc) as f:
                    f.read(100)
                return {"readable": True, "encoding": enc}
            except (UnicodeDecodeError, LookupError):
                continue
        return {"readable": False, "encoding": None}
    except Exception as e:
        return {"readable": False, "error": str(e)}


def validate_excel_file(file_path):
    """Check if an Excel file can be opened."""
    try:
        import openpyxl

        wb = openpyxl.load_workbook(file_path, read_only=True)
        sheets = wb.sheetnames
        wb.close()
        return {"valid": True, "sheets": sheets}
    except ImportError:
        return {"valid": None, "note": "openpyxl not installed"}
    except Exception as e:
        return {"valid": False, "error": str(e)}


def validate_all():
    """Validate all input directories and files."""
    results = {"overall_status": "ok", "inputs": {}, "summary": {"ready": 0, "missing": 0, "errors": 0}}

    for name, spec in INPUT_SPECS.items():
        input_dir = INPUTS_DIR / spec["dir"]
        result = {
            "label": spec["label"],
            "required": spec["required"],
            "directory_exists": input_dir.exists(),
            "files": [],
            "status": "missing",
        }

        if input_dir.exists():
            for ext in spec["extensions"]:
                for f in sorted(input_dir.glob(f"*{ext}")):
                    file_info = {
                        "name": f.name,
                        "size_bytes": f.stat().st_size,
                        "extension": f.suffix.lower(),
                    }

                    if f.suffix.lower() in (".xlsx", ".xls"):
                        file_info["excel_check"] = validate_excel_file(str(f))
                    elif f.suffix.lower() in (".txt", ".md", ".csv"):
                        file_info["encoding_check"] = validate_file_readable(str(f))

                    result["files"].append(file_info)

        if result["files"]:
            has_errors = any(
                f.get("excel_check", {}).get("valid") is False
                or f.get("encoding_check", {}).get("readable") is False
                for f in result["files"]
            )
            result["status"] = "error" if has_errors else "ready"
        else:
            result["status"] = "missing"

        results["inputs"][name] = result

        if result["status"] == "ready":
            results["summary"]["ready"] += 1
        elif result["status"] == "missing":
            results["summary"]["missing"] += 1
            if spec["required"]:
                results["overall_status"] = "incomplete"
        elif result["status"] == "error":
            results["summary"]["errors"] += 1
            results["overall_status"] = "error"

    return results


def print_status(results):
    """Print human-readable status."""
    print("=" * 50)
    print("双周报输入文件验证报告")
    print("=" * 50)
    print()

    for name, info in results["inputs"].items():
        icon = {"ready": "✓", "missing": "✗", "error": "!"}[info["status"]]
        print(f"  [{icon}] {info['label']}")
        if info["files"]:
            for f in info["files"]:
                print(f"      - {f['name']} ({f['size_bytes']} bytes)")
        else:
            print("      (无文件)")
        print()

    s = results["summary"]
    print(f"就绪: {s['ready']}  缺失: {s['missing']}  错误: {s['errors']}")
    print(f"总体状态: {results['overall_status']}")


if __name__ == "__main__":
    results = validate_all()

    if "--json" in sys.argv:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_status(results)

    sys.exit(0 if results["overall_status"] == "ok" else 1)
