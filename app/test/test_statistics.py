import pytest

@pytest.mark.asyncio
async def test_general_statistics(auth_client, test_subject, test_group):
    # Setup: Create quiz and results
    users_resp = await auth_client.get("/user/")
    user_id = users_resp.json()["users"][0]["id"]

    # Create Quiz
    quiz_payload = {
        "title": "General Stats Quiz",
        "question_number": 1,
        "duration": 60,
        "pin": "1111",
        "user_id": user_id,
        "group_id": test_group["id"],
        "subject_id": test_subject.id,
        "is_active": True
    }
    quiz_resp = await auth_client.post("/quiz/", json=quiz_payload)
    quiz_id = quiz_resp.json()["id"]

    # Create Question
    q_payload = {
        "subject_id": test_subject.id,
        "user_id": user_id,
        "text": "Stats Q1",
        "option_a": "A",
        "option_b": "B",
        "option_c": "C",
        "option_d": "D"
    }
    q_resp = await auth_client.post("/question/", json=q_payload)
    q_id = q_resp.json()["id"]

    # Create Result (100%)
    end_payload = {
        "quiz_id": quiz_id,
        "user_id": user_id,
        "answers": [{"question_id": q_id, "answer": "A"}]
    }
    await auth_client.post("/quiz_process/end_quiz", json=end_payload)

    # Fetch General Statistics
    response = await auth_client.get("/statistics/general")
    assert response.status_code == 200
    data = response.json()
    assert data["total_students_tested"] >= 1
    assert data["total_quizzes_taken"] >= 1
    assert data["system_average_grade"] >= 0


@pytest.mark.asyncio
async def test_quiz_statistics(auth_client, test_subject, test_group):
    users_resp = await auth_client.get("/user/")
    user_id = users_resp.json()["users"][0]["id"]

    # Create Quiz
    quiz_payload = {
        "title": "Quiz Stats Quiz",
        "question_number": 1,
        "duration": 60,
        "pin": "2222",
        "user_id": user_id,
        "group_id": test_group["id"],
        "subject_id": test_subject.id,
        "is_active": True
    }
    quiz_resp = await auth_client.post("/quiz/", json=quiz_payload)
    quiz_id = quiz_resp.json()["id"]

    # Create Question
    q_payload = {
        "subject_id": test_subject.id,
        "user_id": user_id,
        "text": "Quiz Stats Q1",
        "option_a": "A",
        "option_b": "B",
        "option_c": "C",
        "option_d": "D"
    }
    q_resp = await auth_client.post("/question/", json=q_payload)
    q_id = q_resp.json()["id"]

    # Run quiz twice. Once 100%, once 0%
    
    # 1. 100%
    end_payload_1 = {
        "quiz_id": quiz_id,
        "user_id": user_id,
        "answers": [{"question_id": q_id, "answer": "A"}]
    }
    await auth_client.post("/quiz_process/end_quiz", json=end_payload_1)

    # 2. 0%
    end_payload_2 = {
        "quiz_id": quiz_id,
        "user_id": user_id,
        "answers": [{"question_id": q_id, "answer": "B"}]
    }
    await auth_client.post("/quiz_process/end_quiz", json=end_payload_2)

    # Verify Stats
    response = await auth_client.get(f"/statistics/quiz/{quiz_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["quiz_id"] == quiz_id
    assert data["times_taken"] == 2
    assert data["average_grade"] == 50.0 # (100 + 0) / 2
    assert data["highest_grade"] == 100
    assert data["lowest_grade"] == 0

@pytest.mark.asyncio
async def test_user_statistics(auth_client, test_subject, test_group):
    # This relies on the current auth user (admin)
    users_resp = await auth_client.get("/user/")
    user_id = users_resp.json()["users"][0]["id"]

    # Start fresh quiz to ensure clean stats contribution? 
    # Or just check if stats are returned.
    
    # Let's create a new quiz and complete it to ensure we have data.
    quiz_payload = {
        "title": "User Stats Quiz",
        "question_number": 1,
        "duration": 60,
        "pin": "3333",
        "user_id": user_id,
        "group_id": test_group["id"],
        "subject_id": test_subject.id,
        "is_active": True
    }
    quiz_resp = await auth_client.post("/quiz/", json=quiz_payload)
    quiz_id = quiz_resp.json()["id"]

    q_payload = {
        "subject_id": test_subject.id,
        "user_id": user_id,
        "text": "User Stats Q1",
        "option_a": "A",
        "option_b": "B",
        "option_c": "C",
        "option_d": "D"
    }
    q_resp = await auth_client.post("/question/", json=q_payload)
    q_id = q_resp.json()["id"]

    end_payload = {
        "quiz_id": quiz_id,
        "user_id": user_id,
        "answers": [{"question_id": q_id, "answer": "A"}]
    }
    await auth_client.post("/quiz_process/end_quiz", json=end_payload)

    # Verify User Stats
    response = await auth_client.get(f"/statistics/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == user_id
    assert data["quizzes_taken"] >= 1
    assert data["average_grade"] >= 0
