from dotenv import load_dotenv
import os
load_dotenv()
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
response = client.chat.completions.create(
    model='llama-3.3-70b-versatile',
    messages=[{'role': 'user', 'content': 'Say hello'}],
    max_tokens=50
)
print(response.choices[0].message.content)
