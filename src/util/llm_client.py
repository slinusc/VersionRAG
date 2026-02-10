import os
import requests
from dotenv import load_dotenv
from util.constants import LLM_MODE, OLLAMA_BASE_URL, OLLAMA_MODEL
import lmstudio as lms
from openai import OpenAI
from util.groq_llm_client import GROQLLM

# Load environment variables from the .env file
load_dotenv()

class LLMClient:
    def __init__(self, json_format=False, temp=None):
        self.temp = temp
        self.json_format = json_format

        if LLM_MODE == 'openai':
            self.client = OpenAI()
        elif LLM_MODE == 'groq':
            self.client = GROQLLM(response_format_json=json_format, temp=temp)
        elif LLM_MODE == 'ollama':
            self.ollama_url = f"{OLLAMA_BASE_URL}/api/generate"
            self.ollama_model = OLLAMA_MODEL
        else:
            self.model = os.getenv("LLM_OFFLINE_MODEL")
            if not self.model:
                raise ValueError("LLM_OFFLINE_MODEL is not set in the environment variables.")

            self.client = lms.llm(self.model)
    

    def generate(self, system_prompt: str, user_prompt: str):
        if LLM_MODE == 'openai':
            kwargs = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }

            if self.temp is not None:
                kwargs["temperature"] = self.temp

            if self.json_format:
                kwargs["response_format"] = {"type": "json_object"}
                
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        elif LLM_MODE == 'groq':
            response = self.client.invoke(system_instruction=system_prompt, input=user_prompt)
            return response.content
        elif LLM_MODE == 'ollama':
            prompt = f"{system_prompt}\n\n{user_prompt}"
            payload = {
                "model": self.ollama_model,
                "prompt": prompt,
                "stream": False
            }
            if self.temp is not None:
                payload["options"] = {"temperature": self.temp}
            if self.json_format:
                payload["format"] = "json"

            response = requests.post(self.ollama_url, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        else:
            config = {}
            if self.temp is not None:
                config["temperature"] = self.temp

            if self.json_format:
                config["response_format"] = {"type": "json_object"}
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            response = self.client.respond({"messages": messages}, config=config)
            return response.content