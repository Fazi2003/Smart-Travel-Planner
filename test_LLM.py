import requests

GROQ_API_KEY = "key"

# آدرس endpoint گروک که دقیقاً ساختار OpenAI را شبیه‌سازی می‌کند
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "qwen/qwen3.8-27b",
    "messages": [
        {"role": "user", "content": "سلام! این یک تست اتصال است. در یک جمله‌ی کوتاه به فارسی جواب بده."}
    ]
}
print("در حال ارسال درخواست به Groq...")
try:
    response = requests.post(url, headers=headers, json=data)
    print("کد وضعیت:", response.status_code)

    if response.status_code == 200:
        result = response.json()
        print("جواب مدل:", result["choices"][0]["message"]["content"])
    else:
        print("خطا در پاسخ:", response.status_code, response.text)
except Exception as e:
    print("خطای شبکه یا اتصال:", e)