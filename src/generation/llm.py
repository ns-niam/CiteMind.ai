"""
CiteMind AI - LLM Wrapper
Unified interface for Groq and Gemini.
"""
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from src.utils.config import config


class LLMProvider:
    """Wraps multiple LLM providers with a unified interface."""

    def __init__(self, provider: str = None):
        self.provider = provider or config.DEFAULT_LLM
        self.llm = self._initialize()

    def _initialize(self):
        if self.provider == "groq":
            return ChatGroq(
                api_key=config.GROQ_API_KEY,
                model=config.GROQ_MODEL,
                temperature=0.2,
                max_tokens=1024,
            )
        elif self.provider == "gemini":
            return ChatGoogleGenerativeAI(
                google_api_key=config.GOOGLE_API_KEY,
                model=config.GEMINI_MODEL,
                temperature=0.2,
                max_output_tokens=1024,
            )
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def ask(self, question: str, system_prompt: str = None) -> str:
        """Send a question and return the answer."""
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=question))

        response = self.llm.invoke(messages)
        return response.content


def get_llm(provider: str = None) -> LLMProvider:
    """Factory function for LLM."""
    return LLMProvider(provider)