from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    language = Column(String, nullable=True)

    # Existing relationships
    cultural_data = relationship("CulturalData", back_populates="country")
    quiz_questions = relationship("QuizQuestion", back_populates="country")
    
    # NEW relationship for detailed data
    details = relationship("CulturalDetail", back_populates="country") 

class CulturalData(Base):
    # NOTE: This table is being kept but will be phased out for detail
    __tablename__ = "cultural_data"
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    category = Column(String, nullable=False) 
    content = Column(Text, nullable=False)

    country = relationship("Country", back_populates="cultural_data")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    question = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    answer = Column(String, nullable=False)

    country = relationship("Country", back_populates="quiz_questions")

class CulturalDetail(Base):
    """
    Detailed, structured cultural and etiquette rules.
    """
    __tablename__ = "cultural_details"
    
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    
    # Major category (e.g., GREETING, DINING, BUSINESS, SOCIAL)
    category = Column(String(50), nullable=False)
    
    # Specific topic within the category (e.g., Tipping, Punctuality, Dress Code)
    topic = Column(String(100), nullable=False)
    
    # Detailed explanation of the rule/etiquette
    description = Column(Text, nullable=False)
    
    # Severity of the rule (helpful for filtering/emphasis)
    is_strict = Column(Boolean, default=False) 
    
    # Relationship back to Country
    country = relationship("Country", back_populates="details")