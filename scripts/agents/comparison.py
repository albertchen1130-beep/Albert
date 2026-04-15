"""
Agent 4: 与上期双周报对比分析
Compares current period data with the previous biweekly report
to identify changes, trends, and notable differences.
"""

from scripts.agents.base import BaseAgent


class ComparisonAgent(BaseAgent):
    AGENT_NAME = "ComparisonAgent (对比分析)"
    MAX_TOKENS = 4096
    SYSTEM_PROMPT = """你是一位资深的金融报告分析师，专门负责双周报的期间对比分析。

你的任务：
1. 接收上期双周报内容和本期各板块的最新数据
2. 进行系统性的对比分析
3. 识别关键变化、趋势和异常

输出要求：
- 使用中文书写
- 按板块分别对比（表4-5 ETF、表6、香港同业信息）
- 用"↑""↓""→"标注变动方向
- 量化关键指标的变动幅度（绝对值和百分比）
- 突出重大变化和需要关注的异常
- 简洁明了，使用要点式列举
- 语气客观、专业
- 输出为Markdown格式

请直接输出对比分析内容，无需额外解释。"""

    def run_with_reports(self, previous_report: str, current_sections: dict) -> str:
        """Compare previous report with current section outputs."""
        current_summary = ""
        for section_name, content in current_sections.items():
            current_summary += f"\n### {section_name}\n{content}\n"

        prompt = f"""请对比上期双周报与本期各板块最新数据，生成对比分析：

===上期双周报===
{previous_report}
===上期双周报结束===

===本期各板块数据===
{current_summary}
===本期数据结束===

请输出系统性的对比分析。"""
        return self.run(prompt)
