from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.ai_helper import StudyAI, string_list
from app.data import COURSES
from app.zybooks_helper import ZyBooksHelper

PROJECT_DIR = Path(__file__).resolve().parent.parent
INDEX_HTML = PROJECT_DIR / "templates" / "index.html"
STATIC_DIR = PROJECT_DIR / "static"
ai = StudyAI()
helper = ZyBooksHelper()

tags_metadata = [
    {
        "name": "System",
        "description": "System health and API information.",
    },
    {
        "name": "Courses",
        "description": "Browse available WGU courses.",
    },
    {
        "name": "Study Plans",
        "description": "Generate personalized study plans.",
    },
    {
        "name": "Quiz",
        "description": "Generate AI-powered quizzes.",
    },
    {
        "name": "Course Guidance",
        "description": "Get AI study recommendations.",
    },
    {
        "name": "Weekly Planner",
        "description": "Create weekly study schedules.",
    },
    {
        "name": "ZyBooks",
        "description": "Summarize course readings and generate review questions.",
    },
]

app = FastAPI(
    title="Study Pilot Air",
    description="🚀 AI-powered study assistant for personalized learning, quizzes, summaries, and study planning.",
    version="1.0.0",
    contact={
        "name": "Guillermo Barreto",
        "url": "https://github.com/GuillermoBarreto",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=tags_metadata,
)

class StudyPlanRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    days: int = Field(..., gt=0, le=14)
    hours_per_day: int = Field(..., gt=0, le=12)


class StudyDay(BaseModel):
    title: str
    focus: str
    goal: str


class StudyPlanResponse(BaseModel):
    topic: str
    hours_per_day: int
    days: List[StudyDay]


class QuizQuestion(BaseModel):
    question: str
    answer: str
    options: List[str]


class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    questions: int = Field(..., gt=0, le=10)


class QuizResponse(BaseModel):
    topic: str
    questions: List[QuizQuestion]


class CourseGuidanceRequest(BaseModel):
    course: str = Field(..., min_length=1, max_length=120)
    topic: str = Field(..., min_length=1, max_length=200)


class CourseGuidanceResponse(BaseModel):
    course: str
    topic: str
    study_tips: List[str]


class WeeklyPlanRequest(BaseModel):
    course: str = Field(..., min_length=1, max_length=120)
    goal: str = Field(..., min_length=1, max_length=400)
    days: int = Field(..., gt=0, le=7)


class WeeklyPlanItem(BaseModel):
    day: str
    task: str


class WeeklyPlanResponse(BaseModel):
    course: str
    goal: str
    schedule: List[WeeklyPlanItem]


class ZyBooksRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=12000)


class ZyBooksResponse(BaseModel):
    summary: str
    key_concepts: List[str]
    quick_questions: List[QuizQuestion]


@app.get("/", response_class=FileResponse)
def read_root():
    return FileResponse(INDEX_HTML, media_type="text/html")


@app.get("/dashboard", response_class=FileResponse)
def read_dashboard():
    return FileResponse(INDEX_HTML, media_type="text/html")


@app.get("/courses")
def get_courses():
    return {"courses": COURSES}


@app.get("/static/{filename}")
def get_static(filename: str):
    return FileResponse(STATIC_DIR / filename)

@app.get("/health", tags=["System"])
def health():
    return {
        "status": "healthy",
        "service": "Study Pilot Air",
        "version": "1.0.0",
    }


@app.get("/api/info", tags=["System"])
def api_info():
    return {
        "name": "Study Pilot Air",
        "version": "1.0.0",
        "author": "Guillermo Barreto",
        "description": "AI-powered study assistant",
    }

@app.post("/study-plan", response_model=StudyPlanResponse)
def generate_study_plan(request: StudyPlanRequest):
    ai_result = ai.generate_json(
        "Create a practical study plan. Return JSON with a 'days' array. Each item must have "
        "'title', 'focus', and 'goal' strings. Create exactly the requested number of days.",
        f"Topic: {request.topic}\nDays: {request.days}\nHours per day: {request.hours_per_day}",
    )
    ai_days = ai_result.get("days") if ai_result else None
    if isinstance(ai_days, list) and len(ai_days) == request.days:
        try:
            return StudyPlanResponse(
                topic=request.topic,
                hours_per_day=request.hours_per_day,
                days=[StudyDay(**day) for day in ai_days],
            )
        except (TypeError, ValueError):
            pass

    focuses = [
        "Core syntax and variables",
        "Control flow and functions",
        "Practice problems and review",
    ]

    days = []
    for index in range(request.days):
        focus = focuses[index % len(focuses)]
        days.append(
            StudyDay(
                title=f"Day {index + 1}",
                focus=focus,
                goal=f"Spend {request.hours_per_day} hours learning {focus.lower()} for {request.topic}",
            )
        )

    return StudyPlanResponse(
        topic=request.topic,
        hours_per_day=request.hours_per_day,
        days=days,
    )


@app.post("/quiz", response_model=QuizResponse)
def generate_quiz(request: QuizRequest):
    ai_result = ai.generate_json(
        "Create a multiple-choice quiz. Return JSON with a 'questions' array. Each item must "
        "have 'question', 'answer', and 'options'. Options must be an array of exactly 3 strings "
        "and include the answer. Create exactly the requested number of questions.",
        f"Topic: {request.topic}\nQuestions: {request.questions}",
    )
    ai_questions = ai_result.get("questions") if ai_result else None
    if isinstance(ai_questions, list) and len(ai_questions) == request.questions:
        try:
            return QuizResponse(topic=request.topic, questions=[QuizQuestion(**item) for item in ai_questions])
        except (TypeError, ValueError):
            pass

    return QuizResponse(
        topic=request.topic,
        questions=[
            QuizQuestion(
                question=f"What is the main idea of {request.topic}?",
                answer="Core concept",
                options=[
                    "Core concept",
                    "Key definition",
                    "Real-world example",
                ],
            )
            for _ in range(request.questions)
        ],
    )


@app.post("/course-guidance", response_model=CourseGuidanceResponse)
def generate_course_guidance(request: CourseGuidanceRequest):
    ai_result = ai.generate_json(
        "Give concise, actionable study advice. Return JSON with a 'study_tips' array of 3 strings.",
        f"Course: {request.course}\nTopic: {request.topic}",
    )
    ai_tips = string_list(ai_result.get("study_tips")) if ai_result else None
    if ai_tips:
        return CourseGuidanceResponse(course=request.course, topic=request.topic, study_tips=ai_tips)

    return CourseGuidanceResponse(
        course=request.course,
        topic=request.topic,
        study_tips=[
            f"Review the main ideas of {request.topic} before class.",
            f"Practice one example problem related to {request.topic} each day.",
            f"Create a short summary sheet for {request.topic} to review before exams.",
        ],
    )


@app.post("/weekly-plan", response_model=WeeklyPlanResponse)
def generate_weekly_plan(request: WeeklyPlanRequest):
    ai_result = ai.generate_json(
        "Create a practical weekly study schedule. Return JSON with a 'schedule' array. Each item "
        "must have a 'day' and 'task' string. Create exactly the requested number of items.",
        f"Course: {request.course}\nGoal: {request.goal}\nDays: {request.days}",
    )
    ai_schedule = ai_result.get("schedule") if ai_result else None
    if isinstance(ai_schedule, list) and len(ai_schedule) == request.days:
        try:
            return WeeklyPlanResponse(
                course=request.course,
                goal=request.goal,
                schedule=[WeeklyPlanItem(**item) for item in ai_schedule],
            )
        except (TypeError, ValueError):
            pass

    tasks = [
        "Review notes and identify the main ideas",
        "Practice one example problem and write out the steps",
        "Summarize the topic in your own words before class",
    ]

    schedule = [
        WeeklyPlanItem(day=f"Day {index + 1}", task=tasks[index % len(tasks)])
        for index in range(request.days)
    ]

    return WeeklyPlanResponse(course=request.course, goal=request.goal, schedule=schedule)


@app.post("/zybooks", response_model=ZyBooksResponse)
def summarize_zybooks_content(request: ZyBooksRequest):
    ai_result = ai.generate_json(
        "Summarize this course reading for a student. Return JSON with 'summary' (a concise string), "
        "'key_concepts' (up to 8 strings), and 'quick_questions' (exactly 2 items). Each question "
        "must have 'question', 'answer', and 'options'; options must be 3 strings including the answer.",
        request.text,
    )
    if ai_result:
        concepts = string_list(ai_result.get("key_concepts"))
        questions = ai_result.get("quick_questions")
        summary = ai_result.get("summary")
        if isinstance(summary, str) and concepts and isinstance(questions, list) and len(questions) == 2:
            try:
                return ZyBooksResponse(
                    summary=summary.strip(),
                    key_concepts=concepts,
                    quick_questions=[QuizQuestion(**question) for question in questions],
                )
            except (TypeError, ValueError):
                pass

    return ZyBooksResponse(
        summary=helper.summarize_text(request.text),
        key_concepts=helper.extract_key_concepts(request.text),
        quick_questions=[
            QuizQuestion(**question)
            for question in helper.generate_quick_questions("the chapter")
        ],
    )
