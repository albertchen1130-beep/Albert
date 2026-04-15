"""
Agent 6: 张总审查 (Manager Zhang Review)
Reviews the compiled report and generates review comments,
suggested edits, and an improved version.
"""

from scripts.agents.base import BaseAgent


class ReviewerAgent(BaseAgent):
    AGENT_NAME = "ReviewerAgent (张总审查)"
    MAX_TOKENS = 16384
    SYSTEM_PROMPT = """你是张总，一位经验丰富的金融机构高管，负责审查团队编写的双周报。

你的审查标准：
1. **数据准确性**：检查数据是否合理、前后是否一致
2. **表述规范性**：用语是否专业、是否有歧义或不当表述
3. **逻辑完整性**：分析是否有遗漏、结论是否有充分支撑
4. **格式规范性**：格式是否统一、排版是否美观
5. **风险提示**：是否遗漏重要的风险提示或合规要求

审查输出包含两部分：

**第一部分：审查意见**
- 逐条列出发现的问题和改进建议
- 按严重程度分类（🔴 必须修改 / 🟡 建议修改 / 🟢 仅供参考）
- 给出具体的修改建议

**第二部分：修改后版本**
- 根据审查意见，输出一份修改后的完整双周报
- 在修改处用 <!--张总修改--> 标记，便于追踪修改

请先输出审查意见，然后输出修改后的完整版本。"""

    def review_report(self, full_report: str) -> str:
        """Review the compiled report and provide feedback + revised version."""
        prompt = f"""请审查以下双周报，给出审查意见并生成修改后版本：

===双周报全文===
{full_report}
===双周报结束===

请输出：
1. 审查意见（逐条列出）
2. 修改后的完整双周报"""
        return self.run(prompt)
