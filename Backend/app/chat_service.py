from sqlalchemy.orm import Session
from app import crud, models
from app.models import Country, CulturalDetail
import random

class ChatService:
    """
    Service to handle cultural chat logic using an improved semantic intent approach.
    """
    
    def __init__(self, db: Session):
        self.db = db

    def detect_country(self, message: str, current_context_name: str):
        """
        Tool: Determine the target country based on message content or current context.
        """
        message = message.lower()
        all_countries = crud.get_all_countries(self.db)
        
        # 1. Message Override (Highest Priority)
        for c in all_countries:
            if c.name.lower() in message:
                return c

        # 2. Current Context (State)
        if current_context_name and current_context_name.lower() != "general":
            return crud.get_country_by_name(self.db, current_context_name)
            
        return None

    def analyze_intent(self, message: str):
        """
        Tool: Classify user intent into categories: GREETING, DO, DONT, TOP_TIPS, or OFF_TOPIC.
        """
        msg_lower = message.lower()
        
        # 1. Greetings
        if any(word in msg_lower for word in ["hello", "hi", "hey", "start", "begin", "good morning"]):
            return "GREETING"
            
        # 2. Specific Intents
        if any(word in msg_lower for word in ["do", "allowed", "okay", "can i", "should i"]):
            return "DO"
        if any(word in msg_lower for word in ["don't", "avoid", "illegal", "rude", "forbidden", "never", "taboo", "bad"]):
            return "DONT"
        if any(word in msg_lower for word in ["tip", "guide", "advice", "help", "summary", "best practice", "tell me", "know about", "what is"]):
            return "TOP_TIPS"
            
        # 3. Off-Topic Filtering (Relaxed)
        # If the message mentions a country but no specific intent, default to TOP_TIPS
        # Only strict off-topic if it looks like math/spam
        
        off_topic_indicators = ["math", "calculation", "weather", "physics", "code"]
        if any(word in msg_lower for word in off_topic_indicators):
            return "OFF_TOPIC"
            
        # Default fallback for ambiguous but safe queries
        return "TOP_TIPS" 

    def get_fallback_content(self, country):
        """
        Tool: Fetch 'Top Tips' (General Fallback).
        """
        details = crud.get_cultural_details(self.db, country.id)
        
        # Priority: Greeting -> ETIQUETTE -> DINING
        priorities = ["GREETING", "ETIQUETTE", "DINING"]
        top_tips = []
        
        for p in priorities:
            match = next((d for d in details if d.category == p), None)
            if match:
                top_tips.append(f"🔹 **{match.topic}**: {match.description}")
        
        if not top_tips:
            top_tips = ["🔹 Be observant and respectful."]
            
        return "\n\n".join(top_tips)

    def process_message(self, message: str, current_country_name: str):
        """
        Orchestrator: Coordinates the tools to generate a response.
        """
        # 1. Detect Country
        target_country = self.detect_country(message, current_country_name)
        
        if not target_country:
            # If no country context at all, just chat generally
            if "hi" in message.lower() or "hello" in message.lower():
                 return {
                     "response": "Hi! I'm GeoPulse. Mention a country (like 'Japan' or 'Brazil') and I'll share local customs!",
                     "active_country": None
                 }
            return {
                "response": "I can help with cultural guides. Which country are you curious about?",
                "active_country": None
            }
            
        # 2. Analyze Intent
        intent = self.analyze_intent(message)
        
        # Handle Off-Topic
        if intent == "OFF_TOPIC":
            return {
                "response": "I can only help with cultural etiquette questions. Ask me about greetings or dining!",
                "active_country": target_country.name
            }

        # 3. Search Knowledge Base
        details = crud.get_cultural_details(self.db, target_country.id)
        
        response_text = ""
        
        if intent == "GREETING":
            response_text = f"Hello! Ready to explore {target_country.name}? You can ask me 'Do I tip?', 'How to greet?', or just 'Tell me about {target_country.name}'."
            
        elif intent == "DO":
            relevant = [d for d in details if d.category == "DOs & DONTs" and d.topic == "Do"]
            if relevant:
                 response_text = f"✅ **{target_country.name} (Do's)**:\n" + "\n".join([f"• {d.description}" for d in relevant])
            else:
                 response_text = f"I don't have specific 'Do' rules for {target_country.name}, but generally be respectful!"

        elif intent == "DONT":
             relevant = [d for d in details if d.category == "DOs & DONTs" and d.topic == "Don't"]
             if relevant:
                  response_text = f"⛔ **{target_country.name} (Don'ts)**:\n" + "\n".join([f"• {d.description}" for d in relevant])
             else:
                  response_text = f"Just be polite! I don't have specific taboos recorded for {target_country.name}."

        else: # TOP_TIPS / GENERAL_INFO
             # Provide a nice summary
             summary = self.get_fallback_content(target_country)
             response_text = f"🌏 **{target_country.name} Cultural Snapshot**:\n\n{summary}\n\n*Try asking: 'Can I tip here?'*"
             
        return {
            "response": response_text,
            "active_country": target_country.name
        }
