#!/usr/bin/env python3
"""
Biweekly Report Generator

Generates a biweekly report based on GitHub activity (commits, PRs, issues)
for the configured repository. Designed to be triggered remotely via
GitHub Actions workflow_dispatch (e.g., from the GitHub mobile app).
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone


def run_cmd(cmd):
    """Run a shell command and return its output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()


def get_git_logs(since_date, until_date):
    """Get git commit logs for the given date range."""
    fmt = "--pretty=format:%H|%an|%ad|%s"
    date_fmt = "--date=short"
    cmd = f'git log {fmt} {date_fmt} --since="{since_date}" --until="{until_date}" --all'
    output = run_cmd(cmd)
    if not output:
        return []

    commits = []
    for line in output.split("\n"):
        parts = line.split("|", 3)
        if len(parts) == 4:
            commits.append({
                "hash": parts[0][:7],
                "author": parts[1],
                "date": parts[2],
                "message": parts[3],
            })
    return commits


def get_file_change_stats(since_date, until_date):
    """Get file change statistics for the given date range."""
    cmd = f'git log --since="{since_date}" --until="{until_date}" --all --numstat --pretty=format:""'
    output = run_cmd(cmd)
    if not output:
        return {"files_changed": 0, "insertions": 0, "deletions": 0}

    files_changed = set()
    insertions = 0
    deletions = 0
    for line in output.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) == 3:
            try:
                insertions += int(parts[0]) if parts[0] != "-" else 0
                deletions += int(parts[1]) if parts[1] != "-" else 0
                files_changed.add(parts[2])
            except ValueError:
                continue

    return {
        "files_changed": len(files_changed),
        "insertions": insertions,
        "deletions": deletions,
    }


def group_commits_by_author(commits):
    """Group commits by author."""
    by_author = {}
    for c in commits:
        author = c["author"]
        if author not in by_author:
            by_author[author] = []
        by_author[author].append(c)
    return by_author


def group_commits_by_date(commits):
    """Group commits by date."""
    by_date = {}
    for c in commits:
        date = c["date"]
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(c)
    return by_date


def generate_report(repo_name, since_date, until_date):
    """Generate the biweekly report as markdown."""
    commits = get_git_logs(since_date, until_date)
    stats = get_file_change_stats(since_date, until_date)
    by_author = group_commits_by_author(commits)
    by_date = group_commits_by_date(commits)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append(f"# Biweekly Report / 双周报")
    lines.append("")
    lines.append(f"**Repository / 仓库:** {repo_name}")
    lines.append(f"**Period / 周期:** {since_date} ~ {until_date}")
    lines.append(f"**Generated / 生成时间:** {now}")
    lines.append("")

    # Summary
    lines.append("---")
    lines.append("## Summary / 概览")
    lines.append("")
    lines.append(f"| Metric / 指标 | Value / 数值 |")
    lines.append(f"|---|---|")
    lines.append(f"| Total Commits / 总提交数 | {len(commits)} |")
    lines.append(f"| Contributors / 贡献者 | {len(by_author)} |")
    lines.append(f"| Files Changed / 变更文件数 | {stats['files_changed']} |")
    lines.append(f"| Lines Added / 新增行数 | +{stats['insertions']} |")
    lines.append(f"| Lines Deleted / 删除行数 | -{stats['deletions']} |")
    lines.append("")

    if not commits:
        lines.append("> No commits found in this period. / 该周期内无提交记录。")
        lines.append("")
        return "\n".join(lines)

    # By Author
    lines.append("---")
    lines.append("## By Contributor / 按贡献者")
    lines.append("")
    for author, author_commits in sorted(by_author.items()):
        lines.append(f"### {author} ({len(author_commits)} commits)")
        lines.append("")
        for c in author_commits:
            lines.append(f"- `{c['hash']}` {c['message']} ({c['date']})")
        lines.append("")

    # Timeline
    lines.append("---")
    lines.append("## Timeline / 时间线")
    lines.append("")
    for date in sorted(by_date.keys(), reverse=True):
        date_commits = by_date[date]
        lines.append(f"### {date} ({len(date_commits)} commits)")
        lines.append("")
        for c in date_commits:
            lines.append(f"- `{c['hash']}` [{c['author']}] {c['message']}")
        lines.append("")

    return "\n".join(lines)


def main():
    repo_name = os.environ.get("GITHUB_REPOSITORY", "unknown/repo")
    period = os.environ.get("REPORT_PERIOD", "14")

    try:
        days = int(period)
    except ValueError:
        days = 14

    until_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    since_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")

    report = generate_report(repo_name, since_date, until_date)

    # Write report to file
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/biweekly-report-{since_date}-to-{until_date}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    # Also print to stdout for GitHub Actions summary
    print(report)

    # Write to GitHub Actions step summary if available
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write(report)

    print(f"\n---\nReport saved to: {filename}", file=sys.stderr)


if __name__ == "__main__":
    main()
