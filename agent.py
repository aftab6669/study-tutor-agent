import os

from groq import Groq

from prompts import SYSTEM_PROMPT
from tools import safe_calculator, create_study_plan


MODEL_NAME = "openai/gpt-oss-120b"


class StudyTutorAgent:

    def __init__(self):

        api_key = os.environ.get("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")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(
            api_key=api_key
        )

    def chat(self, messages):

        response = self.client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                *messages
            ],

            temperature=0.3
        )

        return response.choices[0].message.content


def create_agent():

    return StudyTutorAgent()
