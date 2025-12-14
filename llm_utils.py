import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

API_KEY = os.getenv("VOID_API_KEY")
API_URL = os.getenv("VOID_API_URL")
MODEL = os.getenv("VOID_MODEL", "gpt-4o")

def call_llm(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
