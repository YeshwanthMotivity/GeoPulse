from sqlalchemy.orm import Session
from database import engine
from models import Country, CulturalDetail, QuizQuestion, Base
from sqlalchemy.exc import IntegrityError
from contextlib import contextmanager

# Ensure tables exist
Base.metadata.create_all(bind=engine)

@contextmanager
def get_session():
    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Session error: {e}")
    finally:
        session.close()

def seed_data():
    print("Starting Global Cultural Intelligence database seed...")
    
    # --- Part 1: CULTURAL DETAILS ---
    # Enhanced structure with 'COMMON MISTAKES' and 'SITUATIONAL TIPS'
    
    world_data = {
        # --- ASIA ---
        "Afghanistan": {
            "language": "Pashto, Dari",
            "details": [
                {'category': 'GREETING', 'topic': 'Handshake', 'description': 'Handshakes are standard between men. Men do not make physical contact with women.', 'is_strict': True},
                {'category': 'ETIQUETTE', 'topic': 'Guests', 'description': 'Hospitality is sacred. Guests are served the best food and seated in the place of honor.', 'is_strict': True},
                {'category': 'DINING', 'topic': 'Shared Dish', 'description': 'Eating from a communal dish is common. Use your right hand only.', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Remove your shoes before entering a home or mosque.', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Do not show the soles of your feet to anyone; it is considered offensive.', 'is_strict': True},
                {'category': 'COMMON MISTAKES', 'topic': 'Photography', 'description': 'Taking photos of women is culturally prohibited and very offensive.', 'is_strict': True},
                {'category': 'SITUATIONAL TIPS', 'topic': 'Tea Time', 'description': 'Business often happens over tea. Never rush the tea drinking process.', 'is_strict': False}
            ]
        },
        "China": {
            "language": "Mandarin",
            "details": [
                {'category': 'GREETING', 'topic': 'Nod/Bow', 'description': 'A slight nod or bow is common. Handshakes are also standard now.', 'is_strict': False},
                {'category': 'ETIQUETTE', 'topic': 'Face', 'description': 'Protecting "Face" (honor) is crucial. Never embarrass someone publicly.', 'is_strict': True},
                {'category': 'DINING', 'topic': 'Chopsticks', 'description': 'Don\'t leave chopsticks upright in rice (symbolizes death).', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Leave a little food on your plate to show the host gave enough.', 'is_strict': False},
                {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t give clocks as gifts (sounds like "funeral").', 'is_strict': True},
                {'category': 'COMMON MISTAKES', 'topic': 'Names', 'description': 'Calling someone by their first name too soon is disrespectful. Use titles.', 'is_strict': False},
                {'category': 'SITUATIONAL TIPS', 'topic': 'Business Cards', 'description': 'Present your card with two hands and study theirs carefully.', 'is_strict': True}
            ]
        },
        "India": {
            "language": "Hindi, English",
            "details": [
                {'category': 'GREETING', 'topic': 'Namaste', 'description': 'Palms pressed together with a slight bow. Respectful for all.', 'is_strict': True},
                {'category': 'ETIQUETTE', 'topic': 'Feet', 'description': 'Feet are unclean. Do not touch people or objects with them.', 'is_strict': True},
                {'category': 'DINING', 'topic': 'Right Hand', 'description': 'Always eat with the right hand. Left is for hygiene.', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Remove shoes before entering a home.', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t wink or whistle, it can be seen as rude or insulting.', 'is_strict': False},
                {'category': 'COMMON MISTAKES', 'topic': 'Personal Space', 'description': 'Personal space is smaller than in the West; don\'t back away if someone stands close.', 'is_strict': False},
                {'category': 'SITUATIONAL TIPS', 'topic': 'Elders', 'description': 'In social settings, always greet the eldest person first.', 'is_strict': True}
            ]
        },
        "Japan": {
            "language": "Japanese",
            "details": [
                {'category': 'GREETING', 'topic': 'Bowing', 'description': 'Bow to greet. Deeper bow = more respect.', 'is_strict': True},
                {'category': 'ETIQUETTE', 'topic': 'Shoes', 'description': 'Always remove shoes at the entrance (Genkan) of homes.', 'is_strict': True},
                {'category': 'DINING', 'topic': 'Slurping', 'description': 'Slurping noodles indicates they are delicious.', 'is_strict': False},
                {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Exchange business cards with two hands.', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t tip; good service is standard and tipping causes confusion.', 'is_strict': True},
                {'category': 'COMMON MISTAKES', 'topic': 'Trains', 'description': 'Talking loud on the phone on a train is extremely rude.', 'is_strict': True},
                {'category': 'SITUATIONAL TIPS', 'topic': 'Elevators', 'description': 'The person closest to the buttons operates the door for everyone.', 'is_strict': False}
            ]
        },
        "France": {
            "language": "French",
            "details": [
                {'category': 'GREETING', 'topic': 'Bonjour', 'description': 'Say Bonjour immediately upon entering a shop.', 'is_strict': True},
                {'category': 'ETIQUETTE', 'topic': 'Volume', 'description': 'Speak quietly in public.', 'is_strict': False},
                {'category': 'DINING', 'topic': 'Hands', 'description': 'Hands visible on table.', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Use "Monsieur/Madame".', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t eat on the street (mostly).', 'is_strict': False},
                {'category': 'COMMON MISTAKES', 'topic': 'Service', 'description': 'Expecting "customer is king" service; waiters are professionals, treat them as equals.', 'is_strict': False},
                {'category': 'SITUATIONAL TIPS', 'topic': 'Dinner Party', 'description': 'Arrive 15 minutes late ("quart d\'heure de politesse") to give hosts time.', 'is_strict': False}
            ]
        },
        "United States": {
            "language": "English",
            "details": [
                {'category': 'GREETING', 'topic': 'Handshake', 'description': 'Firm handshake, smile, and "How are you?".', 'is_strict': False},
                {'category': 'ETIQUETTE', 'topic': 'Tipping', 'description': 'Tipping 15-20% is mandatory in restaurants.', 'is_strict': True},
                {'category': 'DINING', 'topic': 'Style', 'description': 'Fork in right hand (or switch) is common.', 'is_strict': False},
                {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Respect personal space (arm\'s length).', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t smoke in public indoor areas.', 'is_strict': True},
                {'category': 'COMMON MISTAKES', 'topic': 'Price Tags', 'description': 'Forgetting that tax is added at the register, not on the tag.', 'is_strict': False},
                {'category': 'SITUATIONAL TIPS', 'topic': 'Small Talk', 'description': 'It is polite to chat with cashiers and strangers in lines.', 'is_strict': False}
            ]
        },
        "Brazil": {
            "language": "Portuguese",
            "details": [
                {'category': 'GREETING', 'topic': 'Kiss/Hug', 'description': 'Women kiss cheeks (1-3 times). Men hug back-slap.', 'is_strict': False},
                {'category': 'ETIQUETTE', 'topic': 'Time', 'description': 'Punctuality is flexible for social events.', 'is_strict': False},
                {'category': 'DINING', 'topic': 'Napkins', 'description': 'Use a napkin to hold food (sandwiches/pizza) if eating with hands.', 'is_strict': True},
                {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Dress smart-casual; appearance matters.', 'is_strict': False},
                {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t use the "OK" hand sign (offensive).', 'is_strict': True},
                {'category': 'COMMON MISTAKES', 'topic': 'Spanish', 'description': 'Speaking Spanish to Brazilians; they speak Portuguese.', 'is_strict': True},
                {'category': 'SITUATIONAL TIPS', 'topic': 'Conversation', 'description': 'Interrupting is seen as enthusiasm, not rudeness.', 'is_strict': False}
            ]
        }
    }

    world_data["United Kingdom"] = {
        "language": "English",
        "details": [
            {'category': 'GREETING', 'topic': 'Handshake', 'description': 'Light handshake.', 'is_strict': False},
            {'category': 'ETIQUETTE', 'topic': 'Queue', 'description': 'Never jump the queue.', 'is_strict': True},
            {'category': 'DINING', 'topic': 'Table Manners', 'description': 'Knife in right, fork in left.', 'is_strict': True},
            {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Say please and thank you constantly.', 'is_strict': True},
            {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t be loud or boastful.', 'is_strict': True},
            {'category': 'COMMON MISTAKES', 'topic': 'Eye Contact', 'description': 'Staring or prolonged eye contact on the Tube is considered rude.', 'is_strict': False},
            {'category': 'SITUATIONAL TIPS', 'topic': 'Pub', 'description': 'Buy "rounds" of drinks when with a group. Don\'t just buy for yourself.', 'is_strict': True}
        ]
    }
    
    # --- Part 2: QUIZ DATA ---
    # Smart, scenario-based questions
    
    quiz_data = {
        "Japan": [
            {
                "question": "You finish your bowl of ramen and it was delicious. What is a polite way to show this?",
                "option_a": "Leave a little bit left in the bowl",
                "option_b": "Slurp loudly while eating",
                "option_c": "Burp loudly after finishing",
                "option_d": "Ask for a doggy bag",
                "answer": "Slurp loudly while eating"
            },
            {
                "question": "You are paying for a souvenir. How should you hand the money to the cashier?",
                "option_a": "Directly into their hand",
                "option_b": "Place it on the small tray provided",
                "option_c": "Throw it on the counter",
                "option_d": "Hide it in a handshake",
                "answer": "Place it on the small tray provided"
            }
        ],
        "France": [
            {
                "question": "You enter a small boutique in Paris. What is the very first thing you must do?",
                "option_a": "Start looking at clothes",
                "option_b": "Ask 'How much is this?'",
                "option_c": "Say 'Bonjour' to the shopkeeper",
                "option_d": "Smile and wave",
                "answer": "Say 'Bonjour' to the shopkeeper"
            },
            {
                "question": "At a dinner party, when should you start eating?",
                "option_a": "As soon as you are served",
                "option_b": "When the host says 'Bon Appétit'",
                "option_c": "When everyone has their food",
                "option_d": "After the first toast",
                "answer": "When the host says 'Bon Appétit'"
            }
        ],
        "United States": [
            {
                "question": "You receive a bill at a restaurant for $100. The service was good. How much should you tip?",
                "option_a": "Nothing, service is included",
                "option_b": "$5 - $10",
                "option_c": "$15 - $20",
                "option_d": "Round up to the nearest dollar",
                "answer": "$15 - $20"
            }
        ],
        "India": [
            {
                "question": "You are eating a traditional meal served on a banana leaf. Which hand do you use?",
                "option_a": "Left hand only",
                "option_b": "Right hand only",
                "option_c": "Both hands",
                "option_d": "Fork and knife",
                "answer": "Right hand only"
            }
        ],
        "China": [
            {
                "question": "You are given a business card. What should you NOT do?",
                "option_a": "Receive it with two hands",
                "option_b": "Read it carefully",
                "option_c": "Put it immediately in your back pocket",
                "option_d": "Smile and thank them",
                "answer": "Put it immediately in your back pocket"
            }
        ]
    }
    
    # Helper to generate basic list names (same as before for coverage)
    other_countries = [
         "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Australia", "Austria", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "Colombia", "Comoros", "Congo (Democratic Republic)", "Congo (Republic)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
    ]
    
    # Regional defaults (Enhanced)
    latin_america = {"language": "Spanish", "details": [
        {'category': 'GREETING', 'topic': 'Kiss/Handshake', 'description': 'Warm greetings, eye contact, often a kiss on cheek.', 'is_strict': False},
        {'category': 'ETIQUETTE', 'topic': 'Time', 'description': 'Time is often flexible (Polychronic).', 'is_strict': False},
        {'category': 'DINING', 'topic': 'Social', 'description': 'Meals are long social events.', 'is_strict': False},
        {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Dress well and neatly.', 'is_strict': False},
        {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t be offended by personal questions.', 'is_strict': False},
        {'category': 'COMMON MISTAKES', 'topic': 'Rushing', 'description': 'Trying to rush business or social interactions is rude.', 'is_strict': False},
        {'category': 'SITUATIONAL TIPS', 'topic': 'Lunch', 'description': 'Lunch is the main meal; allow 2 hours.', 'is_strict': False}
    ]}
    
    europe = {"language": "Local Language", "details": [
        {'category': 'GREETING', 'topic': 'Handshake', 'description': 'Firm handshake is standard.', 'is_strict': True},
        {'category': 'ETIQUETTE', 'topic': 'Privacy', 'description': 'Respect personal space.', 'is_strict': False},
        {'category': 'DINING', 'topic': 'Continental', 'description': 'Fork in left, knife in right.', 'is_strict': True},
        {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Say please and thank you.', 'is_strict': True},
        {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t be loud in public areas.', 'is_strict': True},
        {'category': 'COMMON MISTAKES', 'topic': 'Greetings', 'description': 'Not greeting shopkeepers when entering.', 'is_strict': True},
        {'category': 'SITUATIONAL TIPS', 'topic': 'Public Transport', 'description': 'Keep your voice down and offer seats to elderly.', 'is_strict': True}
    ]}
    
    africa = {"language": "English/French/Local", "details": [
        {'category': 'GREETING', 'topic': 'Handshake', 'description': 'Handshakes are important and often lingering.', 'is_strict': False},
        {'category': 'ETIQUETTE', 'topic': 'Elders', 'description': 'Great respect is shown to elders.', 'is_strict': True},
        {'category': 'DINING', 'topic': 'Right Hand', 'description': 'Eat with right hand.', 'is_strict': True},
        {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Ask about family and health.', 'is_strict': False},
        {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t use left hand for gestures.', 'is_strict': True},
        {'category': 'COMMON MISTAKES', 'topic': 'Impatience', 'description': 'Showing impatience is considered rude.', 'is_strict': True},
        {'category': 'SITUATIONAL TIPS', 'topic': 'Photos', 'description': 'Always ask permission before taking photos of people.', 'is_strict': True}
    ]}
    
    asia = {"language": "Local/English", "details": [
        {'category': 'GREETING', 'topic': 'Respect', 'description': 'Bow or soft handshake. Respect hierarchy.', 'is_strict': True},
        {'category': 'ETIQUETTE', 'topic': 'Shoes', 'description': 'Remove shoes indoors.', 'is_strict': True},
        {'category': 'DINING', 'topic': 'Sharing', 'description': 'Dishes are often shared.', 'is_strict': False},
        {'category': 'DOs & DONTs', 'topic': 'Do', 'description': 'Use both hands to give/receive.', 'is_strict': True},
        {'category': 'DOs & DONTs', 'topic': 'Don\'t', 'description': 'Don\'t touch heads or point feet.', 'is_strict': True},
        {'category': 'COMMON MISTAKES', 'topic': 'Anger', 'description': 'Getting angry in public causes loss of face.', 'is_strict': True},
        {'category': 'SITUATIONAL TIPS', 'topic': 'Temples', 'description': 'Dress modestly (cover shoulders/knees).', 'is_strict': True}
    ]}

    # --- Regional Quiz Defaults ---
    regional_quizzes = {
        "Europe": [
            {"question": "In a formal setting, what is the standard greeting?", "option_a": "High five", "option_b": "Firm handshake", "option_c": "Hug", "option_d": "Wave", "answer": "Firm handshake"},
            {"question": "When dining, where should your hands usually be?", "option_a": "Hidden under the table", "option_b": "Visible on the table", "option_c": "In your pockets", "option_d": "Holding your phone", "answer": "Visible on the table"}
        ],
        "Asia": [
            {"question": "What is the most common rule when entering a home?", "option_a": "Keep shoes on", "option_b": "Remove shoes", "option_c": "Wear outdoor sandals", "option_d": "Clean your shoes before entering", "answer": "Remove shoes"},
            {"question": "How should you generally interact with elders?", "option_a": "Treat them as equals", "option_b": "Show high respect and hierarchy", "option_c": "Speak loudly", "option_d": "Avoid eye contact", "answer": "Show high respect and hierarchy"}
        ],
        "LatinAmerica": [
            {"question": "How is time/punctuality often viewed socially?", "option_a": "Strictly punctual", "option_b": "Flexible (Polychronic)", "option_c": "Arrive 1 hour early", "option_d": "Cancelled if 5 mins late", "answer": "Flexible (Polychronic)"},
            {"question": "What is a common friendly greeting?", "option_a": "Stiff handshake", "option_b": "Kiss on the cheek or hug", "option_c": "Bow", "option_d": "Salute", "answer": "Kiss on the cheek or hug"}
        ],
        "Africa": [
            {"question": "Which hand should you use for eating communal food?", "option_a": "Left hand", "option_b": "Right hand", "option_c": "Both hands", "option_d": "Spoon only", "answer": "Right hand"},
            {"question": "Before taking a photo of someone, what must you do?", "option_a": "Just take it", "option_b": "Ask for permission", "option_c": "Hide the camera", "option_d": "Pay them first", "answer": "Ask for permission"}
        ]
    }

    with get_session() as session:
        # 1. Process explicit detailed countries (world_data)
        for name, data in world_data.items():
            process_country(session, name, data)
            
            # CHECK: If this country has no specific quiz, give it a Regional Quiz
            if name not in quiz_data:
                # Determine region based on simple keywords/lists or default to Asia/Middle East for Afghanistan
                # Simple region mapper for world_data keys
                region_quiz = regional_quizzes["Europe"] 
                
                if name in ["Afghanistan", "China", "India", "Japan", "Thailand", "Vietnam"]:
                     region_quiz = regional_quizzes["Asia"]
                elif name in ["Brazil", "Argentina"]:
                     region_quiz = regional_quizzes["LatinAmerica"]
                elif name in ["Egypt", "Nigeria", "South Africa"]:
                     region_quiz = regional_quizzes["Africa"]
                
                # Check mapping from heuristic logic below to be safe? 
                # Actually, simple region mapping is better.
                if name == "Afghanistan": region_quiz = regional_quizzes["Asia"]
                if name == "Brazil": region_quiz = regional_quizzes["LatinAmerica"]
                
                process_quiz(session, name, region_quiz)

        # 2. Process list countries with heuristic defaults AND QUIZZES
        # Ensure Albania is in the list
        if "Albania" not in other_countries:
            other_countries.append("Albania")

        for name in other_countries:
            if name in world_data: continue 
            
            # Simple heuristic assignments matches
            region_quiz = regional_quizzes["Europe"] # Default
            
            if name in ["Argentina", "Bolivia", "Chile", "Colombia", "Costa Rica", "Cuba", "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Honduras", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru", "Uruguay", "Venezuela"]:
                vals = latin_america
                region_quiz = regional_quizzes["LatinAmerica"]
            elif name in ["Benin", "Botswana", "Burkina Faso", "Burundi", "Cameroon", "Chad", "Congo", "Egypt", "Ethiopia", "Gabon", "Ghana", "Kenya", "Liberia", "Libya", "Nigeria", "Rwanda", "Senegal", "South Africa", "Tanzania", "Uganda", "Zambia", "Zimbabwe"]:
                vals = africa
                region_quiz = regional_quizzes["Africa"]
            elif name in ["Australia", "New Zealand", "Fiji", "Tonga", "Samoa"]:
                vals = europe # Western style roughly
                region_quiz = regional_quizzes["Europe"]
            elif name in ["Thailand", "Vietnam", "Laos", "Cambodia", "Myanmar", "Malaysia", "Indonesia", "Philippines", "Afghanistan", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal"]:
                vals = asia
                region_quiz = regional_quizzes["Asia"]
            else:
                vals = europe 
                region_quiz = regional_quizzes["Europe"]
                
            process_country(session, name, vals)
            
            # Add regional quiz if no specific quiz exists
            if name not in quiz_data:
                process_quiz(session, name, region_quiz)

            
        # 3. Process Specific Quiz Data (Overrides)
        for country_name, questions in quiz_data.items():
            process_quiz(session, country_name, questions)

            
    print("Database Global Cultural Intelligence seed complete!")

def process_country(session, name, data):
    # Upsert Country
    country = session.query(Country).filter_by(name=name).first()
    if not country:
        country = Country(name=name, language=data.get('language', 'Local'))
        session.add(country)
        session.commit()
    
    # Upsert Details
    for detail in data['details']:
        exists = session.query(CulturalDetail).filter_by(
            country_id=country.id, 
            category=detail['category'], 
            topic=detail['topic']
        ).first()
        
        if not exists:
            new_detail = CulturalDetail(
                country_id=country.id,
                category=detail['category'],
                topic=detail['topic'],
                description=detail['description'],
                is_strict=detail['is_strict']
            )
            session.add(new_detail)
    session.commit()

def process_quiz(session, country_name, questions):
    country = session.query(Country).filter_by(name=country_name).first()
    if not country:
        print(f"Skipping quiz for {country_name} - not found")
        return

    for q in questions:
        exists = session.query(QuizQuestion).filter_by(
            country_id=country.id,
            question=q['question']
        ).first()
        
        if not exists:
            new_q = QuizQuestion(
                country_id=country.id,
                question=q['question'],
                option_a=q['option_a'],
                option_b=q['option_b'],
                option_c=q['option_c'],
                option_d=q['option_d'],
                answer=q['answer']
            )
            session.add(new_q)
    session.commit()

if __name__ == "__main__":
    seed_data()