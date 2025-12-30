from models import Base
from database import engine

print("Creating tables in PostgreSQL...")
Base.metadata.create_all(bind=engine)
print("✅ Done! Tables created successfully.")
