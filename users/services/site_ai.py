import requests
from django.conf import settings


def site_assistant(question):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "PulseID AI Assistant"
    }

    system_prompt = """
You are the official AI assistant of PulseID.

PulseID is a healthcare platform where:

- Citizens have a unique health ID and QR health card
- Doctors can add diseases and medications
- Hospitals manage doctors and emergency cases
- Emergency ambulance system connects patients to hospitals
- AI analyzes medical reports

Your behavior rules:

1. Speak politely
2. Use simple language
3. Sometimes add light humor
4. Explain site features clearly
5. Keep answers short
"""

    data = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "temperature": 0.5,
        "max_tokens": 200
    }

    try:

        response = requests.post(url, headers=headers, json=data)

        result = response.json()

        print("AI RAW:", result)

        return result["choices"][0]["message"]["content"]

    except Exception as e:

        return f"AI error: {str(e)}"