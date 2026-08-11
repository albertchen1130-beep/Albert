#!/usr/bin/env python3
"""
Excel/CSV parser for biweekly report data.
Parses ETF data and Table 6 data from Excel/CSV files.
"""

import csv
import json
import os
import sys
from pathlib import Path


def parse_csv(file_path):
    """Parse a CSV file and return list of dicts."""
    rows = []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned = {}
            for k, v in row.items():
                k = k.strip()
                if v is not None:
                    v = v.strip()
                cleaned[k] = v
            rows.append(cleaned)
    return rows


def try_parse_xlsx(file_path):
    """Try to parse xlsx using openpyxl. Returns list of dicts or None."""
    try:
        import openpyxl
    except ImportError:
        print(
            f"WARNING: openpyxl not installed. Cannot parse {file_path}. "
            "Install with: pip install openpyxl",
            file=sys.stderr,
        )
        return None

    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    all_sheets = {}

    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue

        headers = [str(h).strip() if h is not None else f"col_{i}" for i, h in enumerate(rows[0])]
        data = []
        for row in rows[1:]:
            if all(cell is None for cell in row):
                continue
            record = {}
            for i, cell in enumerate(row):
                if i < len(headers):
                    if cell is None:
                        record[headers[i]] = ""
                    elif isinstance(cell, (int, float)):
                        record[headers[i]] = cell
                    else:
                        record[headers[i]] = str(cell).strip()
            data.append(record)
        all_sheets[sheet_name] = data

    wb.close()
    return all_sheets


def parse_file(file_path):
    """Parse a single file (csv or xlsx)."""
    ext = Path(file_path).suffix.lower()
    if ext == ".csv":
        return {"default": parse_csv(file_path)}
    elif ext in (".xlsx", ".xls"):
        result = try_parse_xlsx(file_path)
        if result is None:
            return {"error": f"Cannot parse {file_path} - openpyxl not installed"}
        return result
    else:
        print(f"WARNING: Unsupported file format: {ext}", file=sys.stderr)
        return None


def parse_directory(input_dir, output_file):
    """Parse all Excel/CSV files in a directory and write JSON output."""
    input_path = Path(input_dir)
    if not input_path.exists():
        print(f"ERROR: Input directory does not exist: {input_dir}", file=sys.stderr)
        sys.exit(1)

    all_data = {}
    supported = (".csv", ".xlsx", ".xls")
    files = [f for f in input_path.iterdir() if f.suffix.lower() in supported]

    if not files:
        print(f"WARNING: No Excel/CSV files found in {input_dir}", file=sys.stderr)
        all_data["_status"] = "no_files_found"
    else:
        for file_path in sorted(files):
            print(f"Parsing: {file_path.name}", file=sys.stderr)
            result = parse_file(str(file_path))
            if result is not None:
                all_data[file_path.name] = result

    all_data["_meta"] = {
        "source_dir": str(input_dir),
        "files_processed": len(files),
        "file_names": [f.name for f in files],
    }

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2, default=str)

    print(f"Output written to: {output_file}", file=sys.stderr)
    return all_data


def validate_etf_data(data):
    """Validate ETF data structure and return validation report."""
    issues = []
    warnings = []

    if "_status" in data and data["_status"] == "no_files_found":
        issues.append("No ETF data files found in input directory")
        return {"valid": False, "issues": issues, "warnings": warnings}

    for filename, sheets in data.items():
        if filename.startswith("_"):
            continue
        if isinstance(sheets, dict) and "error" in sheets:
            issues.append(f"{filename}: {sheets['error']}")
            continue
        if isinstance(sheets, dict):
            for sheet_name, rows in sheets.items():
                if not isinstance(rows, list):
                    continue
                if len(rows) == 0:
                    warnings.append(f"{filename}/{sheet_name}: Empty sheet")
                for i, row in enumerate(rows):
                    for key, val in row.items():
                        if val == "" or val is None:
                            warnings.append(
                                f"{filename}/{sheet_name} row {i+1}: "
                                f"Empty value in column '{key}'"
                            )

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings[:20],
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python excel_parser.py <input_dir> <output_file>", file=sys.stderr)
        sys.exit(1)

    data = parse_directory(sys.argv[1], sys.argv[2])
    validation = validate_etf_data(data)
    print(json.dumps(validation, ensure_ascii=False, indent=2))
