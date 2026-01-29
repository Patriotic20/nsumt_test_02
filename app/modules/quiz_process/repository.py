from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.quiz.model import Quiz
from models.question.model import Question
from models.results.model import Result
from models.quiz_questions.model import QuizQuestion

from .schemas import (
    StartQuizRequest,
    StartQuizResponse,
    EndQuizRequest,
    EndQuizResponse,
    QuestionDTO,
)
import random

class QuizProcessRepository:
    async def start_quiz(
        self, session: AsyncSession, data: StartQuizRequest
    ) -> StartQuizResponse:
        # Fetch quiz with questions
        stmt = (
            select(Quiz)
            .options(selectinload(Quiz.quiz_questions).selectinload(QuizQuestion.question))
            .where(Quiz.id == data.quiz_id)
        )
        result = await session.execute(stmt)
        quiz = result.scalar_one_or_none()

        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )

        if not quiz.is_active:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Quiz is not active"
            )
            
        if quiz.pin != data.pin:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid PIN"
            )

        # Prepare questions with shuffled options
        question_dtos = []
        # Accessing questions via quiz_questions association
        # quiz.quiz_questions is a list of QuizQuestion objects
        # each has a .question attribute
        
        # We might want to limit the number of questions if quiz.question_number is set
        # But for now, let's take all or slice? 
        # The user didn't specify random selection logic from pool, so let's assume all linked questions or slice.
        # Let's shuffle the questions themselves too?
        
        quiz_questions = [qq.question for qq in quiz.quiz_questions if qq.question]
        
        # Determine how many questions to show
        num_questions = quiz.question_number
        if len(quiz_questions) > num_questions:
            random.shuffle(quiz_questions)
            quiz_questions = quiz_questions[:num_questions]
        else:
            random.shuffle(quiz_questions)

        for q in quiz_questions:
            q_dict = q.to_dict(randomize_options=True)
            
            question_dtos.append(
                QuestionDTO(
                    id=q_dict["id"],
                    text=q_dict["text"],
                    options=q_dict["options"]
                )
            )

        return StartQuizResponse(
            quiz_id=quiz.id,
            title=quiz.title,
            duration=quiz.duration,
            questions=question_dtos
        )

    async def end_quiz(
        self, session: AsyncSession, data: EndQuizRequest
    ) -> EndQuizResponse:
        # Fetch quiz to get subject/group info if needed, or just for verification
        stmt = select(Quiz).where(Quiz.id == data.quiz_id)
        result = await session.execute(stmt)
        quiz = result.scalar_one_or_none()
        
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )

        correct_count = 0
        wrong_count = 0
        
        # Efficiently fetch all relevant questions to check answers
        question_ids = [ans.question_id for ans in data.answers]
        if not question_ids:
             # No answers submitted?
             pass
             
        # Fetch questions
        q_stmt = select(Question).where(Question.id.in_(question_ids))
        q_result = await session.execute(q_stmt)
        questions_map = {q.id: q for q in q_result.scalars().all()}
        
        for ans in data.answers:
            question = questions_map.get(ans.question_id)
            if question:
                # Option A is always correct
                if ans.answer == question.option_a:
                    correct_count += 1
                else:
                    wrong_count += 1
            else:
                # Question not found? Count as wrong?
                wrong_count += 1
        
        total_questions = len(data.answers) # Or strictly correct + wrong
        
        # Calculate grade (0-100)
        grade = 0
        if total_questions > 0:
            grade = int((correct_count / total_questions) * 100)
            
        # Create Result
        # Assuming user_id is passed or handled via auth in router (for now relying on request data)
        # Note: Result model expects integer for grade
        
        result = Result(
            user_id=data.user_id, # Can be None if anonymous
            quiz_id=quiz.id,
            subject_id=quiz.subject_id,
            group_id=quiz.group_id, # This takes group from quiz, but maybe should take from user? 
                                    # Result model has group_id. Let's use quiz.group_id for now as context.
            correct_answers=correct_count,
            wrong_answers=wrong_count,
            grade=grade
        )
        session.add(result)
        
        try:
            await session.commit()
            await session.refresh(result)
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error while saving result",
            )

        return EndQuizResponse(
            total_questions=total_questions,
            correct_answers=correct_count,
            wrong_answers=wrong_count,
            grade=float(grade)
        )

get_quiz_process_repository = QuizProcessRepository()
