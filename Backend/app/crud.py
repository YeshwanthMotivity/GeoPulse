from sqlalchemy.orm import Session
from . import models

def get_country_by_name(db: Session, country_name: str):
    # Case-insensitive lookup
    country = db.query(models.Country).filter(models.Country.name == country_name).first()
    if not country:
        # Fallback to case-insensitive match
        country = db.query(models.Country).filter(models.Country.name.ilike(country_name)).first()
    return country

def get_cultural_details(db: Session, country_id: int):
    return db.query(models.CulturalDetail).filter(models.CulturalDetail.country_id == country_id).all()

def get_all_countries(db: Session):
    return db.query(models.Country).all()
