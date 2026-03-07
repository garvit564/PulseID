import requests
import base64
from django.conf import settings


def analyze_report(image_path):

    with open(image_path, "rb") as img:
        image_data = base64.b64encode(img.read()).decode("utf-8")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = """
You are a medical AI assistant.

Analyze the uploaded medical report image.

Explain in simple language:

1. What this report says
2. Possible disease
3. Important values if visible
4. Precautions the patient should take

Keep explanation simple and short for patients.
"""

    data = {
        "model": "openrouter/auto",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_data}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 400
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        return result["choices"][0]["message"]["content"]

    except Exception:
        return "AI report analysis unavailable."