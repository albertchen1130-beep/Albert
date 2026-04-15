"""
Agent 5: 报告汇总编撰
Compiles all agent outputs into a cohesive, complete biweekly report.
"""

from scripts.agents.base import BaseAgent


class CompilerAgent(BaseAgent):
    AGENT_NAME = "CompilerAgent (汇总编撰)"
    MAX_TOKENS = 16384
    SYSTEM_PROMPT = """你是一位资深的金融报告编辑，负责将各板块内容汇总编撰为一份完整的双周报。

你的任务：
1. 接收各Agent生成的板块内容（表4-5 ETF分析、表6、香港同业信息、对比分析）
2. 汇总为一份结构完整、风格统一的双周报
3. 确保报告的连贯性、专业性和可读性

报告结构：
1. 封面信息（标题、报告期间、生成日期）
2. 内容摘要 / 本期要点
3. 表四：[ETF相关表格及分析]
4. 表五：[ETF相关表格及分析]
5. 表六：[数据表格及分析]
6. 八、香港同业信息
7. 本期与上期对比分析
8. 附注

编撰要求：
- 使用中文书写
- 统一各板块的格式风格（标题层级、表格格式、用语习惯）
- 撰写简洁有力的"本期要点"摘要（3-5个要点）
- 确保各板块之间的过渡自然
- 检查并修正明显的格式不一致
- 不改变原始数据，但可以优化表述
- 在报告末尾添加附注（数据来源说明、免责声明等）
- 输出完整的Markdown格式报告

请直接输出完整的双周报，无需额外解释。"""

    def run_with_sections(
        self,
        report_period: str,
        etf_section: str,
        table6_section: str,
        hk_peers_section: str,
        comparison_section: str,
    ) -> str:
        """Compile all sections into the final biweekly report."""
        prompt = f"""请将以下各板块内容汇总编撰为一份完整的双周报：

报告期间：{report_period}

===表4-5 ETF数据分析===
{etf_section}
===表4-5结束===

===表6===
{table6_section}
===表6结束===

===八、香港同业信息===
{hk_peers_section}
===香港同业信息结束===

===对比分析===
{comparison_section}
===对比分析结束===

请输出完整的双周报。"""
        return self.run(prompt)
