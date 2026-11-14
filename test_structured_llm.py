import os
import requests
import json
from dotenv import load_dotenv
from models import TravelQuestionnaire  # ایمپورت کردن قالبی که ساختید

# خواندن امن کلید بدون اینکه در کد نوشته شده باشد
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# گرفتن ساختار استاندارد از کلاسی که نوشتید تا به هوش مصنوعی پاس بدهیم
schema = TravelQuestionnaire.model_json_schema()

# دستور ما به هوش مصنوعی (Prompt)
prompt = f"""
تو یک دستیار برنامه‌ریز سفر هستی.
اطلاعات زیر را از صحبت‌های کاربر استخراج کن و دقیقاً و فقط در قالب JSON زیر جواب بده:
{json.dumps(schema, ensure_ascii=False)}

متن کاربر: "من هفته آینده از تهران می‌خوام برم سمت شمال (رشت یا لاهیجان) برای ۳ روز. بودجه‌ام هم اقتصادیه و بیشتر دنبال طبیعت‌گردی و شکم‌گردی هستم."

نکته مهم: فقط و فقط JSON خالص برگردان، بدون هیچ کلمه اضافه‌ای قبل یا بعد از آن.
"""

data = {
    "model": "qwen/qwen3.8-27b",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.1  # دمای پایین یعنی جواب دقیق و بدون خلاقیتِ اضافه
}

print("در حال ارسال درخواست به Groq و استخراج دیتا...")
response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    result_text = response.json()["choices"][0]["message"]["content"]
    print("\nخروجی خام هوش مصنوعی:")
    print(result_text)

    # بخش جادویی: تبدیل متن هوش مصنوعی به آبجکت پایتون و اعتبارسنجی آن
    try:
        final_data = TravelQuestionnaire.model_validate_json(result_text)
        print("\n✅ موفقیت! Pydantic دیتا را تأیید و ساختاریافته کرد:")
        print(f"مبدأ: {final_data.origin_city}")
        print(f"تعداد روزها: {final_data.duration_days}")
        print(f"مقصدهای استخراج شده: {final_data.destination_cities}")
    except Exception as e:
        print("\n❌ خطا در اعتبارسنجی ساختار Pydantic:", e)
else:
    print("خطا در ارتباط با سرور:", response.text)