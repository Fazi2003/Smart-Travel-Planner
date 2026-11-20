
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class TravelQuestionnaire(BaseModel):

    start_date: date = Field(
        description="تاریخ شروع سفر"
    )

    end_date: date = Field(
        description="تاریخ پایان سفر"
    )

    origin_city: str = Field(
        min_length=1,
        description="شهر مبدأ سفر"
    )

    destination_city: str | None = Field(
        default=None,
        description="شهر مقصد موردنظر؛ اختیاری"
    )

    budget_level: Literal["اقتصادی", "متوسط", "لوکس"] = Field(
        description="سطح بودجه سفر"
    )

    interests: list[str] = Field(
        min_length=1,
        description="علاقه‌مندی‌های گردشگری"
    )

    companions: str = Field(
        min_length=1,
        description="همراهان سفر؛ مثل خانواده، دوستان یا انفرادی"
    )

    food_preferences: list[str] = Field(
        default_factory=list,
        description="ترجیحات غذایی کاربر"
    )

    @field_validator("origin_city", "destination_city", "companions")
    @classmethod
    def validate_text(cls, value):
        if value is not None and not value.strip():
            raise ValueError("این فیلد نباید خالی باشد")
        return value.strip() if value else value

    @field_validator("interests", "food_preferences")
    @classmethod
    def validate_lists(cls, values):
        cleaned = [item.strip() for item in values if item.strip()]
        if len(cleaned) != len(values):
            raise ValueError("مقادیر خالی مجاز نیستند")
        return cleaned

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("تاریخ پایان نباید قبل از تاریخ شروع باشد")

        return self


if __name__ == "__main__":

    sample_input = TravelQuestionnaire(
        start_date="2026-12-01",
        end_date="2026-12-04",
        origin_city="تهران",
        destination_city=None,
        budget_level="اقتصادی",
        interests=["طبیعت‌گردی", "تاریخی"],
        companions="دوستان",
        food_preferences=["غذای محلی"]
    )
    try:
        test = TravelQuestionnaire(
            start_date="2026-12-10",
            end_date="2026-12-05",
            origin_city="تهران",
            budget_level="اقتصادی",
            interests=["طبیعت‌گردی"],
            companions="دوستان"
        )
    except Exception as e:
        print("اعتبارسنجی با موفقیت خطا را تشخیص داد:")
        print(e)

    print("مدل با موفقیت ساخته شد!")
    print(sample_input.model_dump_json(indent=2))
