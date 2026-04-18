import google.generativeai as genai
genai.configure(api_key="AIzaSyBWequi2ve-2icPobff0u3JmWiPFy3nnYs")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)