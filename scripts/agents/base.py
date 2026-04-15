"""
Base agent class using the Anthropic API with prompt caching.
All biweekly report agents inherit from this.
"""

import os
import json
import time
from anthropic import Anthropic


class BaseAgent:
    """Base class for all biweekly report agents."""

    # Subclasses override these
    AGENT_NAME = "BaseAgent"
    SYSTEM_PROMPT = "You are a helpful assistant."
    MODEL = "claude-sonnet-4-20250514"
    MAX_TOKENS = 8192

    def __init__(self, client=None):
        self.client = client or Anthropic()
        self._output = None

    def run(self, user_input: str) -> str:
        """Run the agent with the given input and return the response text."""
        print(f"\n{'='*60}")
        print(f"[{self.AGENT_NAME}] Starting...")
        print(f"{'='*60}")

        start = time.time()

        # Use prompt caching for the system prompt (it's reused across runs)
        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=self.MAX_TOKENS,
            system=[
                {
                    "type": "text",
                    "text": self.SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": user_input}],
        )

        self._output = response.content[0].text
        elapsed = time.time() - start

        print(f"[{self.AGENT_NAME}] Done in {elapsed:.1f}s "
              f"(input_tokens={response.usage.input_tokens}, "
              f"output_tokens={response.usage.output_tokens})")

        return self._output

    @property
    def output(self) -> str | None:
        return self._output

    def __repr__(self):
        return f"<{self.AGENT_NAME}>"
