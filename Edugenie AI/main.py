from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from explanation_module import explain_topic
from qna import answer_question_with_gemini
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# --------------------------------------------------
# EduGenie FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="EduGenie Learning Companion",
    description="AI-powered educational assistant",
    version="1.0.0",
)


# --------------------------------------------------
# Static files and templates
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(directory="templates")


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class TopicRequest(BaseModel):
    topic: str


class TextRequest(BaseModel):
    text: str


class QuestionRequest(BaseModel):
    question: str
    level: str = "beginner"


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# --------------------------------------------------
# Question & Answer API
# --------------------------------------------------

@app.get("/qa")
async def qa_api(
    question: str = Query(
        ...,
        description="Student question"
    )
):
    question = question.strip()

    if not question:
        return JSONResponse(
            content={
                "error": "Please provide a question."
            },
            status_code=400
        )

    try:
        answer = answer_question_with_gemini(question)

        return {
            "question": question,
            "answer": answer
        }

    except Exception as error:
        return JSONResponse(
            content={
                "error": str(error)
            },
            status_code=500
        )


# --------------------------------------------------
# Explanation API
# --------------------------------------------------

@app.post("/explain")
async def explain_api(payload: TopicRequest):
    topic = payload.topic.strip()

    if not topic:
        return JSONResponse(
            content={
                "error": "Please provide a topic."
            },
            status_code=400
        )

    try:
        explanation = explain_topic(topic)

        return {
            "topic": topic,
            "explanation": explanation
        }

    except Exception as error:
        return JSONResponse(
            content={
                "error": str(error)
            },
            status_code=500
        )


# --------------------------------------------------
# Summary API
# --------------------------------------------------

@app.post("/summarize")
async def summarize_api(payload: TextRequest):
    text = payload.text.strip()

    if not text:
        return JSONResponse(
            content={
                "error": "Please provide text to summarize."
            },
            status_code=400
        )

    try:
        summary = summarize_text(text)

        return {
            "summary": summary
        }

    except Exception as error:
        return JSONResponse(
            content={
                "error": str(error)
            },
            status_code=500
        )


# --------------------------------------------------
# Quiz API
# --------------------------------------------------

@app.post("/quiz")
async def quiz_api(payload: TextRequest):
    text = payload.text.strip()

    if not text:
        return JSONResponse(
            content={
                "error": "Please provide text for quiz."
            },
            status_code=400
        )

    try:
        quiz = generate_quiz(text)

        return {
            "quiz": quiz
        }

    except Exception as error:
        return JSONResponse(
            content={
                "error": str(error)
            },
            status_code=500
        )


# --------------------------------------------------
# Learning Recommendations API
# --------------------------------------------------

@app.get("/learn/recommendations")
async def learning_recommendations_api(
    topic: str = Query(
        ...,
        description="Topic for learning roadmap"
    )
):
    topic = topic.strip()

    if not topic:
        return JSONResponse(
            content={
                "error": "Please provide a topic."
            },
            status_code=400
        )

    try:
        recommendation = get_learning_recommendations(topic)

        return {
            "topic": topic,
            "recommendation": recommendation
        }

    except Exception as error:
        return JSONResponse(
            content={
                "error": str(error)
            },
            status_code=500
        )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "application": "EduGenie",
        "version": "1.0.0"
    }