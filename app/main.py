from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.data import COURSES
from app.zybooks_helper import ZyBooksHelper

app = FastAPI(title="Study Pilot")
helper = ZyBooksHelper()
INDEX_HTML = Path(__file__).resolve().parent.parent / "templates" / "index.html"
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


class StudyPlanRequest(BaseModel):
    topic: str = Field(..., min_length=1)
    days: int = Field(..., gt=0)
    hours_per_day: int = Field(..., gt=0)


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
    topic: str = Field(..., min_length=1)
    questions: int = Field(..., gt=0)


class QuizResponse(BaseModel):
    topic: str
    questions: List[QuizQuestion]


class CourseGuidanceRequest(BaseModel):
    course: str = Field(..., min_length=1)
    topic: str = Field(..., min_length=1)


class CourseGuidanceResponse(BaseModel):
    course: str
    topic: str
    study_tips: List[str]


class WeeklyPlanRequest(BaseModel):
    course: str = Field(..., min_length=1)
    goal: str = Field(..., min_length=1)
    days: int = Field(..., gt=0)


class WeeklyPlanItem(BaseModel):
    day: str
    task: str


class WeeklyPlanResponse(BaseModel):
    course: str
    goal: str
    schedule: List[WeeklyPlanItem]


class ZyBooksRequest(BaseModel):
    text: str = Field(..., min_length=1)


class ZyBooksResponse(BaseModel):
    summary: str
    key_concepts: List[str]
    quick_questions: List[QuizQuestion]


@app.get("/", response_class=FileResponse)
def read_root():
    return FileResponse(INDEX_HTML, media_type="text/html")


@app.get("/courses")
def get_courses():
    return {"courses": COURSES}


@app.get("/static/{filename}")
def get_static(filename: str):
    return FileResponse(STATIC_DIR / filename)


@app.post("/study-plan", response_model=StudyPlanResponse)
def generate_study_plan(request: StudyPlanRequest):
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
    return ZyBooksResponse(
        summary=helper.summarize_text(request.text),
        key_concepts=helper.extract_key_concepts(request.text),
        quick_questions=[
            QuizQuestion(**question)
            for question in helper.generate_quick_questions("the chapter")
        ],
    )
