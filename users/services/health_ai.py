import requests
from django.conf import settings


def generate_health_summary(history_text):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "PulseID Health Summary"
    }

    prompt = f"""
You are a medical AI assistant.

Patient Treatment History:
{history_text}

Create a SHORT health summary for the patient.

Rules:
- Maximum 5 points
- Each point must be on a NEW LINE
- Do NOT use *, **, markdown or bullets
- Use simple sentences


"""

    data = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 200
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" not in result:
            return "AI summary unavailable."

        return result["choices"][0]["message"]["content"]

    except Exception:
        return "AI summary unavailable."