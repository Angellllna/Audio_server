from db.database import Base, engine
from models.models import Author, User, Track, Playlist

# Створення таблиць
Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")