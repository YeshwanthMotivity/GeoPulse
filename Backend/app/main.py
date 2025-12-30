from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev convenience
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/guide/{country}")
def get_guide(country: str, db: Session = Depends(get_db)):
    # Normalize input: "india" -> "India", "usa" -> "United States" (handling aliases could be added here)
    # Normalize input: strip whitespace
    # We do NOT employ .title() because it breaks names like "Antigua and Barbuda" -> "Antigua And Barbuda"
    # The frontend sends the correct name from the dropdown. 
    # For manual URL entry we will rely on a case-insensitive search in CRUD.
    search_name = country.strip()
    
    # Handle common aliases (manual overrides if needed)
    aliases = {
        "usa": "United States",
        "us": "United States",
        "america": "United States",
        "uk": "United Kingdom",
        "uae": "United Arab Emirates"
    }
    # Check alias case-insensitively
    if search_name.lower() in aliases:
        search_name = aliases[search_name.lower()]

    country_obj = crud.get_country_by_name(db, search_name)
    if not country_obj:
        raise HTTPException(status_code=404, detail=f"Country '{search_name}' not found")
    
    details = crud.get_cultural_details(db, country_obj.id)
    
    # Transform data for frontend
    response_data = {
        "country": country_obj.name,
        "language": country_obj.language,
        "details": [
            {
                "category": d.category,
                "topic": d.topic,
                "description": d.description,
                "is_strict": d.is_strict
            } for d in details
        ]
    }
    return response_data

@app.get("/api/countries")
def get_countries(db: Session = Depends(get_db)):
    countries = crud.get_all_countries(db)
    return [{"id": c.id, "name": c.name} for c in countries]


from pydantic import BaseModel
class ChatRequest(BaseModel):
    message: str
    country: str

from app.chat_service import ChatService

# ... (Previous code remains the same)

@app.post("/api/chat")
def chat_culture(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Intelligent cultural chat using Agentic Pattern (ChatService).
    """
    chat_agent = ChatService(db)
    return chat_agent.process_message(request.message, request.country)

@app.get("/api/quiz/{country}")
def get_quiz(country: str, db: Session = Depends(get_db)):
    # Normalize input same way as guide
    search_name = country.strip()
    aliases = {
        "usa": "United States",
        "us": "United States",
        "america": "United States",
        "uk": "United Kingdom",
        "uae": "United Arab Emirates"
    }
    if search_name.lower() in aliases:
        search_name = aliases[search_name.lower()]
        
    country_obj = crud.get_country_by_name(db, search_name)
    if not country_obj:
        return [] # Return empty list if no country/quiz
        
    # Get quiz questions
    # We need a CRUD method for this, or just query here for simplicity
    questions = db.query(models.QuizQuestion).filter(models.QuizQuestion.country_id == country_obj.id).all()
    
    return [
        {
            "id": q.id,
            "question": q.question,
            "options": [q.option_a, q.option_b, q.option_c, q.option_d],
            "answer": q.answer
        }
        for q in questions
    ]

