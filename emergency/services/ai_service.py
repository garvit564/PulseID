import requests
from django.conf import settings


def analyze_emergency(history, reason):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "PulseID Emergency System"
    }

    prompt = f"""
You are an emergency medical triage AI.

Patient Medical History:
{history}

Current Emergency Reason:
{reason}

Based on medical history and current symptoms:

1. Classify severity strictly as one of: low, medium, high, critical.
2. Summarize relevant past conditions.
3. Mention possible medical risks.
4. Suggest what hospital team should prepare for.

Respond strictly in this format:

PRIORITY: <low/medium/high/critical>

SUMMARY:
<short professional medical summary>
"""

    data = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        print("AI RAW RESPONSE:", result)

        if "error" in result:
            return "medium", result["error"]["message"]

        if "choices" not in result:
            return "medium", "Unexpected AI response format"

        content = result["choices"][0]["message"]["content"]

        priority = "medium"

        text = content.lower()

        if "critical" in text:
            priority = "critical"
        elif "high" in text:
            priority = "high"
        elif "medium" in text:
            priority = "medium"
        elif "low" in text:
            priority = "low"

        return priority, content

    except Exception as e:
        return "medium", str(e)