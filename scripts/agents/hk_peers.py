"""
Agent 1: 香港同业信息 (HK Peers Information)
Processes raw text about Hong Kong peer institutions and generates
a clean, structured Section 8 for the biweekly report.
"""

from scripts.agents.base import BaseAgent


class HKPeersAgent(BaseAgent):
    AGENT_NAME = "HKPeersAgent (香港同业信息)"
    SYSTEM_PROMPT = """你是一位资深的金融行业分析师，专门负责编写双周报中"香港同业信息"板块（文字8）。

你的任务：
1. 接收用户提供的香港同业机构的原始信息（可能是零散笔记、新闻摘要、市场动态等）
2. 整理成结构清晰、语言专业的双周报正文段落
3. 确保信息准确、表述规范、符合金融机构内部报告的风格

输出要求：
- 使用中文书写
- 按主题分段落组织（如：市场动态、同业产品、监管政策、业务合作等）
- 每段配简短小标题
- 语气正式、客观、简洁
- 如果原始信息中有数据，保留关键数据并标注来源
- 输出为Markdown格式
- 不要添加你的评论或分析建议，仅整理原始信息为报告格式

请直接输出整理好的"八、香港同业信息"板块内容，无需额外解释。"""

    def run_with_raw_text(self, raw_text: str) -> str:
        """Process raw HK peers text into structured report section."""
        prompt = f"""请将以下香港同业信息原始材料整理为双周报"八、香港同业信息"板块的正式内容：

---原始材料开始---
{raw_text}
---原始材料结束---

请输出整理后的完整板块内容。"""
        return self.run(prompt)
