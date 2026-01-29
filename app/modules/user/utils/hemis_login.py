from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime
from httpx import AsyncClient

from core.db_helper import db_helper

from user.schemas import UserLoginRequest


class HemisLoginService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, credentials: UserLoginRequest):
        headers = {
            "Content-Type": "application/json"
        }
        async with AsyncClient() as client:
            response = await client.post(
                settings.hemis.base_url, data=credentials.model_dump(), headers=headers
            )
            return response.json().get("data", {})
        

    async def map_student_data(self):
        api_data = self.login()
        user_data = {
            "first_name": api_data.get("first_name"),
            "last_name": api_data.get("second_name"),
            "third_name": api_data.get("third_name"),
            "full_name": api_data.get("full_name"),
            "student_id_number": api_data.get("student_id_number"),
            "image_path": api_data.get("image"),
            "birth_date": api_data.get("birth_date"),
            "phone": api_data.get("phone"),
            "gender": api_data.get("gender", {}).get("name"),
            "university": api_data.get("university"),
            "specialty": api_data.get("specialty", {}).get("name"),
            "student_status": api_data.get("studentStatus", {}).get("name"),
            "education_form": api_data.get("educationForm", {}).get("name"),
            "education_type": api_data.get("educationType", {}).get("name"),
            "payment_form": api_data.get("paymentForm", {}).get("name"),
            "group": api_data.get("group", {}).get("name"),
            "education_lang": api_data.get("educationLang", {}).get("name"),
            "faculty": api_data.get("faculty", {}).get("name"),
            "level": api_data.get("level", {}).get("name"),
            "semester": api_data.get("semester", {}).get("name"),
            "address": api_data.get("address"),
            "avg_gpa": api_data.get("avg_gpa"),
        }

        if user_data["birth_date"]:
            try:
                user_data["birth_date"] = datetime.fromtimestamp(
                    user_data["birth_date"]
                ).date()
            except (TypeError, ValueError):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="birth_date is invalid in API response",
                )

    # async def create_or_update_user(self, user_data: dict):
    #     pass


hemis_login_service = HemisLoginService(session=db_helper.session_getter)
