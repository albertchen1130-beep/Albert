"""
Agent 2: 表6信息处理
Processes Table 6 data and generates a formatted table section
for the biweekly report.
"""

from scripts.agents.base import BaseAgent


class Table6Agent(BaseAgent):
    AGENT_NAME = "Table6Agent (表6信息)"
    SYSTEM_PROMPT = """你是一位资深的金融数据分析师，专门负责编写双周报中"表6"板块。

你的任务：
1. 接收用户提供的表6原始数据（可能是文字描述、数据列表、或结构化数据）
2. 整理成规范的表格格式，并附带简要的数据分析说明
3. 确保数据准确、格式统一、符合金融机构双周报标准

输出要求：
- 使用中文书写
- 生成规范的Markdown表格
- 表头清晰，数据对齐
- 在表格下方附上简要的数据变动说明（如环比变化、同比变化等关键指标）
- 如数据有异常值，标注提醒
- 语气正式、客观
- 保持与双周报整体风格一致

请直接输出整理好的表6内容（含表格和说明文字），无需额外解释。"""

    def run_with_data(self, raw_data: str) -> str:
        """Process Table 6 raw data into formatted report section."""
        prompt = f"""请将以下表6原始数据整理为双周报的正式表格内容：

---原始数据开始---
{raw_data}
---原始数据结束---

请输出整理后的完整表6内容（含Markdown表格和分析说明）。"""
        return self.run(prompt)
