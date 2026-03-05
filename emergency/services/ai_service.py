import requests
from django.conf import settings


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

Emergency Reason:
{reason}

Analyse the case and respond EXACTLY like this:

PRIORITY: <low/medium/high/critical>
SPECIALITY: <cardiology/trauma/orthopedic/neurology/pediatric/general>
SUMMARY: <2-3 sentence medical explanation for doctors>
summary should be shown in bullets points
do not extraggate

The summary must explain:
- patient's past treatment history
- probable condition
- possible risks
- what hospital team should prepare for
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
            return "medium", "general", result["error"]["message"]

        if "choices" not in result:
            return "medium", "general", "Unexpected AI response format"

        content = result["choices"][0]["message"]["content"]

        text = content.lower()

        priority = "medium"
        speciality = "general"
        summary = content

        # priority detection
        if "critical" in text:
            priority = "critical"
        elif "high" in text:
            priority = "high"
        elif "medium" in text:
            priority = "medium"
        elif "low" in text:
            priority = "low"

        # speciality detection
        if "cardiology" in text:
            speciality = "cardiology"
        elif "trauma" in text:
            speciality = "trauma"
        elif "orthopedic" in text:
            speciality = "orthopedic"
        elif "neurology" in text:
            speciality = "neurology"
        elif "pediatric" in text:
            speciality = "pediatric"

        # extract summary
        if "summary:" in text:
            summary = content.split("SUMMARY:")[-1].strip()

        return priority, speciality, summary

    except Exception as e:
        return "medium", "general", str(e)