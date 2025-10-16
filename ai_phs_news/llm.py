from duckduckgo_search import DDGS
from pydantic import BaseModel
from .config import global_config
from openai import OpenAI


class LLMClient:
    llm_client = OpenAI(api_key=global_config.OPENAI_API_KEY,
                    base_url=global_config.OPENAI_BASE_URL)
    model = global_config.OPENAI_MODEL
    CHAT_TYPE = global_config.CHAT_TYPE

    def chat_with_openai(self, messages, max_length=1024, temperature=0.7):
        completion = self.llm_client.chat.completions.create(
            model=self.model,
            max_tokens=max_length,
            messages=messages,
            temperature=temperature,
            stream=False
        )
        return completion.choices[0].message.content

    def chat_with_duckduckgo(self, messages):
        keywords = ""
        for msg in messages:
            keywords = msg["role"]+":\n" + keywords + msg["content"] + "\n\n"
        return DDGS().chat(keywords, model="gpt-4o-mini")

    def chat(self, messages):
        if self.CHAT_TYPE == "openai":
            return self.chat_with_openai(messages)
        elif self.CHAT_TYPE == "duckduckgo":
            return self.chat_with_duckduckgo(messages)
        else:
            raise ValueError("Invalid chat type")