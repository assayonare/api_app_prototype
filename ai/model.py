import os
import re
import requests

from openai import OpenAI

from .base import BaseAI

class Model(BaseAI):
    def __init__(self, api_key: str, system_prompt: str = None):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.client = OpenAI(base_url="https://routerai.ru/api/v1", api_key=self.api_key,)
    
    def generate_response(self, prompt) -> str:
        if self.system_prompt:
            prompt = f"{self.system_prompt}\n\n{prompt}"
            print(f"Combined prompt: {prompt}")
        
        completion = self.client.chat.completions.create(
            model="qwen/qwen3.5-9b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()
    
