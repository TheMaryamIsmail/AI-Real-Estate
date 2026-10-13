from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import joblib
import pandas as pd

from src.recommender import PropertyRecommender
from src.chatbot import RealEstateChatbot
from src.rag_assistant import RAGKnowledgeAssistant

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Verify it's loaded correctly
api_key = os.getenv("GEMINI_API_KEY")

app = FastAPI(title="AI Real Estate Intelligence Platform")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load ML model & helpers
model = joblib.load("models/house_price_model.pkl")
recommender = PropertyRecommender()
chatbot = RealEstateChatbot()
rag = RAGKnowledgeAssistant()

class PredictionRequest(BaseModel):
    OverallQual: int
    GrLivArea: int
    GarageCars: int
    TotalBsmtSF: int
    FullBath: int
    YearBuilt: int
    Neighborhood: str

class RecommendationRequest(BaseModel):
    max_budget: float
    min_beds: int
    neighborhood: str = "Any"

class ChatRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/predict")
def predict_price(req: PredictionRequest):
    input_data = pd.DataFrame([req.dict()])
    prediction = model.predict(input_data)[0]
    return {"estimated_price": round(prediction, 2)}

@app.post("/api/recommend")
def get_recommendations(req: RecommendationRequest):
    recs = recommender.recommend(req.max_budget, req.min_beds, req.neighborhood)
    return {"recommendations": recs}

@app.post("/api/chat")
def chat_with_ai(req: ChatRequest):
    reply = chatbot.ask(req.prompt)
    return {"response": reply}

@app.post("/api/rag")
def rag_query(req: ChatRequest):
    reply = rag.query(req.prompt)
    return {"response": reply}