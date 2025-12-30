# 🌍 GeoPulse: Global Etiquette AI Guide

**GeoPulse** is an interactive, AI-powered cultural companion designed to help travelers and professionals master global etiquette. With a premium, modern interface, it provides instant access to cultural norms, do's and don'ts, and dining etiquette for countries worldwide.

## ✨ Features

- **Interactive Explorer**: Search for any country to instantly view a curated "Cultural Snapshot" covering Greetings, Dining, and Taboos.
- **Test Your Knowledge" Quiz**: A gamified experience with progress tracking and immediate feedback to test your cultural IQ.
- **AI Geo Assistant**: A smart, context-aware chatbot (powered by Google Gemini) that answers specific questions like *"Can I tip in Japan?"* or *"What is the dress code in Brazil?"*.
- **Premium UI**: A fully responsive, glassmorphism-inspired design featuring smooth animations, "blob" backgrounds, and dark-mode aesthetics for the quiz.

## 🛠️ Tech Stack

### Frontend
- **React.js**: Modular component architecture (`HomePage`, `QuizPage`, `ChatWidget`).
- **React Router**: Seamless client-side navigation.
- **Lucide React**: Beautiful, consistent iconography.
- **Vanilla CSS**: Custom "GeoPulse" Design System (Semantic variables, Glassmorphism, Animations) without external framework bloat.

### Backend
- **FastAPI**: High-performance Python web framework for the API.
- **SQLAlchemy**: ORM for managing the SQLite cultural database.
- **Google Gemini API**: sophisticated natural language processing for the Geo Assistant.
- **Pydantic**: Robust data validation.

## 🚀 Getting Started

### Prerequisites
- Node.js & npm
- Python 3.9+
- Google Gemini API Key

### Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/YeshwanthMotivity/GeoPulse.git
    cd GeoPulse
    ```

2.  **Backend Setup**
    ```bash
    cd Backend
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    # source venv/bin/activate
    
    pip install -r requirements.txt
    
    # Set up environment variables
    # Create a .env file in /Backend and add:
    # GOOGLE_API_KEY=your_gemini_key_here
    
    # Seed the database
    python -m app.seeds
    
    # Run the server
    uvicorn app.main:app --reload
    ```

3.  **Frontend Setup**
    ```bash
    cd Frontend/cultural-guide-frontend
    npm install
    npm start
    ```

4.  **Explore**: Open [http://localhost:3000](http://localhost:3000) to start your journey!

## 📂 Project Structure

```
GeoPulse/
├── Backend/              # FastAPI Application
│   ├── app/
│   │   ├── main.py       # API Entry point
│   │   ├── models.py     # Database Schema
│   │   ├── chat_service.py # AI Logic
│   │   └── ...
│   └── data.json         # Cultural Knowledge Base
│
└── Frontend/             # React Application
    └── cultural-guide-frontend/
        ├── src/
        │   ├── components/ # Header, ChatWidget
        │   ├── pages/      # HomePage, QuizPage
        │   ├── App.css     # Premium Styling
        │   └── ...
```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.



## Author

**Yeshwanth Goud** - [MotivityLabs](https://motivitylabs.com)



## Acknowledgments

- Google Gemini for LLM capabilities
- Groq for prompt optimization
- spaCy for NER
- TextRazor for entity recognition
