from pydantic import BaseModel, ConfigDict
from typing import Optional

class GeneralStatisticsResponse(BaseModel):
    total_students_tested: int
    total_quizzes_taken: int
    system_average_grade: float
    
    model_config = ConfigDict(from_attributes=True)

class QuizStatisticsResponse(BaseModel):
    quiz_id: int
    title: str
    times_taken: int
    average_grade: float
    highest_grade: int
    lowest_grade: int
    
    model_config = ConfigDict(from_attributes=True)

class UserStatisticsResponse(BaseModel):
    user_id: int
    full_name: Optional[str]
    quizzes_taken: int
    average_grade: float
    
    model_config = ConfigDict(from_attributes=True)
