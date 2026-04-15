"""
双周报多Agent系统 / Biweekly Report Multi-Agent System

Each agent handles a specific section of the biweekly report:
- HKPeersAgent:    文字8 - 香港同业信息
- Table6Agent:     表6信息
- ETFAgent:        表4-5 ETF数据分析
- ComparisonAgent: 与上期双周报对比
- CompilerAgent:   汇总编撰完整报告
- ReviewerAgent:   张总审查建议
"""

from scripts.agents.base import BaseAgent
from scripts.agents.hk_peers import HKPeersAgent
from scripts.agents.table6 import Table6Agent
from scripts.agents.etf_analysis import ETFAgent
from scripts.agents.comparison import ComparisonAgent
from scripts.agents.compiler import CompilerAgent
from scripts.agents.reviewer import ReviewerAgent

__all__ = [
    "BaseAgent",
    "HKPeersAgent",
    "Table6Agent",
    "ETFAgent",
    "ComparisonAgent",
    "CompilerAgent",
    "ReviewerAgent",
]
