from pydantic import BaseModel, Field
from typing import List


# این کلاس ساختار اطلاعاتی است که از کاربر می‌گیریم
class TravelQuestionnaire(BaseModel):
    origin_city: str = Field(description="شهر مبدأ کاربر")
    destination_cities: List[str] = Field(description="لیست شهرهای مقصد احتمالی (حداکثر ۳ شهر)")
    duration_days: int = Field(description="تعداد روزهای سفر", ge=1, le=14)  # بین 1 تا 14 روز
    budget_level: str = Field(description="سطح بودجه: اقتصادی، متوسط یا لوکس")
    interests: List[str] = Field(description="علاقه‌مندی‌های کاربر (مثلاً: تاریخی، طبیعت‌گردی، کافه‌گردی)")


# بخش تست برای اطمینان از عملکرد مدل
if __name__ == "__main__":
    # فرض می‌کنیم این اطلاعات را از رابط کاربری یا کاربر گرفته‌ایم
    sample_input = TravelQuestionnaire(
        origin_city="تهران",
        destination_cities=["اصفهان", "شیراز"],
        duration_days=4,
        budget_level="متوسط",
        interests=["تاریخی", "رستوران‌گردی"]
    )

    print("مدل Pydantic با موفقیت ساخته شد!")
    print("دیتای تبدیل شده به فرمت JSON:")
    print(sample_input.model_dump_json(indent=2))