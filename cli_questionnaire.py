from datetime import date
from typing import Optional
from pydantic import ValidationError
from models import TravelQuestionnaire

VALID_BUDGETS = ("اقتصادی", "متوسط", "لوکس")
VALID_COMPANIONS = ("انفرادی", "زوج", "خانواده", "دوستان")


def prompt_input(message: str) -> str:
    """دریافت ورودی با امکان خروج در هر مرحله"""
    value = input(message).strip()
    if value.lower() in ("exit", "خروج"):
        raise SystemExit("\nخروج از پرسش‌نامه توسط کاربر.")
    return value


def parse_list(raw_text: str) -> list[str]:
    normalized = raw_text.replace("،", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def ask_date(message: str) -> date:
    while True:
        raw = prompt_input(message)
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("❌ فرمت تاریخ نامعتبر است. فرمت صحیح: YYYY-MM-DD (مثال: 2026-12-01)")


def ask_choice(message: str, options: tuple[str, ...]) -> str:
    options_str = " | ".join(options)
    while True:
        val = prompt_input(f"{message} ({options_str}): ")
        if val in options:
            return val
        print(f"❌ مقدار غیرمجاز. لطفاً یکی از این گزینه‌ها را وارد کنید: {options_str}")


def ask_non_empty(message: str) -> str:
    while True:
        val = prompt_input(message)
        if val:
            return val
        print("❌ این فیلد نمی‌تواند خالی باشد.")


def ask_questionnaire() -> Optional[TravelQuestionnaire]:
    print("=== پرسش‌نامه برنامه‌ریز هوشمند سفر ===")
    print("(برای خروج در هر مرحله، کلمه 'خروج' یا 'exit' را وارد کنید)\n")

    # ۱. تاریخ شروع و پایان (با بررسی ترتیب و حداکثر ۱۴ روز)
    while True:
        start_date = ask_date("تاریخ شروع سفر (مثال 2026-12-01): ")
        end_date = ask_date("تاریخ پایان سفر (مثال 2026-12-04): ")
        if end_date < start_date:
            print("❌ تاریخ پایان نمی‌تواند قبل از تاریخ شروع باشد. دوباره وارد کنید.")
            continue
        if (end_date - start_date).days + 1 > 14:
            print("❌ حداکثر مدت سفر در نسخه اول ۱۴ روز است. دوباره وارد کنید.")
            continue
        break

    # ۲. شهر مبدأ و مقصد
    origin_city = ask_non_empty("شهر مبدأ: ")
    dest_raw = prompt_input("شهر مقصد (اختیاری - برای خالی گذاشتن Enter بزنید): ")
    destination_city = dest_raw if dest_raw else None

    # ۳. بودجه و همراهان
    budget_level = ask_choice("سطح بودجه", VALID_BUDGETS)
    companions = ask_choice("نوع همراهان", VALID_COMPANIONS)

    # ۴. علاقه‌مندی‌ها (حداقل یک مورد)
    while True:
        interests = parse_list(prompt_input("علاقه‌مندی‌ها (با ویرگول جدا کنید، مثال: تاریخی، طبیعت‌گردی): "))
        if interests:
            break
        print("❌ حداقل یک علاقه‌مندی باید وارد کنید.")

    # ۵. ترجیحات غذایی (اختیاری)
    food_preferences = parse_list(prompt_input("ترجیحات غذایی (اختیاری - با ویرگول جدا کنید): "))

    # اعتبارسنجی نهایی با Pydantic
    try:
        return TravelQuestionnaire(
            start_date=start_date,
            end_date=end_date,
            origin_city=origin_city,
            destination_city=destination_city,
            budget_level=budget_level,
            interests=interests,
            companions=companions,
            food_preferences=food_preferences,
        )
    except ValidationError as e:
        print("\n❌ خطای غیرمنتظره در اعتبارسنجی:", e)
        return None


if __name__ == "__main__":
    try:
        result = ask_questionnaire()
        if result:
            print("\n✅ پرسش‌نامه با موفقیت ثبت شد:")
            print(result.model_dump_json(indent=2))
    except SystemExit as e:
        print(e)