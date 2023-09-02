import openai
import os

"""
from dotenv import load_dotenv
load_dotenv()
"""

# Set up OpenAI API credentials
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up the translate function using gpt-3.5
def translate(text, source = "eng", target = "tur"):
    prompt = f'Translate from {source} to {target}: {text}'
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages = [
            {
                'role' : 'user',
                'content' : prompt,
            }
        ]
    )
    return response.choices[0].message.content

