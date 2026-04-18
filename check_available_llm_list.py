import google.generativeai as genai
import sys, os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 읽어오기

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)