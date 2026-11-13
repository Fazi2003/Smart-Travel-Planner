import requests

NESHAN_API_KEY = "key"

# تست سرویس "تبدیل نقطه به آدرس" که تیک آن را زده بودید
lat = 35.6997
lng = 51.3380

url = f"https://api.neshan.org/v5/reverse?lat={lat}&lng={lng}"
headers = {
    "Api-Key": NESHAN_API_KEY
}

print("در حال ارسال درخواست تست دوم (تبدیل نقطه به آدرس) به نشان...")
response = requests.get(url, headers=headers)

print("کد وضعیت:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("تست موفقیت‌آمیز بود! آدرس پیدا شده:")
    print(data.get("formatted_address", "آدرسی یافت نشد"))
else:
    print("خطا در اتصال:", response.text)
