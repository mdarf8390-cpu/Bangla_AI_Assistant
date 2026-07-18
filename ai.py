# ai.py

import requests

from config import MODEL_NAME, PERSONALITY
from memory import recall, remember


OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ayesha(user_message):

    old_memory = recall()


    prompt = f"""
{PERSONALITY}

তোমার আগের স্মৃতি:
{old_memory}


User:
{user_message}

Ayesha:
"""


    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }


    try:

        response = requests.post(
            OLLAMA_URL,
            json=data
        )


        result = response.json()

        answer = result["response"]


        # Save memory
        remember(
            user_message,
            answer
        )


        return answer


    except Exception as e:

        return f"Ayesha এখন connect হতে পারছে না। Error: {e}"