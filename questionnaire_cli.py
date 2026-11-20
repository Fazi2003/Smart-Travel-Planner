
from pydantic import ValidationError
from models import TravelQuestionnaire


def get_list_input(message):
    value = input(message).strip()
    value = value.replace("،", ",")
    return [item.strip() for item in value.split(",") if item.strip()]
def main():
    print("\n===== برنامه‌ریز هوشمند سفر =====\n")
    print("لطفاً اطلاعات سفر خود را وارد کنید.\n")

    start_date = input("تاریخ شروع سفر (مثلاً 2026-12-01): ").strip()
    end_date = input("تاریخ پایان سفر (مثلاً 2026-12-04): ").strip()

    origin_city = input("شهر مبدأ: ").strip()

    destination_city = input(
        "شهر مقصد (در صورت نداشتن مقصد مشخص، خالی بگذارید): "
    ).strip()

    print("\nسطح بودجه:")
    print("اقتصادی | متوسط | لوکس")
    budget_level = input("انتخاب شما: ").strip()

    interests = get_list_input(
        "\nعلاقه‌مندی‌ها را با کاما جدا کنید (مثلاً تاریخی، طبیعت‌گردی): "
    )

    companions = input(
        "همراهان سفر (مثلاً خانواده، دوستان، انفرادی): "
    ).strip()

    food_preferences = get_list_input(
        "ترجیحات غذایی را با کاما جدا کنید (در صورت نداشتن خالی بگذارید): "
    )

    try:
        questionnaire = TravelQuestionnaire(
            start_date=start_date,
            end_date=end_date,
            origin_city=origin_city,
            destination_city=destination_city or None,
            budget_level=budget_level,
            interests=interests,
            companions=companions,
            food_preferences=food_preferences
        )

        print("\nاطلاعات سفر با موفقیت ثبت و اعتبارسنجی شد!")
        print("\nاطلاعات نهایی:")
        print(questionnaire.model_dump_json(indent=2))

    except ValidationError as error:
        print("\nاطلاعات واردشده معتبر نیست:")
        print(error)


if __name__ == "__main__":
    main()
