
from datetime import date
from pydantic import ValidationError
from models import TravelQuestionnaire


def parse_list(raw_text: str) -> list[str]:
    """تبدیل متن جداشده با کاما یا ویرگول فارسی به لیست"""
    normalized = raw_text.replace("،", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def ask_questionnaire() -> TravelQuestionnaire:
    print("=== پرسش‌نامه برنامه‌ریز هوشمند سفر ===\n")

    while True:
        try:
            start_str = input("تاریخ شروع سفر (مثال 2026-12-01): ").strip()
            end_str = input("تاریخ پایان سفر (مثال 2026-12-04): ").strip()

            origin_city = input("شهر مبدأ: ").strip()

            dest_input = input(
                "شهر مقصد (اختیاری - برای خالی گذاشتن Enter بزنید): "
            ).strip()

            destination_city = dest_input if dest_input else None

            print("\nسطح بودجه مجاز: اقتصادی | متوسط | لوکس")
            budget_level = input("سطح بودجه: ").strip()

            interests_raw = input(
                "علاقه‌مندی‌ها (با ویرگول جدا کنید): "
            )
            interests = parse_list(interests_raw)

            print("\nنوع همراهان مجاز: انفرادی | زوج | خانواده | دوستان")
            companions = input("نوع همراهان: ").strip()

            if companions not in ["انفرادی", "زوج", "خانواده", "دوستان"]:
                raise ValueError("نوع همراهان باید یکی از مقادیر مجاز باشد.")

            food_raw = input(
                "ترجیحات غذایی (اختیاری - با ویرگول جدا کنید): "
            )
            food_preferences = parse_list(food_raw)

            questionnaire = TravelQuestionnaire(
                start_date=date.fromisoformat(start_str),
                end_date=date.fromisoformat(end_str),
                origin_city=origin_city,
                destination_city=destination_city,
                budget_level=budget_level,
                interests=interests,
                companions=companions,
                food_preferences=food_preferences,
            )

            return questionnaire

        except ValidationError as e:
            print("\n❌ اطلاعات واردشده معتبر نیست:")

            for err in e.errors():
                field = " -> ".join(str(loc) for loc in err["loc"])
                print(f"  - {field}: {err['msg']}")

            print("لطفاً دوباره اطلاعات را وارد کنید.\n")

        except ValueError as ve:
            print(f"\n❌ خطا: {ve}")
            print("لطفاً دوباره اطلاعات را وارد کنید.\n")


if __name__ == "__main__":
    result = ask_questionnaire()

    print("\n✅ پرسش‌نامه با موفقیت ثبت و اعتبارسنجی شد:")
    print(result.model_dump_json(indent=2))
